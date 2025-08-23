"""
Panel Flutter Analysis GUI - Main Launcher
==========================================

Main launcher script that properly sets up the Python path
and starts the panel flutter analysis GUI application.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Now import and run the application
try:
    from gui.main_app import PanelFlutterApp
    
    if __name__ == "__main__":
        print("Starting Panel Flutter Analysis GUI...")
        print(f"Working directory: {current_dir}")
        print(f"Source directory: {src_dir}")
        
        app = PanelFlutterApp()
        app.run()
        
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Application Error: {e}")
    sys.exit(1)