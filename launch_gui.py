"""
Panel Flutter Analysis GUI - Standalone Launcher
===============================================

Standalone launcher that handles all imports and path setup automatically.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from pathlib import Path
import threading
import time
import logging

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

print("Panel Flutter Analysis GUI")
print("=" * 50)
print(f"Working directory: {current_dir}")
print(f"Source directory: {src_dir}")
print("Checking dependencies...")

# Check dependencies
required_packages = ['numpy', 'matplotlib', 'pandas']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f"✓ {package}")
    except ImportError:
        missing_packages.append(package)
        print(f"✗ {package} (missing)")

if missing_packages:
    print(f"\nMissing packages: {', '.join(missing_packages)}")
    print("Please install with: pip install " + " ".join(missing_packages))
    input("Press Enter to exit...")
    sys.exit(1)

print("✓ All dependencies found")
print("\nStarting application...")

# Import matplotlib early and configure backend
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class PanelFlutterGUI:
    """
    Main Panel Flutter Analysis GUI Application
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_application()
        self.create_interface()
        
    def setup_application(self):
        """Setup the main application window"""
        self.root.title("Panel Flutter Analysis - NASTRAN Aeroelasticity Suite")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Configure colors
        self.colors = {
            'primary': '#2E86AB',
            'background': '#F8F9FA',
            'surface': '#FFFFFF',
            'text': '#212529'
        }
        
        self.root.configure(bg=self.colors['background'])
        
    def create_interface(self):
        """Create the main interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Panel Flutter Analysis GUI", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Create notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs
        self.create_geometry_tab()
        self.create_materials_tab()
        self.create_analysis_tab()
        self.create_results_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Panel Flutter Analysis GUI v1.0")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
    def create_geometry_tab(self):
        """Create geometry definition tab"""
        geom_frame = ttk.Frame(self.notebook)
        self.notebook.add(geom_frame, text="Geometry")
        
        # Panel dimensions
        dim_frame = ttk.LabelFrame(geom_frame, text="Panel Dimensions", padding=10)
        dim_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Length
        ttk.Label(dim_frame, text="Length (m):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.length_var = tk.StringVar(value="1.0")
        length_entry = ttk.Entry(dim_frame, textvariable=self.length_var, width=15)
        length_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Width
        ttk.Label(dim_frame, text="Width (m):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.width_var = tk.StringVar(value="1.0")
        width_entry = ttk.Entry(dim_frame, textvariable=self.width_var, width=15)
        width_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Mesh density
        mesh_frame = ttk.LabelFrame(geom_frame, text="Mesh Parameters", padding=10)
        mesh_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(mesh_frame, text="Chordwise Elements:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.nchord_var = tk.IntVar(value=10)
        nchord_spin = tk.Spinbox(mesh_frame, textvariable=self.nchord_var, 
                                from_=1, to=50, width=10)
        nchord_spin.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(mesh_frame, text="Spanwise Elements:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.nspan_var = tk.IntVar(value=5)
        nspan_spin = tk.Spinbox(mesh_frame, textvariable=self.nspan_var, 
                               from_=1, to=50, width=10)
        nspan_spin.grid(row=1, column=1, padx=5, pady=2)
        
        # Preview button
        ttk.Button(mesh_frame, text="Preview Geometry", 
                  command=self.preview_geometry).grid(row=2, column=0, columnspan=2, pady=10)
                  
    def create_materials_tab(self):
        """Create materials tab"""
        mat_frame = ttk.Frame(self.notebook)
        self.notebook.add(mat_frame, text="Materials")
        
        # Material properties
        prop_frame = ttk.LabelFrame(mat_frame, text="Material Properties", padding=10)
        prop_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Material selection
        ttk.Label(prop_frame, text="Material:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.material_var = tk.StringVar(value="Aluminum 7075-T6")
        material_combo = ttk.Combobox(prop_frame, textvariable=self.material_var,
                                    values=["Aluminum 7075-T6", "Steel AISI 4130", "Titanium Ti-6Al-4V"],
                                    state="readonly", width=20)
        material_combo.grid(row=0, column=1, padx=5, pady=2)
        material_combo.bind('<<ComboboxSelected>>', self.on_material_changed)
        
        # Properties
        ttk.Label(prop_frame, text="Density (kg/m³):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.density_var = tk.StringVar(value="2700")
        ttk.Entry(prop_frame, textvariable=self.density_var, width=15).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(prop_frame, text="Young's Modulus (Pa):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.youngs_var = tk.StringVar(value="7.0e10")
        ttk.Entry(prop_frame, textvariable=self.youngs_var, width=15).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(prop_frame, text="Poisson's Ratio:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.poisson_var = tk.StringVar(value="0.33")
        ttk.Entry(prop_frame, textvariable=self.poisson_var, width=15).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(prop_frame, text="Thickness (m):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.thickness_var = tk.StringVar(value="0.002")
        ttk.Entry(prop_frame, textvariable=self.thickness_var, width=15).grid(row=4, column=1, padx=5, pady=2)
        
    def create_analysis_tab(self):
        """Create analysis parameters tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Analysis")
        
        # Analysis parameters
        param_frame = ttk.LabelFrame(analysis_frame, text="Analysis Parameters", padding=10)
        param_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Method
        ttk.Label(param_frame, text="Method:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.method_var = tk.StringVar(value="PK")
        method_combo = ttk.Combobox(param_frame, textvariable=self.method_var,
                                  values=["PK", "K", "KE", "PKNL"], state="readonly", width=10)
        method_combo.grid(row=0, column=1, padx=5, pady=2)
        
        # Velocity range
        ttk.Label(param_frame, text="Min Velocity (m/s):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.vmin_var = tk.StringVar(value="50")
        ttk.Entry(param_frame, textvariable=self.vmin_var, width=15).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(param_frame, text="Max Velocity (m/s):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.vmax_var = tk.StringVar(value="300")
        ttk.Entry(param_frame, textvariable=self.vmax_var, width=15).grid(row=2, column=1, padx=5, pady=2)
        
        # Mach number
        ttk.Label(param_frame, text="Mach Number:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.mach_var = tk.StringVar(value="0.8")
        ttk.Entry(param_frame, textvariable=self.mach_var, width=15).grid(row=3, column=1, padx=5, pady=2)
        
        # Run analysis button
        run_frame = ttk.Frame(analysis_frame)
        run_frame.pack(pady=20)
        
        self.run_button = ttk.Button(run_frame, text="Run Flutter Analysis", 
                                   command=self.run_analysis, style='Accent.TButton')
        self.run_button.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(run_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.pack(pady=5)
        
    def create_results_tab(self):
        """Create results display tab"""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="Results")
        
        # Results summary
        summary_frame = ttk.LabelFrame(results_frame, text="Flutter Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.flutter_speed_var = tk.StringVar(value="Flutter Speed: -- m/s")
        self.flutter_freq_var = tk.StringVar(value="Flutter Frequency: -- Hz")
        
        ttk.Label(summary_frame, textvariable=self.flutter_speed_var, 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=2)
        ttk.Label(summary_frame, textvariable=self.flutter_freq_var, 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=2)
                 
        # Plot frame
        plot_frame = ttk.LabelFrame(results_frame, text="V-f and V-g Plots", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.fig.patch.set_facecolor('#F8F9FA')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initially empty plot
        self.plot_empty_results()
        
    def preview_geometry(self):
        """Preview geometry visualization"""
        try:
            length = float(self.length_var.get())
            width = float(self.width_var.get())
            nchord = self.nchord_var.get()
            nspan = self.nspan_var.get()
            
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Geometry Preview")
            preview_window.geometry("600x500")
            
            # Create matplotlib figure for preview
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111, projection='3d')
            
            # Generate mesh
            x = np.linspace(0, length, nchord + 1)
            y = np.linspace(0, width, nspan + 1)
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X)
            
            # Plot wireframe
            ax.plot_wireframe(X, Y, Z, color='blue', alpha=0.7)
            
            # Plot panel outline
            outline_x = [0, length, length, 0, 0]
            outline_y = [0, 0, width, width, 0]
            outline_z = [0, 0, 0, 0, 0]
            ax.plot(outline_x, outline_y, outline_z, 'r-', linewidth=2)
            
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_zlabel('Z (m)')
            ax.set_title(f'Panel Geometry ({nchord}×{nspan} elements)')
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, preview_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set(f"Geometry preview: {length}m × {width}m panel with {nchord}×{nspan} elements")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values")
            
    def on_material_changed(self, event=None):
        """Handle material selection change"""
        material = self.material_var.get()
        
        material_props = {
            "Aluminum 7075-T6": {"density": "2700", "youngs": "7.0e10", "poisson": "0.33"},
            "Steel AISI 4130": {"density": "7850", "youngs": "2.0e11", "poisson": "0.29"},
            "Titanium Ti-6Al-4V": {"density": "4430", "youngs": "1.14e11", "poisson": "0.32"}
        }
        
        if material in material_props:
            props = material_props[material]
            self.density_var.set(props["density"])
            self.youngs_var.set(props["youngs"])
            self.poisson_var.set(props["poisson"])
            
    def run_analysis(self):
        """Run flutter analysis simulation"""
        self.run_button.config(state='disabled')
        self.status_var.set("Running flutter analysis...")
        
        # Start analysis in separate thread
        analysis_thread = threading.Thread(target=self._run_analysis_thread)
        analysis_thread.daemon = True
        analysis_thread.start()
        
    def _run_analysis_thread(self):
        """Run analysis in background thread"""
        try:
            # Simulate analysis progress
            for i in range(11):
                progress = i * 10
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda: self.status_var.set(f"Analyzing... {progress}%"))
                time.sleep(0.5)
                
            # Generate simulated results
            vmin = float(self.vmin_var.get())
            vmax = float(self.vmax_var.get())
            velocities = np.linspace(vmin, vmax, 20)
            
            # Simulate flutter analysis results
            frequencies = 10.0 + 0.1 * velocities + 0.001 * velocities**2
            dampings = 0.1 - 0.001 * velocities + 0.0001 * velocities**1.5
            
            # Find flutter point (where damping crosses zero)
            flutter_idx = np.where(dampings <= 0)[0]
            if len(flutter_idx) > 0:
                flutter_speed = velocities[flutter_idx[0]]
                flutter_freq = frequencies[flutter_idx[0]]
            else:
                flutter_speed = None
                flutter_freq = None
                
            # Update GUI in main thread
            self.root.after(0, lambda: self._update_results(velocities, frequencies, dampings, 
                                                          flutter_speed, flutter_freq))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Analysis Error", f"Error: {str(e)}"))
            
        finally:
            self.root.after(0, lambda: self.run_button.config(state='normal'))
            self.root.after(0, lambda: self.progress_var.set(0))
            
    def _update_results(self, velocities, frequencies, dampings, flutter_speed, flutter_freq):
        """Update results display"""
        # Update summary
        if flutter_speed is not None:
            self.flutter_speed_var.set(f"Flutter Speed: {flutter_speed:.1f} m/s")
            self.flutter_freq_var.set(f"Flutter Frequency: {flutter_freq:.2f} Hz")
        else:
            self.flutter_speed_var.set("Flutter Speed: No flutter detected")
            self.flutter_freq_var.set("Flutter Frequency: --")
            
        # Update plots
        self.fig.clear()
        
        # Create subplots
        ax1 = self.fig.add_subplot(1, 2, 1)
        ax2 = self.fig.add_subplot(1, 2, 2)
        
        # V-f plot
        ax1.plot(velocities, frequencies, 'b-o', linewidth=2, markersize=4)
        ax1.set_xlabel('Velocity (m/s)')
        ax1.set_ylabel('Frequency (Hz)')
        ax1.set_title('V-f Diagram')
        ax1.grid(True, alpha=0.3)
        
        if flutter_speed is not None:
            ax1.axvline(x=flutter_speed, color='red', linestyle='--', linewidth=2)
            
        # V-g plot
        ax2.plot(velocities, dampings, 'r-s', linewidth=2, markersize=4)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_xlabel('Velocity (m/s)')
        ax2.set_ylabel('Damping')
        ax2.set_title('V-g Diagram')
        ax2.grid(True, alpha=0.3)
        
        if flutter_speed is not None:
            ax2.axvline(x=flutter_speed, color='red', linestyle='--', linewidth=2)
            
        self.fig.tight_layout()
        self.canvas.draw()
        
        self.status_var.set("Analysis completed successfully")
        
    def plot_empty_results(self):
        """Plot empty results placeholder"""
        self.fig.clear()
        ax = self.fig.add_subplot(1, 1, 1)
        ax.text(0.5, 0.5, 'No Results Available\n\nRun analysis to display V-f and V-g plots',
               transform=ax.transAxes, ha='center', va='center',
               fontsize=14, color='gray')
        ax.set_title('Flutter Analysis Results')
        self.fig.tight_layout()
        self.canvas.draw()
        
    def run(self):
        """Start the application"""
        print("GUI started successfully!")
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = PanelFlutterGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Application error: {e}")
    finally:
        print("Application closed")