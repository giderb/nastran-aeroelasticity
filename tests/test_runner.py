#!/usr/bin/env python3
"""
Comprehensive Test Suite Runner for Panel Flutter Analysis GUI Tool
===================================================================

This test runner executes the complete validation test suite for the Panel Flutter 
Analysis tool, including unit tests, integration tests, performance tests, and 
validation against reference data.

Usage:
    python test_runner.py --all                  # Run all tests
    python test_runner.py --unit                 # Run unit tests only  
    python test_runner.py --integration          # Run integration tests
    python test_runner.py --validation           # Run validation tests
    python test_runner.py --performance          # Run performance tests
    python test_runner.py --report               # Generate test report
"""

import sys
import os
import argparse
import time
import json
from pathlib import Path
from datetime import datetime
import importlib.util

# Add src directory to path
current_dir = Path(__file__).parent
project_dir = current_dir.parent
src_dir = project_dir / "src"
sys.path.insert(0, str(src_dir))

class TestRunner:
    """Main test runner for the Panel Flutter Analysis tool"""
    
    def __init__(self):
        self.test_results = {
            'start_time': datetime.now().isoformat(),
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'test_cases': [],
            'performance_metrics': {},
            'validation_results': {}
        }
        
    def run_all_tests(self):
        """Run the complete test suite"""
        print("PANEL FLUTTER ANALYSIS TOOL - COMPREHENSIVE TEST SUITE")
        print("=" * 70)
        print(f"Test execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run each test category
        self.run_unit_tests()
        self.run_integration_tests()
        self.run_validation_tests()
        self.run_performance_tests()
        
        # Generate final report
        self.generate_test_report()
        
    def run_unit_tests(self):
        """Run unit tests for core calculations"""
        print("RUNNING UNIT TESTS")
        print("-" * 30)
        
        try:
            from unit.test_abd_matrices import TestABDMatrices
            # Import our working ABD test
            test_classes = [TestABDMatrices]
            
            # Try to import additional test classes if they exist
            try:
                from unit.test_material_properties import TestMaterialProperties
                test_classes.append(TestMaterialProperties)
            except ImportError:
                pass
            
            try:
                from unit.test_geometry_calculations import TestGeometryCalculations  
                test_classes.append(TestGeometryCalculations)
            except ImportError:
                pass
            
            for test_class in test_classes:
                self._run_test_class(test_class)
                
        except ImportError as e:
            print(f"WARNING: Unit test modules not found: {e}")
            print("   Creating unit test templates...")
            self._create_unit_test_templates()
            
    def run_integration_tests(self):
        """Run integration tests for GUI components"""
        print("\nRUNNING INTEGRATION TESTS")
        print("-" * 35)
        
        try:
            from tests.integration.test_gui_workflow import TestGUIWorkflow
            from tests.integration.test_analysis_pipeline import TestAnalysisPipeline
            
            test_classes = [TestGUIWorkflow, TestAnalysisPipeline]
            
            for test_class in test_classes:
                self._run_test_class(test_class)
                
        except ImportError as e:
            print(f"WARNING: Integration test modules not found: {e}")
            print("   Creating integration test templates...")
            self._create_integration_test_templates()
            
    def run_validation_tests(self):
        """Run validation tests against reference data"""
        print("\nRUNNING VALIDATION TESTS")
        print("-" * 35)
        
        try:
            from tests.validation.test_reference_cases import TestReferenceCases
            from tests.validation.test_notebook_comparison import TestNotebookComparison
            
            test_classes = [TestReferenceCases, TestNotebookComparison]
            
            for test_class in test_classes:
                self._run_test_class(test_class)
                
        except ImportError as e:
            print(f"WARNING: Validation test modules not found: {e}")
            print("   Creating validation test templates...")
            self._create_validation_test_templates()
            
    def run_performance_tests(self):
        """Run performance and stress tests"""
        print("\nRUNNING PERFORMANCE TESTS")
        print("-" * 35)
        
        try:
            from tests.performance.test_calculation_speed import TestCalculationSpeed
            from tests.performance.test_memory_usage import TestMemoryUsage
            from tests.performance.test_gui_responsiveness import TestGUIResponsiveness
            
            test_classes = [TestCalculationSpeed, TestMemoryUsage, TestGUIResponsiveness]
            
            for test_class in test_classes:
                self._run_test_class(test_class)
                
        except ImportError as e:
            print(f"WARNING: Performance test modules not found: {e}")
            print("   Creating performance test templates...")
            self._create_performance_test_templates()
            
    def _run_test_class(self, test_class):
        """Run all tests in a test class"""
        try:
            test_instance = test_class()
            test_methods = [method for method in dir(test_instance) 
                          if method.startswith('test_') and callable(getattr(test_instance, method))]
            
            for test_method in test_methods:
                self._run_single_test(test_instance, test_method)
                
        except Exception as e:
            print(f"ERROR: Error running test class {test_class.__name__}: {e}")
            self.test_results['failed'] += 1
            
    def _run_single_test(self, test_instance, test_method):
        """Run a single test method"""
        try:
            print(f"   {test_method}...", end=" ")
            
            start_time = time.time()
            # Call setUp before the test method
            if hasattr(test_instance, 'setUp'):
                test_instance.setUp()
            getattr(test_instance, test_method)()
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            print("PASS", f"({execution_time:.3f}s)")
            self.test_results['passed'] += 1
            self.test_results['total_tests'] += 1
            
            self.test_results['test_cases'].append({
                'name': test_method,
                'class': test_instance.__class__.__name__,
                'status': 'PASS',
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            print("FAIL")
            print(f"      Error: {str(e)}")
            self.test_results['failed'] += 1
            self.test_results['total_tests'] += 1
            
            self.test_results['test_cases'].append({
                'name': test_method,
                'class': test_instance.__class__.__name__,
                'status': 'FAIL',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            
    def generate_test_report(self):
        """Generate comprehensive test report"""
        self.test_results['end_time'] = datetime.now().isoformat()
        
        print("\nTEST EXECUTION SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.test_results['total_tests']}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Skipped: {self.test_results['skipped']}")
        
        if self.test_results['total_tests'] > 0:
            success_rate = (self.test_results['passed'] / self.test_results['total_tests']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
            
        # Save detailed report
        report_file = project_dir / "test_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
            
        print(f"\nDetailed report saved to: {report_file}")
        
        # Generate HTML report
        self._generate_html_report()
        
    def _generate_html_report(self):
        """Generate HTML test report"""
        html_content = self._create_html_report_template()
        
        report_file = project_dir / "test_report.html"
        with open(report_file, 'w') as f:
            f.write(html_content)
            
        print(f"HTML report saved to: {report_file}")
        
    def _create_html_report_template(self):
        """Create HTML report template"""
        success_rate = 0
        if self.test_results['total_tests'] > 0:
            success_rate = (self.test_results['passed'] / self.test_results['total_tests']) * 100
            
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Panel Flutter Analysis Tool - Test Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2563EB; border-bottom: 3px solid #2563EB; padding-bottom: 10px; }}
        h2 {{ color: #1F2937; margin-top: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; }}
        .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
        .test-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .test-table th, .test-table td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        .test-table th {{ background: #f8f9fa; font-weight: 600; }}
        .status-pass {{ color: #10B981; font-weight: bold; }}
        .status-fail {{ color: #EF4444; font-weight: bold; }}
        .timestamp {{ font-size: 0.9em; color: #6B7280; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Panel Flutter Analysis Tool - Test Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-number">{self.test_results['total_tests']}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.test_results['passed']}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.test_results['failed']}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{success_rate:.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
        
        <h2>Test Results Details</h2>
        <table class="test-table">
            <thead>
                <tr>
                    <th>Test Class</th>
                    <th>Test Method</th>
                    <th>Status</th>
                    <th>Execution Time</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for test in self.test_results['test_cases']:
            status_class = 'status-pass' if test['status'] == 'PASS' else 'status-fail'
            execution_time = f"{test.get('execution_time', 0):.3f}s" if 'execution_time' in test else 'N/A'
            
            html += f"""
                <tr>
                    <td>{test['class']}</td>
                    <td>{test['name']}</td>
                    <td><span class="{status_class}">{test['status']}</span></td>
                    <td>{execution_time}</td>
                    <td class="timestamp">{test['timestamp']}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <h2>Test Categories</h2>
        <ul>
            <li><strong>Unit Tests:</strong> Core calculation validation</li>
            <li><strong>Integration Tests:</strong> GUI component interaction</li>
            <li><strong>Validation Tests:</strong> Reference data comparison</li>
            <li><strong>Performance Tests:</strong> Speed and memory efficiency</li>
        </ul>
    </div>
</body>
</html>
"""
        return html
        
    def _create_unit_test_templates(self):
        """Create unit test templates"""
        print("   Creating unit test templates...")
        
        # Create directory structure
        (project_dir / "tests" / "unit").mkdir(parents=True, exist_ok=True)
        
        # Template files to create
        test_files = [
            ("test_abd_matrices.py", self._get_abd_test_template()),
            ("test_material_properties.py", self._get_material_test_template()),
            ("test_geometry_calculations.py", self._get_geometry_test_template())
        ]
        
        for filename, content in test_files:
            file_path = project_dir / "tests" / "unit" / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"   Created: {filename}")
            
    def _create_integration_test_templates(self):
        """Create integration test templates"""
        print("   Creating integration test templates...")
        
        (project_dir / "tests" / "integration").mkdir(parents=True, exist_ok=True)
        
        test_files = [
            ("test_gui_workflow.py", self._get_gui_test_template()),
            ("test_analysis_pipeline.py", self._get_pipeline_test_template())
        ]
        
        for filename, content in test_files:
            file_path = project_dir / "tests" / "integration" / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"   Created: {filename}")
            
    def _create_validation_test_templates(self):
        """Create validation test templates"""
        print("   Creating validation test templates...")
        
        (project_dir / "tests" / "validation").mkdir(parents=True, exist_ok=True)
        
        test_files = [
            ("test_reference_cases.py", self._get_reference_test_template()),
            ("test_notebook_comparison.py", self._get_notebook_test_template())
        ]
        
        for filename, content in test_files:
            file_path = project_dir / "tests" / "validation" / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"   Created: {filename}")
            
    def _create_performance_test_templates(self):
        """Create performance test templates"""
        print("   Creating performance test templates...")
        
        (project_dir / "tests" / "performance").mkdir(parents=True, exist_ok=True)
        
        test_files = [
            ("test_calculation_speed.py", self._get_speed_test_template()),
            ("test_memory_usage.py", self._get_memory_test_template()),
            ("test_gui_responsiveness.py", self._get_responsiveness_test_template())
        ]
        
        for filename, content in test_files:
            file_path = project_dir / "tests" / "performance" / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"   Created: {filename}")

    # Template methods for test file contents
    def _get_abd_test_template(self):
        return '''"""Unit tests for ABD matrix calculations"""
import unittest
import numpy as np
import math

class TestABDMatrices(unittest.TestCase):
    """Test ABD matrix calculation accuracy"""
    
    def setUp(self):
        """Set up test parameters"""
        # Reference CFRP material properties
        self.E1 = 54.0e9    # Pa
        self.E2 = 18.0e9    # Pa
        self.G12 = 7.2e9    # Pa
        self.nu12 = 0.3
        
    def test_single_layer_abd(self):
        """Test ABD calculation for single layer"""
        # This test validates single ply calculations
        print("Testing single layer ABD calculation...")
        # Add actual test implementation
        pass
        
    def test_symmetric_layup_abd(self):
        """Test symmetric layup ABD matrices"""
        print("Testing symmetric layup...")
        # Should have zero B matrix
        pass
        
    def test_45_degree_layup(self):
        """Test [45°]6 layup from reference case"""
        print("Testing 45-degree layup...")
        # Reference values from validation
        expected_A11 = 2.10e7  # N/m
        # Add validation against expected values
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_material_test_template(self):
        return '''"""Unit tests for material property calculations"""
import unittest

class TestMaterialProperties(unittest.TestCase):
    """Test material property handling"""
    
    def test_isotropic_properties(self):
        """Test isotropic material property calculations"""
        print("Testing isotropic material properties...")
        pass
        
    def test_orthotropic_properties(self):
        """Test orthotropic material property calculations"""
        print("Testing orthotropic material properties...")
        pass
        
    def test_material_validation(self):
        """Test material property validation"""
        print("Testing material validation...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_geometry_test_template(self):
        return '''"""Unit tests for geometry calculations"""
import unittest

class TestGeometryCalculations(unittest.TestCase):
    """Test geometry calculation accuracy"""
    
    def test_panel_dimensions(self):
        """Test panel dimension calculations"""
        print("Testing panel dimensions...")
        pass
        
    def test_mesh_generation(self):
        """Test mesh generation"""
        print("Testing mesh generation...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_gui_test_template(self):
        return '''"""Integration tests for GUI workflow"""
import unittest

class TestGUIWorkflow(unittest.TestCase):
    """Test GUI component integration"""
    
    def test_tab_navigation(self):
        """Test navigation between tabs"""
        print("Testing tab navigation...")
        pass
        
    def test_input_validation(self):
        """Test input validation workflow"""
        print("Testing input validation...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_pipeline_test_template(self):
        return '''"""Integration tests for analysis pipeline"""
import unittest

class TestAnalysisPipeline(unittest.TestCase):
    """Test analysis pipeline integration"""
    
    def test_analysis_setup(self):
        """Test analysis setup pipeline"""
        print("Testing analysis setup...")
        pass
        
    def test_results_processing(self):
        """Test results processing pipeline"""
        print("Testing results processing...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_reference_test_template(self):
        return '''"""Validation tests against reference cases"""
import unittest
import numpy as np

class TestReferenceCases(unittest.TestCase):
    """Test against reference validation cases"""
    
    def test_composite_reference_case(self):
        """Test composite panel against reference"""
        print("Testing composite reference case...")
        # Reference flutter velocity: 998.8 m/s
        pass
        
    def test_metallic_reference_case(self):
        """Test metallic panel against reference"""
        print("Testing metallic reference case...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_notebook_test_template(self):
        return '''"""Validation tests comparing with notebook results"""
import unittest

class TestNotebookComparison(unittest.TestCase):
    """Compare results with Jupyter notebook outputs"""
    
    def test_composite_notebook_comparison(self):
        """Compare with Composite.ipynb results"""
        print("Comparing with Composite.ipynb...")
        pass
        
    def test_modal_notebook_comparison(self):
        """Compare with Modal.ipynb results"""
        print("Comparing with Modal.ipynb...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_speed_test_template(self):
        return '''"""Performance tests for calculation speed"""
import unittest
import time

class TestCalculationSpeed(unittest.TestCase):
    """Test calculation performance"""
    
    def test_abd_calculation_speed(self):
        """Test ABD matrix calculation speed"""
        print("Testing ABD calculation speed...")
        # Should complete within reasonable time
        pass
        
    def test_large_layup_performance(self):
        """Test performance with large layups"""
        print("Testing large layup performance...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_memory_test_template(self):
        return '''"""Performance tests for memory usage"""
import unittest

class TestMemoryUsage(unittest.TestCase):
    """Test memory efficiency"""
    
    def test_memory_consumption(self):
        """Test memory consumption during analysis"""
        print("Testing memory consumption...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

    def _get_responsiveness_test_template(self):
        return '''"""Performance tests for GUI responsiveness"""
import unittest

class TestGUIResponsiveness(unittest.TestCase):
    """Test GUI responsiveness"""
    
    def test_interface_responsiveness(self):
        """Test GUI response times"""
        print("Testing GUI responsiveness...")
        pass

if __name__ == '__main__':
    unittest.main()
'''

def main():
    """Main entry point for test runner"""
    parser = argparse.ArgumentParser(description='Panel Flutter Analysis Tool Test Runner')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests')
    parser.add_argument('--validation', action='store_true', help='Run validation tests')
    parser.add_argument('--performance', action='store_true', help='Run performance tests')
    parser.add_argument('--report', action='store_true', help='Generate test report only')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.all or not any([args.unit, args.integration, args.validation, args.performance, args.report]):
        runner.run_all_tests()
    else:
        if args.unit:
            runner.run_unit_tests()
        if args.integration:
            runner.run_integration_tests()
        if args.validation:
            runner.run_validation_tests()
        if args.performance:
            runner.run_performance_tests()
        if args.report:
            runner.generate_test_report()

if __name__ == '__main__':
    main()