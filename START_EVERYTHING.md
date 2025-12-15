# 🚀 START EVERYTHING - Complete Setup Guide

## ✅ EVERYTHING IS READY!

Your **entire Qrayti application** is fully integrated and configured. Frontend connects to backend, backend uses microsoft/phi-2 AI model. **No mock data** - everything is real!

---

## 📋 Prerequisites Check

Before starting, make sure you have:

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] At least 8GB RAM
- [ ] At least 10GB free disk space
- [ ] Internet connection (for first-time setup)

---

## 🎯 Complete Setup (First Time Only)

### Part 1: Backend Setup (~20 minutes)

#### Step 1: Install Backend Dependencies

```powershell
cd C:\Users\HP\Desktop\pfa\backend
pip install -r requirements.txt
```

⏱️ **Takes:** ~10-15 minutes (large packages)

---

#### Step 2: Configure Backend

Create `.env` file (copy this content):

```powershell
cd C:\Users\HP\Desktop\pfa\backend
notepad .env
```

**Paste this:**
```env
LOCAL_MODEL_NAME=microsoft/phi-2
DEVICE=auto
LOAD_IN_8BIT=False
MAX_LENGTH=2048
TEMPERATURE=0.7

HOST=0.0.0.0
PORT=8000
DEBUG=True

CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Save and close.

**Or use the template:**
```powershell
copy env_template_phi2 .env
```

---

#### Step 3: Download AI Model

```powershell
python download_model.py
```

**Choose option 3** (microsoft/phi-2)
**Type y** to confirm

⏱️ **Takes:** ~5-15 minutes (downloads ~5GB)

**You'll see:**
```
✅ Model downloaded successfully: microsoft/phi-2
   Device: cuda (or cpu)
   Status: Working
```

---

### Part 2: Frontend Setup (~5 minutes)

#### Step 1: Install Frontend Dependencies

```powershell
cd C:\Users\HP\Desktop\pfa\frontpfa\qrayti-your-moroccan-study-mate
npm install
```

⏱️ **Takes:** ~3-5 minutes

---

#### Step 2: Configure Frontend

The frontend is already configured to connect to `http://localhost:8000`.

**Optional:** Create `.env.local` to customize:
```env
VITE_API_URL=http://localhost:8000
```

---

## 🚀 Running the Application (Every Time)

### Option 1: Manual Start (Recommended for Learning)

**Terminal 1 - Start Backend:**
```powershell
cd C:\Users\HP\Desktop\pfa\backend
python main.py
```

**Wait for:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Loading AI model...
INFO: ✅ Model loaded successfully: microsoft/phi-2
INFO: ✅ Server ready!
```

⏱️ **First time:** ~30-60 seconds
⏱️ **Subsequent times:** ~30 seconds

---

**Terminal 2 - Start Frontend:**
```powershell
cd C:\Users\HP\Desktop\pfa\frontpfa\qrayti-your-moroccan-study-mate
npm run dev
```

**You'll see:**
```
  VITE ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

⏱️ **Takes:** ~2-3 seconds

---

### Option 2: Quick Start (After First Setup)

**Backend:**
```powershell
cd backend && python main.py
```

**Frontend (new terminal):**
```powershell
cd frontpfa/qrayti-your-moroccan-study-mate && npm run dev
```

---

## 🎮 Using the Application

### Step 1: Open in Browser

Go to: **http://localhost:5173**

---

### Step 2: Upload a PDF

**Method A: Real PDF**
1. Click or drag-drop a PDF file
2. Wait for extraction (~5-10 seconds)
3. See extracted content

**Method B: Demo Mode**
1. Click "Essayer avec un exemple"
2. Instant demo content loaded

---

### Step 3: Choose Mode

**Quiz Mode:**
- AI generates 5 questions
- Multiple choice format
- French questions
- Darija explanations
- Takes ~15-60 seconds

**Resume Mode:**
- AI generates structured summary
- Key terms with definitions
- Essential points
- French + Darija
- Takes ~15-60 seconds

---

### Step 4: Enjoy!

- Answer quiz questions
- Get instant feedback
- See explanations in Darija
- Read AI-generated summaries

---

## 🧪 Quick Test

### Test 1: Backend Health

```powershell
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "model_type": "local (microsoft/phi-2)",
  "model_ready": true
}
```

---

### Test 2: Frontend Loading

Open: http://localhost:5173

**Expected:**
- Beautiful landing page
- Upload section visible
- No errors in console

---

### Test 3: Full Flow

1. Go to http://localhost:5173
2. Scroll to "Commencez maintenant"
3. Click "Essayer avec un exemple"
4. Click "Mode Quiz"
5. Wait ~20-60 seconds
6. See AI-generated questions!

---

## 📊 What's Running

### Backend (Terminal 1)
```
URL: http://localhost:8000
API Docs: http://localhost:8000/docs
Model: microsoft/phi-2
Status: ✅ Ready

Endpoints:
- POST /api/upload-pdf
- POST /api/generate-quiz
- POST /api/generate-summary
- GET /health
```

### Frontend (Terminal 2)
```
URL: http://localhost:5173
Framework: React + TypeScript
Status: ✅ Running

Features:
- PDF Upload
- Quiz Mode (AI)
- Resume Mode (AI)
- French + Darija support
```

---

## ⏱️ Performance Guide

### PDF Processing
- **Small PDFs** (< 10 pages): 2-5 seconds
- **Large PDFs** (> 50 pages): 10-20 seconds

### AI Generation
**With GPU (NVIDIA):**
- Quiz: 15-25 seconds
- Summary: 15-25 seconds

**With CPU Only:**
- Quiz: 45-60 seconds
- Summary: 45-60 seconds

**Note:** First generation is slower (model warmup), subsequent generations are faster.

---

## 🐛 Common Issues & Solutions

### Issue 1: "Cannot connect to backend"

**Symptoms:**
- Frontend shows error message
- "Please check your connection"

**Solution:**
1. Check backend is running in Terminal 1
2. Visit http://localhost:8000/health
3. Restart backend if needed

---

### Issue 2: Backend won't start

**Symptoms:**
- Import errors
- Module not found

**Solution:**
```powershell
cd backend
pip install -r requirements.txt
```

---

### Issue 3: Model not loading

**Symptoms:**
- Backend starts but stays at "Loading AI model..."
- No ✅ Model loaded message

**Solution:**
1. Wait longer (first time can take 60+ seconds)
2. Check you have 8GB+ RAM
3. Check model downloaded: Run `python download_model.py` again

---

### Issue 4: Frontend shows blank page

**Symptoms:**
- White screen
- Console errors

**Solution:**
```powershell
cd frontpfa/qrayti-your-moroccan-study-mate
npm install
npm run dev
```

---

### Issue 5: Generation takes forever

**Symptoms:**
- Loading for 2+ minutes
- No response

**Solution:**
1. This is normal for CPU mode first time
2. Check backend logs for errors
3. Try with shorter content
4. Restart backend

---

### Issue 6: Port already in use

**Symptoms:**
- "Port 8000 already in use"
- "Port 5173 already in use"

**Solution for Backend:**
Edit `backend/.env`:
```env
PORT=8001
```

**Solution for Frontend:**
```powershell
npm run dev -- --port 5174
```

---

## 📁 Project Structure

```
C:\Users\HP\Desktop\pfa\
│
├── backend\                           ← Backend (Python)
│   ├── main.py                       ← FastAPI server
│   ├── config.py                     ← Configuration
│   ├── requirements.txt              ← Python packages
│   ├── .env                          ← Your settings (create this)
│   ├── env_template_phi2            ← Template for .env
│   │
│   ├── services\
│   │   ├── local_ai_service.py      ← phi-2 integration
│   │   └── pdf_service.py           ← PDF processing
│   │
│   ├── download_model.py            ← Model downloader
│   ├── test_api.py                  ← API tests
│   ├── quick_setup.py               ← Automated setup
│   │
│   └── Documentation\
│       ├── START_HERE.md
│       ├── LOCAL_MODEL_SETUP.md
│       └── README.md
│
├── frontpfa\qrayti-your-moroccan-study-mate\  ← Frontend (React)
│   ├── src\
│   │   ├── components\
│   │   │   ├── PDFUploader.tsx      ← Upload component (REAL)
│   │   │   ├── QuizMode.tsx         ← Quiz component (REAL AI)
│   │   │   ├── ResumeMode.tsx       ← Summary component (REAL AI)
│   │   │   └── AppSection.tsx       ← Main app container
│   │   │
│   │   └── services\
│   │       └── api.ts                ← API service (NEW!)
│   │
│   ├── package.json
│   ├── .env.local                   ← Frontend config (optional)
│   └── vite.config.ts
│
├── FULL_INTEGRATION_GUIDE.md        ← Complete guide
├── START_EVERYTHING.md              ← This file
└── READY_TO_USE_PHI2.md            ← Backend setup guide
```

---

## 🎯 Quick Reference

### Start Commands
```powershell
# Backend
cd C:\Users\HP\Desktop\pfa\backend
python main.py

# Frontend (new terminal)
cd C:\Users\HP\Desktop\pfa\frontpfa\qrayti-your-moroccan-study-mate
npm run dev
```

### URLs
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Stop Commands
- **Backend:** Press `Ctrl+C` in Terminal 1
- **Frontend:** Press `Ctrl+C` in Terminal 2

---

## 📚 Documentation

- **FULL_INTEGRATION_GUIDE.md** - Complete integration details
- **READY_TO_USE_PHI2.md** - Backend setup guide
- **backend/START_HERE.md** - Backend quick start
- **backend/LOCAL_MODEL_SETUP.md** - Model setup details
- **backend/README.md** - API documentation

---

## ✅ Final Checklist

Before you start:

- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend `.env` file created
- [ ] microsoft/phi-2 model downloaded
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Two terminal windows ready

To start:

- [ ] Terminal 1: `cd backend && python main.py`
- [ ] Wait for "✅ Server ready!"
- [ ] Terminal 2: `cd frontpfa/qrayti-your-moroccan-study-mate && npm run dev`
- [ ] Open browser: http://localhost:5173
- [ ] Test with demo mode first
- [ ] Upload a real PDF
- [ ] Generate quiz and summary

---

## 🎉 You're All Set!

Everything is configured and ready to go. Just run the two commands and your AI-powered educational app will be running!

### Quick Start:
```powershell
# Terminal 1
cd C:\Users\HP\Desktop\pfa\backend && python main.py

# Terminal 2 (new window)
cd C:\Users\HP\Desktop\pfa\frontpfa\qrayti-your-moroccan-study-mate && npm run dev

# Browser
http://localhost:5173
```

---

**🚀 Good luck with your Qrayti project! 🇲🇦📚**

Your AI-powered educational assistant for Moroccan students is ready to launch!

