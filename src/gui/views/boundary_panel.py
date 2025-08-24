"""
Boundary Conditions Panel for Panel Flutter Analysis GUI
======================================================

Provides interface for defining boundary conditions including
edge constraints, applied loads, and environmental conditions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# Add src directory for boundary conditions
src_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_dir))

from gui.utils.widgets import LabeledEntry, LabeledSpinbox, ParameterTable
from analysis.boundary_conditions import BoundaryCondition, BoundaryConditionManager, EdgeConstraint


class BoundaryPanel:
    """
    Panel for boundary condition definition and management.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        
        # Initialize boundary condition manager
        self.bc_manager = BoundaryConditionManager()
        
        # Create main frame
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the user interface components."""
        
        # Standard Boundary Conditions frame
        standard_frame = ttk.LabelFrame(self.frame, text="Standard Boundary Conditions", padding=10)
        standard_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Predefined boundary condition selection
        self.bc_selection_var = tk.StringVar(value="SSSS")
        ttk.Label(standard_frame, text="Boundary Condition Type:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Get all available boundary conditions
        bc_options = []
        bc_descriptions = {}
        for bc_type, bc_props in self.bc_manager.get_all_boundary_conditions().items():
            display_name = f"{bc_type.value} - {bc_props.name}"
            bc_options.append(display_name)
            bc_descriptions[display_name] = bc_props
        
        bc_combo = ttk.Combobox(standard_frame, textvariable=self.bc_selection_var,
                               values=bc_options, state="readonly", width=40)
        bc_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        bc_combo.bind('<<ComboboxSelected>>', self.on_bc_selection_changed)
        
        # Description and properties
        self.description_text = tk.Text(standard_frame, height=3, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.description_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Flutter characteristics
        flutter_frame = ttk.LabelFrame(standard_frame, text="Flutter Characteristics", padding=5)
        flutter_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)
        
        self.flutter_tendency_label = ttk.Label(flutter_frame, text="Flutter Tendency: Medium", style='Modern.TLabel')
        self.flutter_tendency_label.pack(anchor=tk.W)
        
        self.stiffness_label = ttk.Label(flutter_frame, text="Structural Stiffness: 0.5", style='Modern.TLabel')
        self.stiffness_label.pack(anchor=tk.W)
        
        self.convergence_label = ttk.Label(flutter_frame, text="Convergence: Easy", style='Modern.TLabel')
        self.convergence_label.pack(anchor=tk.W)
        
        # Validation warnings
        self.warnings_frame = ttk.LabelFrame(self.frame, text="Analysis Notes & Warnings", padding=10)
        self.warnings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.warnings_text = tk.Text(self.warnings_frame, height=4, width=50, wrap=tk.WORD, 
                                   state=tk.DISABLED, bg='lightyellow')
        self.warnings_text.pack(fill=tk.BOTH, expand=True)
        
        # Custom boundary conditions frame (advanced)
        custom_frame = ttk.LabelFrame(self.frame, text="Custom Edge Constraints (Advanced)", padding=10)
        custom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Enable custom mode checkbox
        self.custom_mode_var = tk.BooleanVar(value=False)
        custom_check = ttk.Checkbutton(custom_frame, text="Enable Custom Boundary Conditions",
                                     variable=self.custom_mode_var, command=self.toggle_custom_mode)
        custom_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Individual edge controls (initially disabled)
        edge_options = ["Free", "Simply Supported", "Clamped", "Elastic"]
        
        # Leading edge
        self.leading_edge_var = tk.StringVar(value="Simply Supported")
        ttk.Label(custom_frame, text="Leading Edge (Upstream):", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, pady=2)
        self.leading_combo = ttk.Combobox(custom_frame, textvariable=self.leading_edge_var,
                                         values=edge_options, state="disabled", width=15)
        self.leading_combo.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Trailing edge
        self.trailing_edge_var = tk.StringVar(value="Simply Supported")
        ttk.Label(custom_frame, text="Trailing Edge (Downstream):", style='Modern.TLabel').grid(row=2, column=0, sticky=tk.W, pady=2)
        self.trailing_combo = ttk.Combobox(custom_frame, textvariable=self.trailing_edge_var,
                                          values=edge_options, state="disabled", width=15)
        self.trailing_combo.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Left edge
        self.left_edge_var = tk.StringVar(value="Simply Supported")
        ttk.Label(custom_frame, text="Left Edge (Port):", style='Modern.TLabel').grid(row=3, column=0, sticky=tk.W, pady=2)
        self.left_combo = ttk.Combobox(custom_frame, textvariable=self.left_edge_var,
                                      values=edge_options, state="disabled", width=15)
        self.left_combo.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Right edge
        self.right_edge_var = tk.StringVar(value="Simply Supported")
        ttk.Label(custom_frame, text="Right Edge (Starboard):", style='Modern.TLabel').grid(row=4, column=0, sticky=tk.W, pady=2)
        self.right_combo = ttk.Combobox(custom_frame, textvariable=self.right_edge_var,
                                       values=edge_options, state="disabled", width=15)
        self.right_combo.grid(row=4, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Bind custom edge changes to validation
        for combo in [self.leading_combo, self.trailing_combo, self.left_combo, self.right_combo]:
            combo.bind('<<ComboboxSelected>>', self.validate_custom_bc)
        
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
        
        # Initialize with default boundary condition
        self.on_bc_selection_changed(None)
        
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
    
    def on_bc_selection_changed(self, event):
        """Handle boundary condition selection change"""
        selected = self.bc_selection_var.get()
        
        if not selected:
            return
            
        # Parse boundary condition type from selection
        bc_type_str = selected.split(' - ')[0]
        try:
            bc_type = BoundaryCondition(bc_type_str)
            bc_props = self.bc_manager.get_boundary_condition(bc_type)
            
            if bc_props:
                # Update description
                self.description_text.config(state=tk.NORMAL)
                self.description_text.delete(1.0, tk.END)
                self.description_text.insert(1.0, bc_props.description)
                self.description_text.config(state=tk.DISABLED)
                
                # Update characteristics
                self.flutter_tendency_label.config(text=f"Flutter Tendency: {bc_props.flutter_tendency.title()}")
                self.stiffness_label.config(text=f"Structural Stiffness: {bc_props.structural_stiffness:.1f}")
                self.convergence_label.config(text=f"Convergence: {bc_props.convergence_difficulty.title()}")
                
                # Update warnings
                valid, warnings = self.bc_manager.validate_boundary_condition(bc_type)
                self.warnings_text.config(state=tk.NORMAL)
                self.warnings_text.delete(1.0, tk.END)
                
                if warnings:
                    warning_text = "\\n".join(warnings)
                    self.warnings_text.insert(1.0, warning_text)
                else:
                    self.warnings_text.insert(1.0, "No special warnings for this boundary condition.")
                    
                self.warnings_text.config(state=tk.DISABLED)
                
                # Update individual edge controls to match
                if not self.custom_mode_var.get():
                    edge_constraints = self.bc_manager.get_edge_constraints(bc_type)
                    self.update_edge_controls(edge_constraints)
                
        except ValueError:
            pass  # Invalid boundary condition selection
    
    def toggle_custom_mode(self):
        """Toggle between standard and custom boundary condition modes"""
        custom_enabled = self.custom_mode_var.get()
        
        # Enable/disable custom edge controls
        state = "readonly" if custom_enabled else "disabled"
        for combo in [self.leading_combo, self.trailing_combo, self.left_combo, self.right_combo]:
            combo.config(state=state)
        
        if custom_enabled:
            # Custom mode - validate current combination
            self.validate_custom_bc(None)
        else:
            # Standard mode - sync with selected standard boundary condition
            self.on_bc_selection_changed(None)
    
    def update_edge_controls(self, edge_constraints):
        """Update individual edge controls based on edge constraints"""
        constraint_map = {
            EdgeConstraint.FREE: "Free",
            EdgeConstraint.SIMPLY_SUPPORTED: "Simply Supported", 
            EdgeConstraint.CLAMPED: "Clamped",
            EdgeConstraint.ELASTIC: "Elastic"
        }
        
        self.leading_edge_var.set(constraint_map.get(edge_constraints.get('leading'), 'Simply Supported'))
        self.trailing_edge_var.set(constraint_map.get(edge_constraints.get('trailing'), 'Simply Supported'))
        self.left_edge_var.set(constraint_map.get(edge_constraints.get('left'), 'Simply Supported'))
        self.right_edge_var.set(constraint_map.get(edge_constraints.get('right'), 'Simply Supported'))
    
    def validate_custom_bc(self, event):
        """Validate custom boundary condition combination"""
        if not self.custom_mode_var.get():
            return
            
        # Get current edge selections
        edge_constraints = {
            'leading': self.leading_edge_var.get(),
            'trailing': self.trailing_edge_var.get(),
            'left': self.left_edge_var.get(),
            'right': self.right_edge_var.get()
        }
        
        # Create boundary condition string (e.g., "CFSS")
        constraint_map = {
            "Free": "F",
            "Simply Supported": "S",
            "Clamped": "C", 
            "Elastic": "E"
        }
        
        bc_string = ''.join([
            constraint_map.get(edge_constraints['leading'], 'S'),
            constraint_map.get(edge_constraints['trailing'], 'S'),
            constraint_map.get(edge_constraints['left'], 'S'),
            constraint_map.get(edge_constraints['right'], 'S')
        ])
        
        # Check if this is a known standard combination
        try:
            bc_type = BoundaryCondition(bc_string)
            bc_props = self.bc_manager.get_boundary_condition(bc_type)
            
            # Update display with custom combination info
            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(1.0, f"Custom: {bc_props.name if bc_props else 'Unknown combination'}")
            self.description_text.config(state=tk.DISABLED)
            
            if bc_props:
                self.flutter_tendency_label.config(text=f"Flutter Tendency: {bc_props.flutter_tendency.title()}")
                self.stiffness_label.config(text=f"Structural Stiffness: {bc_props.structural_stiffness:.1f}")
                self.convergence_label.config(text=f"Convergence: {bc_props.convergence_difficulty.title()}")
                
                valid, warnings = self.bc_manager.validate_boundary_condition(bc_type)
            else:
                # Unknown combination - provide generic warnings
                self.flutter_tendency_label.config(text="Flutter Tendency: Unknown")
                self.stiffness_label.config(text="Structural Stiffness: Unknown")
                self.convergence_label.config(text="Convergence: Unknown")
                warnings = ["⚠️ This boundary condition combination has not been validated",
                          "📝 Results may be unpredictable - use with caution"]
                
        except ValueError:
            # Not a standard boundary condition
            bc_props = None
            warnings = ["⚠️ Custom boundary condition combination",
                       "📝 Verify results against known solutions"]
            
            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(1.0, f"Custom combination: {bc_string}")
            self.description_text.config(state=tk.DISABLED)
            
            self.flutter_tendency_label.config(text="Flutter Tendency: Unknown")
            self.stiffness_label.config(text="Structural Stiffness: Unknown")
            self.convergence_label.config(text="Convergence: Unknown")
        
        # Update warnings
        self.warnings_text.config(state=tk.NORMAL)
        self.warnings_text.delete(1.0, tk.END)
        if warnings:
            warning_text = "\\n".join(warnings)
            self.warnings_text.insert(1.0, warning_text)
        self.warnings_text.config(state=tk.DISABLED)
    
    def get_selected_boundary_condition(self) -> BoundaryCondition:
        """Get the currently selected boundary condition"""
        if self.custom_mode_var.get():
            # Custom mode - build from individual edges
            constraint_map = {
                "Free": "F", "Simply Supported": "S", "Clamped": "C", "Elastic": "E"
            }
            
            bc_string = ''.join([
                constraint_map.get(self.leading_edge_var.get(), 'S'),
                constraint_map.get(self.trailing_edge_var.get(), 'S'),
                constraint_map.get(self.left_edge_var.get(), 'S'),
                constraint_map.get(self.right_edge_var.get(), 'S')
            ])
            
            try:
                return BoundaryCondition(bc_string)
            except ValueError:
                return BoundaryCondition.SSSS  # Default fallback
        else:
            # Standard mode
            selected = self.bc_selection_var.get()
            if selected:
                bc_type_str = selected.split(' - ')[0]
                try:
                    return BoundaryCondition(bc_type_str)
                except ValueError:
                    pass
            return BoundaryCondition.SSSS  # Default fallback