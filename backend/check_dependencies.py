"""
Quick script to check if all required dependencies are installed.
Run this to diagnose missing packages.
"""
import sys

def check_package(name, import_name=None):
    """Check if a package is installed."""
    if import_name is None:
        import_name = name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"[OK] {name}: {version}")
        return True
    except ImportError:
        print(f"[MISSING] {name}: NOT INSTALLED")
        return False

print("=" * 60)
print("  Checking Qrayti Backend Dependencies")
print("=" * 60)
print()

required = [
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("pydantic", "pydantic"),
    ("numpy", "numpy"),
    ("torch", "torch"),
    ("transformers", "transformers"),
    ("accelerate", "accelerate"),
    ("sentencepiece", "sentencepiece"),
    ("protobuf", "protobuf"),
    ("PyPDF2", "PyPDF2"),
]

all_ok = True
for name, import_name in required:
    if not check_package(name, import_name):
        all_ok = False

print()
print("=" * 60)
if all_ok:
    print("  [SUCCESS] All dependencies are installed!")
    print("=" * 60)
    sys.exit(0)
else:
    print("  [ERROR] Some dependencies are missing!")
    print("=" * 60)
    print()
    print("Install missing packages with:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

