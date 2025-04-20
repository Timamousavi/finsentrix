import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_windows_app():
    print("Building Windows application...")
    
    # Create build directory
    build_dir = Path("build/windows")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Install PyInstaller if not already installed
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    subprocess.run([
        "pyinstaller",
        "--name=FinSentrix",
        "--windowed",
        "--onefile",
        "--icon=docs/assets/icon.ico",
        "--add-data=src;src",
        "--add-data=docs;docs",
        "src/gui/main.py"
    ])
    
    # Create installer using Inno Setup
    print("Creating installer...")
    subprocess.run([
        "iscc",
        "/O" + str(build_dir),
        "installer.iss"
    ])
    
    print("Build complete! Installer is available in build/windows/")

if __name__ == "__main__":
    build_windows_app() 