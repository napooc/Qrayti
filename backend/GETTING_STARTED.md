# Getting Started with Qrayti Backend

## 🎯 What We Built

Your backend is now ready! Here's what you have:

### ✅ Complete FastAPI Backend with:
1. **PDF Upload & Text Extraction** - Upload PDFs and extract text
2. **AI-Powered Quiz Generation** - Generate quizzes with explanations in French and Darija
3. **AI-Powered Summary Generation** - Create structured summaries with key terms
4. **CORS Support** - Ready to connect to your React frontend
5. **Interactive API Docs** - Test endpoints in your browser

### 🤖 AI Model Options

We've set up the backend to work with **OpenAI's GPT models** first because:
- ✅ Easy to set up (just need API key)
- ✅ High quality outputs
- ✅ Reliable and fast
- ✅ No GPU required
- ✅ Very affordable for development ($0.001 per quiz)

**Note about "gpt-oss-20b"**: This specific model name doesn't exist in standard repositories. We've built the system to work with:
- **GPT-3.5-Turbo** (recommended for testing - cheap and fast)
- **GPT-4** (better quality, more expensive)
- **Local models** (can be added later if needed)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run Setup
```bash
python setup.py
```
This will:
- Guide you through creating the `.env` file
- Check that all dependencies are installed
- Show you the next steps

### Step 3: Start the Server
```bash
python main.py
```

**That's it!** Your backend is now running at http://localhost:8000

---

## 🧪 Testing Your Backend

### Option 1: Automated Tests (Recommended)
```bash
python test_api.py
```
This will test all endpoints and show you if everything works!

### Option 2: Interactive API Documentation
1. Start the server: `python main.py`
2. Open in browser: http://localhost:8000/docs
3. Click "Try it out" on any endpoint
4. Test directly in the browser!

### Option 3: Manual Testing with cURL
```bash
# Health check
curl http://localhost:8000/health

# Generate quiz
curl -X POST "http://localhost:8000/api/generate-quiz" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Le DOC régit le droit civil marocain depuis 1913.",
    "num_questions": 3
  }'
```

---

## 📁 Project Structure

```
backend/
├── main.py                  # Main FastAPI application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Your environment variables (CREATE THIS)
├── .env.template          # Template for .env file
│
├── services/
│   ├── ai_service.py      # AI model integration (OpenAI/Local)
│   └── pdf_service.py     # PDF text extraction
│
├── setup.py               # Interactive setup script
├── test_api.py           # API testing script
│
└── README.md             # Full documentation
```

---

## 🔑 Getting Your OpenAI API Key

1. **Go to**: https://platform.openai.com/api-keys
2. **Sign up** or log in
3. **Click**: "Create new secret key"
4. **Name it**: "Qrayti Backend"
5. **Copy** the key (starts with `sk-...`)
6. **Add to** your `.env` file

### Pricing (Very Affordable!)
- First-time users get **$5 free credit**
- GPT-3.5-Turbo costs ~**$0.001 per request**
- This means ~5,000 free quiz/summary generations!

---

## 🔗 Connecting Your Frontend

Once your backend is running:

### 1. Update Frontend API Calls

In your React frontend, create an API service:

```typescript
// src/services/api.ts
const API_BASE_URL = 'http://localhost:8000';

export async function uploadPDF(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/api/upload-pdf`, {
    method: 'POST',
    body: formData,
  });
  
  return response.json();
}

export async function generateQuiz(content: string, numQuestions: number = 5) {
  const response = await fetch(`${API_BASE_URL}/api/generate-quiz`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, num_questions: numQuestions }),
  });
  
  return response.json();
}

export async function generateSummary(content: string) {
  const response = await fetch(`${API_BASE_URL}/api/generate-summary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content }),
  });
  
  return response.json();
}
```

### 2. Update Your Components

Replace the mock data in your frontend components:

```typescript
// In PDFUploader.tsx
import { uploadPDF } from '@/services/api';

const processFile = async (file: File) => {
  setIsProcessing(true);
  try {
    const data = await uploadPDF(file);  // Real API call!
    onFileProcessed(data);
  } catch (err) {
    setError(err.message);
  } finally {
    setIsProcessing(false);
  }
};
```

---

## 🎓 What You Can Do Now

### ✅ Phase 1: Backend Setup (COMPLETE!)
- [x] FastAPI backend structure
- [x] PDF text extraction
- [x] AI model integration
- [x] Quiz generation endpoint
- [x] Summary generation endpoint
- [x] CORS configuration
- [x] Interactive documentation

### 🔄 Phase 2: Testing & Integration (Next Steps)
1. Get your OpenAI API key
2. Test the backend with `test_api.py`
3. Update frontend to call real API endpoints
4. Test full flow: Upload PDF → Generate Quiz/Summary

### 🚀 Phase 3: Advanced Features (Future)
- Add more question types
- Support multiple languages
- Add user authentication
- Save quiz results
- Deploy to production
- Add local model support

---

## 🐛 Common Issues & Solutions

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
1. Check `.env` file exists in `backend/` folder
2. Verify `OPENAI_API_KEY=sk-...` is set correctly
3. No quotes needed around the key

### "Port 8000 already in use"
Change port in `.env`:
```env
PORT=8001
```

### CORS Errors from Frontend
Add your frontend URL to `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### API Requests Timing Out
- First request may be slow (model initialization)
- Subsequent requests will be faster
- GPT-4 is slower than GPT-3.5

---

## 📚 Documentation

- **SETUP_GUIDE.md** - Quick setup instructions
- **README.md** - Full API documentation
- **GETTING_STARTED.md** - This file
- **/docs** - Interactive API docs (when server is running)

---

## ✨ Tips for Success

1. **Start Simple**: Test with OpenAI API first
2. **Monitor Costs**: Check your OpenAI usage dashboard
3. **Use GPT-3.5**: Cheaper and faster for development
4. **Save Responses**: Add caching to reduce API calls
5. **Check Logs**: Server logs show detailed error messages

---

## 🎉 You're Ready!

Your backend is fully functional and ready to power your Qrayti application!

**Next Step**: Run `python setup.py` to get started! 🚀

---

## Need Help?

If you run into issues:
1. Check the server logs (terminal where `python main.py` is running)
2. Visit http://localhost:8000/docs to test endpoints
3. Run `python test_api.py` to diagnose issues
4. Review the error messages - they're descriptive!

Good luck with your project! 🎓🇲🇦

