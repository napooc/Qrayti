"""
Quick setup script for Qrayti Backend with microsoft/phi-2
This automates the entire setup process.
"""
import os
import sys
import subprocess


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_step(number, text):
    """Print step number."""
    print(f"\n{'='*70}")
    print(f"  STEP {number}: {text}")
    print(f"{'='*70}\n")


def check_python_version():
    """Check if Python version is adequate."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print("   Please install Python 3.8+")
        return False
    
    print("✅ Python version is compatible")
    return True


def check_dependencies():
    """Check if dependencies are installed."""
    print_step(2, "Checking Dependencies")
    
    try:
        import torch
        import transformers
        import fastapi
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"⚠️  Missing dependencies: {e.name}")
        print("\nWould you like to install them now?")
        choice = input("Install dependencies? (y/N): ").strip().lower()
        
        if choice == 'y':
            print("\n📦 Installing dependencies...")
            print("This will take 10-15 minutes...\n")
            
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
                ])
                print("\n✅ Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies")
                print("   Please run manually: pip install -r requirements.txt")
                return False
        else:
            print("❌ Dependencies required. Run: pip install -r requirements.txt")
            return False


def verify_env_file():
    """Verify .env file exists."""
    print_step(3, "Checking Configuration")
    
    if os.path.exists(".env"):
        print("✅ .env file exists")
        
        # Check if it has phi-2 configured
        with open(".env", "r") as f:
            content = f.read()
            if "microsoft/phi-2" in content:
                print("✅ Configured for microsoft/phi-2")
                return True
            else:
                print("⚠️  .env exists but not configured for phi-2")
                print("   Current .env will be backed up and recreated")
    
    print("📝 Creating .env file for microsoft/phi-2...")
    
    # Backup existing .env if it exists
    if os.path.exists(".env"):
        import shutil
        shutil.copy(".env", ".env.backup")
        print("   Backed up existing .env to .env.backup")
    
    # Create new .env
    env_content = """# Qrayti Backend Configuration
# Using microsoft/phi-2 Local Model

LOCAL_MODEL_NAME=microsoft/phi-2
DEVICE=auto
LOAD_IN_8BIT=False
MAX_LENGTH=2048
TEMPERATURE=0.7

HOST=0.0.0.0
PORT=8000
DEBUG=True

CORS_ORIGINS=http://localhost:5173,http://localhost:3000
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ .env file created with phi-2 configuration")
    return True


def download_model():
    """Download the phi-2 model."""
    print_step(4, "Downloading microsoft/phi-2 Model")
    
    print("The phi-2 model is ~5GB and will be downloaded to:")
    print(f"C:\\Users\\{os.getenv('USERNAME', 'USER')}\\.cache\\huggingface\\hub\\")
    print("\nThis will take 5-15 minutes depending on your internet speed.")
    print("\nOptions:")
    print("  1. Download now (recommended)")
    print("  2. Skip (download will happen when server starts)")
    
    choice = input("\nYour choice (1-2): ").strip()
    
    if choice == "1":
        print("\n📥 Starting download...")
        try:
            result = subprocess.run(
                [sys.executable, "download_model.py"],
                input="3\ny\n",  # Choose option 3 (phi-2) and confirm
                text=True,
                capture_output=False
            )
            
            if result.returncode == 0:
                print("\n✅ Model downloaded successfully!")
                return True
            else:
                print("\n⚠️  Download had issues but continuing...")
                return True
        except Exception as e:
            print(f"\n⚠️  Error during download: {e}")
            print("   Model will download automatically when server starts")
            return True
    else:
        print("\n⏭️  Skipping download - model will download on first server start")
        return True


def verify_setup():
    """Verify the setup is complete."""
    print_step(5, "Verifying Setup")
    
    checks = [
        ("config.py", "Configuration module"),
        ("main.py", "Main application"),
        ("services/local_ai_service.py", "AI service"),
        ("services/pdf_service.py", "PDF service"),
        (".env", "Environment configuration"),
    ]
    
    all_good = True
    for file, desc in checks:
        if os.path.exists(file):
            print(f"✅ {desc}: {file}")
        else:
            print(f"❌ {desc}: {file} - MISSING!")
            all_good = False
    
    return all_good


def print_next_steps():
    """Print instructions for next steps."""
    print_header("🎉 Setup Complete!")
    
    print("Your backend is ready to use with microsoft/phi-2!\n")
    
    print("📋 NEXT STEPS:\n")
    
    print("1️⃣  Start the server:")
    print("   python main.py\n")
    
    print("2️⃣  In a NEW terminal, test the API:")
    print("   python test_api.py\n")
    
    print("3️⃣  Try the interactive docs:")
    print("   Open browser: http://localhost:8000/docs\n")
    
    print("4️⃣  Connect your frontend:")
    print("   Update frontend to call http://localhost:8000/api/...\n")
    
    print("="*70)
    print("\n📚 Documentation:")
    print("   - LOCAL_MODEL_SETUP.md - Detailed setup guide")
    print("   - README.md - API documentation")
    print("   - BACKEND_SETUP_COMPLETE.md - Complete overview\n")
    
    print("💡 Tips:")
    print("   - First server start will load the model (~30-60 seconds)")
    print("   - Quiz/summary generation takes ~15-60 seconds")
    print("   - CPU mode works but GPU is faster\n")


def main():
    """Main setup flow."""
    print_header("Qrayti Backend Setup - microsoft/phi-2")
    
    print("This script will set up your backend to use the microsoft/phi-2")
    print("local AI model. No API keys required!\n")
    
    # Check Python
    if not check_python_version():
        return 1
    
    # Check/install dependencies
    if not check_dependencies():
        return 1
    
    # Setup .env file
    if not verify_env_file():
        return 1
    
    # Download model
    if not download_model():
        return 1
    
    # Verify everything
    if not verify_setup():
        print("\n❌ Setup verification failed!")
        print("   Some files are missing. Please check the backend folder.")
        return 1
    
    # Done!
    print_next_steps()
    
    # Ask if they want to start the server now
    print("\n" + "="*70)
    start = input("\nWould you like to start the server now? (y/N): ").strip().lower()
    
    if start == 'y':
        print("\n🚀 Starting server...\n")
        try:
            subprocess.run([sys.executable, "main.py"])
        except KeyboardInterrupt:
            print("\n\n✋ Server stopped by user")
    else:
        print("\n👍 Setup complete! Run 'python main.py' when ready.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

