"""PDF processing service."""
import io
import logging
from typing import Optional
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

# Maximum pages to process (prevent hanging on huge PDFs)
MAX_PAGES = 100

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        Extracted text as string
    """
    try:
        logger.info(f"Starting PDF extraction, file size: {len(pdf_content) / 1024 / 1024:.2f} MB")
        
        # Create a PDF reader object from bytes
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PdfReader(pdf_file)
        
        total_pages = len(pdf_reader.pages)
        logger.info(f"PDF has {total_pages} pages")
        
        # Limit pages to prevent hanging
        pages_to_process = min(total_pages, MAX_PAGES)
        if total_pages > MAX_PAGES:
            logger.warning(f"PDF has {total_pages} pages, only processing first {MAX_PAGES}")
        
        # Extract text from pages
        text_content = []
        for page_num in range(pages_to_process):
            try:
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text and text.strip():
                    text_content.append(text)
                    logger.debug(f"Extracted {len(text)} chars from page {page_num + 1}")
            except Exception as e:
                logger.warning(f"Error extracting text from page {page_num + 1}: {str(e)}")
                continue
        
        if not text_content:
            raise Exception("No text could be extracted from the PDF. The PDF might be image-based or encrypted.")
        
        # Combine all text
        full_text = "\n\n".join(text_content)
        
        # Clean up the text
        full_text = clean_text(full_text)
        
        logger.info(f"✅ Extracted {len(full_text)} characters from {len(text_content)} pages")
        
        return full_text
    
    except Exception as e:
        logger.error(f"❌ Error reading PDF: {str(e)}")
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace and formatting issues.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]  # Remove empty lines
    
    # Join with single newlines
    cleaned = '\n'.join(lines)
    
    # Remove multiple spaces
    import re
    cleaned = re.sub(r' +', ' ', cleaned)
    
    return cleaned

