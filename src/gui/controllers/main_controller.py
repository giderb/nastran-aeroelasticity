"""
Main Controller for Panel Flutter Analysis GUI
=============================================

The main controller coordinates between the view and model components,
handling user interactions and managing the application state.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import logging
from pathlib import Path

from src.nastran.aero.analysis.panel_flutter import PanelFlutterPistonAnalysisModel
from src.nastran.aero.superpanels import SuperAeroPanel5
from ...gui.utils.validation import InputValidator
from ...gui.utils.file_manager import ProjectFileManager


class MainController:
    """
    Main controller implementing the Controller pattern for MVC architecture.
    Manages user interactions, data validation, and analysis execution.
    """
    
    
    def convert_gui_to_solver_units(self, config):
        """Convert GUI units (mm) to solver units (m)"""
        converted = config.copy()
        if 'geometry' in converted:
            geom = converted['geometry']
            geom['length'] = geom.get('length', 500) / 1000.0  # mm to m
            geom['width'] = geom.get('width', 300) / 1000.0    # mm to m
            geom['thickness'] = geom.get('thickness', 2) / 1000.0  # mm to m
        return converted

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.logger = logging.getLogger(__name__)
        self.validator = InputValidator()
        self.file_manager = ProjectFileManager()
        
        # Analysis state
        self.analysis_thread = None
        self.analysis_running = False
        
        # Current project file
        self.current_project_file = None
        
    def initialize(self):
        """Initialize the controller after all components are created."""
        self.update_view_state()
        self.view.update_status("Ready")
        
    def can_close(self):
        """Check if the application can be closed safely."""
        if self.model.is_modified():
            result = messagebox.askyesnocancel(
                "Unsaved Changes", 
                "There are unsaved changes. Do you want to save before closing?"
            )
            if result is True:
                return self.save_project()
            elif result is False:
                return True
            else:
                return False
        return True
        
    # Project management
    def new_project(self):
        """Create a new project."""
        if not self.can_close():
            return False
            
        self.model.new_project()
        self.current_project_file = None
        self.update_view_state()
        self.view.update_status("New project created")
        return True
        
    def open_project(self):
        """Open an existing project."""
        if not self.can_close():
            return False
            
        file_path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("Panel Flutter Project", "*.pfp"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.model = self.file_manager.load_project(file_path)
                self.current_project_file = file_path
                self.update_view_state()
                self.view.update_status(f"Project opened: {Path(file_path).name}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open project: {str(e)}")
                self.logger.error(f"Failed to open project {file_path}: {str(e)}")
                return False
                
        return False
        
    def save_project(self):
        """Save the current project."""
        if self.current_project_file:
            return self.save_to_file(self.current_project_file)
        else:
            return self.save_project_as()
            
    def save_project_as(self):
        """Save the current project with a new name."""
        file_path = filedialog.asksaveasfilename(
            title="Save Project As",
            filetypes=[("Panel Flutter Project", "*.pfp"), ("All files", "*.*")],
            defaultextension=".pfp"
        )
        
        if file_path:
            return self.save_to_file(file_path)
        return False
        
    def save_to_file(self, file_path):
        """Save the project to a specific file."""
        try:
            self.file_manager.save_project(self.model, file_path)
            self.current_project_file = file_path
            self.model.set_modified(False)
            self.view.update_status(f"Project saved: {Path(file_path).name}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {str(e)}")
            self.logger.error(f"Failed to save project {file_path}: {str(e)}")
            return False
            
    def import_bdf(self):
        """Import a NASTRAN BDF file."""
        file_path = filedialog.askopenfilename(
            title="Import BDF File",
            filetypes=[("NASTRAN BDF", "*.bdf"), ("NASTRAN DAT", "*.dat"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.model.import_bdf(file_path)
                self.update_view_state()
                self.view.update_status(f"BDF imported: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import BDF: {str(e)}")
                self.logger.error(f"Failed to import BDF {file_path}: {str(e)}")
                
    def export_bdf(self):
        """Export to NASTRAN BDF file."""
        file_path = filedialog.asksaveasfilename(
            title="Export BDF File",
            filetypes=[("NASTRAN BDF", "*.bdf"), ("All files", "*.*")],
            defaultextension=".bdf"
        )
        
        if file_path:
            try:
                self.model.export_bdf(file_path)
                self.view.update_status(f"BDF exported: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export BDF: {str(e)}")
                self.logger.error(f"Failed to export BDF {file_path}: {str(e)}")
                
    # Analysis operations
    def run_analysis(self):
        """Run flutter analysis."""
        if self.analysis_running:
            messagebox.showwarning("Analysis Running", "An analysis is already running.")
            return
            
        # Validate inputs
        validation_errors = self.validator.validate_analysis_inputs(self.model)
        if validation_errors:
            error_msg = "\\n".join(validation_errors)
            messagebox.showerror("Validation Error", f"Please fix the following errors:\\n{error_msg}")
            return
            
        # Start analysis in separate thread
        self.analysis_running = True
        self.analysis_thread = threading.Thread(target=self._run_analysis_thread)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
        
        self.view.update_status("Analysis running...")
        
    def _run_analysis_thread(self):
        """Run analysis in background thread using the proper flutter engine."""
        try:
            self.logger.info("Starting panel flutter analysis")
            
            # Get analysis parameters from GUI
            analysis_params = self.model.get_analysis_parameters()
            geometry = self.model.get_geometry()
            materials = self.model.get_materials()
            
            # Get selected solver method from GUI
            solver_method = analysis_params.get('solver_method', 'auto')
            self.logger.info(f"Analysis method selected: {solver_method}")
            
            # Import the flutter analysis system
            from ...gui.analysis.flutter_engine import (
                FlutterAnalysisEngine, FlutterAnalysisConfig, 
                GeometryConfig, MaterialConfig
            )
            from ...gui.analysis.analysis_runner import AnalysisRunner
            
            # Create configuration objects
            config = FlutterAnalysisConfig(
                method=solver_method if solver_method == 'nastran' else 'simulation',
                aerodynamic_theory=solver_method if solver_method == 'nastran' else analysis_params.get('aero_theory', 'Piston'),
                velocity_min=float(analysis_params.get('velocity_min', 50)),
                velocity_max=float(analysis_params.get('velocity_max', 300)),
                velocity_points=int(analysis_params.get('velocity_points', 25)),
                num_modes=int(analysis_params.get('num_modes', 10))
            )
            
            # Convert GUI geometry to engine format
            geometry_config = GeometryConfig(
                length=float(geometry.get('length', 0.5)),
                width=float(geometry.get('width', 0.3)),
                thickness=float(geometry.get('thickness', 0.002)),
                boundary_conditions=geometry.get('boundary_conditions', 'SSSS')
            )
            
            # Convert GUI materials to engine format
            material = materials[0] if materials else {}
            material_config = MaterialConfig(
                material_type='isotropic',
                youngs_modulus=float(material.get('youngs_modulus', 71.7e9)),
                poisson_ratio=float(material.get('poisson_ratio', 0.33)),
                density=float(material.get('density', 2810))
            )
            
            # Progress callback to update GUI
            def progress_callback(step, progress):
                self.view.root.after(0, lambda: self.view.set_progress(progress))
                self.view.root.after(0, lambda: self.view.update_status(step))
            
            # Create and run analysis
            runner = AnalysisRunner(progress_callback)
            results = runner.run_flutter_analysis(config, geometry_config, material_config)
            
            # Update model with results
            if results.analysis_successful:
                self.model.set_results({
                    'flutter_velocity': results.flutter_velocity,
                    'flutter_frequency': results.flutter_frequency,
                    'flutter_mode': results.flutter_mode,
                    'velocities': results.velocities.tolist() if results.velocities is not None else [],
                    'frequencies': results.frequencies.tolist() if results.frequencies is not None else [],
                    'dampings': results.dampings.tolist() if results.dampings is not None else [],
                    'analysis_method': solver_method,
                    'success': True
                })
                
                self.view.root.after(0, lambda: self.view.update_status("Analysis completed successfully"))
                self.logger.info(f"Analysis completed successfully using {solver_method} method")
                
                if results.flutter_velocity:
                    self.logger.info(f"Flutter speed: {results.flutter_velocity:.1f} m/s at {results.flutter_frequency:.1f} Hz")
                else:
                    self.logger.info("No flutter detected in velocity range")
            else:
                error_msg = results.error_message or "Analysis failed"
                self.view.root.after(0, lambda: messagebox.showerror("Analysis Error", error_msg))
                self.view.root.after(0, lambda: self.view.update_status("Analysis failed"))
                self.logger.error(f"Analysis failed: {error_msg}")
            
            self.view.root.after(0, lambda: self.view.set_progress(100))
            self.view.root.after(0, self.update_view_state)
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            self.view.root.after(0, lambda: messagebox.showerror("Analysis Error", f"Analysis failed: {str(e)}"))
            self.view.root.after(0, lambda: self.view.update_status("Analysis failed"))
            
        finally:
            self.analysis_running = False
            self.view.root.after(0, lambda: self.view.set_progress(0))
            
    def stop_analysis(self):
        """Stop running analysis."""
        if self.analysis_running:
            # In a real implementation, this would terminate the NASTRAN process
            self.analysis_running = False
            self.view.update_status("Analysis stopped by user")
            
    def parameter_study(self):
        """Run parameter study."""
        messagebox.showinfo("Parameter Study", "Parameter study functionality coming soon!")
        
    def validation_cases(self):
        """Run validation cases."""
        messagebox.showinfo("Validation Cases", "Validation cases functionality coming soon!")
        
    def _create_analysis_model(self):
        """Create the NASTRAN analysis model from the current project data."""
        # Get project parameters
        geometry = self.model.get_geometry()
        materials = self.model.get_materials()
        boundary_conditions = self.model.get_boundary_conditions()
        analysis_params = self.model.get_analysis_parameters()
        
        # Create analysis model
        analysis_model = PanelFlutterPistonAnalysisModel()
        
        # Set up global parameters
        analysis_model.set_global_case_from_dict({
            'machs': analysis_params.get('mach_numbers', [0.7, 0.8, 0.9]),
            'alphas': analysis_params.get('angles_of_attack', [0.0]),
            'densities_ratio': analysis_params.get('density_ratios', [1.0]),
            'velocities': analysis_params.get('velocities', [100, 200, 300]),
            'method': analysis_params.get('method', 'PK'),
            'n_modes': analysis_params.get('num_modes', 10),
            'frequency_limits': analysis_params.get('frequency_range', [0.1, 100.0]),
            'ref_chord': geometry.get('chord', 1.0),
            'ref_rho': analysis_params.get('reference_density', 1.225),
            'reduced_frequencies': analysis_params.get('reduced_frequencies', [0.1, 0.5, 1.0, 2.0])
        })
        
        # Create superpanel
        p1 = geometry.get('corner_points', [[0, 0, 0]])[0]
        p2 = geometry.get('corner_points', [[1, 0, 0]])[1] if len(geometry.get('corner_points', [])) > 1 else [1, 0, 0]
        p3 = geometry.get('corner_points', [[1, 1, 0]])[2] if len(geometry.get('corner_points', [])) > 2 else [1, 1, 0]
        p4 = geometry.get('corner_points', [[0, 1, 0]])[3] if len(geometry.get('corner_points', [])) > 3 else [0, 1, 0]
        
        superpanel = SuperAeroPanel5(
            eid=1,
            p1=p1, p2=p2, p3=p3, p4=p4,
            nchord=geometry.get('n_chord', 10),
            nspan=geometry.get('n_span', 5),
            theory=analysis_params.get('aero_theory', 'PISTON')
        )
        
        analysis_model.add_superpanel(superpanel)
        
        return analysis_model
        
    def _load_analysis_results(self):
        """Load analysis results (simulated for now)."""
        # In a real implementation, this would parse NASTRAN output files
        import numpy as np
        
        # Simulate flutter results
        velocities = np.linspace(50, 300, 20)
        frequencies = np.array([
            10.0 + 0.1 * v + 0.001 * v**2 for v in velocities
        ])
        dampings = np.array([
            0.1 - 0.001 * v + 0.0001 * v**1.5 for v in velocities
        ])
        
        results = {
            'flutter_summary': {
                'velocities': velocities.tolist(),
                'frequencies': frequencies.tolist(),
                'dampings': dampings.tolist(),
                'flutter_speed': 200.0,  # Example flutter speed
                'flutter_frequency': 15.2  # Example flutter frequency
            },
            'modes': [
                {'mode_number': 1, 'frequency': 10.5, 'description': 'First bending'},
                {'mode_number': 2, 'frequency': 25.8, 'description': 'Second bending'},
                {'mode_number': 3, 'frequency': 42.1, 'description': 'First torsion'}
            ]
        }
        
        return results
        
    def update_view_state(self):
        """Update the view to reflect current model state."""
        # This method would update all panels with current data
        pass
        
    # Geometry operations
    def update_geometry(self, geometry_data):
        """Update geometry parameters."""
        self.model.set_geometry(geometry_data)
        self.model.set_modified(True)
        
    def update_materials(self, materials_data):
        """Update material properties."""
        self.model.set_materials(materials_data)
        self.model.set_modified(True)
        
    def update_boundary_conditions(self, bc_data):
        """Update boundary conditions."""
        self.model.set_boundary_conditions(bc_data)
        self.model.set_modified(True)
        
    def update_analysis_parameters(self, analysis_data):
        """Update analysis parameters."""
        self.model.set_analysis_parameters(analysis_data)
        self.model.set_modified(True)