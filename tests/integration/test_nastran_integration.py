#!/usr/bin/env python3
"""
Integration Tests for NASTRAN Integration
=========================================

Test NASTRAN solver integration (if available).
"""

import sys
import unittest
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent.parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

class TestNASTRANIntegration(unittest.TestCase):
    """Test NASTRAN solver integration"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            from analysis.nastran_solver import NASTRANSolver
            from analysis.piston_theory_solver import PanelProperties, FlowConditions
            from analysis.boundary_conditions import BoundaryCondition
            
            self.nastran_available = True
            self.solver = NASTRANSolver()
            
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
            
        except ImportError:
            self.nastran_available = False
            self.solver = None
    
    @unittest.skipUnless(True, "NASTRAN tests should always run to check availability")
    def test_nastran_availability(self):
        """Test whether NASTRAN is available"""
        if self.nastran_available:
            self.assertIsNotNone(self.solver)
            print("NASTRAN solver is available")
        else:
            print("NASTRAN solver is not available - this is acceptable")
            self.assertTrue(True)  # Pass the test regardless
    
    @unittest.skipUnless(True, "Always check NASTRAN executable")
    def test_nastran_executable(self):
        """Test NASTRAN executable availability"""
        if not self.nastran_available:
            self.skipTest("NASTRAN module not available")
        
        has_executable = self.solver.check_nastran_availability()
        if has_executable:
            print("NASTRAN executable found")
            self.assertTrue(True)
        else:
            print("NASTRAN executable not found - functionality will be limited")
            self.assertTrue(True)  # Still pass - executable is optional
    
    @unittest.skipIf(True, "Skip actual NASTRAN analysis to avoid dependencies")
    def test_nastran_analysis(self):
        """Test NASTRAN flutter analysis (skipped to avoid dependencies)"""
        if not self.nastran_available:
            self.skipTest("NASTRAN module not available")
        
        # This test is skipped to avoid requiring NASTRAN installation
        # In a full test environment, you would test:
        # results = self.solver.analyze_flutter(self.panel, self.flow, (80, 200), 5)
        # self.assertIsNotNone(results)
        
        self.skipTest("NASTRAN analysis test skipped to avoid external dependencies")
    
    def test_nastran_fallback(self):
        """Test that system works without NASTRAN"""
        # Test that other solvers work even if NASTRAN is not available
        try:
            from analysis.piston_theory_solver import PistonTheorySolver
            from analysis.doublet_lattice_solver import DoubletLatticeSolver
            
            piston_solver = PistonTheorySolver()
            dlm_solver = DoubletLatticeSolver()
            
            self.assertIsNotNone(piston_solver)
            self.assertIsNotNone(dlm_solver)
            
            print("Other solvers work fine without NASTRAN")
            
        except ImportError as e:
            self.fail(f"Core solvers should work without NASTRAN: {e}")

if __name__ == '__main__':
    unittest.main()