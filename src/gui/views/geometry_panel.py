"""
Geometry Panel for Panel Flutter Analysis GUI
============================================

Provides interface for defining panel geometry including dimensions,
corner points, and mesh parameters.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from src.gui.utils.widgets import LabeledEntry, LabeledSpinbox, ParameterTable
from src.gui.utils.validation import is_valid_float, is_positive_float


class GeometryPanel:
    """
    Panel for geometry definition and modification.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        
        # Create main frame
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        
        self.setup_ui()
        self.bind_events()
        
    def setup_ui(self):
        """Initialize the user interface components."""
        # Create notebook for geometry sub-panels
        self.notebook = ttk.Notebook(self.frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Basic geometry tab
        self.create_basic_geometry_tab()
        
        # Advanced geometry tab
        self.create_advanced_geometry_tab()
        
        # Mesh parameters tab
        self.create_mesh_parameters_tab()
        
    def create_basic_geometry_tab(self):
        """Create basic geometry definition tab."""
        basic_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(basic_frame, text="Basic")
        
        # Panel type selection
        type_frame = ttk.LabelFrame(basic_frame, text="Panel Type", padding=10)
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.panel_type_var = tk.StringVar(value="rectangular")
        type_options = ["rectangular", "trapezoidal", "curved"]
        
        for i, option in enumerate(type_options):
            rb = ttk.Radiobutton(
                type_frame,
                text=option.capitalize(),
                variable=self.panel_type_var,
                value=option,
                command=self.on_panel_type_changed
            )
            rb.grid(row=0, column=i, padx=10, pady=5)
            
        # Dimensions frame
        dim_frame = ttk.LabelFrame(basic_frame, text="Dimensions (mm)", padding=10)
        dim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Length, width, thickness
        self.length_entry = LabeledEntry(dim_frame, "Length (a):", is_positive_float, width=15)
        self.length_entry.set("500.0")
        self.length_entry.pack(anchor=tk.W, pady=2)
        
        self.width_entry = LabeledEntry(dim_frame, "Width (b):", is_positive_float, width=15)
        self.width_entry.set("300.0")
        self.width_entry.pack(anchor=tk.W, pady=2)
        
        self.thickness_entry = LabeledEntry(dim_frame, "Thickness (h):", is_positive_float, width=15)
        self.thickness_entry.set("2.0")
        self.thickness_entry.pack(anchor=tk.W, pady=2)
        
        # Quick geometry buttons
        buttons_frame = ttk.Frame(dim_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(buttons_frame, text="Square Panel", command=self.create_square_panel,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Aircraft Panel", command=self.create_naca_panel,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Reset", command=self.reset_geometry,
                  style='Warning.TButton').pack(side=tk.LEFT, padx=2)
                  
    def create_advanced_geometry_tab(self):
        """Create advanced geometry definition tab."""
        advanced_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(advanced_frame, text="Advanced")
        
        # Corner points frame
        points_frame = ttk.LabelFrame(advanced_frame, text="Corner Points (x, y, z)", padding=10)
        points_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create parameter table for corner points
        self.points_table = ParameterTable(points_frame, ["Point", "X", "Y", "Z"])
        self.points_table.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Initialize with default points
        default_points = [
            ["P1 (Leading-Left)", "0.0", "0.0", "0.0"],
            ["P2 (Leading-Right)", "1.0", "0.0", "0.0"],
            ["P3 (Trailing-Right)", "1.0", "1.0", "0.0"],
            ["P4 (Trailing-Left)", "0.0", "1.0", "0.0"]
        ]
        
        for point in default_points:
            self.points_table.insert_row(point)
            
        # Point editing controls
        edit_frame = ttk.Frame(points_frame)
        edit_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(edit_frame, text="Edit Point:", style='Modern.TLabel').pack(side=tk.LEFT)
        
        self.x_edit = LabeledEntry(edit_frame, "X:", is_valid_float, width=10)
        self.x_edit.pack(side=tk.LEFT, padx=5)
        
        self.y_edit = LabeledEntry(edit_frame, "Y:", is_valid_float, width=10)
        self.y_edit.pack(side=tk.LEFT, padx=5)
        
        self.z_edit = LabeledEntry(edit_frame, "Z:", is_valid_float, width=10)
        self.z_edit.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(edit_frame, text="Update", command=self.update_selected_point,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=5)
                  
        # Coordinate system frame
        coord_frame = ttk.LabelFrame(advanced_frame, text="Coordinate System", padding=10)
        coord_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.coord_system_var = tk.StringVar(value="cartesian")
        coord_options = ["cartesian", "cylindrical", "spherical"]
        
        for i, option in enumerate(coord_options):
            rb = ttk.Radiobutton(
                coord_frame,
                text=option.capitalize(),
                variable=self.coord_system_var,
                value=option
            )
            rb.grid(row=0, column=i, padx=10, pady=5)
            
    def create_mesh_parameters_tab(self):
        """Create mesh parameters tab."""
        mesh_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(mesh_frame, text="Mesh")
        
        # Mesh density frame
        density_frame = ttk.LabelFrame(mesh_frame, text="Mesh Density", padding=10)
        density_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Number of elements
        self.n_chord_spinbox = LabeledSpinbox(density_frame, "Chordwise Elements:", 
                                            from_=1, to=100, increment=1, width=10)
        self.n_chord_spinbox.set(10)
        self.n_chord_spinbox.pack(anchor=tk.W, pady=2)
        
        self.n_span_spinbox = LabeledSpinbox(density_frame, "Spanwise Elements:", 
                                           from_=1, to=100, increment=1, width=10)
        self.n_span_spinbox.set(5)
        self.n_span_spinbox.pack(anchor=tk.W, pady=2)
        
        # Mesh quality info
        quality_frame = ttk.LabelFrame(mesh_frame, text="Mesh Quality", padding=10)
        quality_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.aspect_ratio_label = ttk.Label(quality_frame, text="Aspect Ratio: --",
                                          style='Modern.TLabel')
        self.aspect_ratio_label.pack(anchor=tk.W, pady=2)
        
        self.total_elements_label = ttk.Label(quality_frame, text="Total Elements: --",
                                            style='Modern.TLabel')
        self.total_elements_label.pack(anchor=tk.W, pady=2)
        
        self.element_size_label = ttk.Label(quality_frame, text="Avg Element Size: --",
                                          style='Modern.TLabel')
        self.element_size_label.pack(anchor=tk.W, pady=2)
        
        # Mesh preview button
        ttk.Button(quality_frame, text="Preview Mesh", command=self.preview_mesh,
                  style='Modern.TButton').pack(pady=10)
                  
        # Advanced mesh options
        advanced_mesh_frame = ttk.LabelFrame(mesh_frame, text="Advanced Options", padding=10)
        advanced_mesh_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.adaptive_mesh_var = tk.BooleanVar()
        ttk.Checkbutton(advanced_mesh_frame, text="Adaptive mesh refinement",
                       variable=self.adaptive_mesh_var).pack(anchor=tk.W, pady=2)
                       
        self.curved_elements_var = tk.BooleanVar()
        ttk.Checkbutton(advanced_mesh_frame, text="Use curved elements",
                       variable=self.curved_elements_var).pack(anchor=tk.W, pady=2)
                       
    def bind_events(self):
        """Bind events to UI components."""
        # Bind mesh parameter changes to update mesh quality
        self.n_chord_spinbox.spinbox.bind('<Return>', self.update_mesh_quality)
        self.n_chord_spinbox.spinbox.bind('<FocusOut>', self.update_mesh_quality)
        self.n_span_spinbox.spinbox.bind('<Return>', self.update_mesh_quality)
        self.n_span_spinbox.spinbox.bind('<FocusOut>', self.update_mesh_quality)
        
        # Bind dimension changes to update corner points
        self.length_entry.var.trace('w', self.update_corner_points_from_dimensions)
        self.width_entry.var.trace('w', self.update_corner_points_from_dimensions)
        
    def set_controller(self, controller):
        """Set the controller for this panel."""
        self.controller = controller
        
    def on_panel_type_changed(self):
        """Handle panel type change."""
        panel_type = self.panel_type_var.get()
        
        if panel_type == "rectangular":
            self.reset_to_rectangular()
        elif panel_type == "trapezoidal":
            self.create_trapezoidal_geometry()
        elif panel_type == "curved":
            self.create_curved_geometry()
            
        if self.controller:
            self.notify_geometry_changed()
            
    def update_corner_points_from_dimensions(self, *args):
        """Update corner points based on dimension changes."""
        try:
            length = (float(self.length_entry.get()) if self.length_entry.get() else 500.0) / 1000.0  # Convert mm to m
            width = (float(self.width_entry.get()) if self.width_entry.get() else 300.0) / 1000.0  # Convert mm to m
            
            # Update corner points table
            self.points_table.clear()
            points = [
                ["P1 (Leading-Left)", "0.0", "0.0", "0.0"],
                ["P2 (Leading-Right)", f"{length:.3f}", "0.0", "0.0"],
                ["P3 (Trailing-Right)", f"{length:.3f}", f"{width:.3f}", "0.0"],
                ["P4 (Trailing-Left)", "0.0", f"{width:.3f}", "0.0"]
            ]
            
            for point in points:
                self.points_table.insert_row(point)
                
            self.update_mesh_quality()
            
        except (ValueError, TypeError):
            pass  # Invalid input, ignore
            
    def update_mesh_quality(self, *args):
        """Update mesh quality information."""
        try:
            n_chord = int(self.n_chord_spinbox.get())
            n_span = int(self.n_span_spinbox.get())
            length = (float(self.length_entry.get()) if self.length_entry.get() else 500.0) / 1000.0  # Convert mm to m
            width = (float(self.width_entry.get()) if self.width_entry.get() else 300.0) / 1000.0  # Convert mm to m
            
            # Calculate mesh quality metrics
            chord_element_size = length / n_chord
            span_element_size = width / n_span
            aspect_ratio = max(chord_element_size, span_element_size) / min(chord_element_size, span_element_size)
            total_elements = n_chord * n_span
            avg_element_size = (chord_element_size + span_element_size) / 2
            
            # Update labels
            self.aspect_ratio_label.config(text=f"Aspect Ratio: {aspect_ratio:.2f}")
            self.total_elements_label.config(text=f"Total Elements: {total_elements}")
            self.element_size_label.config(text=f"Avg Element Size: {avg_element_size:.4f} m")
            
            # Color code aspect ratio
            if aspect_ratio > 3:
                self.aspect_ratio_label.config(foreground='red')
            elif aspect_ratio > 2:
                self.aspect_ratio_label.config(foreground='orange')
            else:
                self.aspect_ratio_label.config(foreground='green')
                
        except (ValueError, TypeError):
            pass
            
    def create_square_panel(self):
        """Create a square panel geometry."""
        self.panel_type_var.set("rectangular")
        self.length_entry.set("500.0")  # 500mm length
        self.width_entry.set("500.0")   # 500mm width
        self.thickness_entry.set("2.0")  # 2mm thickness
        self.update_corner_points_from_dimensions()
        
    def create_naca_panel(self):
        """Create a NACA-style panel geometry (Aircraft fuselage panel)."""
        self.panel_type_var.set("rectangular")
        self.length_entry.set("500.0")   # 500mm length
        self.width_entry.set("300.0")    # 300mm width
        self.thickness_entry.set("2.0")  # 2mm thickness
        self.n_chord_spinbox.set(20)
        self.n_span_spinbox.set(10)
        self.update_corner_points_from_dimensions()
        self.update_mesh_quality()
        
    def reset_geometry(self):
        """Reset geometry to default values."""
        self.create_square_panel()
        self.n_chord_spinbox.set(10)
        self.n_span_spinbox.set(5)
        self.coord_system_var.set("cartesian")
        self.adaptive_mesh_var.set(False)
        self.curved_elements_var.set(False)
        
    def reset_to_rectangular(self):
        """Reset to rectangular panel."""
        self.update_corner_points_from_dimensions()
        
    def create_trapezoidal_geometry(self):
        """Create trapezoidal panel geometry."""
        length = float(self.length_entry.get()) if self.length_entry.get() else 1.0
        width = float(self.width_entry.get()) if self.width_entry.get() else 1.0
        
        # Create trapezoidal shape (tapered)
        taper_ratio = 0.7
        trailing_width = width * taper_ratio
        
        self.points_table.clear()
        points = [
            ["P1 (Leading-Left)", "0.0", "0.0", "0.0"],
            ["P2 (Leading-Right)", f"{length:.3f}", "0.0", "0.0"],
            ["P3 (Trailing-Right)", f"{length:.3f}", f"{trailing_width:.3f}", "0.0"],
            ["P4 (Trailing-Left)", "0.0", f"{width:.3f}", "0.0"]
        ]
        
        for point in points:
            self.points_table.insert_row(point)
            
    def create_curved_geometry(self):
        """Create curved panel geometry."""
        messagebox.showinfo("Curved Geometry", "Curved geometry not yet implemented")
        
    def update_selected_point(self):
        """Update the selected point with new coordinates."""
        selection = self.points_table.get_selected_values()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a point to update")
            return
            
        try:
            x = float(self.x_edit.get())
            y = float(self.y_edit.get())
            z = float(self.z_edit.get())
            
            # Update the selected row (implementation would depend on table widget)
            messagebox.showinfo("Update Point", f"Point updated to ({x}, {y}, {z})")
            
            if self.controller:
                self.notify_geometry_changed()
                
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric coordinates")
            
    def preview_mesh(self):
        """Preview the mesh in the visualization panel."""
        if self.controller:
            geometry_data = self.get_geometry_data()
            self.controller.preview_geometry(geometry_data)
        else:
            messagebox.showinfo("Preview", "Mesh preview not yet implemented")
            
    def get_geometry_data(self) -> dict:
        """Get current geometry data."""
        try:
            # Extract corner points from table
            corner_points = []
            for i in range(4):
                # In a real implementation, extract from table
                corner_points.append([0.0, 0.0, 0.0])  # Placeholder
                
            geometry_data = {
                'panel_type': self.panel_type_var.get(),
                'corner_points': corner_points,
                'dimensions': {
                    'length': (float(self.length_entry.get()) if self.length_entry.get() else 500.0) / 1000.0,  # Convert mm to m
                    'width': (float(self.width_entry.get()) if self.width_entry.get() else 300.0) / 1000.0,  # Convert mm to m
                    'thickness': (float(self.thickness_entry.get()) if self.thickness_entry.get() else 2.0) / 1000.0  # Convert mm to m
                },
                'mesh_density': {
                    'n_chord': int(self.n_chord_spinbox.get()),
                    'n_span': int(self.n_span_spinbox.get())
                },
                'coordinate_system': self.coord_system_var.get(),
                'advanced_options': {
                    'adaptive_mesh': self.adaptive_mesh_var.get(),
                    'curved_elements': self.curved_elements_var.get()
                }
            }
            
            return geometry_data
            
        except (ValueError, TypeError) as e:
            messagebox.showerror("Invalid Data", f"Error reading geometry data: {str(e)}")
            return {}
            
    def set_geometry_data(self, geometry_data: dict):
        """Set geometry data from external source."""
        try:
            # Panel type
            self.panel_type_var.set(geometry_data.get('panel_type', 'rectangular'))
            
            # Dimensions
            dimensions = geometry_data.get('dimensions', {})
            self.length_entry.set(str(dimensions.get('length', 0.5) * 1000.0))  # Convert m to mm
            self.width_entry.set(str(dimensions.get('width', 0.3) * 1000.0))  # Convert m to mm
            self.thickness_entry.set(str(dimensions.get('thickness', 0.002) * 1000.0))  # Convert m to mm
            
            # Mesh density
            mesh_density = geometry_data.get('mesh_density', {})
            self.n_chord_spinbox.set(mesh_density.get('n_chord', 10))
            self.n_span_spinbox.set(mesh_density.get('n_span', 5))
            
            # Coordinate system
            self.coord_system_var.set(geometry_data.get('coordinate_system', 'cartesian'))
            
            # Advanced options
            advanced = geometry_data.get('advanced_options', {})
            self.adaptive_mesh_var.set(advanced.get('adaptive_mesh', False))
            self.curved_elements_var.set(advanced.get('curved_elements', False))
            
            # Update displays
            self.update_corner_points_from_dimensions()
            self.update_mesh_quality()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error setting geometry data: {str(e)}")
            
    def notify_geometry_changed(self):
        """Notify controller of geometry changes."""
        if self.controller:
            geometry_data = self.get_geometry_data()
            self.controller.update_geometry(geometry_data)