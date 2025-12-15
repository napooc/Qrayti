# Qrayti Backend API

AI-powered study assistant backend for Moroccan students built with FastAPI.

## Features

- 📄 **PDF Text Extraction**: Upload and extract text from PDF documents
- 🎯 **Quiz Generation**: AI-generated multiple-choice questions with explanations in French and Darija
- 📝 **Summary Generation**: Structured summaries with key terms and essential points in French and Darija
- 🚀 **Fast & Async**: Built with FastAPI for high performance
- 🔌 **Flexible AI Backend**: Supports OpenAI API and local models

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (for OpenAI model) OR local GPU (for local models)

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from the template:

```bash
cp .env.template .env
```

Edit `.env` and add your configuration:

```env
# For OpenAI API (Recommended for testing)
OPENAI_API_KEY=sk-your-openai-api-key-here
MODEL_TYPE=openai

# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS (add your frontend URLs)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Getting an OpenAI API Key:**
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy it to your `.env` file

### 3. Run the Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### 4. Test the API

Visit the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
```http
GET /health
```
Check if the server and AI model are ready.

### Upload PDF
```http
POST /api/upload-pdf
Content-Type: multipart/form-data

file: <PDF file>
```
Upload a PDF and extract its text content.

**Response:**
```json
{
  "fileName": "document.pdf",
  "content": "extracted text...",
  "pageCount": 10
}
```

### Generate Quiz
```http
POST /api/generate-quiz
Content-Type: application/json

{
  "content": "text content to generate quiz from",
  "num_questions": 5
}
```

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctIndex": 1,
      "explanation": "Explanation in French",
      "explanationDarija": "Explanation in Darija"
    }
  ]
}
```

### Generate Summary
```http
POST /api/generate-summary
Content-Type: application/json

{
  "content": "text content to summarize"
}
```

**Response:**
```json
{
  "sections": [
    {
      "title": "Section Title",
      "content": "Summary content",
      "keyTerms": [
        {
          "term": "Term",
          "definition": "Definition in French",
          "definitionDarija": "Definition in Darija"
        }
      ],
      "essentialPoints": ["Point 1", "Point 2"]
    }
  ]
}
```

## Configuration Options

### Model Types

#### 1. OpenAI API (Recommended for testing)
```env
MODEL_TYPE=openai
OPENAI_API_KEY=sk-your-key-here
```
**Pros:**
- Fast and reliable
- High-quality outputs
- No GPU required
- Easy to set up

**Cons:**
- Requires API key and credits
- Costs per request (but relatively cheap with GPT-3.5)

#### 2. Local Models (Coming soon)
```env
MODEL_TYPE=local
LOCAL_MODEL_NAME=gpt2
```

For local models, install additional dependencies:
```bash
pip install transformers torch accelerate
```

**Popular local models:**
- `gpt2` - Small, fast, but lower quality
- `mistralai/Mistral-7B-Instruct-v0.2` - Better quality, needs GPU
- `TheBloke/Mistral-7B-Instruct-v0.2-GGUF` - Quantized version

## Testing

### Test with cURL

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Generate Quiz:**
```bash
curl -X POST "http://localhost:8000/api/generate-quiz" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Le Dahir des Obligations et Contrats (DOC) est le texte fondamental qui régit le droit civil au Maroc.",
    "num_questions": 3
  }'
```

**Upload PDF:**
```bash
curl -X POST "http://localhost:8000/api/upload-pdf" \
  -F "file=@your-document.pdf"
```

### Test with Python Script

Run the included test script:
```bash
python test_api.py
```

## Project Structure

```
backend/
├── main.py                 # FastAPI application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .env.template          # Environment template
├── services/
│   ├── __init__.py
│   ├── ai_service.py      # AI model integration
│   └── pdf_service.py     # PDF processing
└── README.md              # This file
```

## Troubleshooting

### "OpenAI API key not found"
Make sure you've created a `.env` file with your API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### "Module not found" errors
Install all dependencies:
```bash
pip install -r requirements.txt
```

### CORS errors from frontend
Add your frontend URL to `CORS_ORIGINS` in `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Port already in use
Change the port in `.env`:
```env
PORT=8001
```

## Development

### Hot Reload
The server automatically reloads when you make changes (when `DEBUG=True`).

### Logs
Logs are printed to the console. Adjust logging level in `main.py`.

### Adding New Endpoints
1. Define your endpoint in `main.py`
2. Add any new services in the `services/` directory
3. Update this README with documentation

## Next Steps

1. ✅ **Test the basic setup** - Make sure the server runs and responds to health checks
2. ✅ **Test with OpenAI** - Verify quiz and summary generation work
3. 🔄 **Integrate with frontend** - Update frontend to call these endpoints
4. 🔄 **Add local model support** - Set up local models if needed
5. 🔄 **Deploy** - Deploy to a production server

## Contributing

This is a project for Moroccan students. Contributions are welcome!

## License

MIT License

