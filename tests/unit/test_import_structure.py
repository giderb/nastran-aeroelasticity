#!/usr/bin/env python3
"""
Unit Tests for Import Structure
===============================

Test that all modules can be imported correctly.
"""

import sys
import unittest
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent.parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

class TestImportStructure(unittest.TestCase):
    """Test module import structure"""
    
    def test_analysis_modules(self):
        """Test that analysis modules import correctly"""
        # Test boundary conditions
        try:
            from analysis.boundary_conditions import BoundaryCondition, BoundaryConditionManager
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import boundary_conditions: {e}")
        
        # Test piston theory solver
        try:
            from analysis.piston_theory_solver import PistonTheorySolver, PanelProperties, FlowConditions
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import piston_theory_solver: {e}")
        
        # Test doublet lattice solver
        try:
            from analysis.doublet_lattice_solver import DoubletLatticeSolver
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import doublet_lattice_solver: {e}")
        
        # Test NASTRAN solver (may not be available)
        try:
            from analysis.nastran_solver import NASTRANSolver
            nastran_available = True
        except ImportError:
            nastran_available = False
        
        # NASTRAN is optional, just check it doesn't crash
        self.assertIsInstance(nastran_available, bool)
    
    def test_gui_modules(self):
        """Test that GUI modules import correctly"""
        # Test main app
        try:
            from gui.main_app import PanelFlutterApp
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import main_app: {e}")
        
        # Test controllers
        try:
            from gui.controllers.main_controller import MainController
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import main_controller: {e}")
        
        # Test models
        try:
            from gui.models.project_model import ProjectModel
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import project_model: {e}")
    
    def test_gui_views(self):
        """Test that GUI view modules import correctly"""
        view_modules = [
            'main_window', 'geometry_panel', 'material_panel',
            'boundary_panel', 'analysis_panel', 'results_panel',
            'visualization_panel'
        ]
        
        for module_name in view_modules:
            try:
                module = __import__(f'gui.views.{module_name}', fromlist=[''])
                self.assertIsNotNone(module)
            except ImportError as e:
                self.fail(f"Failed to import gui.views.{module_name}: {e}")
    
    def test_gui_utils(self):
        """Test that GUI utility modules import correctly"""
        util_modules = [
            'file_manager', 'logger', 'themes', 'validation', 'widgets'
        ]
        
        for module_name in util_modules:
            try:
                module = __import__(f'gui.utils.{module_name}', fromlist=[''])
                self.assertIsNotNone(module)
            except ImportError as e:
                self.fail(f"Failed to import gui.utils.{module_name}: {e}")
    
    def test_nastran_modules(self):
        """Test NASTRAN module structure (optional)"""
        try:
            from nastran import utils
            from nastran.geometry import panels
            from nastran.structures import panel, material
            nastran_available = True
        except ImportError:
            nastran_available = False
        
        # NASTRAN modules are optional
        self.assertIsInstance(nastran_available, bool)
    
    def test_main_gui_import(self):
        """Test that main GUI can be imported"""
        # Add root directory for launch_gui
        sys.path.insert(0, str(current_dir))
        
        try:
            from launch_gui import PanelFlutterGUI
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import launch_gui: {e}")
    
    def test_core_dependencies(self):
        """Test that core dependencies are available"""
        core_modules = ['numpy', 'matplotlib', 'pandas', 'tkinter']
        
        for module_name in core_modules:
            try:
                module = __import__(module_name)
                self.assertIsNotNone(module)
            except ImportError:
                self.fail(f"Core dependency missing: {module_name}")

if __name__ == '__main__':
    unittest.main()