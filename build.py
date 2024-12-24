import os
import shutil
import subprocess
import platform

def clean_build():
    """Clean build directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def build_executable():
    """Build the executable using PyInstaller"""
    subprocess.run(['pyinstaller', 'mahalli.spec'], check=True)

def post_build():
    """Post-build tasks"""
    if platform.system() == 'Windows':
        # Windows-specific tasks
        pass
    else:
        # Linux/Mac-specific tasks
        os.chmod('dist/mahalli/mahalli', 0o755)

def main():
    print("Cleaning previous builds...")
    clean_build()
    
    print("Building executable...")
    build_executable()
    
    print("Running post-build tasks...")
    post_build()
    
    print("Build complete! Executable is in dist/mahalli/")

if __name__ == "__main__":
    main() 