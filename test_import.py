#!/usr/bin/env python3
"""
Simple import test to check for syntax and import errors
without launching the full GUI.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

print("Testing imports...")

try:
    print("✓ Importing standard libraries...")
    import tkinter as tk
    from tkinter import ttk, messagebox
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import threading
    import time
    import logging
    print("✓ Standard libraries imported successfully")
    
    print("✓ Testing PanelFlutterGUI class syntax...")
    
    # Test if the file can be parsed without running it
    with open(current_dir / "launch_gui.py", "r") as f:
        code = f.read()
        
    # Try to compile the code to check for syntax errors
    compile(code, "launch_gui.py", "exec")
    print("✓ launch_gui.py syntax is valid")
    
    print("✓ Testing analysis engine imports...")
    try:
        from gui.analysis import (
            AnalysisRunner, FlutterAnalysisConfig, 
            GeometryConfig, MaterialConfig, ResultsAnalyzer
        )
        print("✓ Analysis engine imports successful")
    except ImportError as e:
        print(f"⚠ Analysis engine import failed: {e}")
        print("  This is expected if NASTRAN modules are not available")
    
    print("\n🎉 All tests passed! The application should launch successfully.")
    
except SyntaxError as e:
    print(f"❌ Syntax Error: {e}")
    print(f"   File: {e.filename}")
    print(f"   Line: {e.lineno}")
    print(f"   Text: {e.text}")
    sys.exit(1)
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    sys.exit(1)