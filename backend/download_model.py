"""
Script to download and test a local model before using it in the API.
This helps ensure the model works before starting the server.
"""
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import settings


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_gpu():
    """Check if GPU is available."""
    print_header("Checking Hardware")
    
    if torch.cuda.is_available():
        print(f"✅ GPU Available: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        return True
    else:
        print("ℹ️  No GPU detected - will use CPU")
        print("   Note: CPU mode is slower but works fine for smaller models")
        return False


def download_and_test_model(model_name: str = None):
    """
    Download and test a model.
    
    Args:
        model_name: Model name from Hugging Face (e.g., 'microsoft/phi-2')
    """
    if model_name is None:
        model_name = settings.local_model_name
    
    print_header(f"Downloading Model: {model_name}")
    
    print("This may take several minutes depending on:")
    print("  - Model size")
    print("  - Your internet speed")
    print("  - First time download")
    print("\nPlease be patient...\n")
    
    try:
        # Check GPU
        has_gpu = check_gpu()
        device = "cuda" if has_gpu else "cpu"
        
        # Download tokenizer
        print("\n📥 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        print("✅ Tokenizer downloaded")
        
        # Set padding token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Download model
        print("\n📥 Downloading model...")
        print(f"   This is the big file - may take 5-15 minutes")
        
        model_kwargs = {
            "trust_remote_code": True,
            "torch_dtype": torch.float16 if has_gpu else torch.float32,
        }
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            **model_kwargs
        )
        
        model = model.to(device)
        print(f"✅ Model downloaded and loaded to {device}")
        
        # Test the model
        print_header("Testing Model")
        
        test_prompt = "Hello, my name is"
        print(f"Test prompt: '{test_prompt}'")
        print("Generating...")
        
        inputs = tokenizer(test_prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=20,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\n✅ Model Response: {result}\n")
        
        print_header("Success!")
        print(f"✅ Model '{model_name}' is ready to use!")
        print(f"   Device: {device}")
        print(f"   Status: Working")
        print("\nYou can now start the server with:")
        print("   python main.py")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        print("Possible solutions:")
        print("  1. Check your internet connection")
        print("  2. Try a smaller model:")
        print("     - gpt2 (smallest, fastest)")
        print("     - microsoft/phi-2 (good balance)")
        print("  3. Check if you have enough disk space")
        print("  4. Make sure you have the latest transformers:")
        print("     pip install --upgrade transformers")
        print()
        return False


def list_recommended_models():
    """List recommended models."""
    print_header("Recommended Models")
    
    models = [
        {
            "name": "gpt2",
            "size": "~500 MB",
            "quality": "⭐⭐",
            "speed": "⚡⚡⚡",
            "gpu": "Not required",
            "desc": "Smallest, fastest, lower quality"
        },
        {
            "name": "microsoft/phi-2",
            "size": "~5 GB",
            "quality": "⭐⭐⭐⭐",
            "speed": "⚡⚡",
            "gpu": "Recommended",
            "desc": "Good balance, educational tasks"
        },
        {
            "name": "google/gemma-2b-it",
            "size": "~4 GB",
            "quality": "⭐⭐⭐⭐",
            "speed": "⚡⚡",
            "gpu": "Recommended",
            "desc": "Good instruction following"
        },
        {
            "name": "mistralai/Mistral-7B-Instruct-v0.2",
            "size": "~15 GB",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "⚡",
            "gpu": "Required",
            "desc": "Best quality, needs powerful GPU"
        },
    ]
    
    for i, model in enumerate(models, 1):
        print(f"{i}. {model['name']}")
        print(f"   Size: {model['size']}")
        print(f"   Quality: {model['quality']}")
        print(f"   Speed: {model['speed']}")
        print(f"   GPU: {model['gpu']}")
        print(f"   Description: {model['desc']}")
        print()


def interactive_download():
    """Interactive model download."""
    print_header("Qrayti Model Downloader")
    
    print("This script will help you download a local AI model.")
    print()
    
    list_recommended_models()
    
    print("Current model in config: " + settings.local_model_name)
    print()
    
    choice = input("Choose an option:\n"
                   "  1. Download current model from config\n"
                   "  2. Download gpt2 (smallest)\n"
                   "  3. Download microsoft/phi-2 (recommended)\n"
                   "  4. Enter custom model name\n"
                   "\nYour choice (1-4): ").strip()
    
    if choice == "1":
        model_name = settings.local_model_name
    elif choice == "2":
        model_name = "gpt2"
    elif choice == "3":
        model_name = "microsoft/phi-2"
    elif choice == "4":
        model_name = input("\nEnter model name from Hugging Face: ").strip()
    else:
        print("Invalid choice")
        return
    
    print(f"\n📦 Will download: {model_name}")
    confirm = input("Continue? (y/N): ").strip().lower()
    
    if confirm == 'y':
        success = download_and_test_model(model_name)
        
        if success and model_name != settings.local_model_name:
            print(f"\n💡 To use this model, update your .env file:")
            print(f"   LOCAL_MODEL_NAME={model_name}")
    else:
        print("Cancelled.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line argument provided
        model_name = sys.argv[1]
        download_and_test_model(model_name)
    else:
        # Interactive mode
        interactive_download()

