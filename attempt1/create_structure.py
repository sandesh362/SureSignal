import os

def create_structure():
    """Create the proper directory structure"""
    
    base_dir = "D:/mumbaihacks"
    
    # Directories to create
    directories = [
        "preprocessing",
        "ingestion", 
        "storage",
        "config"
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create __init__.py files (except for config)
        if directory != "config":
            init_file = os.path.join(dir_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write("# Auto-generated __init__.py\n")
        
        print(f"✅ Created directory: {directory}")
    
    print("\n📁 Directory structure created successfully!")
    print("Now copy the individual files from the artifact above into their respective directories.")

if __name__ == "__main__":
    create_structure()