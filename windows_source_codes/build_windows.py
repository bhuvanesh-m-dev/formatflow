import os
import subprocess
import sys
import shutil

def install_requirements():
    """Install necessary packages if not present."""
    required = {'pyinstaller', 'Pillow'}
    installed = set()
    
    # Check what's installed
    try:
        import PyInstaller
        installed.add('pyinstaller')
    except ImportError:
        pass
        
    try:
        import PIL
        installed.add('Pillow')
    except ImportError:
        pass
        
    missing = required - installed
    if missing:
        print(f"Installing missing requirements: {', '.join(missing)}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

def build_exe():
    print("Preparing build...")
    
    # 1. Convert PNG to ICO (Images work better as icons on Windows if they are .ico)
    try:
        from PIL import Image
        img = Image.open("FormatFlow.png")
        icon_path = "FormatFlow.ico"
        img.save(icon_path, format='ICO', sizes=[(256, 256)])
        print(f"Generated {icon_path}")
    except Exception as e:
        print(f"Error converting icon: {e}")
        return

    # 2. Run PyInstaller
    print("Running PyInstaller...")
    # --onefile: Single executable
    # --noconfirm: Don't ask to overwrite
    # --windowed: No console window (GUI app)
    # --icon: Path to icon
    # --name: Output name
    # --distpath: Output directory
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon", icon_path,
        "--name", "formatflow_0.1",
        "--distpath", "v0.1",
        "main.py"
    ]
    
    subprocess.check_call(cmd)
    
    # 3. Cleanup build artifacts
    print("Cleaning up...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("formatflow_0.1.spec"):
        os.remove("formatflow_0.1.spec")
    if os.path.exists(icon_path):
        os.remove(icon_path)
        
    print(f"Build complete! Executable saved in v0.1/")

if __name__ == "__main__":
    install_requirements()
    build_exe()
