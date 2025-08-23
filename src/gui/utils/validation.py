"""
Input Validation for Panel Flutter Analysis GUI
==============================================

Provides validation functions for user inputs across the application.
"""

import re
import numpy as np
from typing import List, Any, Union


class InputValidator:
    """
    Comprehensive input validation for the panel flutter analysis application.
    """
    
    def __init__(self):
        self.errors = []
        
    def reset_errors(self):
        """Reset the error list."""
        self.errors = []
        
    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
        
    def get_errors(self) -> List[str]:
        """Get all error messages."""
        return self.errors.copy()
        
    def has_errors(self) -> bool:
        """Check if there are any validation errors."""
        return len(self.errors) > 0
        
    # Basic validation functions
    def validate_positive_number(self, value: Any, field_name: str = "Value") -> bool:
        """Validate that a value is a positive number."""
        try:
            num = float(value)
            if num <= 0:
                self.add_error(f"{field_name} must be positive")
                return False
            return True
        except (ValueError, TypeError):
            self.add_error(f"{field_name} must be a valid number")
            return False
            
    def validate_non_negative_number(self, value: Any, field_name: str = "Value") -> bool:
        """Validate that a value is a non-negative number."""
        try:
            num = float(value)
            if num < 0:
                self.add_error(f"{field_name} must be non-negative")
                return False
            return True
        except (ValueError, TypeError):
            self.add_error(f"{field_name} must be a valid number")
            return False
            
    def validate_integer(self, value: Any, field_name: str = "Value", min_val: int = None, max_val: int = None) -> bool:
        """Validate that a value is an integer within optional bounds."""
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                self.add_error(f"{field_name} must be at least {min_val}")
                return False
            if max_val is not None and num > max_val:
                self.add_error(f"{field_name} must be at most {max_val}")
                return False
            return True
        except (ValueError, TypeError):
            self.add_error(f"{field_name} must be a valid integer")
            return False
            
    def validate_range(self, value: Any, min_val: float, max_val: float, field_name: str = "Value") -> bool:
        """Validate that a value is within a specified range."""
        try:
            num = float(value)
            if not (min_val <= num <= max_val):
                self.add_error(f"{field_name} must be between {min_val} and {max_val}")
                return False
            return True
        except (ValueError, TypeError):
            self.add_error(f"{field_name} must be a valid number")
            return False
            
    def validate_list_of_numbers(self, values: List[Any], field_name: str = "Values") -> bool:
        """Validate that all values in a list are valid numbers."""
        if not values:
            self.add_error(f"{field_name} cannot be empty")
            return False
            
        valid = True
        for i, value in enumerate(values):
            try:
                float(value)
            except (ValueError, TypeError):
                self.add_error(f"{field_name}[{i}] must be a valid number")
                valid = False
                
        return valid
        
    # Geometry validation
    def validate_geometry(self, geometry_data: dict) -> bool:
        """Validate geometry parameters."""
        self.reset_errors()
        valid = True
        
        # Validate corner points
        corner_points = geometry_data.get('corner_points', [])
        if len(corner_points) != 4:
            self.add_error("Geometry must have exactly 4 corner points")
            valid = False
        else:
            for i, point in enumerate(corner_points):
                if len(point) != 3:
                    self.add_error(f"Corner point {i+1} must have x, y, z coordinates")
                    valid = False
                else:
                    for j, coord in enumerate(point):
                        try:
                            float(coord)
                        except (ValueError, TypeError):
                            coord_names = ['x', 'y', 'z']
                            self.add_error(f"Corner point {i+1} {coord_names[j]} coordinate must be a number")
                            valid = False
                            
        # Validate mesh density
        mesh_density = geometry_data.get('mesh_density', {})
        if not self.validate_integer(mesh_density.get('n_chord', 1), "Number of chordwise elements", min_val=1, max_val=100):
            valid = False
        if not self.validate_integer(mesh_density.get('n_span', 1), "Number of spanwise elements", min_val=1, max_val=100):
            valid = False
            
        # Validate dimensions
        dimensions = geometry_data.get('dimensions', {})
        for dim_name in ['length', 'width', 'chord']:
            if dim_name in dimensions:
                if not self.validate_positive_number(dimensions[dim_name], f"Geometry {dim_name}"):
                    valid = False
                    
        return valid
        
    # Material validation
    def validate_materials(self, materials_data: dict) -> bool:
        """Validate material properties."""
        self.reset_errors()
        valid = True
        
        # Density
        if not self.validate_positive_number(materials_data.get('density', 0), "Material density"):
            valid = False
            
        # Young's modulus
        if not self.validate_positive_number(materials_data.get('youngs_modulus', 0), "Young's modulus"):
            valid = False
            
        # Poisson's ratio
        poissons_ratio = materials_data.get('poissons_ratio', 0)
        if not self.validate_range(poissons_ratio, 0, 0.5, "Poisson's ratio"):
            valid = False
            
        # Thickness
        if not self.validate_positive_number(materials_data.get('thickness', 0), "Material thickness"):
            valid = False
            
        # Material name
        name = materials_data.get('name', '').strip()
        if not name:
            self.add_error("Material name cannot be empty")
            valid = False
            
        return valid
        
    # Boundary conditions validation
    def validate_boundary_conditions(self, bc_data: dict) -> bool:
        """Validate boundary conditions."""
        self.reset_errors()
        valid = True
        
        # Edge constraints
        edge_constraints = bc_data.get('edge_constraints', {})
        valid_constraints = ['free', 'simply_supported', 'clamped', 'elastic']
        
        for edge, constraint in edge_constraints.items():
            if constraint not in valid_constraints:
                self.add_error(f"Edge constraint '{constraint}' is not valid. Must be one of: {', '.join(valid_constraints)}")
                valid = False
                
        return valid
        
    # Analysis parameters validation
    def validate_analysis_parameters(self, analysis_data: dict) -> bool:
        """Validate analysis parameters."""
        self.reset_errors()
        valid = True
        
        # Mach numbers
        mach_numbers = analysis_data.get('mach_numbers', [])
        if not self.validate_list_of_numbers(mach_numbers, "Mach numbers"):
            valid = False
        else:
            for i, mach in enumerate(mach_numbers):
                if not self.validate_positive_number(mach, f"Mach number {i+1}"):
                    valid = False
                    
        # Velocities
        velocities = analysis_data.get('velocities', [])
        if not self.validate_list_of_numbers(velocities, "Velocities"):
            valid = False
        else:
            for i, vel in enumerate(velocities):
                if not self.validate_positive_number(vel, f"Velocity {i+1}"):
                    valid = False
                    
        # Density ratios
        density_ratios = analysis_data.get('density_ratios', [])
        if density_ratios and not self.validate_list_of_numbers(density_ratios, "Density ratios"):
            valid = False
        else:
            for i, ratio in enumerate(density_ratios):
                if not self.validate_positive_number(ratio, f"Density ratio {i+1}"):
                    valid = False
                    
        # Reduced frequencies
        reduced_frequencies = analysis_data.get('reduced_frequencies', [])
        if reduced_frequencies and not self.validate_list_of_numbers(reduced_frequencies, "Reduced frequencies"):
            valid = False
        else:
            for i, freq in enumerate(reduced_frequencies):
                if not self.validate_positive_number(freq, f"Reduced frequency {i+1}"):
                    valid = False
                    
        # Frequency range
        frequency_range = analysis_data.get('frequency_range', [])
        if len(frequency_range) != 2:
            self.add_error("Frequency range must have exactly 2 values (min and max)")
            valid = False
        elif not self.validate_list_of_numbers(frequency_range, "Frequency range"):
            valid = False
        elif frequency_range[0] >= frequency_range[1]:
            self.add_error("Frequency range minimum must be less than maximum")
            valid = False
            
        # Number of modes
        if not self.validate_integer(analysis_data.get('num_modes', 1), "Number of modes", min_val=1, max_val=50):
            valid = False
            
        # Method
        method = analysis_data.get('method', '')
        valid_methods = ['PK', 'K', 'KE', 'PKNL', 'PKS', 'PKNLS']
        if method not in valid_methods:
            self.add_error(f"Analysis method must be one of: {', '.join(valid_methods)}")
            valid = False
            
        # Aerodynamic theory
        aero_theory = analysis_data.get('aero_theory', '')
        valid_theories = ['PISTON', 'VANDYKE', 'VDSWEEP']
        if aero_theory not in valid_theories:
            self.add_error(f"Aerodynamic theory must be one of: {', '.join(valid_theories)}")
            valid = False
            
        return valid
        
    def validate_analysis_inputs(self, project_model) -> List[str]:
        """Validate all inputs required for analysis."""
        all_errors = []
        
        # Validate geometry
        if not self.validate_geometry(project_model.get_geometry()):
            all_errors.extend(self.get_errors())
            
        # Validate materials
        if not self.validate_materials(project_model.get_materials()):
            all_errors.extend(self.get_errors())
            
        # Validate boundary conditions
        if not self.validate_boundary_conditions(project_model.get_boundary_conditions()):
            all_errors.extend(self.get_errors())
            
        # Validate analysis parameters
        if not self.validate_analysis_parameters(project_model.get_analysis_parameters()):
            all_errors.extend(self.get_errors())
            
        return all_errors


# Standalone validation functions
def is_valid_float(value: str) -> bool:
    """Check if a string represents a valid float."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def is_positive_float(value: str) -> bool:
    """Check if a string represents a positive float."""
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


def is_valid_integer(value: str) -> bool:
    """Check if a string represents a valid integer."""
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_coordinate(coord_str: str) -> bool:
    """Check if a string represents a valid coordinate (x, y, z)."""
    try:
        coords = coord_str.strip().split(',')
        if len(coords) != 3:
            return False
        for coord in coords:
            float(coord.strip())
        return True
    except (ValueError, TypeError):
        return False