"""
Modern Themes for Panel Flutter Analysis GUI
==========================================

Provides modern styling and themes for the tkinter-based GUI.
"""

import tkinter as tk
from tkinter import ttk


class ModernTheme:
    """
    Modern theme with professional colors and styling.
    """
    
    def __init__(self):
        self.colors = {
            # Primary colors
            'primary': '#2E86AB',
            'primary_light': '#5AA5C7',
            'primary_dark': '#1F5F79',
            
            # Secondary colors
            'secondary': '#F24236',
            'secondary_light': '#F56C6C',
            'secondary_dark': '#D32F2F',
            
            # Neutral colors
            'background': '#F8F9FA',
            'surface': '#FFFFFF',
            'surface_dark': '#E9ECEF',
            
            # Text colors
            'text_primary': '#212529',
            'text_secondary': '#6C757D',
            'text_light': '#FFFFFF',
            
            # Status colors
            'success': '#28A745',
            'warning': '#FFC107',
            'error': '#DC3545',
            'info': '#17A2B8',
            
            # Border colors
            'border': '#DEE2E6',
            'border_dark': '#ADB5BD',
            
            # Focus colors
            'focus': '#80BDFF',
            'hover': '#E7F3FF'
        }
        
        self.fonts = {
            'default': ('Segoe UI', 9),
            'heading': ('Segoe UI', 12, 'bold'),
            'subheading': ('Segoe UI', 10, 'bold'),
            'small': ('Segoe UI', 8),
            'monospace': ('Consolas', 9)
        }
        
    def apply(self, root):
        """Apply the modern theme to the root window."""
        # Configure root window
        root.configure(bg=self.colors['background'])
        
        # Create custom style
        style = ttk.Style()
        
        # Set theme
        try:
            style.theme_use('clam')
        except tk.TclError:
            style.theme_use('default')
            
        # Configure styles
        self.configure_styles(style)
        
    def configure_styles(self, style):
        """Configure ttk styles."""
        # Configure frame styles
        style.configure('Modern.TFrame',
                       background=self.colors['surface'],
                       borderwidth=1,
                       relief='flat')
                       
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'])
                       
        # Configure label styles
        style.configure('Modern.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['default'])
                       
        style.configure('Heading.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['heading'])
                       
        style.configure('Subheading.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text_secondary'],
                       font=self.fonts['subheading'])
                       
        # Configure button styles
        style.configure('Modern.TButton',
                       background=self.colors['primary'],
                       foreground=self.colors['text_light'],
                       borderwidth=1,
                       focuscolor='none',
                       font=self.fonts['default'])
                       
        style.map('Modern.TButton',
                 background=[('active', self.colors['primary_light']),
                           ('pressed', self.colors['primary_dark'])])
                           
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['text_light'])
                       
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground=self.colors['text_primary'])
                       
        style.configure('Error.TButton',
                       background=self.colors['error'],
                       foreground=self.colors['text_light'])
                       
        # Configure entry styles
        style.configure('Modern.TEntry',
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       font=self.fonts['default'])
                       
        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.colors['primary'])])
                 
        # Configure combobox styles
        style.configure('Modern.TCombobox',
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'])
                       
        # Configure notebook styles
        style.configure('Modern.TNotebook',
                       background=self.colors['background'],
                       borderwidth=0)
                       
        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['surface_dark'],
                       foreground=self.colors['text_primary'],
                       padding=[12, 8],
                       font=self.fonts['default'])
                       
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['surface']),
                           ('active', self.colors['hover'])])
                           
        # Configure treeview styles
        style.configure('Modern.Treeview',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       rowheight=25,
                       font=self.fonts['default'])
                       
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['surface_dark'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['subheading'])
                       
        # Configure progressbar styles
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors['primary'],
                       troughcolor=self.colors['surface_dark'],
                       borderwidth=1,
                       lightcolor=self.colors['primary_light'],
                       darkcolor=self.colors['primary_dark'])
                       
        # Configure scale styles
        style.configure('Modern.Horizontal.TScale',
                       background=self.colors['surface'],
                       troughcolor=self.colors['surface_dark'],
                       borderwidth=1,
                       sliderthickness=20)
                       
        # Configure scrollbar styles
        style.configure('Modern.Vertical.TScrollbar',
                       background=self.colors['surface_dark'],
                       troughcolor=self.colors['surface'],
                       borderwidth=1,
                       arrowcolor=self.colors['text_secondary'])
                       
        style.configure('Modern.Horizontal.TScrollbar',
                       background=self.colors['surface_dark'],
                       troughcolor=self.colors['surface'],
                       borderwidth=1,
                       arrowcolor=self.colors['text_secondary'])


class DarkTheme(ModernTheme):
    """
    Dark theme variant for the application.
    """
    
    def __init__(self):
        super().__init__()
        
        # Override colors for dark theme
        self.colors.update({
            'background': '#1E1E1E',
            'surface': '#2D2D30',
            'surface_dark': '#3E3E42',
            
            'text_primary': '#FFFFFF',
            'text_secondary': '#CCCCCC',
            
            'border': '#3E3E42',
            'border_dark': '#555555',
            
            'hover': '#404040'
        })


class HighContrastTheme(ModernTheme):
    """
    High contrast theme for accessibility.
    """
    
    def __init__(self):
        super().__init__()
        
        # Override colors for high contrast
        self.colors.update({
            'background': '#FFFFFF',
            'surface': '#FFFFFF',
            'surface_dark': '#F0F0F0',
            
            'text_primary': '#000000',
            'text_secondary': '#333333',
            
            'primary': '#0066CC',
            'border': '#000000',
            'border_dark': '#666666',
        })