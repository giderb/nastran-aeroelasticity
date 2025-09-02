"""
Analysis Panel for Panel Flutter Analysis GUI
============================================

Provides interface for setting up and configuring flutter analysis parameters
including Mach numbers, velocities, methods, and solver options.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from src.gui.utils.widgets import LabeledEntry, LabeledSpinbox, ParameterTable
from src.gui.utils.validation import is_valid_float, is_positive_float


class AnalysisPanel:
    """
    Panel for analysis parameter configuration and execution control.
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
        # Create notebook for analysis sub-panels
        self.notebook = ttk.Notebook(self.frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Analysis parameters tab
        self.create_parameters_tab()
        
        # Flight conditions tab
        self.create_flight_conditions_tab()
        
        # Solver options tab
        self.create_solver_options_tab()
        
    def create_parameters_tab(self):
        """Create analysis parameters tab."""
        params_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(params_frame, text="Parameters")
        
        # Analysis type frame
        type_frame = ttk.LabelFrame(params_frame, text="Analysis Type", padding=10)
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.analysis_type_var = tk.StringVar(value="flutter")
        analysis_types = ["flutter", "stability", "frequency_response"]
        
        for i, analysis_type in enumerate(analysis_types):
            rb = ttk.Radiobutton(
                type_frame,
                text=analysis_type.replace('_', ' ').title(),
                variable=self.analysis_type_var,
                value=analysis_type
            )
            rb.grid(row=0, column=i, padx=10, pady=5)
            
        # Aerodynamic theory frame
        aero_frame = ttk.LabelFrame(params_frame, text="Aerodynamic Theory", padding=10)
        aero_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.aero_theory_var = tk.StringVar(value="piston")
        aero_theories = ["piston", "vandyke", "vdsweep"]
        
        for i, theory in enumerate(aero_theories):
            rb = ttk.Radiobutton(
                aero_frame,
                text=theory.upper(),
                variable=self.aero_theory_var,
                value=theory
            )
            rb.grid(row=0, column=i, padx=10, pady=5)
            
        # Solver selection frame
        solver_frame = ttk.LabelFrame(params_frame, text="Flutter Analysis Solver", padding=10)
        solver_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Solver method selection
        ttk.Label(solver_frame, text="Primary Solver:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.solver_method_var = tk.StringVar(value="auto")
        solver_combo = ttk.Combobox(solver_frame, textvariable=self.solver_method_var,
                                   values=["auto", "piston_theory", "doublet_lattice", "nastran"],
                                   state="readonly", width=15)
        solver_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Multi-solver comparison option
        self.multi_solver_var = tk.BooleanVar(value=True)
        multi_solver_check = ttk.Checkbutton(solver_frame, text="Enable multi-solver comparison",
                                            variable=self.multi_solver_var)
        multi_solver_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Solver info button
        info_btn = ttk.Button(solver_frame, text="Solver Info", command=self.show_solver_info,
                             style='Modern.TButton')
        info_btn.grid(row=0, column=2, padx=10, pady=2)
        
        # Solution method frame (for NASTRAN compatibility)
        method_frame = ttk.LabelFrame(params_frame, text="Solution Method (NASTRAN)", padding=10)
        method_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(method_frame, text="Method:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.method_var = tk.StringVar(value="PK")
        method_combo = ttk.Combobox(method_frame, textvariable=self.method_var,
                                  values=["K", "KE", "PK", "PKNL", "PKS", "PKNLS"],
                                  state="readonly", width=10)
        method_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Modal analysis parameters
        modal_frame = ttk.LabelFrame(params_frame, text="Modal Analysis", padding=10)
        modal_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.num_modes_spinbox = LabeledSpinbox(modal_frame, "Number of Modes:", 
                                              from_=1, to=50, increment=1, width=10)
        self.num_modes_spinbox.set(10)
        self.num_modes_spinbox.pack(anchor=tk.W, pady=2)
        
        # Frequency range
        self.freq_min_entry = LabeledEntry(modal_frame, "Min Frequency (Hz):", is_positive_float, width=15)
        self.freq_min_entry.set("0.1")
        self.freq_min_entry.pack(anchor=tk.W, pady=2)
        
        self.freq_max_entry = LabeledEntry(modal_frame, "Max Frequency (Hz):", is_positive_float, width=15)
        self.freq_max_entry.set("100.0")
        self.freq_max_entry.pack(anchor=tk.W, pady=2)
        
    def create_flight_conditions_tab(self):
        """Create flight conditions tab."""
        flight_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(flight_frame, text="Flight Conditions")
        
        # Mach numbers frame
        mach_frame = ttk.LabelFrame(flight_frame, text="Mach Numbers", padding=10)
        mach_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Mach number input
        input_frame = ttk.Frame(mach_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.mach_entry = LabeledEntry(input_frame, "Mach Numbers (comma separated):", width=30)
        self.mach_entry.set("0.5, 0.7, 0.8, 0.9, 1.0, 1.2")
        self.mach_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Parse", command=self.parse_mach_numbers,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=5)
                  
        # Mach numbers table
        self.mach_table = ParameterTable(mach_frame, ["Index", "Mach Number"])
        self.mach_table.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Velocities frame
        vel_frame = ttk.LabelFrame(flight_frame, text="Velocities", padding=10)
        vel_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Velocity range
        self.vel_min_entry = LabeledEntry(vel_frame, "Min Velocity (m/s):", is_positive_float, width=15)
        self.vel_min_entry.set("50")
        self.vel_min_entry.pack(anchor=tk.W, pady=2)
        
        self.vel_max_entry = LabeledEntry(vel_frame, "Max Velocity (m/s):", is_positive_float, width=15)
        self.vel_max_entry.set("300")
        self.vel_max_entry.pack(anchor=tk.W, pady=2)
        
        self.vel_points_spinbox = LabeledSpinbox(vel_frame, "Number of Points:", 
                                               from_=5, to=100, increment=5, width=10)
        self.vel_points_spinbox.set(20)
        self.vel_points_spinbox.pack(anchor=tk.W, pady=2)
        
        ttk.Button(vel_frame, text="Generate Velocity Range", command=self.generate_velocities,
                  style='Modern.TButton').pack(pady=5)
                  
        # Reduced frequencies frame
        freq_frame = ttk.LabelFrame(flight_frame, text="Reduced Frequencies", padding=10)
        freq_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.reduced_freq_entry = LabeledEntry(freq_frame, "Reduced Frequencies:", width=30)
        self.reduced_freq_entry.set("0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0")
        self.reduced_freq_entry.pack(anchor=tk.W, pady=2)
        
    def create_solver_options_tab(self):
        """Create solver options tab."""
        solver_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(solver_frame, text="Solver Options")
        
        # Convergence parameters
        conv_frame = ttk.LabelFrame(solver_frame, text="Convergence Parameters", padding=10)
        conv_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.tolerance_entry = LabeledEntry(conv_frame, "Convergence Tolerance:", width=15)
        self.tolerance_entry.set("1e-6")
        self.tolerance_entry.pack(anchor=tk.W, pady=2)
        
        self.max_iter_spinbox = LabeledSpinbox(conv_frame, "Maximum Iterations:", 
                                             from_=10, to=1000, increment=10, width=10)
        self.max_iter_spinbox.set(100)
        self.max_iter_spinbox.pack(anchor=tk.W, pady=2)
        
        # Reference parameters
        ref_frame = ttk.LabelFrame(solver_frame, text="Reference Parameters", padding=10)
        ref_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.ref_chord_entry = LabeledEntry(ref_frame, "Reference Chord (mm):", is_positive_float, width=15)
        self.ref_chord_entry.set("1.0")
        self.ref_chord_entry.pack(anchor=tk.W, pady=2)
        
        self.ref_density_entry = LabeledEntry(ref_frame, "Reference Density (kg/m³):", is_positive_float, width=15)
        self.ref_density_entry.set("1.225")
        self.ref_density_entry.pack(anchor=tk.W, pady=2)
        
        # Output options
        output_frame = ttk.LabelFrame(solver_frame, text="Output Options", padding=10)
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.detailed_output_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(output_frame, text="Detailed output",
                       variable=self.detailed_output_var).pack(anchor=tk.W, pady=2)
                       
        self.save_modes_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(output_frame, text="Save mode shapes",
                       variable=self.save_modes_var).pack(anchor=tk.W, pady=2)
                       
        self.save_matrices_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(output_frame, text="Save system matrices",
                       variable=self.save_matrices_var).pack(anchor=tk.W, pady=2)
                       
        # Run analysis button
        run_frame = ttk.Frame(solver_frame)
        run_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(run_frame, text="Run Analysis", command=self.run_analysis,
                  style='Success.TButton').pack(pady=10)
                  
    def bind_events(self):
        """Bind events to UI components."""
        # Parse Mach numbers when entry changes
        self.mach_entry.var.trace('w', lambda *args: self.parse_mach_numbers())
        
    def set_controller(self, controller):
        """Set the controller for this panel."""
        self.controller = controller
        
    def parse_mach_numbers(self):
        """Parse Mach numbers from entry field."""
        try:
            mach_str = self.mach_entry.get()
            mach_numbers = [float(x.strip()) for x in mach_str.split(',') if x.strip()]
            
            # Update table
            self.mach_table.clear()
            for i, mach in enumerate(mach_numbers):
                self.mach_table.insert_row([str(i+1), f"{mach:.2f}"])
                
        except ValueError:
            pass  # Invalid input, ignore
            
    def generate_velocities(self):
        """Generate velocity range."""
        try:
            v_min = float(self.vel_min_entry.get())
            v_max = float(self.vel_max_entry.get())
            n_points = int(self.vel_points_spinbox.get())
            
            velocities = np.linspace(v_min, v_max, n_points)
            vel_str = ', '.join([f"{v:.1f}" for v in velocities])
            
            messagebox.showinfo("Generated Velocities", 
                              f"Generated {n_points} velocities from {v_min} to {v_max} m/s")
                              
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error generating velocities: {str(e)}")
            
    def run_analysis(self):
        """Run the flutter analysis."""
        if self.controller:
            self.controller.run_analysis()
        else:
            messagebox.showinfo("Run Analysis", "Analysis execution not yet implemented")
            
    def show_solver_info(self):
        """Show information about available solvers"""
        info_text = """
FLUTTER ANALYSIS SOLVERS:

• AUTO - Intelligent solver selection based on flow conditions
  Recommends best method automatically

• PISTON THEORY (Level 1)
  - Fast, preliminary analysis
  - Best for: Supersonic flow (M > 1.2)
  - Accuracy: Good for thin panels, high speed
  - Speed: Very fast (~1 second)

• DOUBLET LATTICE (Level 2) 
  - Moderate accuracy, good performance
  - Best for: Subsonic/transonic (M < 0.95)
  - Accuracy: Better than piston theory
  - Speed: Fast (~10 seconds)

• NASTRAN (Level 3)
  - High fidelity analysis
  - Best for: All conditions, final design
  - Accuracy: Most accurate
  - Speed: Slow (~minutes)

RECOMMENDATIONS:
- Preliminary design: Piston Theory or Auto
- Design validation: Multi-solver comparison
- Final analysis: NASTRAN
        """
        
        messagebox.showinfo("Solver Information", info_text)
    
    def get_analysis_data(self) -> dict:
        """Get current analysis parameters."""
        try:
            # Parse Mach numbers
            mach_str = self.mach_entry.get()
            mach_numbers = [float(x.strip()) for x in mach_str.split(',') if x.strip()]
            
            # Parse reduced frequencies
            freq_str = self.reduced_freq_entry.get()
            reduced_frequencies = [float(x.strip()) for x in freq_str.split(',') if x.strip()]
            
            # Generate velocities
            v_min = float(self.vel_min_entry.get()) if self.vel_min_entry.get() else 50.0
            v_max = float(self.vel_max_entry.get()) if self.vel_max_entry.get() else 300.0
            n_points = int(self.vel_points_spinbox.get())
            velocities = np.linspace(v_min, v_max, n_points).tolist()
            
            analysis_data = {
                'analysis_type': self.analysis_type_var.get(),
                'aero_theory': self.aero_theory_var.get(),
                'solver_method': self.solver_method_var.get(),
            'multi_solver_enabled': self.multi_solver_var.get(),
            'method': self.method_var.get(),
                'num_modes': int(self.num_modes_spinbox.get()),
                'frequency_range': [
                    float(self.freq_min_entry.get()) if self.freq_min_entry.get() else 0.1,
                    float(self.freq_max_entry.get()) if self.freq_max_entry.get() else 100.0
                ],
                'mach_numbers': mach_numbers,
                'velocities': velocities,
                'reduced_frequencies': reduced_frequencies,
                'convergence_tolerance': float(self.tolerance_entry.get()) if self.tolerance_entry.get() else 1e-6,
                'max_iterations': int(self.max_iter_spinbox.get()),
                'reference_chord': float(self.ref_chord_entry.get()) if self.ref_chord_entry.get() else 1.0,
                'reference_density': float(self.ref_density_entry.get()) if self.ref_density_entry.get() else 1.225,
                'output_options': {
                    'detailed_output': self.detailed_output_var.get(),
                    'save_modes': self.save_modes_var.get(),
                    'save_matrices': self.save_matrices_var.get()
                }
            }
            
            return analysis_data
            
        except (ValueError, TypeError) as e:
            messagebox.showerror("Invalid Data", f"Error reading analysis parameters: {str(e)}")
            return {}
            
    def set_analysis_data(self, analysis_data: dict):
        """Set analysis parameters from external source."""
        try:
            # Basic parameters
            self.analysis_type_var.set(analysis_data.get('analysis_type', 'flutter'))
            self.aero_theory_var.set(analysis_data.get('aero_theory', 'piston'))
            self.method_var.set(analysis_data.get('method', 'PK'))
            
            # Modal parameters
            self.num_modes_spinbox.set(analysis_data.get('num_modes', 10))
            
            freq_range = analysis_data.get('frequency_range', [0.1, 100.0])
            if len(freq_range) >= 2:
                self.freq_min_entry.set(str(freq_range[0]))
                self.freq_max_entry.set(str(freq_range[1]))
                
            # Flight conditions
            mach_numbers = analysis_data.get('mach_numbers', [])
            if mach_numbers:
                mach_str = ', '.join([str(m) for m in mach_numbers])
                self.mach_entry.set(mach_str)
                
            velocities = analysis_data.get('velocities', [])
            if velocities:
                self.vel_min_entry.set(str(min(velocities)))
                self.vel_max_entry.set(str(max(velocities)))
                self.vel_points_spinbox.set(len(velocities))
                
            reduced_freq = analysis_data.get('reduced_frequencies', [])
            if reduced_freq:
                freq_str = ', '.join([str(f) for f in reduced_freq])
                self.reduced_freq_entry.set(freq_str)
                
            # Solver options
            self.tolerance_entry.set(str(analysis_data.get('convergence_tolerance', 1e-6)))
            self.max_iter_spinbox.set(analysis_data.get('max_iterations', 100))
            self.ref_chord_entry.set(str(analysis_data.get('reference_chord', 1.0)))
            self.ref_density_entry.set(str(analysis_data.get('reference_density', 1.225)))
            
            # Output options
            output_options = analysis_data.get('output_options', {})
            self.detailed_output_var.set(output_options.get('detailed_output', True))
            self.save_modes_var.set(output_options.get('save_modes', True))
            self.save_matrices_var.set(output_options.get('save_matrices', False))
            
            # Update displays
            self.parse_mach_numbers()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error setting analysis data: {str(e)}")