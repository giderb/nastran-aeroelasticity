#!/usr/bin/env python3
"""
Integration Tests for GUI Functionality  
=======================================

Test core GUI functionality and user interactions.
"""

import sys
import unittest
from pathlib import Path
import tkinter as tk

# Add src directory to path
current_dir = Path(__file__).parent.parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(current_dir))

class TestGUIFunctionality(unittest.TestCase):
    """Test GUI functionality and integration"""
    
    def setUp(self):
        """Set up GUI test environment"""
        from launch_gui import PanelFlutterGUI
        
        # Create hidden GUI instance for testing
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = PanelFlutterGUI()
    
    def tearDown(self):
        """Clean up GUI test environment"""
        self.root.destroy()
    
    def test_gui_initialization(self):
        """Test that GUI initializes properly"""
        # Check main window exists
        self.assertIsNotNone(self.app.root)
        
        # Check notebook (tabs) exists
        self.assertTrue(hasattr(self.app, 'notebook'))
        
        # Check all tabs are created
        tab_count = self.app.notebook.index("end")
        self.assertEqual(tab_count, 4, "Should have 4 tabs")
        
        # Check tab titles have icons
        for i in range(tab_count):
            tab_text = self.app.notebook.tab(i, "text")
            has_icon = any(ord(char) > 127 for char in tab_text)
            self.assertTrue(has_icon, f"Tab {i+1} should have an icon: {tab_text}")
    
    def test_thickness_consolidation(self):
        """Test that thickness is only in materials section"""
        # Should have thickness_var
        self.assertTrue(hasattr(self.app, 'thickness_var'))
        
        # Should have default value
        thickness_default = self.app.thickness_var.get()
        self.assertEqual(thickness_default, "2.0")
        
        # Test thickness value changes
        test_values = ["1.0", "3.5", "0.8"]
        for test_val in test_values:
            self.app.thickness_var.set(test_val)
            retrieved_val = self.app.thickness_var.get()
            self.assertEqual(retrieved_val, test_val)
    
    def test_boundary_conditions_integration(self):
        """Test boundary conditions in GUI"""
        # Should have boundary conditions attribute
        self.assertTrue(hasattr(self.app, 'boundary_conditions'))
        
        # Should have boundary condition code extraction method
        self.assertTrue(hasattr(self.app, 'get_boundary_condition_code'))
        
        # Test boundary condition extraction
        bc_code = self.app.get_boundary_condition_code()
        self.assertIn(bc_code, ['SSSS', 'CCCC', 'CFFF', 'CSSS', 'CCSS', 'CFCF', 'SSSF', 'CCCF', 'SFSS', 'CFCC', 'FFFF'])
        
        # Test boundary condition selection changes
        test_selections = [
            "SSSS - Simply Supported All Edges",
            "CCCC - Clamped All Edges", 
            "CFFF - Cantilever Configuration"
        ]
        
        for selection in test_selections:
            self.app.boundary_conditions.set(selection)
            bc_code = self.app.get_boundary_condition_code()
            expected_code = selection.split(' - ')[0]
            self.assertEqual(bc_code, expected_code)
    
    def test_scrolling_setup(self):
        """Test that scrolling is properly set up"""
        # Check for canvas widgets and their mousewheel bindings
        canvases_found = 0
        bindings_found = 0
        
        def check_widget(widget):
            nonlocal canvases_found, bindings_found
            
            if isinstance(widget, tk.Canvas):
                canvases_found += 1
                bindings = widget.bind()
                
                # Check for mousewheel binding
                if any('MouseWheel' in str(binding) for binding in bindings):
                    bindings_found += 1
                    
            # Check children recursively
            try:
                for child in widget.winfo_children():
                    check_widget(child)
            except:
                pass
        
        # Check all tabs for scrollable canvases
        tab_count = self.app.notebook.index("end")
        for i in range(tab_count):
            self.app.notebook.select(i)
            tab_widget = self.app.notebook.nametowidget(self.app.notebook.tabs()[i])
            check_widget(tab_widget)
        
        # Should find scrollable canvases with proper bindings
        self.assertGreater(canvases_found, 0, "Should find scrollable canvases")
        self.assertGreater(bindings_found, 0, "Should find mousewheel bindings")
        
        # Should have helper method for scroll event filtering
        self.assertTrue(hasattr(self.app, '_widget_in_canvas'))
    
    def test_input_variables(self):
        """Test that all required input variables exist"""
        required_vars = [
            'length_var', 'width_var', 'thickness_var',
            'density_var', 'youngs_var', 'poisson_var',
            'mach_var', 'altitude_var', 'vmin_var', 'vmax_var',
            'boundary_conditions'
        ]
        
        for var_name in required_vars:
            self.assertTrue(hasattr(self.app, var_name), f"Missing variable: {var_name}")
            
            # Check that variables have reasonable default values
            if hasattr(getattr(self.app, var_name), 'get'):
                value = getattr(self.app, var_name).get()
                self.assertIsNotNone(value)
                self.assertNotEqual(value, "")
    
    def test_geometry_validation(self):
        """Test geometry validation functionality"""
        # Should have validate_geometry method
        self.assertTrue(hasattr(self.app, 'validate_geometry'))
        
        # Set valid geometry values
        self.app.length_var.set("500.0")
        self.app.width_var.set("300.0")
        
        # Validation should work without errors
        try:
            self.app.validate_geometry()
            validation_works = True
        except Exception:
            validation_works = False
        
        self.assertTrue(validation_works, "Geometry validation should work")

if __name__ == '__main__':
    unittest.main()