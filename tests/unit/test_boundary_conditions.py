#!/usr/bin/env python3
"""
Unit Tests for Boundary Conditions
==================================

Comprehensive tests for all boundary condition functionality.
"""

import sys
import unittest
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent.parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

class TestBoundaryConditions(unittest.TestCase):
    """Test boundary conditions functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        from analysis.boundary_conditions import BoundaryCondition, BoundaryConditionManager
        self.bc_manager = BoundaryConditionManager()
        self.BoundaryCondition = BoundaryCondition
    
    def test_boundary_condition_definitions(self):
        """Test that all boundary conditions are properly defined"""
        expected_bcs = [
            "SSSS", "CCCC", "CFFF", "CSSS", "CCSS", "CFCF", 
            "SSSF", "CCCF", "SFSS", "CFCC", "FFFF"
        ]
        
        all_bcs = self.bc_manager.get_all_boundary_conditions()
        available_bcs = [bc.value for bc in all_bcs.keys()]
        
        for expected_bc in expected_bcs:
            self.assertIn(expected_bc, available_bcs, f"Missing boundary condition: {expected_bc}")
    
    def test_boundary_condition_properties(self):
        """Test that boundary condition properties are complete"""
        for bc_type, bc_props in self.bc_manager.get_all_boundary_conditions().items():
            # Check required properties exist
            self.assertTrue(hasattr(bc_props, 'name'))
            self.assertTrue(hasattr(bc_props, 'description'))
            self.assertTrue(hasattr(bc_props, 'flutter_tendency'))
            self.assertTrue(hasattr(bc_props, 'structural_stiffness'))
            
            # Check property values are reasonable
            self.assertIsInstance(bc_props.structural_stiffness, (int, float))
            self.assertGreaterEqual(bc_props.structural_stiffness, 0.0)
            self.assertLessEqual(bc_props.structural_stiffness, 1.0)
            
            self.assertIn(bc_props.flutter_tendency, ['low', 'medium', 'high', 'medium-high'])
    
    def test_edge_constraints(self):
        """Test edge constraint extraction"""
        # Test SSSS - all simply supported
        ssss_constraints = self.bc_manager.get_edge_constraints(self.BoundaryCondition.SSSS)
        expected_pattern = "SSSS"
        actual_pattern = ''.join([c.value for c in ssss_constraints.values()])
        self.assertEqual(actual_pattern, expected_pattern)
        
        # Test CFFF - cantilever
        cfff_constraints = self.bc_manager.get_edge_constraints(self.BoundaryCondition.CFFF)
        expected_pattern = "CFFF"
        actual_pattern = ''.join([c.value for c in cfff_constraints.values()])
        self.assertEqual(actual_pattern, expected_pattern)
    
    def test_stiffness_matrix_factors(self):
        """Test stiffness matrix factors"""
        # Test that all boundary conditions have stiffness factors
        for bc_type in self.BoundaryCondition:
            factors = self.bc_manager.get_stiffness_matrix_factors(bc_type)
            
            # Check required keys exist
            self.assertIn('kxx', factors)
            self.assertIn('kyy', factors)
            self.assertIn('kxy', factors)
            
            # Check values are positive
            self.assertGreater(factors['kxx'], 0)
            self.assertGreater(factors['kyy'], 0) 
            self.assertGreater(factors['kxy'], 0)
    
    def test_natural_frequency_factors(self):
        """Test natural frequency factors"""
        # Test basic mode (1,1) for all boundary conditions
        for bc_type in self.BoundaryCondition:
            freq_factor = self.bc_manager.get_natural_frequency_factors(bc_type, (1, 1))
            self.assertIsInstance(freq_factor, (int, float))
            self.assertGreater(freq_factor, 0)
    
    def test_boundary_condition_validation(self):
        """Test boundary condition validation"""
        # Test valid boundary condition
        valid, warnings = self.bc_manager.validate_boundary_condition(self.BoundaryCondition.SSSS)
        self.assertTrue(valid)
        
        # Test high flutter tendency warning
        valid, warnings = self.bc_manager.validate_boundary_condition(self.BoundaryCondition.CFFF)
        self.assertTrue(valid)
        self.assertTrue(any("High flutter tendency" in str(w) for w in warnings))
    
    def test_string_parsing(self):
        """Test boundary condition string parsing"""
        # Test valid string
        parsed = self.bc_manager.parse_boundary_condition("SSSS")
        self.assertEqual(parsed, self.BoundaryCondition.SSSS)
        
        # Test case insensitive
        parsed = self.bc_manager.parse_boundary_condition("ssss")
        self.assertEqual(parsed, self.BoundaryCondition.SSSS)
        
        # Test invalid string
        parsed = self.bc_manager.parse_boundary_condition("INVALID")
        self.assertIsNone(parsed)
    
    def test_recommendations(self):
        """Test boundary condition recommendations"""
        # Test general recommendation
        rec = self.bc_manager.recommend_boundary_condition("general")
        self.assertEqual(rec, self.BoundaryCondition.SSSS)
        
        # Test conservative recommendation  
        rec = self.bc_manager.recommend_boundary_condition("conservative")
        self.assertEqual(rec, self.BoundaryCondition.CCCC)
        
        # Test critical recommendation
        rec = self.bc_manager.recommend_boundary_condition("critical")
        self.assertEqual(rec, self.BoundaryCondition.CFFF)

if __name__ == '__main__':
    unittest.main()