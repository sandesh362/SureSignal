"""
Setup script for Misinformation Detection Pipeline
"""
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def download_spacy_model():
    """Download spaCy English model"""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Could not download spaCy model: {e}")
        print("💡 You can run this manually: python -m spacy download en_core_web_sm")

def create_directories():
    """Create necessary directories"""
    directories = ["config", "storage", "ingestion", "preprocessing", "tests"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create __init__.py files
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("# Auto-generated __init__.py\n")
    print("✅ Directories created successfully")

def main():
    print("🚀 Setting up Misinformation Detection Pipeline...")
    
    create_directories()
    
    if install_requirements():
        download_spacy_model()
    
    print("\n📋 Next steps:")
    print("1. Update config/config.yaml with your API keys")
    print("2. Make sure MongoDB is running")
    print("3. Run: python main.py")

if __name__ == "__main__":
    main()