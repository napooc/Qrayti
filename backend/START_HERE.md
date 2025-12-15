# 🚀 START HERE - Qrayti Backend with microsoft/phi-2

## ⚡ Super Quick Start (One Command)

Run this single command to set everything up:

```powershell
python quick_setup.py
```

This will:
1. ✅ Check Python version
2. ✅ Install dependencies
3. ✅ Create configuration file
4. ✅ Download phi-2 model
5. ✅ Verify everything works
6. ✅ Start the server (optional)

**Total time: ~20-25 minutes**

---

## 📋 Manual Setup (If You Prefer)

### Step 1: Install Dependencies (10 min)
```powershell
pip install -r requirements.txt
```

### Step 2: Configuration is Ready!
The `.env` file is already created with phi-2 configuration. ✅

### Step 3: Download Model (5-10 min)
```powershell
python download_model.py
```
Choose option `3` for microsoft/phi-2

### Step 4: Start Server (30 sec)
```powershell
python main.py
```

### Step 5: Test It (2 min)
Open NEW terminal:
```powershell
python test_api.py
```

---

## 🎯 What You Get

Your backend with **microsoft/phi-2** provides:

✅ **PDF Processing** - Upload PDFs, extract text
✅ **AI Quiz Generation** - Create questions with French & Darija explanations
✅ **AI Summaries** - Generate structured summaries with key terms
✅ **100% Local** - No API keys, no costs, complete privacy
✅ **Ready for Frontend** - CORS configured, endpoints ready

---

## 🤖 About microsoft/phi-2

- **Size**: 2.7 billion parameters (~5GB download)
- **Quality**: ⭐⭐⭐⭐ Excellent for educational tasks
- **Speed**: Fast (15-60 seconds per request)
- **Hardware**: Works on CPU, faster with GPU
- **Languages**: English, French, Arabic support
- **Cost**: FREE - runs locally

**Perfect for educational applications!**

---

## 📊 System Requirements

### Minimum (CPU Mode)
- **RAM**: 8GB
- **Disk**: 10GB free space
- **CPU**: Modern multi-core
- **Internet**: For initial download only

### Recommended (GPU Mode)
- **GPU**: NVIDIA with 6GB+ VRAM
- **RAM**: 16GB
- **Disk**: 20GB free space

---

## 🎮 Quick Test After Setup

### Test 1: Health Check
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

### Test 2: Generate Quiz
```powershell
curl -X POST http://localhost:8000/api/generate-quiz -H "Content-Type: application/json" -d "{\"content\": \"Le DOC régit le droit civil marocain\", \"num_questions\": 2}"
```

### Test 3: Interactive Docs
Open browser: **http://localhost:8000/docs**

---

## 📚 Documentation

- **START_HERE.md** ← You are here
- **LOCAL_MODEL_SETUP.md** - Detailed setup & troubleshooting
- **BACKEND_SETUP_COMPLETE.md** - Complete overview
- **README.md** - API documentation

---

## 🆘 Troubleshooting

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Out of memory"
Update `.env`:
```env
LOAD_IN_8BIT=True
```

### Port 8000 in use
Update `.env`:
```env
PORT=8001
```

### Model download fails
- Check internet connection
- Try again: `python download_model.py`
- Or skip - will auto-download on server start

---

## ✨ Pro Tips

1. **Use quick_setup.py** - Automates everything
2. **Be patient** - First download takes time
3. **GPU is faster** - But CPU works fine
4. **Check the docs** - Interactive at /docs
5. **Test first** - Use test_api.py

---

## 🎯 Current Configuration

```
✅ Model: microsoft/phi-2 (2.7B parameters)
✅ Device: Auto-detect (GPU if available, else CPU)
✅ Server: http://localhost:8000
✅ CORS: Enabled for frontend
✅ PDF Support: Yes
✅ API Keys: None needed!
```

---

## 🚀 Ready? Run This!

```powershell
python quick_setup.py
```

Or manually:
```powershell
pip install -r requirements.txt
python download_model.py
python main.py
```

---

## 💬 Need Help?

1. Check server logs (terminal where main.py runs)
2. Read LOCAL_MODEL_SETUP.md for detailed troubleshooting
3. Visit http://localhost:8000/docs when server is running
4. Review error messages - they're descriptive!

---

**🎉 Your AI backend is ready! Let's go! 🇲🇦📚**

