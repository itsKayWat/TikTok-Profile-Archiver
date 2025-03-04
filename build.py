import os
import sys
import PyInstaller.__main__
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    """Create a black square icon with white music note"""
    # Create a new image with a black background
    size = (256, 256)
    icon = Image.new('RGB', size, 'black')
    draw = ImageDraw.Draw(icon)
    
    try:
        # Try to use a font that has music note symbol
        font = ImageFont.truetype("arial.ttf", 150)
        # Unicode for music note
        music_note = "♪"
    except:
        # Fallback if font not found
        font = ImageFont.load_default()
        music_note = "♪"
    
    # Get text size
    text_bbox = draw.textbbox((0, 0), music_note, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate center position
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw white music note
    draw.text((x, y), music_note, fill='white', font=font)
    
    # Save as ICO file
    icon_path = os.path.join('assets', 'icon.ico')
    os.makedirs('assets', exist_ok=True)
    icon.save(icon_path, format='ICO')
    
    return icon_path

def build_exe():
    """Build the executable using PyInstaller"""
    # Create icon
    icon_path = create_icon()
    
    # PyInstaller command line arguments
    args = [
        'gui.py',  # Main script
        '--onefile',
        '--noconsole',
        f'--icon={icon_path}',
        '--name=TikTok Profile Archiver',
        '--add-data=assets;assets',
        
        # Add all required hidden imports
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=customtkinter',
        '--hidden-import=selenium',
        '--hidden-import=webdriver_manager',
        '--hidden-import=requests',
        '--hidden-import=json',
        '--hidden-import=datetime',
        '--hidden-import=threading',
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--hidden-import=src.licensing.license_manager',
        '--hidden-import=src.licensing.activation_wizard',
        '--hidden-import=src.licensing.activation_splash',
        '--hidden-import=src.splash_screen',
        
        # Add collect-all for key packages
        '--collect-all=customtkinter',
        '--collect-all=selenium',
        '--collect-all=webdriver_manager',
        
        # Add debug and logging
        '--debug=all',
        '--log-level=DEBUG',
    ]
    
    # Add all required data files and folders
    additional_data = [
        ('src', 'src'),
        ('licensing', 'licensing'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('tt-backup.py', '.'),
        ('web', 'web'),
        ('assets', 'assets'),
    ]
    
    for src, dst in additional_data:
        if os.path.exists(src):
            args.append(f'--add-data={src};{dst}')
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    # Clean previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
    
    # Install required packages
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    os.system(f"{sys.executable} -m pip install pillow pyinstaller")
    
    # Build the executable
    build_exe()
    
    print("\nBuild complete! Executable is in the dist folder.") 