# NASTRAN Aeroelasticity Test Suite

This directory contains the comprehensive test suite for the NASTRAN Aeroelasticity flutter analysis software.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_boundary_conditions.py  # Boundary condition functionality
│   ├── test_import_structure.py     # Module import structure
│   ├── test_abd_matrices.py         # ABD matrix calculations
│   ├── test_geometry_calculations.py # Geometry utilities
│   └── test_material_properties.py  # Material property handling
│
├── integration/             # Integration tests for component interaction
│   ├── test_multi_solver.py         # Multi-solver framework
│   ├── test_gui_functionality.py    # GUI functionality
│   ├── test_nastran_integration.py  # NASTRAN integration
│   ├── test_analysis_pipeline.py    # Analysis workflow
│   ├── test_gui_integration.py      # GUI integration
│   └── test_gui_workflow.py         # GUI workflow
│
├── performance/             # Performance and benchmarking tests
│   ├── test_calculation_speed.py    # Calculation performance
│   ├── test_gui_responsiveness.py   # GUI responsiveness
│   └── test_memory_usage.py         # Memory usage analysis
│
├── validation/              # Validation against reference cases
│   ├── test_notebook_comparison.py  # Compare with Jupyter notebooks
│   └── test_reference_cases.py      # Reference case validation
│
├── files/                   # Test data and reference files
│   └── flutter-f06-result.txt      # Sample NASTRAN output
│
├── run_all_tests.py         # Main test runner
├── test_runner.py           # Legacy test runner
└── README.md               # This file
```

## Running Tests

### Quick Start
```bash
# Run all tests
python tests/run_all_tests.py

# Run with verbose output
python tests/run_all_tests.py -v
```

### Test Categories

#### Unit Tests
Test individual components in isolation:
- **Boundary Conditions**: All 11 boundary condition types and their properties
- **Import Structure**: Module import verification and dependency checking
- **ABD Matrices**: Composite material matrix calculations
- **Geometry**: Geometric calculations and transformations
- **Materials**: Material property handling and validation

#### Integration Tests  
Test component interactions:
- **Multi-Solver**: Piston Theory, Doublet Lattice, and NASTRAN solver integration
- **GUI Functionality**: Core GUI features and user interactions
- **NASTRAN Integration**: NASTRAN solver availability and functionality
- **Analysis Pipeline**: End-to-end analysis workflow
- **GUI Workflow**: Complete user interaction scenarios

#### Performance Tests
Test system performance:
- **Calculation Speed**: Flutter analysis computation benchmarks
- **GUI Responsiveness**: User interface response time testing
- **Memory Usage**: Memory consumption and leak detection

#### Validation Tests
Test against reference cases:
- **Notebook Comparison**: Compare results with Jupyter notebook implementations
- **Reference Cases**: Validate against known reference solutions

## Test Requirements

### Core Dependencies
- Python 3.8+
- numpy
- matplotlib  
- pandas
- tkinter (for GUI tests)

### Optional Dependencies
- pyNastran (for NASTRAN integration tests)
- NASTRAN executable (for full NASTRAN workflow tests)

## Test Categories Explained

### Unit Tests (`tests/unit/`)
- **Fast execution** (< 1 second per test)
- **No external dependencies**
- **Isolated component testing**
- **High code coverage**

### Integration Tests (`tests/integration/`)
- **Moderate execution time** (1-10 seconds per test)  
- **Test component interactions**
- **May require GUI components**
- **End-to-end functionality verification**

### Performance Tests (`tests/performance/`)
- **Longer execution time** (5-30 seconds per test)
- **Benchmark critical operations**
- **Memory and speed profiling**
- **Regression detection**

### Validation Tests (`tests/validation/`)
- **Variable execution time**
- **Compare with reference implementations**
- **Ensure engineering accuracy**
- **Validate against literature/standards**

## Key Features Tested

### ✅ Boundary Conditions
- All 11 boundary condition types (SSSS, CCCC, CFFF, CSSS, CCSS, CFCF, SSSF, CCCF, SFSS, CFCC, FFFF)
- Edge constraint parsing and validation
- Stiffness matrix factors
- Natural frequency factors
- Flutter tendency warnings

### ✅ Multi-Solver Framework
- Piston Theory solver
- Doublet Lattice Method solver
- NASTRAN solver integration
- Result consistency between solvers
- Boundary condition effects

### ✅ GUI Functionality
- Tab structure and iconography
- Input validation and handling
- Scrolling functionality
- Material property consolidation
- Boundary condition selection
- Real-time feedback systems

### ✅ Import Structure
- Module availability
- Dependency verification
- Optional component handling
- Graceful degradation

## Continuous Integration

These tests are designed to be run in CI/CD environments:

```yaml
# Example CI configuration
- name: Run Unit Tests
  run: python tests/run_all_tests.py --unit

- name: Run Integration Tests  
  run: python tests/run_all_tests.py --integration

- name: Run Performance Tests
  run: python tests/run_all_tests.py --performance
```

## Contributing Tests

When adding new features:

1. **Add unit tests** for new components
2. **Add integration tests** for component interactions  
3. **Update validation tests** if engineering models change
4. **Add performance tests** for computationally intensive features

### Test Naming Convention
- `test_<component>_<functionality>.py` for unit tests
- `test_<integration_area>.py` for integration tests
- Use descriptive method names: `test_boundary_condition_stiffness_factors()`

### Test Structure
```python
class TestComponent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_specific_functionality(self):
        """Test a specific aspect of the component"""
        # Arrange
        # Act  
        # Assert
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        pass
```

## Test Results Interpretation

### Success Indicators
- **All tests pass**: ✅ Software is ready for use
- **Only skipped tests**: ⚠️ Some optional features unavailable but core functionality works
- **Performance regressions**: ⚠️ Functionality works but may be slower

### Failure Indicators
- **Unit test failures**: ❌ Core component issues - fix before release
- **Integration test failures**: ❌ Component interaction problems - investigate thoroughly
- **Validation test failures**: ❌ Engineering accuracy issues - critical fix needed

## Debugging Failed Tests

1. **Run with verbose output**: `python tests/run_all_tests.py -v`
2. **Run specific test category**: `python tests/run_all_tests.py --unit`
3. **Run individual test**: `python -m unittest tests.unit.test_boundary_conditions`
4. **Check test logs** for detailed error messages
5. **Verify dependencies** are installed and accessible

## Test Maintenance

- **Review tests quarterly** for relevance and accuracy
- **Update validation tests** when reference implementations change
- **Add performance baselines** for new computational features
- **Maintain test documentation** alongside code changes

This comprehensive test suite ensures the NASTRAN Aeroelasticity software maintains high quality, reliability, and engineering accuracy across all its components and use cases.