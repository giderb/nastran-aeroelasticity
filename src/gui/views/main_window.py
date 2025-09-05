"""
Main Window View for Panel Flutter Analysis GUI
==============================================

The main window provides a tabbed interface with different sections for:
- Geometry definition
- Material properties
- Boundary conditions
- Analysis parameters
- Results visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from ...gui.views.geometry_panel import GeometryPanel
from ...gui.views.material_panel import MaterialPanel
from ...gui.views.boundary_panel import BoundaryPanel
from ...gui.views.analysis_panel import AnalysisPanel
from ...gui.views.results_panel import ResultsPanel
from ...gui.views.visualization_panel import VisualizationPanel
from ...gui.utils.widgets import ModernMenuBar, ModernStatusBar, ModernToolBar


class MainWindow:
    """
    Main application window with tabbed interface and modern styling.
    """
    
    def __init__(self, root):
        self.root = root
        self.controller = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the main user interface components."""
        self.create_menu_bar()
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()
        
    def create_menu_bar(self):
        """Create the main menu bar."""
        self.menu_bar = ModernMenuBar(self.root)
        
        # File menu
        file_menu = self.menu_bar.add_menu("File")
        file_menu.add_command(label="New Project", accelerator="Ctrl+N", command=self.new_project)
        file_menu.add_command(label="Open Project", accelerator="Ctrl+O", command=self.open_project)
        file_menu.add_command(label="Save Project", accelerator="Ctrl+S", command=self.save_project)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Import BDF", command=self.import_bdf)
        file_menu.add_command(label="Export BDF", command=self.export_bdf)
        file_menu.add_separator()
        file_menu.add_command(label="Recent Projects", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.root.quit)
        
        # Edit menu
        edit_menu = self.menu_bar.add_menu("Edit")
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", state="disabled")
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", state="disabled")
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences", command=self.show_preferences)
        
        # Analysis menu
        analysis_menu = self.menu_bar.add_menu("Analysis")
        analysis_menu.add_command(label="Run Flutter Analysis", accelerator="F5", command=self.run_analysis)
        analysis_menu.add_command(label="Parameter Study", command=self.parameter_study)
        analysis_menu.add_command(label="Validation Cases", command=self.validation_cases)
        
        # View menu
        view_menu = self.menu_bar.add_menu("View")
        view_menu.add_command(label="Zoom Fit", accelerator="Ctrl+0", command=self.zoom_fit)
        view_menu.add_command(label="Reset View", command=self.reset_view)
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Grid", variable=tk.BooleanVar(value=True))
        view_menu.add_checkbutton(label="Show Coordinate System", variable=tk.BooleanVar(value=True))
        
        # Help menu
        help_menu = self.menu_bar.add_menu("Help")
        help_menu.add_command(label="User Manual", command=self.show_manual)
        help_menu.add_command(label="Theory Guide", command=self.show_theory)
        help_menu.add_command(label="Examples", command=self.show_examples)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        
        self.root.config(menu=self.menu_bar.menu)
        
    def create_toolbar(self):
        """Create the main toolbar."""
        self.toolbar = ModernToolBar(self.root)
        
        # Project operations
        self.toolbar.add_button("New", "assets/icons/new.png", self.new_project, "New Project")
        self.toolbar.add_button("Open", "assets/icons/open.png", self.open_project, "Open Project")
        self.toolbar.add_button("Save", "assets/icons/save.png", self.save_project, "Save Project")
        self.toolbar.add_separator()
        
        # Analysis operations
        self.toolbar.add_button("Run", "assets/icons/run.png", self.run_analysis, "Run Analysis")
        self.toolbar.add_button("Stop", "assets/icons/stop.png", self.stop_analysis, "Stop Analysis")
        self.toolbar.add_separator()
        
        # View operations
        self.toolbar.add_button("Fit", "assets/icons/fit.png", self.zoom_fit, "Zoom Fit")
        self.toolbar.add_button("Reset", "assets/icons/reset.png", self.reset_view, "Reset View")
        
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
    def create_main_content(self):
        """Create the main content area with tabs."""
        # Main paned window
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel with input tabs
        self.left_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.left_frame, weight=1)
        
        # Right panel with visualization
        self.right_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.right_frame, weight=2)
        
        self.create_input_tabs()
        self.create_visualization_area()
        
    def create_input_tabs(self):
        """Create tabbed interface for input panels."""
        self.notebook = ttk.Notebook(self.left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Geometry tab
        self.geometry_panel = GeometryPanel(self.notebook)
        self.notebook.add(self.geometry_panel.frame, text="Geometry", image=None)
        
        # Material tab
        self.material_panel = MaterialPanel(self.notebook)
        self.notebook.add(self.material_panel.frame, text="Materials", image=None)
        
        # Boundary conditions tab
        self.boundary_panel = BoundaryPanel(self.notebook)
        self.notebook.add(self.boundary_panel.frame, text="Boundary", image=None)
        
        # Analysis parameters tab
        self.analysis_panel = AnalysisPanel(self.notebook)
        self.notebook.add(self.analysis_panel.frame, text="Analysis", image=None)
        
        # Results tab
        self.results_panel = ResultsPanel(self.notebook)
        self.notebook.add(self.results_panel.frame, text="Results", image=None)
        
    def create_visualization_area(self):
        """Create the 3D visualization area."""
        self.viz_frame = ttk.LabelFrame(self.right_frame, text="Visualization", padding=10)
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Visualization panel
        self.visualization_panel = VisualizationPanel(self.viz_frame)
        
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ModernStatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def set_controller(self, controller):
        """Set the controller for this view."""
        self.controller = controller
        
        # Pass controller to all panels
        self.geometry_panel.set_controller(controller)
        self.material_panel.set_controller(controller)
        self.boundary_panel.set_controller(controller)
        self.analysis_panel.set_controller(controller)
        self.results_panel.set_controller(controller)
        self.visualization_panel.set_controller(controller)
        
    def update_status(self, message):
        """Update the status bar message."""
        self.status_bar.set_status(message)
        
    def set_progress(self, value):
        """Set the progress bar value."""
        self.status_bar.set_progress(value)
        
    # Menu and toolbar callbacks
    def new_project(self):
        """Create a new project."""
        if self.controller:
            self.controller.new_project()
            
    def open_project(self):
        """Open an existing project."""
        if self.controller:
            self.controller.open_project()
            
    def save_project(self):
        """Save the current project."""
        if self.controller:
            self.controller.save_project()
            
    def save_project_as(self):
        """Save the current project with a new name."""
        if self.controller:
            self.controller.save_project_as()
            
    def import_bdf(self):
        """Import a NASTRAN BDF file."""
        if self.controller:
            self.controller.import_bdf()
            
    def export_bdf(self):
        """Export to NASTRAN BDF file."""
        if self.controller:
            self.controller.export_bdf()
            
    def run_analysis(self):
        """Run flutter analysis."""
        if self.controller:
            self.controller.run_analysis()
            
    def stop_analysis(self):
        """Stop running analysis."""
        if self.controller:
            self.controller.stop_analysis()
            
    def parameter_study(self):
        """Run parameter study."""
        if self.controller:
            self.controller.parameter_study()
            
    def validation_cases(self):
        """Run validation cases."""
        if self.controller:
            self.controller.validation_cases()
            
    def zoom_fit(self):
        """Zoom to fit all geometry."""
        self.visualization_panel.zoom_fit()
        
    def reset_view(self):
        """Reset the view to default."""
        self.visualization_panel.reset_view()
        
    def show_preferences(self):
        """Show preferences dialog."""
        messagebox.showinfo("Preferences", "Preferences dialog not yet implemented")
        
    def show_manual(self):
        """Show user manual."""
        messagebox.showinfo("User Manual", "User manual not yet implemented")
        
    def show_theory(self):
        """Show theory guide."""
        messagebox.showinfo("Theory Guide", "Theory guide not yet implemented")
        
    def show_examples(self):
        """Show examples."""
        messagebox.showinfo("Examples", "Examples not yet implemented")
        
    def show_about(self):
        """Show about dialog."""
        about_text = """
        Panel Flutter Analysis GUI
        Version 1.0.0
        
        A comprehensive tool for panel flutter analysis using NASTRAN.
        
        Features:
        • Interactive geometry definition
        • Material property specification  
        • Boundary condition setup
        • Flutter analysis execution
        • 3D results visualization
        
        Built with Python and Tkinter
        """
        messagebox.showinfo("About", about_text)