# Panel Flutter Analysis GUI

A comprehensive graphical user interface for panel flutter analysis using NASTRAN aeroelasticity methods.

## Features

### ✨ Modern GUI Interface
- **Clean, Professional Design**: Modern styling with intuitive tabbed interface
- **Responsive Layout**: Adaptive interface that works on different screen sizes
- **Interactive Visualization**: 3D geometry and results visualization with matplotlib

### 🛩️ Comprehensive Analysis Capabilities
- **Panel Geometry Definition**: Interactive geometry specification with corner points and dimensions
- **Material Properties**: Support for isotropic, orthotropic, and composite materials
- **Boundary Conditions**: Flexible edge constraint definition (free, simply supported, clamped)
- **Analysis Parameters**: Complete flutter analysis setup with Mach numbers, velocities, and methods

### 📊 Advanced Visualization
- **3D Geometry Display**: Interactive 3D visualization of panel geometry
- **Mesh Visualization**: Display of finite element mesh with quality metrics
- **Results Plotting**: V-f, V-g diagrams, mode shapes, and root locus plots
- **Real-time Updates**: Dynamic visualization updates as parameters change

### 💾 Data Management
- **Project Files**: Save and load complete analysis projects (.pfp format)
- **BDF Import/Export**: NASTRAN bulk data file integration
- **Results Export**: Export results in CSV, Excel, JSON formats
- **Report Generation**: Comprehensive analysis reports

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
- matplotlib>=3.1.3 (plotting and visualization)
- numpy>=1.18.1 (numerical computations)
- pyNastran>=1.3.2 (NASTRAN integration)
- pandas>=1.3 (data handling)
- openpyxl>=3.0.0 (Excel export)
- scipy>=1.5.0 (scientific computations)

## Running the Application

### Quick Start
```bash
cd src
python gui/main_app.py
```

### Alternative Launch
```python
from gui.main_app import PanelFlutterApp

app = PanelFlutterApp()
app.run()
```

## User Guide

### 1. Getting Started
1. Launch the application
2. Create a new project or open an existing one
3. Define your panel geometry in the **Geometry** tab
4. Specify material properties in the **Materials** tab
5. Set boundary conditions in the **Boundary** tab
6. Configure analysis parameters in the **Analysis** tab
7. Run the analysis and view results in the **Results** tab

### 2. Geometry Definition
- **Panel Types**: Rectangular, trapezoidal, or custom geometry
- **Dimensions**: Length, width, chord specifications
- **Corner Points**: Precise coordinate definition
- **Mesh Parameters**: Element density control with quality metrics

### 3. Material Properties
- **Built-in Database**: Common aerospace materials (aluminum, steel, titanium, composites)
- **Custom Materials**: Define your own material properties
- **Composite Layups**: Layer-by-layer composite definition
- **Property Validation**: Automatic validation of material parameters

### 4. Analysis Setup
- **Flight Conditions**: Mach number and velocity ranges
- **Solution Methods**: K, KE, PK, PKNL methods
- **Convergence Control**: Tolerance and iteration settings
- **Output Options**: Detailed results and mode shape saving

### 5. Results Visualization
- **Flutter Summary**: Critical flutter speed and frequency
- **Detailed Results**: Complete tabular data
- **Interactive Plots**: V-f, V-g diagrams with zoom and pan
- **3D Mode Shapes**: Animated mode shape visualization

## Architecture

The application follows a modern **Model-View-Controller (MVC)** architecture:

### Components
- **Models** (`gui/models/`): Data structures and business logic
- **Views** (`gui/views/`): User interface components and panels
- **Controllers** (`gui/controllers/`): Application logic and event handling
- **Utils** (`gui/utils/`): Utilities for themes, widgets, validation, and file management

### Key Files
- `main_app.py`: Main application entry point
- `main_window.py`: Primary GUI window
- `main_controller.py`: Core application controller
- `project_model.py`: Project data model
- Individual panel views for each functionality area

## Example Usage

### Basic Flutter Analysis
1. **Geometry**: Create 1m × 2m rectangular panel
2. **Material**: Select Aluminum 7075-T6 from database
3. **Boundary**: Clamped leading edge, free trailing edge
4. **Analysis**: PK method, Mach 0.5-1.2, velocities 50-300 m/s
5. **Results**: View flutter speed and critical modes

### Advanced Analysis
- Multi-layer composite panels
- Custom aerodynamic theories (Piston, Van Dyke)
- Parameter studies across Mach/velocity ranges
- Detailed mode shape analysis

## Validation Cases

The application includes several validation examples:
- NACA standard panels
- Benchmark flutter cases
- Composite panel comparisons

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **pyNastran Issues**: Check NASTRAN installation and paths
3. **Display Problems**: Update graphics drivers for 3D visualization
4. **Performance**: Reduce mesh density for faster visualization

### Debug Mode
Set logging level for detailed debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Development Setup
1. Clone repository
2. Install development dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest tests/`

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Document all public methods
- Write unit tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using pyNastran for NASTRAN integration
- GUI framework based on tkinter with modern styling
- Visualization powered by matplotlib
- Inspired by aerospace flutter analysis needs

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review existing documentation
3. Create detailed issue reports
4. Include system information and error messages

---

**Panel Flutter Analysis GUI v1.0.0**  
*A comprehensive tool for aerospace panel flutter analysis*