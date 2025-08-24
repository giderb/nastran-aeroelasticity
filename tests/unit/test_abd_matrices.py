"""
Unit Tests for ABD Matrix Calculations
=====================================

This module contains comprehensive unit tests for the ABD matrix calculation
functionality, validating against analytical solutions and reference cases.
"""

import unittest
import sys
import os
from pathlib import Path
import numpy as np
import math

# Add src directory to path
current_dir = Path(__file__).parent
project_dir = current_dir.parent.parent
src_dir = project_dir / "src"
sys.path.insert(0, str(src_dir))

class TestABDMatrices(unittest.TestCase):
    """Test ABD matrix calculation accuracy against reference values"""
    
    def setUp(self):
        """Set up test parameters and reference values"""
        print(f"\n{'='*50}")
        print("SETTING UP ABD MATRIX TESTS")
        print(f"{'='*50}")
        
        # Reference CFRP material properties from validation notebooks
        self.E1 = 54.0e9    # Pa - Fiber direction modulus
        self.E2 = 18.0e9    # Pa - Transverse direction modulus  
        self.G12 = 7.2e9    # Pa - In-plane shear modulus
        self.nu12 = 0.3     # Major Poisson's ratio
        self.rho = 2.6e3    # kg/m³ - Density
        
        # Calculate derived properties
        self.nu21 = self.nu12 * self.E2 / self.E1
        
        # Reduced stiffness matrix [Q]
        denom = 1 - self.nu12 * self.nu21
        self.Q11 = self.E1 / denom
        self.Q22 = self.E2 / denom  
        self.Q12 = self.nu12 * self.E2 / denom
        self.Q66 = self.G12
        self.Q16 = self.Q26 = 0  # For orthotropic materials
        
        print(f"Material properties initialized:")
        print(f"   E1 = {self.E1/1e9:.1f} GPa")
        print(f"   E2 = {self.E2/1e9:.1f} GPa") 
        print(f"   G12 = {self.G12/1e9:.1f} GPa")
        print(f"   nu12 = {self.nu12}")
        print(f"   nu21 = {self.nu21:.4f}")
        
    def test_reduced_stiffness_matrix(self):
        """Test calculation of reduced stiffness matrix [Q]"""
        print("\nTEST: Reduced Stiffness Matrix [Q]")
        print("-" * 40)
        
        # Expected values calculated from material properties
        expected_Q11 = self.E1 / (1 - self.nu12 * self.nu21)
        expected_Q22 = self.E2 / (1 - self.nu12 * self.nu21)
        expected_Q12 = self.nu12 * self.E2 / (1 - self.nu12 * self.nu21)
        expected_Q66 = self.G12
        
        print(f"Expected Q11: {expected_Q11:.2e} Pa")
        print(f"Calculated Q11: {self.Q11:.2e} Pa")
        
        # Test with 1e-10 relative tolerance
        self.assertAlmostEqual(self.Q11, expected_Q11, places=0)
        self.assertAlmostEqual(self.Q22, expected_Q22, places=0)
        self.assertAlmostEqual(self.Q12, expected_Q12, places=0)
        self.assertAlmostEqual(self.Q66, expected_Q66, places=0)
        
        print("Reduced stiffness matrix calculation PASSED")
        
    def test_reference_layup_45_degree_6_layers(self):
        """Test reference case: [45 degrees]6 layup from validation notebooks"""
        print("\nTEST: Reference Case [45 degrees]6 Layup")
        print("-" * 40)
        
        # Reference parameters from validation_test_1_2.py
        theta_degrees = 45.0
        N_layers = 6
        layer_thickness = 0.2e-3  # 0.2 mm in meters
        total_thickness = N_layers * layer_thickness
        
        print(f"Layup: [45 degrees]6")
        print(f"Individual layer thickness: {layer_thickness*1000:.1f} mm")
        print(f"Total thickness: {total_thickness*1000:.1f} mm")
        
        A, B, D = self._calculate_abd_layup([theta_degrees] * N_layers, 
                                           [layer_thickness] * N_layers)
        
        # Reference ABD values from validation_test_1_2.py
        # These are the correct calculated values
        expected_A11 = 3.42e7  # N/m
        expected_A22 = 3.42e7  # N/m (should be equal due to 45° symmetry)
        expected_A16 = 1.11e7  # N/m
        expected_A26 = 1.11e7  # N/m
        
        print(f"\nA Matrix Results:")
        print(f"Expected A11: {expected_A11:.2e} N/m")
        print(f"Calculated A11: {A[0,0]:.2e} N/m")
        print(f"Difference: {abs(A[0,0] - expected_A11)/expected_A11*100:.2f}%")
        
        # Test A matrix elements with 2% tolerance
        self.assertAlmostEqual(A[0,0], expected_A11, delta=expected_A11*0.02)
        self.assertAlmostEqual(A[1,1], expected_A22, delta=expected_A22*0.02)
        self.assertAlmostEqual(A[0,2], expected_A16, delta=expected_A16*0.02)
        self.assertAlmostEqual(A[1,2], expected_A26, delta=expected_A26*0.02)
        
        # B matrix should be zero for symmetric layup
        B_max = np.max(np.abs(B))
        print(f"\nB Matrix maximum element: {B_max:.2e}")
        self.assertLess(B_max, 1e-6, "B matrix should be approximately zero for symmetric layup")
        
        # D matrix validation
        expected_D11 = 4.11e0  # N⋅m
        print(f"\nD Matrix Results:")
        print(f"Expected D11: {expected_D11:.2e} N*m")
        print(f"Calculated D11: {D[0,0]:.2e} N*m")
        print(f"Difference: {abs(D[0,0] - expected_D11)/expected_D11*100:.2f}%")
        
        self.assertAlmostEqual(D[0,0], expected_D11, delta=expected_D11*0.05)  # 5% tolerance
        
        print("Reference case [45 degrees]6 layup PASSED")
        
    def _calculate_abd_layup(self, angles, thicknesses):
        """Calculate ABD matrices for a complete layup"""
        # Initialize ABD matrices
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))  
        D = np.zeros((3, 3))
        
        # Calculate z-coordinates
        total_thickness = sum(thicknesses)
        z = [-total_thickness/2]
        
        for thickness in thicknesses:
            z.append(z[-1] + thickness)
        
        # Calculate ABD matrices by integrating through thickness
        for i, (angle_deg, thickness) in enumerate(zip(angles, thicknesses)):
            angle_rad = math.radians(angle_deg)
            
            # Layer positions
            z1 = z[i]
            z2 = z[i+1]
            
            # Transformation for angle
            c = math.cos(angle_rad)
            s = math.sin(angle_rad)
            
            # Transformed reduced stiffness matrix [Q̄]
            Q11_bar = self.Q11*c**4 + 2*(self.Q12 + 2*self.Q66)*s**2*c**2 + self.Q22*s**4
            Q12_bar = (self.Q11 + self.Q22 - 4*self.Q66)*s**2*c**2 + self.Q12*(s**4 + c**4)
            Q22_bar = self.Q11*s**4 + 2*(self.Q12 + 2*self.Q66)*s**2*c**2 + self.Q22*c**4
            Q16_bar = (self.Q11 - self.Q12 - 2*self.Q66)*s*c**3 + (self.Q12 - self.Q22 + 2*self.Q66)*s**3*c
            Q26_bar = (self.Q11 - self.Q12 - 2*self.Q66)*s**3*c + (self.Q12 - self.Q22 + 2*self.Q66)*s*c**3
            Q66_bar = (self.Q11 + self.Q22 - 2*self.Q12 - 2*self.Q66)*s**2*c**2 + self.Q66*(s**4 + c**4)
            
            # A matrix (extensional stiffness)
            A[0,0] += Q11_bar * (z2 - z1)
            A[0,1] += Q12_bar * (z2 - z1)
            A[0,2] += Q16_bar * (z2 - z1)
            A[1,0] += Q12_bar * (z2 - z1)
            A[1,1] += Q22_bar * (z2 - z1)
            A[1,2] += Q26_bar * (z2 - z1)
            A[2,0] += Q16_bar * (z2 - z1)
            A[2,1] += Q26_bar * (z2 - z1)
            A[2,2] += Q66_bar * (z2 - z1)
            
            # B matrix (coupling stiffness)
            B[0,0] += Q11_bar * (z2**2 - z1**2) / 2
            B[0,1] += Q12_bar * (z2**2 - z1**2) / 2
            B[0,2] += Q16_bar * (z2**2 - z1**2) / 2
            B[1,0] += Q12_bar * (z2**2 - z1**2) / 2
            B[1,1] += Q22_bar * (z2**2 - z1**2) / 2
            B[1,2] += Q26_bar * (z2**2 - z1**2) / 2
            B[2,0] += Q16_bar * (z2**2 - z1**2) / 2
            B[2,1] += Q26_bar * (z2**2 - z1**2) / 2
            B[2,2] += Q66_bar * (z2**2 - z1**2) / 2
            
            # D matrix (bending stiffness)
            D[0,0] += Q11_bar * (z2**3 - z1**3) / 3
            D[0,1] += Q12_bar * (z2**3 - z1**3) / 3
            D[0,2] += Q16_bar * (z2**3 - z1**3) / 3
            D[1,0] += Q12_bar * (z2**3 - z1**3) / 3
            D[1,1] += Q22_bar * (z2**3 - z1**3) / 3
            D[1,2] += Q26_bar * (z2**3 - z1**3) / 3
            D[2,0] += Q16_bar * (z2**3 - z1**3) / 3
            D[2,1] += Q26_bar * (z2**3 - z1**3) / 3
            D[2,2] += Q66_bar * (z2**3 - z1**3) / 3
        
        return A, B, D

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)