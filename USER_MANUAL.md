# Panel Flutter Analysis Tool - User Manual

## Overview

A comprehensive desktop application for panel flutter analysis in aerospace applications. This tool provides accurate aeroelastic analysis capabilities using multiple computational methods including Piston Theory, Doublet Lattice Method, and NASTRAN integration.

## Key Features

### 🎯 **Multi-Solver Framework**
- **Piston Theory Solver**: Fast, reliable for supersonic applications
- **Doublet Lattice Method**: Advanced subsonic/transonic analysis
- **NASTRAN Integration**: Professional-grade finite element analysis
- **Automatic solver selection** based on flow conditions

### 🔧 **Comprehensive Boundary Conditions**
- **11 boundary condition types**: SSSS, CCCC, CFFF, CSSS, CCSS, CFCF, SSSF, CCCF, SFSS, CFCC, FFFF
- **Real-time flutter tendency feedback** for each boundary condition
- **Edge constraint visualization** with engineering descriptions
- **Smart recommendations** based on analysis type

### 🧪 **Advanced Materials Support**
- **Isotropic materials**: Metals (aluminum, steel, titanium)
- **Composite materials**: Full laminate analysis capability
- **Material property database** with common aerospace materials
- **Real-time property validation** and unit conversion

### 📊 **Professional User Interface**
- **Modern tabbed interface**: 🔧 Geometry, 🧪 Materials, ⚡ Analysis, 📊 Results
- **Real-time input validation** with immediate feedback
- **Consistent mouse scrolling** across all tabs
- **Professional iconography** and visual design
- **Context-sensitive help** and tooltips

### ✅ **Quality Assurance**
- **Comprehensive test suite** with 16+ test modules
- **Validated boundary conditions** against reference implementations
- **Multi-solver consistency** verification
- **Professional-grade error handling**

## Quick Start

### System Requirements
- **Windows 10/11** (primary support)
- **Python 3.8+** with scientific libraries
- **4GB RAM** minimum, 8GB recommended
- **Dependencies**: numpy, matplotlib, pandas, tkinter

### Installation & Launch

1. **Ensure Python dependencies**:
   ```bash
   pip install numpy matplotlib pandas
   ```

2. **Launch the application**:
   ```bash
   python launch_gui.py
   ```
   or
   ```bash
   python run_gui.py
   ```

### First Analysis (5-Step Process)

1. **🔧 Geometry Tab**: Define panel dimensions and boundary conditions
2. **🧪 Materials Tab**: Enter material properties (density, thickness, modulus)  
3. **⚡ Analysis Tab**: Set flow conditions and velocity range
4. **Run Analysis**: Execute flutter analysis
5. **📊 Results Tab**: Review flutter speed, frequency, and plots

## Detailed User Guide

### 1. 🔧 Geometry Configuration

#### Panel Dimensions
- **Length**: Panel length in millimeters (typical: 100-2000 mm)
  - Represents the dimension in flow direction
  - Used for aerodynamic length scale

- **Width**: Panel width in millimeters (typical: 50-1000 mm)
  - Represents span dimension
  - Used for structural aspect ratio

#### Boundary Conditions (11 Types Available)

**Most Common:**
- **SSSS** - Simply Supported All Edges
  - Medium flutter tendency, good baseline
  - Typical for aircraft panels with flexible attachments

- **CCCC** - Clamped All Edges  
  - Low flutter tendency, conservative
  - Rigid attachments, thick panels

- **CFFF** - Cantilever Configuration
  - High flutter tendency, most critical
  - Control surfaces, free trailing edge

**Advanced Configurations:**
- **CSSS** - Clamped Leading Edge: Realistic for wing panels
- **CCSS** - Clamped Chordwise Edges: Wing panels with spars  
- **CFCF** - Clamped Chordwise, Free Spanwise: Strip theory validation
- **SSSF** - Simply Supported with Free Trailing: Control surfaces, flaps
- **CCCF** - Clamped with Free Trailing: Fixed-root control surfaces
- **SFSS** - Simply Supported with Free Trailing: Wing trailing edge panels
- **CFCC** - Clamped with Free Trailing: Control surface roots
- **FFFF** - Free All Edges: Theoretical validation only

#### Mesh Parameters
- **Lengthwise Elements**: 10-50 (recommended: 20-30)
- **Spanwise Elements**: 5-25 (recommended: 10-15)
- **Guidelines**: Maintain reasonable element aspect ratios (1:1 to 3:1)

### 2. 🧪 Materials Configuration

#### Material Properties (All Required)
- **Density (kg/m³)**: Material density
  - Aluminum: ~2700 kg/m³
  - Steel: ~7800 kg/m³
  - Carbon/Epoxy: ~1600 kg/m³

- **Thickness (mm)**: Panel thickness
  - **NOTE**: Thickness appears only in Materials tab (no longer duplicated in Geometry)
  - Metals: 1-10 mm typical
  - Composites: 0.5-5 mm typical

#### Isotropic Materials
- **Young's Modulus (Pa)**: Elastic modulus
  - Aluminum 6061: 69.0e9 Pa
  - Aluminum 7075: 71.7e9 Pa  
  - Steel: 200e9 Pa

- **Poisson's Ratio**: Lateral strain ratio (0.25-0.35 typical)
  - Aluminum: 0.33
  - Steel: 0.30

**Example: Aluminum 7075-T6**
```
Density: 2810 kg/m³
Thickness: 2.0 mm
Young's Modulus: 71.7e9 Pa
Poisson's Ratio: 0.33
```

#### Advanced Material Support
The tool supports composite materials through:
- **Orthotropic Properties**: E1, E2, G12, ν12
- **Laminate Analysis**: Multiple layer definitions
- **ABD Matrix Computation**: Classical Laminate Theory

### 3. ⚡ Analysis Configuration

#### Flow Conditions
- **Mach Number**: Flow Mach number
  - Subsonic: 0.3-0.9
  - Transonic: 0.9-1.1  
  - Supersonic: 1.1-3.0

- **Altitude (m)**: Flight altitude for atmospheric properties
  - Sea level: 0 m
  - Cruise altitude: 8000-12000 m
  - Affects air density and temperature

#### Velocity Range
- **Minimum Velocity (m/s)**: Start of analysis range
  - Set below expected flutter speed
  - Typical: 50-80 m/s

- **Maximum Velocity (m/s)**: End of analysis range  
  - Set above expected flutter speed
  - Typical: 150-300 m/s

- **Velocity Points**: Number of analysis points
  - More points = smoother curves but longer analysis
  - Recommended: 15-25 points

#### Analysis Parameters
- **Dynamic Pressure Range**: Automatically computed from velocity
- **Reduced Frequency**: Internal parameter for unsteady aerodynamics
- **Solver Selection**: Automatic based on Mach number and boundary conditions

### 4. Running Analysis

#### Multi-Solver Framework
The tool automatically selects the best solver:

1. **Piston Theory Solver**
   - Best for: Mach > 1.2, all boundary conditions
   - Speed: Very fast (seconds)
   - Accuracy: Good for supersonic

2. **Doublet Lattice Method**
   - Best for: Mach < 1.2, complex boundary conditions
   - Speed: Moderate (minutes) 
   - Accuracy: Excellent for subsonic/transonic

3. **NASTRAN Solver** (if available)
   - Best for: All conditions, highest accuracy
   - Speed: Slower (minutes)
   - Accuracy: Professional-grade

#### Analysis Progress
- **Status updates** in real-time
- **Progress indicators** for long analyses
- **Error messages** with specific guidance
- **Automatic result validation**

### 5. 📊 Results Interpretation

#### Primary Results
- **Flutter Speed (m/s)**: Critical velocity for instability
- **Flutter Frequency (Hz)**: Frequency at flutter condition
- **Flutter Mode**: Structural mode number that becomes unstable
- **Damping Coefficient**: Stability margin at analysis points

#### Flutter Characteristics by Boundary Condition

**Low Flutter Speed (High Risk):**
- CFFF (Cantilever): Lowest speeds, most critical
- SSSF, SFSS: Free trailing edge configurations

**Medium Flutter Speed:**
- SSSS: Baseline reference condition
- CSSS, CCSS: Realistic wing panel conditions
- CFCF, CCCF, CFCC: Mixed constraint conditions

**High Flutter Speed (Conservative):**
- CCCC: Highest speeds, most conservative

#### Safety Guidelines
- **Aerospace Certification**: Flutter speed > 1.15 × Never-exceed speed
- **Design Margin**: Use conservative boundary conditions for preliminary design
- **Validation**: Compare results between multiple solvers when available

### 6. Advanced Features

#### Boundary Condition Selection Guidance
The interface provides real-time feedback:
- **Green indicators**: Low flutter tendency, conservative
- **Yellow indicators**: Medium flutter tendency, typical
- **Red indicators**: High flutter tendency, critical cases

#### Input Validation
- **Real-time checking**: Immediate feedback on parameter validity
- **Unit consistency**: All calculations in SI units internally
- **Range verification**: Parameters checked against physical limits
- **Error prevention**: Invalid combinations prevented before analysis

#### Professional Integration
- **Test Suite**: Run `python tests/run_all_tests.py` for validation
- **Quality Assurance**: All 11 boundary conditions tested and validated
- **Consistency Verification**: Multi-solver results compared automatically

## Example Applications

### Commercial Aircraft Panel
```
Dimensions: 500mm × 300mm × 2mm
Material: Aluminum 7075-T6 (ρ=2810, E=71.7e9, ν=0.33)
Boundary: SSSS (Simply Supported)
Flow: Mach 0.8, Altitude 10000m
Expected Flutter: ~120-180 m/s
```

### Control Surface
```  
Dimensions: 300mm × 200mm × 1.5mm
Material: Aluminum 6061-T6 (ρ=2700, E=69.0e9, ν=0.33)
Boundary: CCCF (Clamped with Free Trailing)
Flow: Mach 0.7, Altitude 8000m
Expected Flutter: ~90-150 m/s
```

### Wing Panel
```
Dimensions: 800mm × 400mm × 3mm
Material: Carbon/Epoxy Equivalent (ρ=1600, E=80e9, ν=0.3)
Boundary: CFCF (Wing-like)
Flow: Mach 0.85, Altitude 11000m
Expected Flutter: ~100-160 m/s
```

## Troubleshooting

### Common Issues

#### "Analysis Failed to Start"
- **Check all inputs**: Ensure no fields are empty
- **Verify positive values**: All dimensions and material properties > 0
- **Check units**: Tool expects specific units (mm for dimensions, Pa for modulus)
- **Boundary conditions**: Ensure a boundary condition is selected

#### "Unrealistic Results"
- **Unit verification**: 
  - Length/Width: millimeters
  - Thickness: millimeters  
  - Density: kg/m³
  - Young's Modulus: Pascals
  - Velocities: m/s
- **Material properties**: Verify against reference data
- **Boundary conditions**: Ensure appropriate for application

#### "Analysis Takes Too Long"
- **Reduce velocity points**: Start with 10-15 points
- **Simplify mesh**: Use fewer elements for initial studies
- **Check solver**: Piston Theory is fastest for supersonic cases
- **Close other applications**: Free system resources

#### GUI Scrolling Issues
- **Fixed in current version**: All tabs have consistent mouse wheel scrolling
- **If problems persist**: Try clicking in the tab area first, then scroll

### Performance Optimization

#### For Faster Analysis:
1. **Piston Theory**: Best for Mach > 1.2
2. **Fewer velocity points**: 10-20 for initial studies
3. **Coarser mesh**: 15×8 elements for preliminary analysis
4. **Simple boundary conditions**: SSSS, CCCC converge fastest

#### For Higher Accuracy:
1. **Doublet Lattice**: Best for Mach < 1.2
2. **More velocity points**: 25-40 for smooth curves
3. **Refined mesh**: 30×15 elements or higher
4. **NASTRAN solver**: If available and properly configured

### Getting Help

#### Built-in Resources
- **Tooltips**: Hover over inputs for quick guidance
- **Real-time validation**: Immediate feedback on input validity
- **Boundary condition help**: Flutter tendency indicators
- **Status messages**: Detailed progress and error reporting

#### Validation and Testing
- **Run test suite**: `python tests/run_all_tests.py`
- **Check boundary conditions**: All 11 types tested and validated
- **Verify installation**: Test suite confirms proper setup
- **Performance testing**: Benchmark against reference cases

## Technical Implementation

### Solver Architecture
- **Multi-solver framework**: Automatic best-solver selection
- **Boundary condition engine**: 11 validated configurations
- **Input validation**: Real-time error checking and prevention
- **Professional GUI**: Modern interface with consistent behavior

### Quality Assurance  
- **16+ test modules**: Unit, integration, performance, validation tests
- **100% boundary condition coverage**: All types tested
- **Cross-solver validation**: Results compared between methods
- **Professional error handling**: Graceful failure modes

### Recent Improvements
- **Consolidated thickness input**: Now only in Materials tab (eliminated duplication)
- **Fixed mouse scrolling**: Consistent behavior across all tabs  
- **Enhanced boundary conditions**: Added SFSS and CFCC configurations
- **Professional iconography**: All tabs have consistent visual design
- **Comprehensive testing**: Organized test suite for reliability

---

## Support

### Technical Support
- **User Manual**: This comprehensive guide
- **Test Suite**: Built-in validation and verification
- **Error Messages**: Specific guidance for common issues
- **Input Validation**: Real-time help and feedback

### Software Quality
- **Validated Implementation**: All features tested against reference cases
- **Professional Standards**: Aerospace-grade analysis capabilities
- **Continuous Testing**: Automated test suite ensures reliability
- **Multi-solver Verification**: Results validated across different methods

---

**© 2024 NASTRAN Aeroelasticity Development Team**  
*Professional flutter analysis tools for aerospace applications*

Version: 1.2.0 | Last Updated: December 2024