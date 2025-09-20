"""
Setup script for Twitter Fact-Checking Bot
"""
import os
import subprocess
import sys

def create_directories():
    """Create necessary directories"""
    directories = ["config", "bot", "logs"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # Create __init__.py for Python packages
        if directory == "bot":
            init_file = os.path.join(directory, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write("# Bot package\n")
    
    print("✅ Directories created")

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tweepy>=4.14.0", "PyYAML>=6.0", "requests>=2.31.0"])
        print("✅ Requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_config_template():
    """Create config template if it doesn't exist"""
    config_path = "config/config.yaml"
    
    if not os.path.exists(config_path):
        config_content = '''twitter:
  api_key: "your_api_key_here"
  api_secret: "your_api_secret_here"
  access_token: "your_access_token_here"
  access_token_secret: "your_access_token_secret_here"
  bearer_token: "your_bearer_token_here"

bot:
  username: "your_bot_username"  # Your bot's Twitter username (without @)
  check_interval: 60  # Check for mentions every 60 seconds

factcheck:
  confidence_threshold: 0.7  # Minimum confidence to make a definitive claim
'''
        
        with open(config_path, "w") as f:
            f.write(config_content)
        
        print("✅ Config template created")
    else:
        print("ℹ️ Config file already exists")

def main():
    print("🤖 Setting up Twitter Fact-Checking Bot...")
    
    create_directories()
    
    if install_requirements():
        create_config_template()
        
        print("\n📋 Setup Complete! Next steps:")
        print("1. Get Twitter API credentials from https://developer.twitter.com")
        print("2. Update config/config.yaml with your credentials")
        print("3. Set your bot's username in the config")
        print("4. Run the bot: python run_bot.py")
        print("\n⚠️ Note: Your bot account needs to have API access and be approved for posting")

if __name__ == "__main__":
    main()