"""
File Management for Panel Flutter Analysis GUI
==============================================

Provides file I/O operations for project management and data exchange.
"""

import json
import pickle
import os
from pathlib import Path
from typing import Dict, Any
import logging


class ProjectFileManager:
    """
    Manages project file operations including save, load, import, and export.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = {
            '.pfp': self._save_pfp,
            '.json': self._save_json,
            '.pickle': self._save_pickle
        }
        
    def save_project(self, project_model, file_path: str):
        """
        Save project to file based on file extension.
        
        Args:
            project_model: The project model instance
            file_path: Path where to save the project
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension in self.supported_formats:
            self.supported_formats[extension](project_model, file_path)
            self.logger.info(f"Project saved to {file_path}")
        else:
            # Default to JSON if extension not recognized
            self._save_json(project_model, file_path.with_suffix('.json'))
            self.logger.info(f"Project saved as JSON to {file_path.with_suffix('.json')}")
            
    def load_project(self, file_path: str):
        """
        Load project from file.
        
        Args:
            file_path: Path to the project file
            
        Returns:
            Loaded project model
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pfp' or extension == '.json':
            return self._load_json(file_path)
        elif extension == '.pickle':
            return self._load_pickle(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
            
    def _save_pfp(self, project_model, file_path: Path):
        """Save project as PFP (Panel Flutter Project) file - JSON format."""
        self._save_json(project_model, file_path)
        
    def _save_json(self, project_model, file_path: Path):
        """Save project as JSON file."""
        try:
            project_data = project_model.to_dict()
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving JSON project: {str(e)}")
            raise
            
    def _save_pickle(self, project_model, file_path: Path):
        """Save project as pickle file."""
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'wb') as f:
                pickle.dump(project_model, f)
                
        except Exception as e:
            self.logger.error(f"Error saving pickle project: {str(e)}")
            raise
            
    def _load_json(self, file_path: Path):
        """Load project from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
                
            # Create new project model and load data
            from gui.models.project_model import ProjectModel
            project_model = ProjectModel()
            project_model.from_dict(project_data)
            
            return project_model
            
        except Exception as e:
            self.logger.error(f"Error loading JSON project: {str(e)}")
            raise
            
    def _load_pickle(self, file_path: Path):
        """Load project from pickle file."""
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
                
        except Exception as e:
            self.logger.error(f"Error loading pickle project: {str(e)}")
            raise
            
    def export_to_nastran_bdf(self, project_model, file_path: str):
        """
        Export project data to NASTRAN BDF format.
        
        Args:
            project_model: The project model instance
            file_path: Path where to save the BDF file
        """
        try:
            from nastran.aero.analysis.panel_flutter import PanelFlutterPistonAnalysisModel
            from nastran.aero.superpanels import SuperAeroPanel5
            
            # Create analysis model
            analysis_model = PanelFlutterPistonAnalysisModel()
            
            # Get project data
            geometry = project_model.get_geometry()
            materials = project_model.get_materials()
            boundary_conditions = project_model.get_boundary_conditions()
            analysis_params = project_model.get_analysis_parameters()
            
            # Set up global parameters
            analysis_model.set_global_case_from_dict({
                'machs': analysis_params.get('mach_numbers', [0.8]),
                'alphas': analysis_params.get('angles_of_attack', [0.0]),
                'densities_ratio': analysis_params.get('density_ratios', [1.0]),
                'velocities': analysis_params.get('velocities', [100, 200, 300]),
                'method': analysis_params.get('method', 'PK'),
                'n_modes': analysis_params.get('num_modes', 10),
                'frequency_limits': analysis_params.get('frequency_range', [0.1, 100.0]),
                'ref_chord': geometry.get('dimensions', {}).get('chord', 1.0),
                'ref_rho': analysis_params.get('reference_density', 1.225),
                'reduced_frequencies': analysis_params.get('reduced_frequencies', [0.1, 0.5, 1.0, 2.0])
            })
            
            # Create superpanel from geometry
            corner_points = geometry.get('corner_points', [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
            mesh_density = geometry.get('mesh_density', {'n_chord': 10, 'n_span': 5})
            
            superpanel = SuperAeroPanel5(
                eid=1,
                p1=corner_points[0],
                p2=corner_points[1], 
                p3=corner_points[2],
                p4=corner_points[3],
                nchord=mesh_density['n_chord'],
                nspan=mesh_density['n_span'],
                theory=analysis_params.get('aero_theory', 'PISTON')
            )
            
            analysis_model.add_superpanel(superpanel)
            
            # Generate NASTRAN cards
            analysis_model.write_cards()
            
            # Export to BDF
            analysis_model.export_to_bdf(file_path)
            
            self.logger.info(f"BDF exported to {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error exporting BDF: {str(e)}")
            raise
            
    def import_from_nastran_bdf(self, file_path: str):
        """
        Import data from NASTRAN BDF file.
        
        Args:
            file_path: Path to the BDF file
            
        Returns:
            Dictionary with extracted data
        """
        try:
            from pyNastran.bdf.bdf import BDF
            
            # Read BDF file
            model = BDF(debug=False)
            model.read_bdf(file_path)
            
            # Extract relevant data
            extracted_data = {
                'geometry': self._extract_geometry_from_bdf(model),
                'materials': self._extract_materials_from_bdf(model),
                'boundary_conditions': self._extract_bc_from_bdf(model),
                'analysis_parameters': self._extract_analysis_params_from_bdf(model)
            }
            
            self.logger.info(f"BDF imported from {file_path}")
            return extracted_data
            
        except Exception as e:
            self.logger.error(f"Error importing BDF: {str(e)}")
            raise
            
    def _extract_geometry_from_bdf(self, model) -> Dict:
        """Extract geometry data from BDF model."""
        geometry_data = {
            'panel_type': 'rectangular',
            'corner_points': [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
            'dimensions': {'length': 1.0, 'width': 1.0, 'chord': 1.0},
            'mesh_density': {'n_chord': 10, 'n_span': 5}
        }
        
        # Try to extract actual geometry from CAERO cards
        if model.caeros:
            caero_id = list(model.caeros.keys())[0]
            caero = model.caeros[caero_id]
            
            if hasattr(caero, 'p1') and hasattr(caero, 'p4'):
                # Extract corner points from CAERO card
                geometry_data['corner_points'] = [
                    caero.p1.tolist() if hasattr(caero.p1, 'tolist') else caero.p1,
                    [caero.p1[0] + caero.x12, caero.p1[1], caero.p1[2]],
                    caero.p4.tolist() if hasattr(caero.p4, 'tolist') else caero.p4,
                    [caero.p4[0] + caero.x43, caero.p4[1], caero.p4[2]]
                ]
                
                # Extract mesh density
                if hasattr(caero, 'nspan') and hasattr(caero, 'nchord'):
                    geometry_data['mesh_density'] = {
                        'n_chord': caero.nchord if hasattr(caero, 'nchord') else 10,
                        'n_span': caero.nspan
                    }
                    
        return geometry_data
        
    def _extract_materials_from_bdf(self, model) -> Dict:
        """Extract material data from BDF model."""
        materials_data = {
            'material_type': 'isotropic',
            'name': 'Imported Material',
            'density': 2700.0,
            'youngs_modulus': 70e9,
            'poissons_ratio': 0.33,
            'thickness': 0.002
        }
        
        # Try to extract actual material properties
        if model.materials:
            mat_id = list(model.materials.keys())[0]
            material = model.materials[mat_id]
            
            if hasattr(material, 'E') and hasattr(material, 'nu'):
                materials_data.update({
                    'youngs_modulus': material.E,
                    'poissons_ratio': material.nu,
                    'density': getattr(material, 'rho', 2700.0)
                })
                
        return materials_data
        
    def _extract_bc_from_bdf(self, model) -> Dict:
        """Extract boundary conditions from BDF model."""
        bc_data = {
            'edge_constraints': {
                'leading': 'clamped',
                'trailing': 'free',
                'left': 'simply_supported',
                'right': 'simply_supported'
            },
            'applied_loads': [],
            'temperature_conditions': {}
        }
        
        # Could extract SPC cards and other boundary condition information
        return bc_data
        
    def _extract_analysis_params_from_bdf(self, model) -> Dict:
        """Extract analysis parameters from BDF model."""
        analysis_data = {
            'analysis_type': 'flutter',
            'aero_theory': 'piston',
            'mach_numbers': [0.8],
            'angles_of_attack': [0.0],
            'density_ratios': [1.0],
            'velocities': [100, 200, 300],
            'reduced_frequencies': [0.1, 0.5, 1.0, 2.0],
            'frequency_range': [0.1, 100.0],
            'num_modes': 10,
            'method': 'PK'
        }
        
        # Try to extract actual parameters from FLUTTER, FLFACT cards
        if model.flutters:
            flutter_id = list(model.flutters.keys())[0]
            flutter_card = model.flutters[flutter_id]
            
            analysis_data['method'] = flutter_card.method
            
            # Extract FLFACT data if available
            if hasattr(flutter_card, 'density') and flutter_card.density in model.flfacts:
                density_flfact = model.flfacts[flutter_card.density]
                analysis_data['density_ratios'] = density_flfact.factors
                
            if hasattr(flutter_card, 'mach') and flutter_card.mach in model.flfacts:
                mach_flfact = model.flfacts[flutter_card.mach]
                analysis_data['mach_numbers'] = mach_flfact.factors
                
            if hasattr(flutter_card, 'reduced_freq_velocity') and flutter_card.reduced_freq_velocity in model.flfacts:
                vel_flfact = model.flfacts[flutter_card.reduced_freq_velocity]
                analysis_data['velocities'] = vel_flfact.factors
                
        return analysis_data
        
    def create_backup(self, project_model, backup_dir: str = "backups"):
        """Create a backup of the current project."""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            # Generate backup filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = project_model.project_info.get('name', 'untitled').replace(' ', '_')
            backup_file = backup_path / f"{project_name}_backup_{timestamp}.pfp"
            
            self.save_project(project_model, str(backup_file))
            self.logger.info(f"Backup created: {backup_file}")
            
            return str(backup_file)
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {str(e)}")
            raise