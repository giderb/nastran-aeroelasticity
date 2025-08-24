#!/usr/bin/env python3
"""
Comprehensive Test Runner
========================

Run all tests in the test suite with proper reporting.
"""

import sys
import unittest
import os
from pathlib import Path
from io import StringIO

# Add paths for imports
current_dir = Path(__file__).parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(current_dir))

def run_all_tests(verbose=False):
    """Run all tests and return results"""
    
    print("NASTRAN AEROELASTICITY - COMPREHENSIVE TEST SUITE")
    print("=" * 55)
    print()
    
    # Test categories
    test_categories = {
        'Unit Tests': [
            'tests.unit.test_boundary_conditions',
            'tests.unit.test_import_structure',
            'tests.unit.test_abd_matrices',
            'tests.unit.test_geometry_calculations',
            'tests.unit.test_material_properties'
        ],
        'Integration Tests': [
            'tests.integration.test_multi_solver',
            'tests.integration.test_gui_functionality',
            'tests.integration.test_nastran_integration',
            'tests.integration.test_analysis_pipeline',
            'tests.integration.test_gui_integration',
            'tests.integration.test_gui_workflow'
        ],
        'Performance Tests': [
            'tests.performance.test_calculation_speed',
            'tests.performance.test_gui_responsiveness',
            'tests.performance.test_memory_usage'
        ],
        'Validation Tests': [
            'tests.validation.test_notebook_comparison',
            'tests.validation.test_reference_cases'
        ]
    }
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    category_results = {}
    
    for category_name, test_modules in test_categories.items():
        print(f"\n{category_name}")
        print("-" * len(category_name))
        
        category_tests = 0
        category_failures = 0
        category_errors = 0
        category_skipped = 0
        
        for module_name in test_modules:
            try:
                # Load the test module
                loader = unittest.TestLoader()
                suite = loader.loadTestsFromName(module_name)
                
                # Run tests with custom result handler
                stream = StringIO()
                runner = unittest.TextTestRunner(
                    stream=stream, 
                    verbosity=2 if verbose else 1
                )
                result = runner.run(suite)
                
                # Count results
                tests_run = result.testsRun
                failures = len(result.failures)
                errors = len(result.errors)
                skipped = len(result.skipped)
                
                category_tests += tests_run
                category_failures += failures
                category_errors += errors
                category_skipped += skipped
                
                # Status
                if failures == 0 and errors == 0:
                    status = "PASS"
                    if skipped > 0:
                        status += f" ({skipped} skipped)"
                elif failures == 0:
                    status = f"ERROR ({errors} errors)"
                else:
                    status = f"FAIL ({failures} failures, {errors} errors)"
                
                module_short = module_name.split('.')[-1]
                print(f"  {module_short:<30} {status}")
                
                # Show details if verbose or if there were failures/errors
                if verbose or failures > 0 or errors > 0:
                    output = stream.getvalue()
                    if output.strip():
                        # Show only the summary line or error details
                        lines = output.split('\n')
                        relevant_lines = [line for line in lines if 
                                        ('FAIL:' in line or 'ERROR:' in line or 
                                         'AssertionError' in line or 'Exception' in line)]
                        if relevant_lines:
                            for line in relevant_lines[:3]:  # Show first 3 error lines
                                print(f"    {line}")
                
            except ImportError as e:
                print(f"  {module_name:<30} IMPORT ERROR: {e}")
                category_errors += 1
            except Exception as e:
                print(f"  {module_name:<30} EXCEPTION: {e}")
                category_errors += 1
        
        # Category summary
        print(f"\n  Category Summary: {category_tests} tests, {category_failures} failures, {category_errors} errors, {category_skipped} skipped")
        
        total_tests += category_tests
        total_failures += category_failures
        total_errors += category_errors
        total_skipped += category_skipped
        
        category_results[category_name] = {
            'tests': category_tests,
            'failures': category_failures,
            'errors': category_errors,
            'skipped': category_skipped
        }
    
    # Overall summary
    print("\n" + "=" * 55)
    print("OVERALL TEST SUMMARY")
    print("=" * 55)
    print(f"Total Tests Run:  {total_tests}")
    print(f"Failures:         {total_failures}")
    print(f"Errors:           {total_errors}")
    print(f"Skipped:          {total_skipped}")
    print(f"Success Rate:     {((total_tests - total_failures - total_errors) / max(total_tests, 1)) * 100:.1f}%")
    
    # Category breakdown
    print(f"\nBREAKDOWN BY CATEGORY:")
    for category, results in category_results.items():
        success_rate = ((results['tests'] - results['failures'] - results['errors']) / max(results['tests'], 1)) * 100
        print(f"  {category:<20} {success_rate:>5.1f}% ({results['tests']} tests)")
    
    # Overall result
    if total_failures == 0 and total_errors == 0:
        if total_skipped > 0:
            print(f"\n✓ ALL TESTS PASSED ({total_skipped} skipped)")
            result_code = 0
        else:
            print(f"\n✅ ALL TESTS PASSED!")
            result_code = 0
    else:
        print(f"\n❌ SOME TESTS FAILED ({total_failures + total_errors} issues)")
        result_code = 1
    
    print("=" * 55)
    
    return result_code, {
        'total_tests': total_tests,
        'failures': total_failures,
        'errors': total_errors,
        'skipped': total_skipped,
        'categories': category_results
    }

def main():
    """Main test runner entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run NASTRAN Aeroelasticity Test Suite')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Verbose output showing detailed test results')
    parser.add_argument('--unit', action='store_true',
                       help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', 
                       help='Run only integration tests')
    parser.add_argument('--performance', action='store_true',
                       help='Run only performance tests')
    parser.add_argument('--validation', action='store_true',
                       help='Run only validation tests')
    
    args = parser.parse_args()
    
    if any([args.unit, args.integration, args.performance, args.validation]):
        print("Selective test running not yet implemented. Running all tests.")
    
    result_code, results = run_all_tests(verbose=args.verbose)
    
    sys.exit(result_code)

if __name__ == '__main__':
    main()