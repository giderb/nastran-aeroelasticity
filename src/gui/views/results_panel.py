"""
Results Panel for Panel Flutter Analysis GUI
===========================================

Provides interface for displaying and analyzing flutter analysis results
including summary data, plots, and export capabilities.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from ...gui.utils.widgets import ParameterTable


class ResultsPanel:
    """
    Panel for displaying and analyzing flutter analysis results.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        self.results_data = None
        
        # Create main frame
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the user interface components."""
        # Create notebook for results sub-panels
        self.notebook = ttk.Notebook(self.frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Summary tab
        self.create_summary_tab()
        
        # Detailed results tab
        self.create_detailed_tab()
        
        # Plots tab
        self.create_plots_tab()
        
        # Export tab
        self.create_export_tab()
        
    def create_summary_tab(self):
        """Create results summary tab."""
        summary_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(summary_frame, text="Summary")
        
        # Flutter summary frame
        flutter_frame = ttk.LabelFrame(summary_frame, text="Flutter Summary", padding=10)
        flutter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Flutter speed
        self.flutter_speed_label = ttk.Label(flutter_frame, text="Flutter Speed: -- m/s",
                                           style='Heading.TLabel')
        self.flutter_speed_label.pack(anchor=tk.W, pady=2)
        
        # Flutter frequency
        self.flutter_freq_label = ttk.Label(flutter_frame, text="Flutter Frequency: -- Hz",
                                          style='Heading.TLabel')
        self.flutter_freq_label.pack(anchor=tk.W, pady=2)
        
        # Flutter mode
        self.flutter_mode_label = ttk.Label(flutter_frame, text="Flutter Mode: --",
                                          style='Modern.TLabel')
        self.flutter_mode_label.pack(anchor=tk.W, pady=2)
        
        # Critical Mach number
        self.critical_mach_label = ttk.Label(flutter_frame, text="Critical Mach: --",
                                           style='Modern.TLabel')
        self.critical_mach_label.pack(anchor=tk.W, pady=2)
        
        # Analysis status frame
        status_frame = ttk.LabelFrame(summary_frame, text="Analysis Status", padding=10)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.analysis_status_label = ttk.Label(status_frame, text="Status: No analysis run",
                                             style='Modern.TLabel')
        self.analysis_status_label.pack(anchor=tk.W, pady=2)
        
        self.convergence_label = ttk.Label(status_frame, text="Convergence: --",
                                         style='Modern.TLabel')
        self.convergence_label.pack(anchor=tk.W, pady=2)
        
        self.iterations_label = ttk.Label(status_frame, text="Iterations: --",
                                        style='Modern.TLabel')
        self.iterations_label.pack(anchor=tk.W, pady=2)
        
        self.runtime_label = ttk.Label(status_frame, text="Runtime: --",
                                     style='Modern.TLabel')
        self.runtime_label.pack(anchor=tk.W, pady=2)
        
        # Mode summary table
        modes_frame = ttk.LabelFrame(summary_frame, text="Mode Summary", padding=10)
        modes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.modes_table = ParameterTable(modes_frame, 
                                        ["Mode", "Frequency (Hz)", "Description", "Critical"])
        self.modes_table.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def create_detailed_tab(self):
        """Create detailed results tab."""
        detailed_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(detailed_frame, text="Detailed")
        
        # Results table
        table_frame = ttk.LabelFrame(detailed_frame, text="Detailed Results", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.detailed_table = ParameterTable(table_frame, 
                                           ["Velocity", "Frequency", "Damping", "Mode", "Mach"])
        self.detailed_table.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(table_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Sort by Velocity", command=self.sort_by_velocity,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Sort by Frequency", command=self.sort_by_frequency,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Filter Critical", command=self.filter_critical,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
                  
    def create_plots_tab(self):
        """Create plots tab."""
        plots_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(plots_frame, text="Plots")
        
        # Plot controls
        control_frame = ttk.Frame(plots_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Plot Type:", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.plot_type_var = tk.StringVar(value="vf")
        plot_types = [("V-f Plot", "vf"), ("V-g Plot", "vg"), ("Root Locus", "root_locus"), 
                     ("Mode Shapes", "modes")]
        
        plot_combo = ttk.Combobox(control_frame, textvariable=self.plot_type_var,
                                values=[pt[1] for pt in plot_types], 
                                state="readonly", width=15)
        plot_combo.pack(side=tk.LEFT, padx=5)
        plot_combo.bind('<<ComboboxSelected>>', self.on_plot_type_changed)
        
        ttk.Button(control_frame, text="Update Plot", command=self.update_plot,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Save Plot", command=self.save_plot,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
                  
        # Plot area
        self.plot_frame = ttk.Frame(plots_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize empty plot
        self.setup_plot()
        
    def create_export_tab(self):
        """Create export tab."""
        export_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(export_frame, text="Export")
        
        # Export options frame
        options_frame = ttk.LabelFrame(export_frame, text="Export Options", padding=10)
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Data format selection
        self.export_format_var = tk.StringVar(value="csv")
        formats = [("CSV", "csv"), ("Excel", "xlsx"), ("JSON", "json"), ("MATLAB", "mat")]
        
        ttk.Label(options_frame, text="Format:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, pady=2)
        
        for i, (name, value) in enumerate(formats):
            rb = ttk.Radiobutton(options_frame, text=name, variable=self.export_format_var, value=value)
            rb.grid(row=0, column=i+1, padx=10, pady=2)
            
        # Data selection
        data_frame = ttk.LabelFrame(export_frame, text="Data Selection", padding=10)
        data_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.export_summary_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(data_frame, text="Flutter summary", 
                       variable=self.export_summary_var).pack(anchor=tk.W, pady=2)
                       
        self.export_detailed_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(data_frame, text="Detailed results", 
                       variable=self.export_detailed_var).pack(anchor=tk.W, pady=2)
                       
        self.export_modes_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(data_frame, text="Mode shapes", 
                       variable=self.export_modes_var).pack(anchor=tk.W, pady=2)
                       
        self.export_plots_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(data_frame, text="Plots", 
                       variable=self.export_plots_var).pack(anchor=tk.W, pady=2)
                       
        # Export buttons
        button_frame = ttk.Frame(export_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Export Results", command=self.export_results,
                  style='Success.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Export Report", command=self.export_report,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=10)
                  
    def setup_plot(self):
        """Initialize matplotlib plot."""
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.figure.patch.set_facecolor('#F8F9FA')
        
        self.plot_ax = self.figure.add_subplot(111)
        self.plot_ax.set_facecolor('#FFFFFF')
        
        self.plot_canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial empty plot
        self.plot_empty()
        
    def plot_empty(self):
        """Plot empty placeholder."""
        self.plot_ax.clear()
        self.plot_ax.text(0.5, 0.5, 'No Results Available', 
                         transform=self.plot_ax.transAxes, ha='center', va='center',
                         fontsize=16, color='gray')
        self.plot_ax.set_title('Flutter Analysis Results')
        self.plot_canvas.draw()
        
    def set_controller(self, controller):
        """Set the controller for this panel."""
        self.controller = controller
        
    def update_results(self, results_data):
        """Update results display with new data."""
        self.results_data = results_data
        
        try:
            # Update summary
            flutter_summary = results_data.get('flutter_summary', {})
            
            # Flutter speed and frequency
            flutter_speed = flutter_summary.get('flutter_speed', 0)
            flutter_freq = flutter_summary.get('flutter_frequency', 0)
            
            if flutter_speed > 0:
                self.flutter_speed_label.config(text=f"Flutter Speed: {flutter_speed:.1f} m/s",
                                               foreground='red')
                self.flutter_freq_label.config(text=f"Flutter Frequency: {flutter_freq:.2f} Hz")
            else:
                self.flutter_speed_label.config(text="Flutter Speed: No flutter detected",
                                               foreground='green')
                self.flutter_freq_label.config(text="Flutter Frequency: --")
                
            # Update analysis status
            self.analysis_status_label.config(text="Status: Analysis completed")
            
            # Update mode summary
            modes = results_data.get('modes', [])
            self.modes_table.clear()
            for mode in modes:
                mode_num = mode.get('mode_number', '--')
                frequency = mode.get('frequency', '--')
                description = mode.get('description', '--')
                critical = "Yes" if mode.get('critical', False) else "No"
                
                self.modes_table.insert_row([str(mode_num), f"{frequency:.2f}" if isinstance(frequency, (int, float)) else str(frequency), 
                                           description, critical])
                
            # Update detailed results
            self.update_detailed_results(flutter_summary)
            
            # Update plot
            self.update_plot()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating results: {str(e)}")
            
    def update_detailed_results(self, flutter_summary):
        """Update detailed results table."""
        try:
            self.detailed_table.clear()
            
            velocities = flutter_summary.get('velocities', [])
            frequencies = flutter_summary.get('frequencies', [])
            dampings = flutter_summary.get('dampings', [])
            
            for i, (v, f, d) in enumerate(zip(velocities, frequencies, dampings)):
                mode = "1"  # Simplified - in real implementation, track mode numbers
                mach = v / 343.0  # Approximate Mach number
                
                self.detailed_table.insert_row([f"{v:.1f}", f"{f:.2f}", f"{d:.4f}", mode, f"{mach:.3f}"])
                
        except Exception as e:
            print(f"Error updating detailed results: {str(e)}")
            
    def on_plot_type_changed(self, event=None):
        """Handle plot type change."""
        self.update_plot()
        
    def update_plot(self):
        """Update the current plot."""
        if not self.results_data:
            self.plot_empty()
            return
            
        plot_type = self.plot_type_var.get()
        
        try:
            self.plot_ax.clear()
            
            flutter_summary = self.results_data.get('flutter_summary', {})
            velocities = flutter_summary.get('velocities', [])
            frequencies = flutter_summary.get('frequencies', [])
            dampings = flutter_summary.get('dampings', [])
            
            if plot_type == "vf":
                self.plot_vf(velocities, frequencies)
            elif plot_type == "vg":
                self.plot_vg(velocities, dampings)
            elif plot_type == "root_locus":
                self.plot_root_locus()
            elif plot_type == "modes":
                self.plot_mode_shapes()
                
        except Exception as e:
            self.plot_ax.text(0.5, 0.5, f'Plot Error: {str(e)}',
                            transform=self.plot_ax.transAxes, ha='center', va='center',
                            fontsize=12, color='red')
                            
        self.plot_canvas.draw()
        
    def plot_vf(self, velocities, frequencies):
        """Plot V-f diagram."""
        if velocities and frequencies:
            self.plot_ax.plot(velocities, frequencies, 'b-o', linewidth=2, markersize=4)
            self.plot_ax.set_xlabel('Velocity (m/s)')
            self.plot_ax.set_ylabel('Frequency (Hz)')
            self.plot_ax.set_title('V-f Diagram')
            self.plot_ax.grid(True, alpha=0.3)
            
            # Mark flutter point if available
            flutter_speed = self.results_data.get('flutter_summary', {}).get('flutter_speed')
            if flutter_speed:
                self.plot_ax.axvline(x=flutter_speed, color='red', linestyle='--', 
                                   linewidth=2, label=f'Flutter: {flutter_speed:.1f} m/s')
                self.plot_ax.legend()
        else:
            self.plot_ax.text(0.5, 0.5, 'No V-f data available',
                            transform=self.plot_ax.transAxes, ha='center', va='center')
            
    def plot_vg(self, velocities, dampings):
        """Plot V-g diagram."""
        if velocities and dampings:
            self.plot_ax.plot(velocities, dampings, 'r-s', linewidth=2, markersize=4)
            self.plot_ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            self.plot_ax.set_xlabel('Velocity (m/s)')
            self.plot_ax.set_ylabel('Damping')
            self.plot_ax.set_title('V-g Diagram')
            self.plot_ax.grid(True, alpha=0.3)
            
            # Mark flutter point
            flutter_speed = self.results_data.get('flutter_summary', {}).get('flutter_speed')
            if flutter_speed:
                self.plot_ax.axvline(x=flutter_speed, color='red', linestyle='--', 
                                   linewidth=2, label=f'Flutter: {flutter_speed:.1f} m/s')
                self.plot_ax.legend()
        else:
            self.plot_ax.text(0.5, 0.5, 'No V-g data available',
                            transform=self.plot_ax.transAxes, ha='center', va='center')
            
    def plot_root_locus(self):
        """Plot root locus."""
        self.plot_ax.text(0.5, 0.5, 'Root locus plot not yet implemented',
                        transform=self.plot_ax.transAxes, ha='center', va='center',
                        fontsize=12, color='gray')
        self.plot_ax.set_title('Root Locus')
        
    def plot_mode_shapes(self):
        """Plot mode shapes."""
        self.plot_ax.text(0.5, 0.5, 'Mode shapes shown in 3D visualization',
                        transform=self.plot_ax.transAxes, ha='center', va='center',
                        fontsize=12, color='gray')
        self.plot_ax.set_title('Mode Shapes')
        
    def sort_by_velocity(self):
        """Sort detailed results by velocity."""
        messagebox.showinfo("Sort", "Sorting by velocity not yet implemented")
        
    def sort_by_frequency(self):
        """Sort detailed results by frequency."""
        messagebox.showinfo("Sort", "Sorting by frequency not yet implemented")
        
    def filter_critical(self):
        """Filter for critical results only."""
        messagebox.showinfo("Filter", "Critical filtering not yet implemented")
        
    def save_plot(self):
        """Save current plot to file."""
        file_path = filedialog.asksaveasfilename(
            title="Save Plot",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")],
            defaultextension=".png"
        )
        
        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Plot saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plot: {str(e)}")
                
    def export_results(self):
        """Export results data."""
        if not self.results_data:
            messagebox.showwarning("No Data", "No results available to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Results",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("JSON files", "*.json")],
            defaultextension=".csv"
        )
        
        if file_path:
            try:
                format_type = self.export_format_var.get()
                
                if format_type == "csv":
                    self.export_to_csv(file_path)
                elif format_type == "xlsx":
                    self.export_to_excel(file_path)
                elif format_type == "json":
                    self.export_to_json(file_path)
                    
                messagebox.showinfo("Success", f"Results exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")
                
    def export_to_csv(self, file_path):
        """Export results to CSV format."""
        import csv
        
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Velocity', 'Frequency', 'Damping', 'Mode', 'Mach'])
            
            # Write data
            flutter_summary = self.results_data.get('flutter_summary', {})
            velocities = flutter_summary.get('velocities', [])
            frequencies = flutter_summary.get('frequencies', [])
            dampings = flutter_summary.get('dampings', [])
            
            for i, (v, f, d) in enumerate(zip(velocities, frequencies, dampings)):
                mach = v / 343.0
                writer.writerow([v, f, d, 1, mach])
                
    def export_to_json(self, file_path):
        """Export results to JSON format."""
        import json
        
        with open(file_path, 'w') as jsonfile:
            json.dump(self.results_data, jsonfile, indent=2)
            
    def export_to_excel(self, file_path):
        """Export results to Excel format."""
        messagebox.showinfo("Excel Export", "Excel export requires pandas/openpyxl")
        
    def export_report(self):
        """Export comprehensive report."""
        messagebox.showinfo("Export Report", "Report generation not yet implemented")