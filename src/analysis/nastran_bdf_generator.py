"""
FIXED NASTRAN BDF Generator for Panel Flutter Analysis
=======================================================
Generates proper SOL 145 BDF files with all required cards.
"""

import numpy as np
from datetime import datetime
from typing import Dict, Any

class NastranBDFGenerator:
    """Generate proper NASTRAN BDF files for SOL 145 flutter analysis"""
    
    def __init__(self):
        self.cards = []
    
    def generate_bdf(self, config: Dict[str, Any]) -> str:
        """Generate complete BDF for flutter analysis"""
        self.cards = []
        
        # Add all sections
        self._add_header()
        self._add_executive_control()
        self._add_case_control()
        self._add_bulk_data(config)
        
        return '\n'.join(self.cards)
    
    def _add_header(self):
        """Add BDF header"""
        self.cards.extend([
            "$ NASTRAN Panel Flutter Analysis - SOL 145",
            f"$ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "$ Complete flutter analysis setup",
            "$"
        ])
    
    def _add_executive_control(self):
        """Add executive control section"""
        self.cards.extend([
            "ID PANEL,FLUTTER",
            "SOL 145",  # Aerodynamic Flutter
            "TIME 600",
            "CEND"
        ])
    
    def _add_case_control(self):
        """Add case control section"""
        self.cards.extend([
            "TITLE = Panel Flutter Analysis",
            "ECHO = NONE",
            "SPC = 1",
            "METHOD = 10",     # Eigenvalue method ID
            "FMETHOD = 20",    # Flutter method ID
            "DISPLACEMENT = ALL",
            "SPCFORCE = ALL",
            "STRESS = ALL",
            "STRAIN = ALL",
            "FORCE = ALL",
            "ESE = ALL",
            "SDAMPING = 30",   # Structural damping ID
            "BEGIN BULK"
        ])
    
    def _add_bulk_data(self, config):
        """Add complete bulk data section"""
        
        # Extract configuration
        geom = config.get('geometry', {})
        mat = config.get('material', {})
        analysis = config.get('analysis', {})
        
        # Geometry
        length = geom.get('length', 0.5)
        width = geom.get('width', 0.3)
        thickness = geom.get('thickness', 0.002)
        nx = geom.get('nx', 10)
        ny = geom.get('ny', 5)
        
        # Material
        E = mat.get('E', 70e9)
        nu = mat.get('nu', 0.3)
        rho = mat.get('rho', 2700)
        damping = mat.get('damping', 0.02)
        
        # Analysis
        mach = analysis.get('mach', 1.5)
        altitude = analysis.get('altitude', 10000)
        
        # Calculate air properties
        rho_air, a_sound = self._calculate_air_properties(altitude)
        
        # PARAM cards - Essential for flutter
        self._add_param_cards(damping)
        
        # AERO card - Reference conditions
        self._add_aero_card(rho_air, a_sound)
        
        # Material and property
        self._add_material_property(E, nu, rho, thickness)
        
        # Structural mesh
        self._add_structural_mesh(length, width, nx, ny)
        
        # Boundary conditions
        self._add_boundary_conditions(nx, ny)
        
        # Aerodynamic model
        self._add_aerodynamic_model(length, width)
        
        # Flutter analysis setup
        self._add_flutter_setup(rho_air, mach)
        
        # End
        self.cards.append("ENDDATA")
    
    def _add_param_cards(self, damping):
        """Add PARAM cards for flutter analysis"""
        self.cards.extend([
            "$ Parameter cards",
            "PARAM   GRDPNT  0",
            "PARAM   WTMASS  0.00259",
            f"PARAM   G       {damping:.3f}",
            "PARAM   KDAMP   -1",
            "PARAM   LMODES  10",
            "PARAM   VREF    1.0",
            "$"
        ])
    
    def _add_aero_card(self, rho_air, a_sound):
        """Add AERO reference card"""
        self.cards.extend([
            "$ Aerodynamic reference",
            f"AERO    0       1.0     {rho_air:.3E}{a_sound:.1f}1.0     1",
            "$"
        ])
    
    def _add_material_property(self, E, nu, rho, thickness):
        """Add material and property cards"""
        self.cards.extend([
            "$ Material",
            f"MAT1    1       {E:.3E}        {nu:.3f} {rho:.1f}",
            "$ Property", 
            f"PSHELL  1       1       {thickness:.5f}1               1",
            "$"
        ])
    
    def _add_structural_mesh(self, length, width, nx, ny):
        """Add structural grid and elements"""
        self.cards.append("$ Grid points")
        
        grid_id = 1
        dx = length / nx
        dy = width / ny
        
        # Grid points
        for i in range(nx + 1):
            for j in range(ny + 1):
                x = i * dx
                y = j * dy
                z = 0.0
                self.cards.append(
                    f"GRID    {grid_id:<8d}        {x:<8.4f}{y:<8.4f}{z:<8.4f}"
                )
                grid_id += 1
        
        self.cards.append("$ Elements")
        
        # CQUAD4 elements
        elem_id = 1
        for i in range(nx):
            for j in range(ny):
                n1 = i * (ny + 1) + j + 1
                n2 = n1 + 1
                n3 = (i + 1) * (ny + 1) + j + 2
                n4 = n3 - 1
                self.cards.append(
                    f"CQUAD4  {elem_id:<8d}1       {n1:<8d}{n2:<8d}{n3:<8d}{n4:<8d}"
                )
                elem_id += 1
        
        self.cards.append("$")
    
    def _add_boundary_conditions(self, nx, ny):
        """Add boundary conditions"""
        self.cards.append("$ Boundary conditions")
        
        # Simply supported edges - fix Z displacement
        # Left edge
        for j in range(ny + 1):
            grid_id = j + 1
            self.cards.append(f"SPC1    1       3       {grid_id}")
        
        # Right edge
        for j in range(ny + 1):
            grid_id = nx * (ny + 1) + j + 1
            self.cards.append(f"SPC1    1       3       {grid_id}")
        
        self.cards.append("$")
    
    def _add_aerodynamic_model(self, length, width):
        """Add aerodynamic panels and splines"""
        self.cards.extend([
            "$ Aerodynamic panel",
            "CAERO1  1001    1002    0       1       4       1       1",
            "+       0.0     0.0     0.0     1.0     0.0     1.0     0.0     0.0",
            f"+       {length:.4f}1.0     0.0     1.0     {width:.4f}1.0     0.0     0.0",
            "$ Spline",
            "SPLINE1 1       1001    1002    ALL",
            "$"
        ])
    
    def _add_flutter_setup(self, rho_air, mach):
        """Add flutter analysis cards"""
        
        # Eigenvalue extraction
        self.cards.extend([
            "$ Eigenvalues",
            "EIGRL   10              0.1     100.0   10              MASS",
            "$"
        ])
        
        # FLFACT cards
        self.cards.extend([
            "$ Flutter parameters",
            "$ Mach numbers",
            "FLFACT  1       0.3     0.5     0.7     0.9     1.1     1.3     1.5",
            "$ Reduced frequencies",
            "FLFACT  2       0.001   0.01    0.1     0.3     0.5     1.0",
            "$ Densities",
            f"FLFACT  3       {rho_air:.3E}",
            "$ Velocities",
            "FLFACT  4       50.     100.    150.    200.    250.    300.    350.",
            "FLFACT  4       400.    450.    500.",
            "$"
        ])
        
        # FLUTTER card
        self.cards.extend([
            "$ Flutter solution",
            "FLUTTER 20      PK      1       2       3       L       4",
            "+       1.0-4   1.0-3",
            "$"
        ])
        
        # MKAERO1 cards
        self.cards.extend([
            "$ Aerodynamic matrices",
            "MKAERO1 0.0     0.3     0.5     0.7     0.9     1.1     1.3     1.5",
            "MKAERO1 0.001   0.01    0.1     0.3     0.5     1.0",
            "$"
        ])
    
    def _calculate_air_properties(self, altitude):
        """Calculate air properties at altitude"""
        if altitude <= 11000:
            T = 288.15 - 0.0065 * altitude
            p = 101325 * (T / 288.15) ** 5.2561
        else:
            T = 216.65
            p = 22632 * np.exp(-0.0001577 * (altitude - 11000))
        
        rho = p / (287.0 * T)
        a = np.sqrt(1.4 * 287.0 * T)
        
        return rho, a
