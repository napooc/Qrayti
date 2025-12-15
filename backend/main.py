"""Main FastAPI application."""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging

from config import settings
from services.pdf_service import extract_text_from_pdf
from services.local_ai_service import LocalAIService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Qrayti API",
    description="AI-powered study assistant for Moroccan students (Local Models)",
    version="2.0.0"
)

# Configure CORS - Allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize AI Service
ai_service = LocalAIService()

# Load model on startup
@app.on_event("startup")
async def startup_event():
    """Load the AI model when the server starts."""
    logger.info("Loading AI model...")
    try:
        ai_service.load_model()
        logger.info("✅ Server ready!")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        logger.warning("Server will start but AI features will not work")


# Pydantic models for request/response
class QuizRequest(BaseModel):
    content: str
    num_questions: int = 5


class QuizOption(BaseModel):
    text: str


class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correctIndex: int
    explanation: str
    explanationDarija: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]


class SummaryRequest(BaseModel):
    content: str


class KeyTerm(BaseModel):
    term: str
    definition: str
    definitionDarija: str


class SummarySection(BaseModel):
    title: str
    content: str
    keyTerms: List[KeyTerm]
    essentialPoints: List[str]


class SummaryResponse(BaseModel):
    sections: List[SummarySection]


class PDFUploadResponse(BaseModel):
    fileName: str
    content: str
    pageCount: int


class HealthResponse(BaseModel):
    status: str
    model_type: str
    model_ready: bool


# Routes
@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Qrayti API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    model_ready = ai_service.is_ready()
    return HealthResponse(
        status="healthy" if model_ready else "initializing",
        model_type=f"{settings.model_type} ({settings.local_model_name})",
        model_ready=model_ready
    )


@app.post("/api/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file.
    Extracts text content from the PDF.
    """
    import time
    start_time = time.time()
    
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.PDF')):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        logger.info(f"📄 Processing PDF: {file.filename}")
        
        # Read file content
        content = await file.read()
        file_size_mb = len(content) / 1024 / 1024
        logger.info(f"   File size: {file_size_mb:.2f} MB")
        
        # Check file size (50MB limit)
        if file_size_mb > 50:
            raise HTTPException(
                status_code=400,
                detail=f"File too large ({file_size_mb:.2f} MB). Maximum size is 50 MB."
            )
        
        # Extract text from PDF
        text = extract_text_from_pdf(content)
        
        if not text or len(text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from PDF. Please ensure the PDF contains readable text, not just images."
            )
        
        # Count pages (approximate based on content length)
        page_count = max(1, len(text) // 2000)
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Successfully processed PDF: {file.filename}")
        logger.info(f"   Pages: {page_count}, Characters: {len(text)}, Time: {elapsed:.2f}s")
        
        return PDFUploadResponse(
            fileName=file.filename,
            content=text,
            pageCount=page_count
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/api/generate-quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """
    Generate a quiz from the provided content.
    Creates multiple-choice questions with explanations in French and Darija.
    """
    import time
    start_time = time.time()
    
    try:
        if not request.content or len(request.content.strip()) < 50:
            raise HTTPException(status_code=400, detail="Content is too short to generate a quiz")
        
        # Truncate content BEFORE sending to AI (critical for speed!)
        max_content = 400  # Very aggressive truncation
        content = request.content[:max_content] if len(request.content) > max_content else request.content
        
        logger.info(f"Generating quiz with {request.num_questions} questions from {len(content)} characters (truncated from {len(request.content)})")
        
        # Generate quiz using AI service
        questions = await ai_service.generate_quiz(
            content=content,
            num_questions=request.num_questions
        )
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Quiz generation completed in {elapsed:.2f} seconds")
        
        return QuizResponse(questions=questions)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


@app.post("/api/generate-summary", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """
    Generate a structured summary from the provided content.
    Creates sections with key terms and essential points in French and Darija.
    """
    import time
    start_time = time.time()
    
    try:
        if not request.content or len(request.content.strip()) < 50:
            raise HTTPException(status_code=400, detail="Content is too short to generate a summary")
        
        # Truncate content BEFORE sending to AI (critical for speed!)
        max_content = 400  # Very aggressive truncation
        content = request.content[:max_content] if len(request.content) > max_content else request.content
        
        logger.info(f"Generating summary from {len(content)} characters (truncated from {len(request.content)})")
        
        # Generate summary using AI service
        sections = await ai_service.generate_summary(content=content)
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Summary generation completed in {elapsed:.2f} seconds")
        
        return SummaryResponse(sections=sections)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

