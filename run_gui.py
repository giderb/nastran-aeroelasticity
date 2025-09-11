"""
PANEL FLUTTER ANALYSIS GUI - FINAL LAUNCHER
===========================================
This launcher ensures the GUI runs correctly.
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Setup paths
current_dir = Path(__file__).parent.absolute()
os.chdir(current_dir)
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "src"))

print("=" * 60)
print("PANEL FLUTTER ANALYSIS - NASTRAN AEROELASTICITY SUITE")
print("=" * 60)
print()
print(f"Working directory: {current_dir}")
print()

# Check dependencies
print("Checking dependencies...")
required = ['numpy', 'matplotlib', 'pandas', 'tkinter']
missing = []

for pkg in required:
    try:
        if pkg == 'tkinter':
            import tkinter
        else:
            __import__(pkg)
        print(f"  [OK] {pkg}")
    except ImportError:
        print(f"  [MISSING] {pkg}")
        missing.append(pkg)

if missing:
    print()
    print("ERROR: Missing required packages!")
    print(f"Please install: {', '.join(missing)}")
    input("Press Enter to exit...")
    sys.exit(1)

print()
print("All dependencies satisfied!")
print()
print("Starting GUI application...")
print("-" * 60)

try:
    # Import the GUI
    from launch_gui import PanelFlutterGUI
    
    # Create application instance
    app = PanelFlutterGUI()
    
    print("GUI initialized successfully!")
    print()
    print("APPLICATION IS NOW RUNNING")
    print("Close the GUI window to exit")
    print("-" * 60)
    
    # Run the application
    app.run()
    
    print()
    print("Application closed normally")
    
except KeyboardInterrupt:
    print()
    print("Application terminated by user")
    
except Exception as e:
    print()
    print("ERROR: Failed to start GUI!")
    print(f"Error details: {e}")
    print()
    import traceback
    traceback.print_exc()
    print()
    input("Press Enter to exit...")
    sys.exit(1)
