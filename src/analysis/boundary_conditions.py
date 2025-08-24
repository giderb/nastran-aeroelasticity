"""
Comprehensive Boundary Conditions for Flutter Analysis
======================================================

Defines all common boundary condition combinations used in panel flutter analysis
with their theoretical basis, implementation details, and flutter characteristics.
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import logging

class EdgeConstraint(Enum):
    """Individual edge constraint types"""
    FREE = "F"         # Free edge (no constraint)
    SIMPLY_SUPPORTED = "S"  # Simply supported (w=0, moments=0)
    CLAMPED = "C"      # Clamped (w=0, ∂w/∂n=0)
    ELASTIC = "E"      # Elastic support (spring-supported)

class BoundaryCondition(Enum):
    """Standard boundary condition combinations for rectangular panels"""
    # Format: Leading-Trailing-Left-Right edges
    SSSS = "SSSS"  # Simply supported all edges (most common)
    CCCC = "CCCC"  # Clamped all edges (stiffest)
    CFFF = "CFFF"  # Clamped leading, free elsewhere (cantilever)
    CSSS = "CSSS"  # Clamped leading, simply supported elsewhere
    CCSS = "CCSS"  # Clamped leading/trailing, simply supported sides
    CSCS = "CSCS"  # Clamped leading/trailing, simply supported sides (alt)
    CFCS = "CFCS"  # Clamped leading/trailing, free/simply supported sides
    CFCF = "CFCF"  # Clamped leading/trailing, free sides
    SSSF = "SSSF"  # Simply supported with free trailing edge
    CCCF = "CCCF"  # Clamped with free trailing edge
    SFSS = "SFSS"  # Simply supported leading/sides, free trailing
    CFCC = "CFCC"  # Clamped leading/sides, free trailing
    FFFF = "FFFF"  # Free all edges (theoretical only)
    FSSS = "FSSS"  # Free leading, simply supported elsewhere
    FCCC = "FCCC"  # Free leading, clamped elsewhere
    SCCC = "SCCC"  # Simply supported leading, clamped elsewhere
    SFFF = "SFFF"  # Simply supported leading, free elsewhere

@dataclass
class BoundaryConditionProperties:
    """Properties and characteristics of boundary condition"""
    name: str
    description: str
    leading_edge: EdgeConstraint
    trailing_edge: EdgeConstraint
    left_edge: EdgeConstraint
    right_edge: EdgeConstraint
    
    # Flutter characteristics
    flutter_tendency: str  # "low", "medium", "high"
    typical_applications: List[str]
    structural_stiffness: float  # Relative stiffness factor (0-1)
    
    # Analysis considerations
    convergence_difficulty: str  # "easy", "medium", "difficult"
    mode_shapes: List[str]  # Typical mode shapes
    special_notes: str

class BoundaryConditionManager:
    """Manages boundary conditions and their properties"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize_boundary_conditions()
    
    def _initialize_boundary_conditions(self):
        """Initialize all supported boundary conditions with their properties"""
        
        self.boundary_conditions = {
            BoundaryCondition.SSSS: BoundaryConditionProperties(
                name="Simply Supported All Edges",
                description="All edges simply supported - most common for flutter analysis",
                leading_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                trailing_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                left_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                right_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                flutter_tendency="medium",
                typical_applications=["Wing panels", "Control surfaces", "General analysis"],
                structural_stiffness=0.5,
                convergence_difficulty="easy",
                mode_shapes=["(1,1)", "(1,2)", "(2,1)", "(2,2)"],
                special_notes="Baseline condition - good convergence, well-studied"
            ),
            
            BoundaryCondition.CCCC: BoundaryConditionProperties(
                name="Clamped All Edges",
                description="All edges clamped - highest stiffness configuration",
                leading_edge=EdgeConstraint.CLAMPED,
                trailing_edge=EdgeConstraint.CLAMPED,
                left_edge=EdgeConstraint.CLAMPED,
                right_edge=EdgeConstraint.CLAMPED,
                flutter_tendency="low",
                typical_applications=["Thick panels", "Highly constrained structures", "Conservative analysis"],
                structural_stiffness=1.0,
                convergence_difficulty="easy",
                mode_shapes=["(1,1)", "(1,2)", "(2,1)"],
                special_notes="Highest flutter speeds - most conservative estimate"
            ),
            
            BoundaryCondition.CFFF: BoundaryConditionProperties(
                name="Cantilever Configuration",
                description="Clamped leading edge, free elsewhere - cantilever beam behavior",
                leading_edge=EdgeConstraint.CLAMPED,
                trailing_edge=EdgeConstraint.FREE,
                left_edge=EdgeConstraint.FREE,
                right_edge=EdgeConstraint.FREE,
                flutter_tendency="high",
                typical_applications=["Cantilever panels", "Flaps", "Tabs"],
                structural_stiffness=0.2,
                convergence_difficulty="difficult",
                mode_shapes=["(1,0)", "(2,0)", "(3,0)", "(0,1)"],
                special_notes="Lowest flutter speeds - most critical condition"
            ),
            
            BoundaryCondition.CSSS: BoundaryConditionProperties(
                name="Clamped Leading Edge",
                description="Clamped leading edge, simply supported elsewhere",
                leading_edge=EdgeConstraint.CLAMPED,
                trailing_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                left_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                right_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                flutter_tendency="medium",
                typical_applications=["Wing root panels", "Attached panels", "Realistic constraints"],
                structural_stiffness=0.7,
                convergence_difficulty="easy",
                mode_shapes=["(1,1)", "(2,1)", "(1,2)"],
                special_notes="Good balance between realism and flutter criticality"
            ),
            
            BoundaryCondition.CCSS: BoundaryConditionProperties(
                name="Clamped Chordwise Edges",
                description="Clamped leading/trailing edges, simply supported spanwise",
                leading_edge=EdgeConstraint.CLAMPED,
                trailing_edge=EdgeConstraint.CLAMPED,
                left_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                right_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                flutter_tendency="medium",
                typical_applications=["Wing panels with spars", "Control surfaces"],
                structural_stiffness=0.8,
                convergence_difficulty="easy",
                mode_shapes=["(1,1)", "(1,2)", "(1,3)"],
                special_notes="Dominant spanwise bending modes"
            ),
            
            BoundaryCondition.CFCF: BoundaryConditionProperties(
                name="Clamped Chordwise, Free Spanwise",
                description="Clamped leading/trailing, free left/right edges",
                leading_edge=EdgeConstraint.CLAMPED,
                trailing_edge=EdgeConstraint.CLAMPED,
                left_edge=EdgeConstraint.FREE,
                right_edge=EdgeConstraint.FREE,
                flutter_tendency="medium",
                typical_applications=["Strip theory validation", "Narrow panels"],
                structural_stiffness=0.6,
                convergence_difficulty="medium",
                mode_shapes=["(1,0)", "(2,0)", "(3,0)"],
                special_notes="Approaches infinite strip behavior"
            ),
            
            BoundaryCondition.SSSF: BoundaryConditionProperties(
                name="Simply Supported with Free Trailing Edge",
                description="Simply supported leading and sides, free trailing edge",
                leading_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                trailing_edge=EdgeConstraint.FREE,
                left_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                right_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                flutter_tendency="high",
                typical_applications=["Control surfaces", "Flaps with free trailing edge", "Rudders"],
                structural_stiffness=0.4,
                convergence_difficulty="medium",
                mode_shapes=["(1,1)", "(2,1)", "(1,2)", "(1,0)"],
                special_notes="Free trailing edge creates critical flutter condition"
            ),
            
            BoundaryCondition.CCCF: BoundaryConditionProperties(
                name="Clamped with Free Trailing Edge",
                description="Clamped leading and sides, free trailing edge",
                leading_edge=EdgeConstraint.CLAMPED,
                trailing_edge=EdgeConstraint.FREE,
                left_edge=EdgeConstraint.CLAMPED,
                right_edge=EdgeConstraint.CLAMPED,
                flutter_tendency="medium-high",
                typical_applications=["Control surfaces", "Tabs", "Flaps with fixed root"],
                structural_stiffness=0.6,
                convergence_difficulty="medium",
                mode_shapes=["(1,1)", "(2,1)", "(1,2)", "(3,1)"],
                special_notes="Combines high root stiffness with free trailing edge flexibility"
            ),
            
            BoundaryCondition.SFSS: BoundaryConditionProperties(
                name="Simply Supported with Free Trailing",
                description="Simply supported leading and sides, free trailing edge",
                leading_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                trailing_edge=EdgeConstraint.FREE,
                left_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                right_edge=EdgeConstraint.SIMPLY_SUPPORTED,
                flutter_tendency="high",
                typical_applications=["Control surfaces", "Flaps", "Wing trailing edge panels"],
                structural_stiffness=0.4,
                convergence_difficulty="medium",
                mode_shapes=["(1,1)", "(2,1)", "(1,2)", "(1,0)"],
                special_notes="Free trailing edge creates critical flutter condition similar to SSSF"
            ),
            
            BoundaryCondition.CFCC: BoundaryConditionProperties(
                name="Clamped with Free Trailing",
                description="Clamped leading and sides, free trailing edge",
                leading_edge=EdgeConstraint.CLAMPED,
                trailing_edge=EdgeConstraint.FREE,
                left_edge=EdgeConstraint.CLAMPED,
                right_edge=EdgeConstraint.CLAMPED,
                flutter_tendency="medium-high",
                typical_applications=["Control surface roots", "Fixed-root flaps", "Elevator tabs"],
                structural_stiffness=0.6,
                convergence_difficulty="medium",
                mode_shapes=["(1,1)", "(2,1)", "(1,2)", "(3,1)"],
                special_notes="High root constraint with free trailing edge flexibility"
            ),
            
            BoundaryCondition.FFFF: BoundaryConditionProperties(
                name="Free All Edges",
                description="All edges free - theoretical/validation case only",
                leading_edge=EdgeConstraint.FREE,
                trailing_edge=EdgeConstraint.FREE,
                left_edge=EdgeConstraint.FREE,
                right_edge=EdgeConstraint.FREE,
                flutter_tendency="high",
                typical_applications=["Theoretical studies", "Method validation"],
                structural_stiffness=0.1,
                convergence_difficulty="difficult",
                mode_shapes=["(0,0)", "(1,0)", "(0,1)", "(1,1)"],
                special_notes="Includes rigid body modes - numerical challenges"
            )
        }
    
    def get_boundary_condition(self, bc_type: BoundaryCondition) -> BoundaryConditionProperties:
        """Get properties for a specific boundary condition"""
        return self.boundary_conditions.get(bc_type)
    
    def get_all_boundary_conditions(self) -> Dict[BoundaryCondition, BoundaryConditionProperties]:
        """Get all supported boundary conditions"""
        return self.boundary_conditions
    
    def parse_boundary_condition(self, bc_string: str) -> Optional[BoundaryCondition]:
        """Parse boundary condition from string (e.g., 'SSSS', 'CFFF')"""
        try:
            return BoundaryCondition(bc_string.upper())
        except ValueError:
            self.logger.warning(f"Unknown boundary condition: {bc_string}")
            return None
    
    def get_edge_constraints(self, bc_type: BoundaryCondition) -> Dict[str, EdgeConstraint]:
        """Get individual edge constraints for a boundary condition"""
        bc_props = self.get_boundary_condition(bc_type)
        if not bc_props:
            return {}
        
        return {
            "leading": bc_props.leading_edge,
            "trailing": bc_props.trailing_edge,
            "left": bc_props.left_edge,
            "right": bc_props.right_edge
        }
    
    def get_stiffness_matrix_factors(self, bc_type: BoundaryCondition) -> Dict[str, float]:
        """Get stiffness matrix modification factors for boundary condition"""
        
        bc_props = self.get_boundary_condition(bc_type)
        if not bc_props:
            return {"kxx": 1.0, "kyy": 1.0, "kxy": 1.0}
        
        # Base factors based on boundary condition characteristics
        stiffness_factors = {
            BoundaryCondition.SSSS: {"kxx": 1.0, "kyy": 1.0, "kxy": 1.0},
            BoundaryCondition.CCCC: {"kxx": 2.56, "kyy": 2.56, "kxy": 1.8},
            BoundaryCondition.CFFF: {"kxx": 0.25, "kyy": 0.1, "kxy": 0.2},
            BoundaryCondition.CSSS: {"kxx": 1.8, "kyy": 1.2, "kxy": 1.1},
            BoundaryCondition.CCSS: {"kxx": 2.0, "kyy": 1.5, "kxy": 1.3},
            BoundaryCondition.CFCF: {"kxx": 1.5, "kyy": 0.8, "kxy": 0.9},
            BoundaryCondition.SSSF: {"kxx": 0.7, "kyy": 1.0, "kxy": 0.8},  # Reduced chordwise stiffness
            BoundaryCondition.CCCF: {"kxx": 1.6, "kyy": 2.2, "kxy": 1.4},  # High spanwise, reduced chordwise
            BoundaryCondition.SFSS: {"kxx": 0.7, "kyy": 1.0, "kxy": 0.8},  # Similar to SSSF - reduced chordwise stiffness
            BoundaryCondition.CFCC: {"kxx": 1.6, "kyy": 2.2, "kxy": 1.4},  # Similar to CCCF - high spanwise, reduced chordwise
            BoundaryCondition.FFFF: {"kxx": 0.05, "kyy": 0.05, "kxy": 0.05}
        }
        
        return stiffness_factors.get(bc_type, {"kxx": 1.0, "kyy": 1.0, "kxy": 1.0})
    
    def get_natural_frequency_factors(self, bc_type: BoundaryCondition, 
                                    mode: Tuple[int, int] = (1, 1)) -> float:
        """Get natural frequency factors for different boundary conditions and modes"""
        
        m, n = mode
        
        # Natural frequency factors relative to SSSS condition
        # Based on classical plate theory solutions
        frequency_factors = {
            BoundaryCondition.SSSS: {
                (1, 1): 1.0,
                (1, 2): 2.25,
                (2, 1): 2.25,
                (2, 2): 4.0,
                (1, 3): 4.84,
                (3, 1): 4.84
            },
            BoundaryCondition.CCCC: {
                (1, 1): 1.596,
                (1, 2): 2.93,
                (2, 1): 2.93,
                (2, 2): 4.64,
                (1, 3): 5.78,
                (3, 1): 5.78
            },
            BoundaryCondition.CFFF: {
                (1, 0): 0.160,  # First bending mode
                (2, 0): 1.004,  # Second bending mode
                (3, 0): 2.790,  # Third bending mode
                (0, 1): 0.455,  # First torsion mode
                (1, 1): 0.582
            },
            BoundaryCondition.CSSS: {
                (1, 1): 1.248,
                (1, 2): 2.68,
                (2, 1): 2.68,
                (2, 2): 4.32
            },
            BoundaryCondition.CCSS: {
                (1, 1): 1.435,
                (1, 2): 2.87,
                (2, 1): 3.24,
                (2, 2): 4.58
            },
            BoundaryCondition.SSSF: {
                (1, 1): 0.895,  # Lower than SSSS due to free trailing edge
                (1, 2): 2.01,   # Reduced stiffness in chordwise direction
                (2, 1): 2.12,   # Spanwise modes less affected
                (2, 2): 3.65,   # Combined mode reduced
                (1, 0): 0.354   # Chordwise bending mode
            },
            BoundaryCondition.CCCF: {
                (1, 1): 1.127,  # Between CCCC and SSSF
                (1, 2): 2.45,   # Reduced from CCCC due to free trailing edge
                (2, 1): 2.89,   # Spanwise modes closer to CCCC
                (2, 2): 4.12,   # Combined mode
                (1, 0): 0.428   # Chordwise bending mode with clamped sides
            },
            BoundaryCondition.SFSS: {
                (1, 1): 0.895,  # Similar to SSSF due to free trailing edge
                (1, 2): 2.01,   # Reduced stiffness in chordwise direction
                (2, 1): 2.12,   # Spanwise modes less affected
                (2, 2): 3.65,   # Combined mode reduced
                (1, 0): 0.354   # Chordwise bending mode
            },
            BoundaryCondition.CFCC: {
                (1, 1): 1.127,  # Similar to CCCF - between CCCC and free trailing conditions
                (1, 2): 2.45,   # Reduced from CCCC due to free trailing edge
                (2, 1): 2.89,   # Spanwise modes closer to CCCC due to clamped sides
                (2, 2): 4.12,   # Combined mode
                (1, 0): 0.428   # Chordwise bending mode with clamped sides
            }
        }
        
        bc_factors = frequency_factors.get(bc_type, {})
        return bc_factors.get(mode, 1.0)
    
    def validate_boundary_condition(self, bc_type: BoundaryCondition) -> Tuple[bool, List[str]]:
        """Validate boundary condition and return warnings/notes"""
        
        warnings = []
        bc_props = self.get_boundary_condition(bc_type)
        
        if not bc_props:
            return False, ["Invalid boundary condition"]
        
        # Add warnings based on boundary condition characteristics
        if bc_props.flutter_tendency == "high":
            warnings.append("⚠️ High flutter tendency - expect low flutter speeds")
        
        if bc_props.convergence_difficulty == "difficult":
            warnings.append("⚠️ Convergence may be challenging - use fine analysis settings")
        
        if bc_type == BoundaryCondition.FFFF:
            warnings.append("⚠️ Free-free condition includes rigid body modes - use with caution")
        
        if bc_type == BoundaryCondition.CFFF:
            warnings.append("⚠️ Cantilever condition is most critical for flutter")
        
        if bc_props.special_notes:
            warnings.append(f"📝 {bc_props.special_notes}")
        
        return True, warnings
    
    def recommend_boundary_condition(self, analysis_type: str = "general") -> BoundaryCondition:
        """Recommend boundary condition based on analysis type"""
        
        recommendations = {
            "general": BoundaryCondition.SSSS,
            "conservative": BoundaryCondition.CCCC,
            "critical": BoundaryCondition.CFFF,
            "realistic": BoundaryCondition.CSSS,
            "wing_panel": BoundaryCondition.CSSS,
            "control_surface": BoundaryCondition.CCSS,
            "validation": BoundaryCondition.SSSS
        }
        
        return recommendations.get(analysis_type, BoundaryCondition.SSSS)

# Example usage and testing
if __name__ == "__main__":
    
    bc_manager = BoundaryConditionManager()
    
    print("BOUNDARY CONDITIONS FOR PANEL FLUTTER ANALYSIS")
    print("=" * 60)
    
    for bc_type, bc_props in bc_manager.get_all_boundary_conditions().items():
        print(f"\n{bc_type.value}: {bc_props.name}")
        print(f"  Description: {bc_props.description}")
        print(f"  Flutter Tendency: {bc_props.flutter_tendency}")
        print(f"  Structural Stiffness: {bc_props.structural_stiffness:.1f}")
        print(f"  Applications: {', '.join(bc_props.typical_applications[:2])}")
        
        # Validation
        valid, warnings = bc_manager.validate_boundary_condition(bc_type)
        if warnings:
            for warning in warnings[:2]:  # Show first 2 warnings
                print(f"    {warning}")
    
    print(f"\nRecommended for general analysis: {bc_manager.recommend_boundary_condition('general').value}")
    print(f"Recommended for critical analysis: {bc_manager.recommend_boundary_condition('critical').value}")