"""
Interactive setup script for Qrayti Backend.
Run this to quickly set up your environment.
"""
import os
import sys

def print_header():
    """Print welcome header."""
    print("\n" + "="*60)
    print("  🎓 Qrayti Backend Setup")
    print("="*60 + "\n")

def check_env_file():
    """Check if .env file exists."""
    return os.path.exists(".env")

def create_env_file():
    """Interactive creation of .env file."""
    print("Creating your .env file...\n")
    
    # Get API key
    print("📝 You need an OpenAI API key to use the AI features.")
    print("   Get one at: https://platform.openai.com/api-keys\n")
    
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        api_key = "your_openai_api_key_here"
        print("\n⚠️  No API key provided. You'll need to add it manually to .env later.")
    
    # Get port
    port = input("\nEnter port number (default 8000): ").strip() or "8000"
    
    # Get frontend URL
    frontend_url = input("\nEnter frontend URL (default http://localhost:5173): ").strip() or "http://localhost:5173"
    
    # Create .env content
    env_content = f"""# Qrayti Backend Configuration

# API Configuration
OPENAI_API_KEY={api_key}
MODEL_TYPE=openai

# Server Configuration
HOST=0.0.0.0
PORT={port}
DEBUG=True

# CORS Configuration (comma-separated URLs)
CORS_ORIGINS={frontend_url},http://localhost:3000
"""
    
    # Write .env file
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("\n✅ .env file created successfully!")
    return api_key != "your_openai_api_key_here"

def check_dependencies():
    """Check if required packages are installed."""
    print("\n" + "-"*60)
    print("Checking dependencies...")
    print("-"*60)
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("openai", "OpenAI"),
        ("PyPDF2", "PyPDF2"),
    ]
    
    missing = []
    
    for package, display_name in required_packages:
        try:
            __import__(package)
            print(f"✅ {display_name} installed")
        except ImportError:
            print(f"❌ {display_name} NOT installed")
            missing.append(display_name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall them with:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

def print_next_steps(has_api_key):
    """Print next steps."""
    print("\n" + "="*60)
    print("  🚀 Next Steps")
    print("="*60 + "\n")
    
    if not has_api_key:
        print("1. Add your OpenAI API key to the .env file:")
        print("   - Open backend/.env")
        print("   - Replace 'your_openai_api_key_here' with your actual key")
        print("   - Get a key at: https://platform.openai.com/api-keys\n")
    
    print(f"{2 if not has_api_key else 1}. Start the backend server:")
    print("   python main.py\n")
    
    print(f"{3 if not has_api_key else 2}. Test the API:")
    print("   python test_api.py\n")
    
    print(f"{4 if not has_api_key else 3}. Open API documentation:")
    print("   http://localhost:8000/docs\n")
    
    print("📚 For detailed instructions, see:")
    print("   - SETUP_GUIDE.md (quick start)")
    print("   - README.md (full documentation)")
    print()

def main():
    """Main setup flow."""
    print_header()
    
    # Check if .env exists
    if check_env_file():
        print("ℹ️  .env file already exists.")
        overwrite = input("Do you want to recreate it? (y/N): ").strip().lower()
        
        if overwrite != 'y':
            print("\nKeeping existing .env file.")
            has_api_key = True
        else:
            has_api_key = create_env_file()
    else:
        has_api_key = create_env_file()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n⚠️  Please install dependencies first:")
        print("   pip install -r requirements.txt")
        print("\nThen run this setup script again.")
        sys.exit(1)
    
    # Print next steps
    print_next_steps(has_api_key)
    
    print("="*60)
    print("  Setup complete! 🎉")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

