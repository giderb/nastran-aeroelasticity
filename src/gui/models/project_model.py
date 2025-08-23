"""
Project Model for Panel Flutter Analysis GUI
==========================================

The project model holds all data and state for a panel flutter analysis project,
including geometry, materials, boundary conditions, analysis parameters, and results.
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class GeometryData:
    """Data class for panel geometry definition."""
    panel_type: str = "rectangular"
    corner_points: List[List[float]] = field(default_factory=lambda: [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    dimensions: Dict[str, float] = field(default_factory=lambda: {"length": 1.0, "width": 1.0, "chord": 1.0})
    mesh_density: Dict[str, int] = field(default_factory=lambda: {"n_chord": 10, "n_span": 5})
    coordinate_system: str = "cartesian"
    

@dataclass
class MaterialData:
    """Data class for material properties."""
    material_type: str = "isotropic"
    name: str = "Aluminum"
    density: float = 2700.0  # kg/m³
    youngs_modulus: float = 70e9  # Pa
    poissons_ratio: float = 0.33
    thickness: float = 0.002  # m
    
    # For composite materials
    composite_layers: List[Dict] = field(default_factory=list)
    

@dataclass
class BoundaryConditionData:
    """Data class for boundary conditions."""
    edge_constraints: Dict[str, str] = field(default_factory=lambda: {
        "leading": "clamped",
        "trailing": "free", 
        "left": "simply_supported",
        "right": "simply_supported"
    })
    applied_loads: List[Dict] = field(default_factory=list)
    temperature_conditions: Dict[str, float] = field(default_factory=dict)
    

@dataclass
class AnalysisParametersData:
    """Data class for analysis parameters."""
    analysis_type: str = "flutter"
    aero_theory: str = "piston"
    mach_numbers: List[float] = field(default_factory=lambda: [0.7, 0.8, 0.9, 1.0, 1.2])
    angles_of_attack: List[float] = field(default_factory=lambda: [0.0])
    density_ratios: List[float] = field(default_factory=lambda: [1.0])
    velocities: List[float] = field(default_factory=lambda: [50, 100, 150, 200, 250, 300])
    reduced_frequencies: List[float] = field(default_factory=lambda: [0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0])
    frequency_range: List[float] = field(default_factory=lambda: [0.1, 100.0])
    num_modes: int = 10
    method: str = "PK"
    convergence_tolerance: float = 1e-6
    max_iterations: int = 100
    reference_density: float = 1.225  # kg/m³
    

@dataclass
class ResultsData:
    """Data class for analysis results."""
    flutter_summary: Dict = field(default_factory=dict)
    mode_shapes: Dict = field(default_factory=dict)
    frequencies: Dict = field(default_factory=dict)
    dampings: Dict = field(default_factory=dict)
    stability_boundaries: Dict = field(default_factory=dict)
    convergence_history: Dict = field(default_factory=dict)
    

class ProjectModel:
    """
    Main project model implementing the Model pattern for MVC architecture.
    Manages all project data and provides methods for data manipulation.
    """
    
    def __init__(self):
        self.initialize_default_project()
        
    def initialize_default_project(self):
        """Initialize with default project data."""
        self.project_info = {
            "name": "Untitled Project",
            "description": "",
            "author": "",
            "created_date": datetime.now().isoformat(),
            "modified_date": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        self.geometry = GeometryData()
        self.materials = MaterialData()
        self.boundary_conditions = BoundaryConditionData()
        self.analysis_parameters = AnalysisParametersData()
        self.results = ResultsData()
        
        self._modified = False
        self._observers = []
        
    def new_project(self):
        """Create a new project."""
        self.initialize_default_project()
        self.notify_observers("project_new")
        
    def is_modified(self) -> bool:
        """Check if the project has unsaved changes."""
        return self._modified
        
    def set_modified(self, modified: bool = True):
        """Set the modified state of the project."""
        self._modified = modified
        if modified:
            self.project_info["modified_date"] = datetime.now().isoformat()
        self.notify_observers("project_modified" if modified else "project_saved")
        
    def add_observer(self, observer):
        """Add an observer for model changes."""
        self._observers.append(observer)
        
    def remove_observer(self, observer):
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
            
    def notify_observers(self, event_type: str, data: Any = None):
        """Notify all observers of a model change."""
        for observer in self._observers:
            if hasattr(observer, 'on_model_changed'):
                observer.on_model_changed(event_type, data)
                
    # Geometry methods
    def get_geometry(self) -> Dict:
        """Get geometry data as dictionary."""
        return asdict(self.geometry)
        
    def set_geometry(self, geometry_data: Dict):
        """Set geometry data from dictionary."""
        for key, value in geometry_data.items():
            if hasattr(self.geometry, key):
                setattr(self.geometry, key, value)
        self.set_modified(True)
        self.notify_observers("geometry_changed", geometry_data)
        
    def update_corner_points(self, points: List[List[float]]):
        """Update corner points of the panel."""
        if len(points) == 4:
            self.geometry.corner_points = points
            self.set_modified(True)
            self.notify_observers("geometry_changed", {"corner_points": points})
            
    def update_mesh_density(self, n_chord: int, n_span: int):
        """Update mesh density parameters."""
        self.geometry.mesh_density = {"n_chord": n_chord, "n_span": n_span}
        self.set_modified(True)
        self.notify_observers("geometry_changed", {"mesh_density": self.geometry.mesh_density})
        
    # Material methods
    def get_materials(self) -> Dict:
        """Get material data as dictionary."""
        return asdict(self.materials)
        
    def set_materials(self, materials_data: Dict):
        """Set material data from dictionary."""
        for key, value in materials_data.items():
            if hasattr(self.materials, key):
                setattr(self.materials, key, value)
        self.set_modified(True)
        self.notify_observers("materials_changed", materials_data)
        
    def update_material_properties(self, properties: Dict):
        """Update material properties."""
        for key, value in properties.items():
            if hasattr(self.materials, key):
                setattr(self.materials, key, value)
        self.set_modified(True)
        self.notify_observers("materials_changed", properties)
        
    # Boundary conditions methods
    def get_boundary_conditions(self) -> Dict:
        """Get boundary conditions as dictionary."""
        return asdict(self.boundary_conditions)
        
    def set_boundary_conditions(self, bc_data: Dict):
        """Set boundary conditions from dictionary."""
        for key, value in bc_data.items():
            if hasattr(self.boundary_conditions, key):
                setattr(self.boundary_conditions, key, value)
        self.set_modified(True)
        self.notify_observers("boundary_conditions_changed", bc_data)
        
    def update_edge_constraints(self, constraints: Dict[str, str]):
        """Update edge constraints."""
        self.boundary_conditions.edge_constraints.update(constraints)
        self.set_modified(True)
        self.notify_observers("boundary_conditions_changed", {"edge_constraints": constraints})
        
    # Analysis parameters methods
    def get_analysis_parameters(self) -> Dict:
        """Get analysis parameters as dictionary."""
        return asdict(self.analysis_parameters)
        
    def set_analysis_parameters(self, analysis_data: Dict):
        """Set analysis parameters from dictionary."""
        for key, value in analysis_data.items():
            if hasattr(self.analysis_parameters, key):
                setattr(self.analysis_parameters, key, value)
        self.set_modified(True)
        self.notify_observers("analysis_parameters_changed", analysis_data)
        
    def update_mach_numbers(self, mach_numbers: List[float]):
        """Update Mach number range."""
        self.analysis_parameters.mach_numbers = mach_numbers
        self.set_modified(True)
        self.notify_observers("analysis_parameters_changed", {"mach_numbers": mach_numbers})
        
    def update_velocity_range(self, velocities: List[float]):
        """Update velocity range."""
        self.analysis_parameters.velocities = velocities
        self.set_modified(True)
        self.notify_observers("analysis_parameters_changed", {"velocities": velocities})
        
    # Results methods
    def get_results(self) -> Dict:
        """Get results data as dictionary."""
        return asdict(self.results)
        
    def set_results(self, results_data: Dict):
        """Set results data from dictionary."""
        for key, value in results_data.items():
            if hasattr(self.results, key):
                setattr(self.results, key, value)
        self.notify_observers("results_changed", results_data)
        
    def has_results(self) -> bool:
        """Check if the project has analysis results."""
        return bool(self.results.flutter_summary)
        
    def get_flutter_speed(self) -> Optional[float]:
        """Get the flutter speed from results."""
        return self.results.flutter_summary.get('flutter_speed')
        
    def get_flutter_frequency(self) -> Optional[float]:
        """Get the flutter frequency from results."""
        return self.results.flutter_summary.get('flutter_frequency')
        
    # Data validation methods
    def validate_geometry(self) -> List[str]:
        """Validate geometry data and return list of errors."""
        errors = []
        
        if len(self.geometry.corner_points) != 4:
            errors.append("Geometry must have exactly 4 corner points")
            
        if self.geometry.mesh_density["n_chord"] < 1:
            errors.append("Number of chordwise elements must be at least 1")
            
        if self.geometry.mesh_density["n_span"] < 1:
            errors.append("Number of spanwise elements must be at least 1")
            
        return errors
        
    def validate_materials(self) -> List[str]:
        """Validate material data and return list of errors."""
        errors = []
        
        if self.materials.density <= 0:
            errors.append("Material density must be positive")
            
        if self.materials.youngs_modulus <= 0:
            errors.append("Young's modulus must be positive")
            
        if not (0 <= self.materials.poissons_ratio < 0.5):
            errors.append("Poisson's ratio must be between 0 and 0.5")
            
        if self.materials.thickness <= 0:
            errors.append("Material thickness must be positive")
            
        return errors
        
    def validate_analysis_parameters(self) -> List[str]:
        """Validate analysis parameters and return list of errors."""
        errors = []
        
        if not self.analysis_parameters.mach_numbers:
            errors.append("At least one Mach number must be specified")
            
        if not self.analysis_parameters.velocities:
            errors.append("At least one velocity must be specified")
            
        if self.analysis_parameters.num_modes < 1:
            errors.append("Number of modes must be at least 1")
            
        if len(self.analysis_parameters.frequency_range) != 2:
            errors.append("Frequency range must have exactly 2 values")
        elif self.analysis_parameters.frequency_range[0] >= self.analysis_parameters.frequency_range[1]:
            errors.append("Frequency range minimum must be less than maximum")
            
        return errors
        
    def validate_all(self) -> List[str]:
        """Validate all project data and return list of errors."""
        all_errors = []
        all_errors.extend(self.validate_geometry())
        all_errors.extend(self.validate_materials())
        all_errors.extend(self.validate_analysis_parameters())
        return all_errors
        
    # Import/Export methods
    def import_bdf(self, file_path: str):
        """Import data from a NASTRAN BDF file."""
        # This would parse a BDF file and extract relevant data
        # For now, just mark as modified
        self.set_modified(True)
        self.notify_observers("bdf_imported", file_path)
        
    def export_bdf(self, file_path: str):
        """Export data to a NASTRAN BDF file."""
        # This would generate a complete BDF file from current data
        # For now, just notify
        self.notify_observers("bdf_exported", file_path)
        
    def to_dict(self) -> Dict:
        """Convert entire project to dictionary for serialization."""
        return {
            "project_info": self.project_info,
            "geometry": asdict(self.geometry),
            "materials": asdict(self.materials),
            "boundary_conditions": asdict(self.boundary_conditions),
            "analysis_parameters": asdict(self.analysis_parameters),
            "results": asdict(self.results)
        }
        
    def from_dict(self, data: Dict):
        """Load project data from dictionary."""
        self.project_info = data.get("project_info", self.project_info)
        
        if "geometry" in data:
            self.geometry = GeometryData(**data["geometry"])
            
        if "materials" in data:
            self.materials = MaterialData(**data["materials"])
            
        if "boundary_conditions" in data:
            self.boundary_conditions = BoundaryConditionData(**data["boundary_conditions"])
            
        if "analysis_parameters" in data:
            self.analysis_parameters = AnalysisParametersData(**data["analysis_parameters"])
            
        if "results" in data:
            self.results = ResultsData(**data["results"])
            
        self._modified = False
        self.notify_observers("project_loaded")