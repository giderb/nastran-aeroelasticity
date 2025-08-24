#!/usr/bin/env python3
"""
Integration Tests for Multi-Solver Framework
===========================================

Test the integration between different flutter analysis solvers.
"""

import sys
import unittest
from pathlib import Path
import numpy as np

# Add src directory to path
current_dir = Path(__file__).parent.parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

class TestMultiSolver(unittest.TestCase):
    """Test multi-solver framework integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        from analysis.piston_theory_solver import PistonTheorySolver, PanelProperties, FlowConditions
        from analysis.doublet_lattice_solver import DoubletLatticeSolver
        from analysis.boundary_conditions import BoundaryCondition
        
        # Standard test panel
        self.panel = PanelProperties(
            length=0.3,
            width=0.2, 
            thickness=0.001,
            youngs_modulus=70e9,
            poissons_ratio=0.33,
            density=2700,
            boundary_conditions=BoundaryCondition.SSSS
        )
        
        # Standard test flow conditions
        self.flow = FlowConditions(mach_number=1.1, altitude=8000)
        
        # Initialize solvers
        self.piston_solver = PistonTheorySolver()
        self.dlm_solver = DoubletLatticeSolver()
    
    def test_piston_theory_solver(self):
        """Test piston theory solver functionality"""
        results = self.piston_solver.analyze_flutter(self.panel, self.flow, (80, 200), 10)
        
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        
        # Check result structure
        for result in results[:3]:  # Check first few results
            self.assertIsNotNone(result.flutter_speed)
            self.assertIsNotNone(result.flutter_frequency)
            self.assertIsNotNone(result.flutter_mode)
            self.assertGreater(result.flutter_speed, 0)
            self.assertGreater(result.flutter_frequency, 0)
    
    def test_doublet_lattice_solver(self):
        """Test doublet lattice method solver"""
        results = self.dlm_solver.analyze_flutter(self.panel, self.flow, (80, 200), 10)
        
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        
        # Check result structure
        for result in results[:3]:
            self.assertIsNotNone(result.flutter_speed)
            self.assertIsNotNone(result.flutter_frequency)
            self.assertIsNotNone(result.flutter_mode)
            self.assertGreater(result.flutter_speed, 0)
            self.assertGreater(result.flutter_frequency, 0)
    
    def test_solver_consistency(self):
        """Test that different solvers give reasonable relative results"""
        piston_results = self.piston_solver.analyze_flutter(self.panel, self.flow, (80, 200), 5)
        dlm_results = self.dlm_solver.analyze_flutter(self.panel, self.flow, (80, 200), 5)
        
        self.assertGreater(len(piston_results), 0)
        self.assertGreater(len(dlm_results), 0)
        
        # Get critical flutter speeds
        piston_critical = min(piston_results, key=lambda r: r.flutter_speed).flutter_speed
        dlm_critical = min(dlm_results, key=lambda r: r.flutter_speed).flutter_speed
        
        # Results should be within reasonable range (order of magnitude)
        ratio = max(piston_critical, dlm_critical) / min(piston_critical, dlm_critical)
        self.assertLess(ratio, 10.0, "Solver results differ by more than order of magnitude")
    
    def test_boundary_condition_effects(self):
        """Test that boundary conditions affect results appropriately"""
        from analysis.boundary_conditions import BoundaryCondition
        
        # Test different boundary conditions
        bc_results = {}
        test_bcs = [BoundaryCondition.SSSS, BoundaryCondition.CCCC, BoundaryCondition.CFFF]
        
        for bc in test_bcs:
            panel_bc = PanelProperties(
                length=0.3, width=0.2, thickness=0.001,
                youngs_modulus=70e9, poissons_ratio=0.33, density=2700,
                boundary_conditions=bc
            )
            
            results = self.piston_solver.analyze_flutter(panel_bc, self.flow, (80, 200), 5)
            if results:
                critical_speed = min(results, key=lambda r: r.flutter_speed).flutter_speed
                bc_results[bc.value] = critical_speed
        
        # Check that we got results for different boundary conditions
        self.assertGreater(len(bc_results), 1)
        
        # CCCC (clamped) should generally have higher flutter speed than CFFF (cantilever)
        if 'CCCC' in bc_results and 'CFFF' in bc_results:
            self.assertGreater(bc_results['CCCC'], bc_results['CFFF'] * 0.8,
                              "Clamped BC should have higher flutter speed than cantilever")

if __name__ == '__main__':
    unittest.main()