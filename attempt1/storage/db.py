from pymongo import MongoClient
import yaml
import os

def load_config():
    """Load configuration with error handling"""
    try:
        # Look for config in the parent directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(current_dir), "config", "config.yaml")
        
        if not os.path.exists(config_path):
            print(f"❌ Config file not found at: {config_path}")
            return None
            
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ Config file not found. Please create config/config.yaml")
        return None
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

config = load_config()
db = None
db_connected = False

if config:
    try:
        client = MongoClient(config["mongo"]["uri"])
        db = client[config["mongo"]["db_name"]]
        # Test connection
        client.admin.command('ping')
        db_connected = True
        print("✅ MongoDB connected")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        db = None
        db_connected = False