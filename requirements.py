import subprocess
import sys

def install_requirements():
    requirements = [
        'openai',
        'python-dotenv',
        'requests',
        'colorama',
        'rich',
        'typer'
    ]

    print("Installing required packages...")
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            sys.exit(1)
    
    print("\nAll requirements installed successfully!")

if __name__ == "__main__":
    install_requirements() 