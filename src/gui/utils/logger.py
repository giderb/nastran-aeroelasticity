"""
Logging Configuration for Panel Flutter Analysis GUI
===================================================

Provides centralized logging configuration for the application.
"""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logger(name, log_level=logging.INFO):
    """
    Set up a logger with file and console handlers.
    
    Args:
        name: Name of the logger
        log_level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    log_filename = os.path.join(logs_dir, f"panel_flutter_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


class GUILogHandler(logging.Handler):
    """
    Custom log handler for displaying logs in GUI.
    """
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        
    def emit(self, record):
        """Emit a log record to the text widget."""
        try:
            msg = self.format(record)
            
            # Insert message in GUI thread
            self.text_widget.after(0, self._insert_message, msg)
            
        except Exception:
            self.handleError(record)
            
    def _insert_message(self, message):
        """Insert message into text widget."""
        import tkinter as tk
        self.text_widget.insert(tk.END, message + "\n")
        self.text_widget.see(tk.END)


def configure_analysis_logging():
    """Configure logging specifically for analysis operations."""
    analysis_logger = logging.getLogger("analysis")
    analysis_logger.setLevel(logging.DEBUG)
    
    # Create analysis-specific log file
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    log_filename = os.path.join(logs_dir, "analysis.log")
    handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    analysis_logger.addHandler(handler)
    return analysis_logger