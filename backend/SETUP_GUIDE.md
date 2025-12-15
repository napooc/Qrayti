# Quick Setup Guide for Qrayti Backend

## Step-by-Step Setup (First Time)

### 1️⃣ Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install all required packages including FastAPI, OpenAI, PyPDF2, etc.

### 2️⃣ Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in to your account
3. Click "Create new secret key"
4. Give it a name (e.g., "Qrayti Backend")
5. Copy the key (starts with `sk-...`)
6. **Important**: Save it somewhere safe - you can only see it once!

### 3️⃣ Create .env File

Create a file named `.env` in the `backend` folder with this content:

```env
OPENAI_API_KEY=sk-paste-your-key-here
MODEL_TYPE=openai
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Replace** `sk-paste-your-key-here` with your actual OpenAI API key!

### 4️⃣ Start the Server

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     AI Service initialized with model type: openai
```

### 5️⃣ Test the Backend

Open a new terminal and run:

```bash
python test_api.py
```

This will test all the endpoints and show you if everything is working!

### 6️⃣ Try the Interactive Docs

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- You can test all endpoints directly from the browser!

---

## Quick Commands Reference

### Start the server:
```bash
python main.py
```

### Stop the server:
Press `CTRL+C` in the terminal

### Test the API:
```bash
python test_api.py
```

### Check if server is running:
```bash
curl http://localhost:8000/health
```

---

## Troubleshooting

### ❌ "Module not found" error
```bash
pip install -r requirements.txt
```

### ❌ "OpenAI API key not found"
- Check your `.env` file exists in the `backend` folder
- Make sure the key starts with `sk-`
- No quotes needed around the key in .env

### ❌ "Port 8000 already in use"
Change the port in `.env`:
```env
PORT=8001
```

### ❌ "Connection refused" when testing
Make sure the server is running in another terminal

---

## Cost Information

**OpenAI API Costs** (as of 2024):
- GPT-3.5-Turbo: ~$0.001 per request
- GPT-4: ~$0.03 per request

For testing and development, GPT-3.5-Turbo is recommended and very affordable.
You can start with a $5 credit which will last for thousands of requests.

---

## Next: Connect Frontend

Once your backend is running successfully:

1. Update your frontend API calls to point to `http://localhost:8000`
2. The backend will accept requests from `http://localhost:5173` (default Vite port)
3. Test uploading a PDF and generating quizzes!

---

## Need Help?

- Check the logs in the terminal where the server is running
- Visit http://localhost:8000/docs to see all available endpoints
- Review `README.md` for detailed documentation

