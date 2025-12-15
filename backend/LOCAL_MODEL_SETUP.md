# Local Model Setup Guide

## 🎯 Overview

Your backend is now configured to use **LOCAL AI MODELS** - no API keys needed! Everything runs on your computer.

## 🤖 About Local Models

### What are Local Models?

- AI models that run on **YOUR** computer
- **No internet** needed after download
- **No API costs** - completely free
- **Private** - your data never leaves your machine

### Trade-offs

| Aspect | Local Models | API (OpenAI) |
|--------|-------------|--------------|
| Cost | Free (after download) | Pay per use |
| Privacy | 100% private | Data sent to servers |
| Setup | More complex | Simple |
| Speed | Depends on hardware | Fast |
| Quality | Varies by model | Consistently high |
| Hardware | Needs good CPU/GPU | Any computer |

---

## 📋 Requirements

### Minimum Requirements (CPU Mode)
- **RAM**: 8GB+ (16GB recommended)
- **Disk Space**: 5-20GB depending on model
- **CPU**: Modern multi-core processor
- **Internet**: For initial model download only

### Recommended (GPU Mode)
- **GPU**: NVIDIA GPU with 6GB+ VRAM
- **CUDA**: Installed (for NVIDIA GPUs)
- **RAM**: 16GB+
- **Disk Space**: 20GB+

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```powershell
cd C:\Users\HP\Desktop\pfa\backend
pip install -r requirements.txt
```

This installs:
- ✅ PyTorch (deep learning framework)
- ✅ Transformers (model loading)
- ✅ Accelerate (optimization)
- ✅ FastAPI and other dependencies

**Note**: First installation may take 10-15 minutes due to large packages.

### Step 2: Create .env File

Copy the template:
```powershell
copy .env.template .env
```

Or create `.env` with this content:

```env
# Model Configuration
LOCAL_MODEL_NAME=microsoft/phi-2
DEVICE=auto
LOAD_IN_8BIT=False
MAX_LENGTH=2048
TEMPERATURE=0.7

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Step 3: Download a Model

Run the interactive downloader:
```powershell
python download_model.py
```

This will:
1. Show you recommended models
2. Check your hardware (CPU/GPU)
3. Download and test the model
4. Verify it works

---

## 🎨 Choosing a Model

### Option 1: gpt2 (Fastest, CPU-friendly)
```env
LOCAL_MODEL_NAME=gpt2
```
- **Size**: ~500 MB
- **Quality**: ⭐⭐ Basic
- **Speed**: ⚡⚡⚡ Very Fast
- **Hardware**: CPU is fine
- **Best for**: Testing, development

### Option 2: microsoft/phi-2 (Recommended)
```env
LOCAL_MODEL_NAME=microsoft/phi-2
```
- **Size**: ~5 GB
- **Quality**: ⭐⭐⭐⭐ Good
- **Speed**: ⚡⚡ Moderate
- **Hardware**: CPU works, GPU better
- **Best for**: Education, production use

### Option 3: google/gemma-2b-it
```env
LOCAL_MODEL_NAME=google/gemma-2b-it
```
- **Size**: ~4 GB
- **Quality**: ⭐⭐⭐⭐ Good
- **Speed**: ⚡⚡ Moderate
- **Hardware**: GPU recommended
- **Best for**: Instruction following

### Option 4: mistralai/Mistral-7B-Instruct-v0.2 (Best Quality)
```env
LOCAL_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
```
- **Size**: ~15 GB
- **Quality**: ⭐⭐⭐⭐⭐ Excellent
- **Speed**: ⚡ Slower
- **Hardware**: GPU with 8GB+ VRAM required
- **Best for**: Production with GPU

---

## 📥 Model Download Process

### Method 1: Interactive Downloader (Recommended)

```powershell
python download_model.py
```

Follow the prompts:
1. Choose a model
2. Wait for download (5-20 minutes)
3. Model is tested automatically
4. Ready to use!

### Method 2: Command Line

Download a specific model:
```powershell
python download_model.py gpt2
python download_model.py microsoft/phi-2
python download_model.py mistralai/Mistral-7B-Instruct-v0.2
```

### Method 3: Manual Download

The model will auto-download when you first start the server:
```powershell
python main.py
```

---

## 🖥️ Hardware Optimization

### If You Have an NVIDIA GPU

1. **Check if CUDA is available:**
```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

If `True`: You can use GPU acceleration! 🎉

2. **Update .env for GPU:**
```env
DEVICE=cuda
LOAD_IN_8BIT=True  # Saves memory
```

3. **Install GPU support (if not already):**
```powershell
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### If You Only Have CPU

That's fine! Use smaller models:

```env
LOCAL_MODEL_NAME=gpt2
# or
LOCAL_MODEL_NAME=microsoft/phi-2
DEVICE=cpu
```

---

## ▶️ Starting the Server

### First Run (Downloads Model)

```powershell
python main.py
```

Expected output:
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Loading AI model...
INFO: Loading model: microsoft/phi-2
INFO: This may take a few minutes on first run (downloading model)...
INFO: Using device: cuda  (or cpu)
INFO: ✅ Model loaded successfully: microsoft/phi-2
INFO: ✅ Server ready!
```

**First run**: May take 5-20 minutes (downloading model)
**Subsequent runs**: Fast (~30 seconds to load model)

### Subsequent Runs

Model is cached, so it loads from disk:
```powershell
python main.py
```

Much faster! (~30 seconds)

---

## 🧪 Testing the Backend

### Test Script

```powershell
python test_api.py
```

This tests:
- ✅ Health check
- ✅ Quiz generation
- ✅ Summary generation

### Manual Testing

1. Start the server: `python main.py`
2. Open browser: http://localhost:8000/docs
3. Try the `/api/generate-quiz` endpoint
4. Click "Try it out" and test!

---

## 📊 Model Comparison

| Model | Download Size | RAM Needed | GPU VRAM | Speed (CPU) | Quality | Arabic Support |
|-------|--------------|-----------|----------|-------------|---------|----------------|
| gpt2 | 500 MB | 4GB | N/A | Fast | Basic | Limited |
| phi-2 | 5 GB | 8GB | 4GB | Moderate | Good | Yes |
| gemma-2b | 4 GB | 8GB | 4GB | Moderate | Good | Yes |
| Mistral-7B | 15 GB | 16GB | 8GB | Slow | Excellent | Yes |

**For Darija (Moroccan Arabic)**: Larger models (phi-2, Mistral) work better with Arabic text.

---

## 🐛 Troubleshooting

### "Out of memory" Error

**Solution 1**: Use a smaller model
```env
LOCAL_MODEL_NAME=gpt2
```

**Solution 2**: If you have GPU, enable 8-bit mode
```env
LOAD_IN_8BIT=True
```

**Solution 3**: Close other applications to free RAM

### "CUDA out of memory"

**Solution 1**: Enable 8-bit quantization
```env
LOAD_IN_8BIT=True
```

**Solution 2**: Use CPU instead
```env
DEVICE=cpu
```

**Solution 3**: Use a smaller model

### Model Download Fails

**Solution 1**: Check internet connection

**Solution 2**: Try a different model

**Solution 3**: Download manually from Hugging Face website

### Model Loading is Very Slow

**Normal on first run** (downloading)
**Subsequent runs should be faster** (~30 seconds)

If still slow:
- Check disk speed (SSD is faster than HDD)
- Close other applications
- Use a smaller model

### Generated Responses are Poor Quality

**Solution 1**: Use a larger model (phi-2 or Mistral-7B)

**Solution 2**: Adjust temperature in .env:
```env
TEMPERATURE=0.7  # Lower = more focused, Higher = more creative
```

**Solution 3**: The model may need fine-tuning for your specific use case

---

## 💡 Tips for Best Results

1. **Start with phi-2** - Good balance of quality and speed
2. **Use GPU if available** - Much faster
3. **Be patient on first run** - Model download takes time
4. **Close other apps** - Free up RAM
5. **SSD recommended** - Faster model loading

---

## 📈 Performance Expectations

### Quiz Generation Time

| Model | CPU | GPU |
|-------|-----|-----|
| gpt2 | ~30s | ~10s |
| phi-2 | ~60s | ~15s |
| Mistral-7B | ~120s | ~20s |

### Summary Generation Time

Similar to quiz generation.

**Note**: First request is slower (model warmup), subsequent requests are faster.

---

## 🔄 Switching Models

To try a different model:

1. Update `.env`:
```env
LOCAL_MODEL_NAME=gpt2
```

2. Download new model:
```powershell
python download_model.py gpt2
```

3. Restart server:
```powershell
python main.py
```

Models are cached, so you can switch between them easily!

---

## 📦 Where are Models Stored?

Models are downloaded to:
```
C:\Users\HP\.cache\huggingface\hub\
```

You can delete old models to free space:
```powershell
# WARNING: This deletes ALL cached models
rmdir /s C:\Users\HP\.cache\huggingface
```

---

## 🎯 Next Steps

1. ✅ Install dependencies (`pip install -r requirements.txt`)
2. ✅ Create `.env` file
3. ✅ Download a model (`python download_model.py`)
4. ✅ Start server (`python main.py`)
5. ✅ Test it (`python test_api.py`)
6. 🔄 Connect frontend to backend

---

## 🆘 Getting Help

If you run into issues:

1. Check the server logs (terminal output)
2. Try a smaller model first (gpt2)
3. Check hardware requirements
4. Make sure you have enough disk space
5. Verify internet connection for download

---

## 🎉 You're Ready!

Once the model is downloaded and the server starts successfully, you have a **fully functional AI backend** running locally on your machine!

No API keys, no costs, complete privacy. 🚀

