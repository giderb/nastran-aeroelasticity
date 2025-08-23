"""
Panel Flutter Analysis GUI - Main Application
=============================================

A comprehensive graphical user interface for panel flutter analysis using NASTRAN.
This application provides tools for geometry definition, material specification,
analysis setup, execution, and results visualization.

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from pathlib import Path
import threading
import logging

from gui.controllers.main_controller import MainController
from gui.views.main_window import MainWindow
from gui.models.project_model import ProjectModel
from gui.utils.logger import setup_logger
from gui.utils.themes import ModernTheme


class PanelFlutterApp:
    """
    Main application class for the Panel Flutter Analysis GUI.
    Implements the Model-View-Controller pattern for clean separation of concerns.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_application()
        self.initialize_components()
        
    def setup_application(self):
        """Initialize the main application window and global settings."""
        self.root.title("Panel Flutter Analysis - NASTRAN Aeroelasticity Suite")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Set modern theme
        self.theme = ModernTheme()
        self.theme.apply(self.root)
        
        # Setup logging
        self.logger = setup_logger("PanelFlutterApp")
        self.logger.info("Starting Panel Flutter Analysis Application")
        
        # Application icon (if available)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except tk.TclError:
            pass  # Icon not available
            
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def initialize_components(self):
        """Initialize MVC components."""
        # Model
        self.project_model = ProjectModel()
        
        # View
        self.main_window = MainWindow(self.root)
        
        # Controller
        self.controller = MainController(self.main_window, self.project_model)
        
        # Connect components
        self.main_window.set_controller(self.controller)
        self.controller.initialize()
        
    def run(self):
        """Start the application main loop."""
        try:
            self.logger.info("Application started successfully")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Application error: {str(e)}")
            messagebox.showerror("Application Error", f"An error occurred: {str(e)}")
            
    def on_closing(self):
        """Handle application closing."""
        if self.controller.can_close():
            self.logger.info("Application closing")
            self.root.destroy()


if __name__ == "__main__":
    app = PanelFlutterApp()
    app.run()