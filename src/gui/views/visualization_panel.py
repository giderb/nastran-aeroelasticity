"""
Visualization Panel for Panel Flutter Analysis GUI
=================================================

Provides 3D visualization capabilities for geometry display and results visualization
using matplotlib with interactive navigation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches


class VisualizationPanel:
    """
    Panel for 3D visualization of geometry, mesh, and analysis results.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        
        # Create main frame
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_ui()
        self.setup_plot()
        
    def setup_ui(self):
        """Initialize the user interface components."""
        # Control frame
        control_frame = ttk.Frame(self.frame, style='Modern.TFrame')
        control_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # View mode selection
        ttk.Label(control_frame, text="View Mode:", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.view_mode_var = tk.StringVar(value="geometry")
        view_modes = ["geometry", "mesh", "mode_shapes", "flutter_results"]
        
        self.view_combo = ttk.Combobox(control_frame, textvariable=self.view_mode_var,
                                      values=view_modes, state="readonly", width=15,
                                      style='Modern.TCombobox')
        self.view_combo.pack(side=tk.LEFT, padx=5)
        self.view_combo.bind('<<ComboboxSelected>>', self.on_view_mode_changed)
        
        # Display options
        self.show_grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Grid", 
                       variable=self.show_grid_var,
                       command=self.update_display).pack(side=tk.LEFT, padx=5)
                       
        self.show_axes_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Axes", 
                       variable=self.show_axes_var,
                       command=self.update_display).pack(side=tk.LEFT, padx=5)
                       
        self.show_labels_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Labels", 
                       variable=self.show_labels_var,
                       command=self.update_display).pack(side=tk.LEFT, padx=5)
                       
        # View controls
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(control_frame, text="Fit", command=self.zoom_fit,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Reset", command=self.reset_view,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Top", command=self.view_top,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Side", command=self.view_side,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="3D", command=self.view_3d,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
                  
        # Results-specific controls (initially hidden)
        self.results_frame = ttk.Frame(control_frame, style='Modern.TFrame')
        
        ttk.Label(self.results_frame, text="Mode:", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="1")
        self.mode_spinbox = tk.Spinbox(self.results_frame, textvariable=self.mode_var,
                                      from_=1, to=10, width=5,
                                      command=self.on_mode_changed)
        self.mode_spinbox.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(self.results_frame, text="Scale:", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.scale_var = tk.DoubleVar(value=1.0)
        self.scale_scale = tk.Scale(self.results_frame, variable=self.scale_var,
                                   from_=0.1, to=5.0, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=100,
                                   command=self.on_scale_changed)
        self.scale_scale.pack(side=tk.LEFT, padx=2)
        
    def setup_plot(self):
        """Initialize the matplotlib plot."""
        # Create figure and axis
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.figure.patch.set_facecolor('#F8F9FA')
        
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#FFFFFF')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()
        
        # Initialize empty plot
        self.plot_empty_scene()
        
    def set_controller(self, controller):
        """Set the controller for this panel."""
        self.controller = controller
        
    def plot_empty_scene(self):
        """Plot an empty scene with coordinate system."""
        self.ax.clear()
        
        # Set labels and title
        self.ax.set_xlabel('X (mm)')
        self.ax.set_ylabel('Y (mm)')
        self.ax.set_zlabel('Z (mm)')
        self.ax.set_title('Panel Flutter Analysis - No Data')
        
        # Draw coordinate system axes
        if self.show_axes_var.get():
            self.ax.quiver(0, 0, 0, 1, 0, 0, color='red', alpha=0.8, linewidth=2, label='X')
            self.ax.quiver(0, 0, 0, 0, 1, 0, color='green', alpha=0.8, linewidth=2, label='Y')
            self.ax.quiver(0, 0, 0, 0, 0, 1, color='blue', alpha=0.8, linewidth=2, label='Z')
            
        # Grid
        if self.show_grid_var.get():
            self.ax.grid(True, alpha=0.3)
            
        # Set equal aspect ratio
        self.ax.set_box_aspect([1,1,1])
        
        self.canvas.draw()
        
    def plot_geometry(self, geometry_data):
        """Plot panel geometry."""
        self.ax.clear()
        
        try:
            # Extract geometry data
            corner_points = geometry_data.get('corner_points', [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
            dimensions = geometry_data.get('dimensions', {'length': 1.0, 'width': 1.0})
            
            # Convert to numpy arrays
            points = np.array(corner_points)
            
            # Create panel surface
            if len(points) >= 4:
                # Create surface patch
                x = points[:, 0]
                y = points[:, 1]
                z = points[:, 2]
                
                # Close the polygon
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                z = np.append(z, z[0])
                
                # Plot panel outline
                self.ax.plot(x, y, z, 'b-', linewidth=2, label='Panel Outline')
                
                # Fill the panel surface
                vertices = list(zip(x[:-1], y[:-1], z[:-1]))
                from mpl_toolkits.mplot3d.art3d import Poly3DCollection
                
                collection = Poly3DCollection([vertices], alpha=0.3, facecolor='lightblue', 
                                           edgecolor='blue', linewidth=1)
                self.ax.add_collection3d(collection)
                
                # Plot corner points
                self.ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                              c='red', s=50, label='Corner Points')
                
                # Add point labels if requested
                if self.show_labels_var.get():
                    labels = ['P1', 'P2', 'P3', 'P4']
                    for i, (point, label) in enumerate(zip(points, labels)):
                        self.ax.text(point[0], point[1], point[2], f'  {label}', 
                                   fontsize=10, color='red')
                        
            # Set labels and title
            self.ax.set_xlabel('X (mm)')
            self.ax.set_ylabel('Y (mm)')
            self.ax.set_zlabel('Z (mm)')
            self.ax.set_title('Panel Geometry')
            
            # Draw coordinate system
            if self.show_axes_var.get():
                max_dim = max(dimensions.get('length', 1), dimensions.get('width', 1))
                scale = max_dim * 0.2
                self.ax.quiver(0, 0, 0, scale, 0, 0, color='red', alpha=0.8, linewidth=2)
                self.ax.quiver(0, 0, 0, 0, scale, 0, color='green', alpha=0.8, linewidth=2)
                self.ax.quiver(0, 0, 0, 0, 0, scale, color='blue', alpha=0.8, linewidth=2)
                
            # Grid
            if self.show_grid_var.get():
                self.ax.grid(True, alpha=0.3)
                
            # Set equal aspect ratio and fit view
            self.set_equal_aspect_3d()
            self.ax.legend()
            
        except Exception as e:
            self.ax.text(0.5, 0.5, 0.5, f'Error plotting geometry: {str(e)}',
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=12, color='red')
            
        self.canvas.draw()
        
    def plot_mesh(self, geometry_data):
        """Plot panel mesh."""
        self.ax.clear()
        
        try:
            # Extract data
            corner_points = geometry_data.get('corner_points', [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
            mesh_density = geometry_data.get('mesh_density', {'n_chord': 10, 'n_span': 5})
            
            points = np.array(corner_points)
            n_chord = mesh_density['n_chord']
            n_span = mesh_density['n_span']
            
            # Generate mesh grid
            if len(points) >= 4:
                # Create parametric representation
                u = np.linspace(0, 1, n_chord + 1)
                v = np.linspace(0, 1, n_span + 1)
                U, V = np.meshgrid(u, v)
                
                # Bilinear interpolation for rectangular panel
                P1, P2, P3, P4 = points[0], points[1], points[2], points[3]
                
                X = (1-U) * (1-V) * P1[0] + U * (1-V) * P2[0] + U * V * P3[0] + (1-U) * V * P4[0]
                Y = (1-U) * (1-V) * P1[1] + U * (1-V) * P2[1] + U * V * P3[1] + (1-U) * V * P4[1]
                Z = (1-U) * (1-V) * P1[2] + U * (1-V) * P2[2] + U * V * P3[2] + (1-U) * V * P4[2]
                
                # Plot mesh lines
                # Chordwise lines
                for i in range(n_span + 1):
                    self.ax.plot(X[i, :], Y[i, :], Z[i, :], 'b-', alpha=0.6, linewidth=0.8)
                    
                # Spanwise lines
                for j in range(n_chord + 1):
                    self.ax.plot(X[:, j], Y[:, j], Z[:, j], 'b-', alpha=0.6, linewidth=0.8)
                    
                # Highlight panel outline
                outline_x = [P1[0], P2[0], P3[0], P4[0], P1[0]]
                outline_y = [P1[1], P2[1], P3[1], P4[1], P1[1]]
                outline_z = [P1[2], P2[2], P3[2], P4[2], P1[2]]
                self.ax.plot(outline_x, outline_y, outline_z, 'r-', linewidth=2, label='Panel Outline')
                
                # Plot corner points
                self.ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                              c='red', s=50, label='Corner Points')
                              
            # Set labels and title
            self.ax.set_xlabel('X (mm)')
            self.ax.set_ylabel('Y (mm)')
            self.ax.set_zlabel('Z (mm)')
            self.ax.set_title(f'Panel Mesh ({n_chord}×{n_span} elements)')
            
            # Grid and axes
            if self.show_grid_var.get():
                self.ax.grid(True, alpha=0.3)
                
            self.set_equal_aspect_3d()
            self.ax.legend()
            
        except Exception as e:
            self.ax.text(0.5, 0.5, 0.5, f'Error plotting mesh: {str(e)}',
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=12, color='red')
                        
        self.canvas.draw()
        
    def plot_mode_shapes(self, results_data):
        """Plot mode shapes."""
        self.ax.clear()
        
        try:
            mode_number = int(self.mode_var.get())
            scale_factor = self.scale_var.get()
            
            # Simulate mode shape data (in real implementation, extract from results)
            # Create a simple mode shape visualization
            x = np.linspace(0, 1, 21)
            y = np.linspace(0, 1, 11)
            X, Y = np.meshgrid(x, y)
            
            # Simple mode shape (first bending mode)
            if mode_number == 1:
                Z = scale_factor * 0.1 * np.sin(np.pi * X) * np.sin(np.pi * Y)
                mode_name = "First Bending Mode"
            elif mode_number == 2:
                Z = scale_factor * 0.1 * np.sin(2 * np.pi * X) * np.sin(np.pi * Y)
                mode_name = "Second Bending Mode"
            else:
                Z = scale_factor * 0.1 * np.sin(mode_number * np.pi * X) * np.sin(np.pi * Y)
                mode_name = f"Mode {mode_number}"
                
            # Plot surface
            surf = self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, 
                                      linewidth=0.5, antialiased=True)
            
            # Add color bar
            self.figure.colorbar(surf, ax=self.ax, shrink=0.5, aspect=5)
            
            # Plot original geometry outline
            outline_x = [0, 1, 1, 0, 0]
            outline_y = [0, 0, 1, 1, 0]
            outline_z = [0, 0, 0, 0, 0]
            self.ax.plot(outline_x, outline_y, outline_z, 'r-', linewidth=2, 
                        label='Undeformed Shape')
            
            # Set labels and title
            self.ax.set_xlabel('X (mm)')
            self.ax.set_ylabel('Y (mm)')
            self.ax.set_zlabel('Displacement (mm)')
            self.ax.set_title(f'{mode_name} (Scale: {scale_factor:.1f})')
            
            if self.show_grid_var.get():
                self.ax.grid(True, alpha=0.3)
                
            self.ax.legend()
            
        except Exception as e:
            self.ax.text(0.5, 0.5, 0.5, f'Error plotting mode shapes: {str(e)}',
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=12, color='red')
                        
        self.canvas.draw()
        
    def plot_flutter_results(self, results_data):
        """Plot flutter analysis results."""
        self.ax.clear()
        
        # Switch to 2D plot for flutter results
        self.ax.remove()
        self.ax = self.figure.add_subplot(111)
        
        try:
            # Extract flutter results
            flutter_summary = results_data.get('flutter_summary', {})
            velocities = flutter_summary.get('velocities', [])
            frequencies = flutter_summary.get('frequencies', [])
            dampings = flutter_summary.get('dampings', [])
            
            if velocities and frequencies and dampings:
                # Create V-f and V-g plots
                ax1 = self.ax
                ax2 = ax1.twinx()
                
                # Plot V-f curve
                line1 = ax1.plot(velocities, frequencies, 'b-o', linewidth=2, 
                                markersize=4, label='Frequency')
                ax1.set_xlabel('Velocity (m/s)')
                ax1.set_ylabel('Frequency (Hz)', color='b')
                ax1.tick_params(axis='y', labelcolor='b')
                
                # Plot V-g curve
                line2 = ax2.plot(velocities, dampings, 'r-s', linewidth=2, 
                                markersize=4, label='Damping')
                ax2.set_ylabel('Damping', color='r')
                ax2.tick_params(axis='y', labelcolor='r')
                
                # Mark flutter point if available
                flutter_speed = flutter_summary.get('flutter_speed')
                if flutter_speed:
                    ax1.axvline(x=flutter_speed, color='green', linestyle='--', 
                              linewidth=2, label=f'Flutter Speed: {flutter_speed:.1f} m/s')
                    
                # Zero damping line
                ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                
                # Set title
                self.ax.set_title('Flutter Analysis Results')
                
                # Grid
                if self.show_grid_var.get():
                    ax1.grid(True, alpha=0.3)
                    
                # Legend
                lines1, labels1 = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
                
            else:
                self.ax.text(0.5, 0.5, 'No flutter results available', 
                           transform=self.ax.transAxes, ha='center', va='center',
                           fontsize=14, color='gray')
                           
        except Exception as e:
            self.ax.text(0.5, 0.5, f'Error plotting flutter results: {str(e)}',
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=12, color='red')
                        
        self.canvas.draw()
        
    def on_view_mode_changed(self, event=None):
        """Handle view mode change."""
        view_mode = self.view_mode_var.get()
        
        if view_mode in ["mode_shapes", "flutter_results"]:
            self.results_frame.pack(side=tk.LEFT, padx=10)
        else:
            self.results_frame.pack_forget()
            
        # Request data update from controller
        if self.controller:
            self.controller.update_visualization(view_mode)
            
    def on_mode_changed(self):
        """Handle mode number change."""
        if self.view_mode_var.get() == "mode_shapes" and self.controller:
            self.controller.update_visualization("mode_shapes")
            
    def on_scale_changed(self, value):
        """Handle scale factor change."""
        if self.view_mode_var.get() == "mode_shapes" and self.controller:
            self.controller.update_visualization("mode_shapes")
            
    def update_display(self):
        """Update display options."""
        # Redraw current view
        if self.controller:
            view_mode = self.view_mode_var.get()
            self.controller.update_visualization(view_mode)
        else:
            self.plot_empty_scene()
            
    def zoom_fit(self):
        """Zoom to fit all geometry."""
        if hasattr(self.ax, 'set_xlim3d'):  # 3D plot
            self.set_equal_aspect_3d()
        else:  # 2D plot
            self.ax.relim()
            self.ax.autoscale()
        self.canvas.draw()
        
    def reset_view(self):
        """Reset view to default."""
        if hasattr(self.ax, 'view_init'):
            self.ax.view_init(elev=20, azim=45)
        self.zoom_fit()
        
    def view_top(self):
        """Set top view."""
        if hasattr(self.ax, 'view_init'):
            self.ax.view_init(elev=90, azim=0)
            self.canvas.draw()
            
    def view_side(self):
        """Set side view."""
        if hasattr(self.ax, 'view_init'):
            self.ax.view_init(elev=0, azim=0)
            self.canvas.draw()
            
    def view_3d(self):
        """Set 3D view."""
        if hasattr(self.ax, 'view_init'):
            self.ax.view_init(elev=20, azim=45)
            self.canvas.draw()
            
    def set_equal_aspect_3d(self):
        """Set equal aspect ratio for 3D plot."""
        if hasattr(self.ax, 'set_box_aspect'):
            # Get current axis limits
            try:
                x_limits = self.ax.get_xlim3d()
                y_limits = self.ax.get_ylim3d()
                z_limits = self.ax.get_zlim3d()
                
                # Calculate ranges
                x_range = x_limits[1] - x_limits[0]
                y_range = y_limits[1] - y_limits[0]
                z_range = z_limits[1] - z_limits[0]
                
                # Set equal aspect ratio
                max_range = max(x_range, y_range, z_range)
                if max_range > 0:
                    self.ax.set_box_aspect([x_range/max_range, y_range/max_range, z_range/max_range])
                else:
                    self.ax.set_box_aspect([1, 1, 1])
                    
            except Exception:
                self.ax.set_box_aspect([1, 1, 1])
                
    def clear_plot(self):
        """Clear the current plot."""
        self.plot_empty_scene()