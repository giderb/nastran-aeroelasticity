"""
Boundary Conditions Panel for Panel Flutter Analysis GUI
======================================================

Provides interface for defining boundary conditions including
edge constraints, applied loads, and environmental conditions.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from gui.utils.widgets import LabeledEntry, LabeledSpinbox, ParameterTable


class BoundaryPanel:
    """
    Panel for boundary condition definition and management.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        
        # Create main frame
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the user interface components."""
        # Edge constraints frame
        constraints_frame = ttk.LabelFrame(self.frame, text="Edge Constraints", padding=10)
        constraints_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Leading edge
        self.leading_edge_var = tk.StringVar(value="clamped")
        ttk.Label(constraints_frame, text="Leading Edge:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, pady=2)
        leading_combo = ttk.Combobox(constraints_frame, textvariable=self.leading_edge_var,
                                   values=["free", "simply_supported", "clamped", "elastic"],
                                   state="readonly", width=15)
        leading_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Trailing edge
        self.trailing_edge_var = tk.StringVar(value="free")
        ttk.Label(constraints_frame, text="Trailing Edge:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, pady=2)
        trailing_combo = ttk.Combobox(constraints_frame, textvariable=self.trailing_edge_var,
                                    values=["free", "simply_supported", "clamped", "elastic"],
                                    state="readonly", width=15)
        trailing_combo.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Left edge
        self.left_edge_var = tk.StringVar(value="simply_supported")
        ttk.Label(constraints_frame, text="Left Edge:", style='Modern.TLabel').grid(row=2, column=0, sticky=tk.W, pady=2)
        left_combo = ttk.Combobox(constraints_frame, textvariable=self.left_edge_var,
                                values=["free", "simply_supported", "clamped", "elastic"],
                                state="readonly", width=15)
        left_combo.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Right edge
        self.right_edge_var = tk.StringVar(value="simply_supported")
        ttk.Label(constraints_frame, text="Right Edge:", style='Modern.TLabel').grid(row=3, column=0, sticky=tk.W, pady=2)
        right_combo = ttk.Combobox(constraints_frame, textvariable=self.right_edge_var,
                                 values=["free", "simply_supported", "clamped", "elastic"],
                                 state="readonly", width=15)
        right_combo.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Environmental conditions frame
        env_frame = ttk.LabelFrame(self.frame, text="Environmental Conditions", padding=10)
        env_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Temperature
        self.temperature_entry = LabeledEntry(env_frame, "Temperature (K):", width=15)
        self.temperature_entry.set("293.15")
        self.temperature_entry.pack(anchor=tk.W, pady=2)
        
        # Pressure
        self.pressure_entry = LabeledEntry(env_frame, "Pressure (Pa):", width=15)
        self.pressure_entry.set("101325")
        self.pressure_entry.pack(anchor=tk.W, pady=2)
        
    def set_controller(self, controller):
        """Set the controller for this panel."""
        self.controller = controller
        
    def get_boundary_data(self) -> dict:
        """Get current boundary condition data."""
        return {
            'edge_constraints': {
                'leading': self.leading_edge_var.get(),
                'trailing': self.trailing_edge_var.get(),
                'left': self.left_edge_var.get(),
                'right': self.right_edge_var.get()
            },
            'environmental': {
                'temperature': float(self.temperature_entry.get()) if self.temperature_entry.get() else 293.15,
                'pressure': float(self.pressure_entry.get()) if self.pressure_entry.get() else 101325
            }
        }
        
    def set_boundary_data(self, boundary_data: dict):
        """Set boundary condition data."""
        edge_constraints = boundary_data.get('edge_constraints', {})
        self.leading_edge_var.set(edge_constraints.get('leading', 'clamped'))
        self.trailing_edge_var.set(edge_constraints.get('trailing', 'free'))
        self.left_edge_var.set(edge_constraints.get('left', 'simply_supported'))
        self.right_edge_var.set(edge_constraints.get('right', 'simply_supported'))
        
        environmental = boundary_data.get('environmental', {})
        self.temperature_entry.set(str(environmental.get('temperature', 293.15)))
        self.pressure_entry.set(str(environmental.get('pressure', 101325)))