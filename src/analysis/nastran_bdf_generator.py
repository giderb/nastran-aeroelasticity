"""
FIXED NASTRAN BDF Generator for Panel Flutter Analysis
=======================================================
Generates proper SOL 145 BDF files with correct PSHELL thickness.
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
            "$ Complete flutter analysis setup with thickness dependency",
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
        
        # Geometry - CRITICAL: thickness must be in meters
        length = geom.get('length', 0.5)
        width = geom.get('width', 0.3)
        thickness = geom.get('thickness', 0.002)  # CRITICAL PARAMETER
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
        
        # Log thickness for debugging
        print(f"    BDF Generation: thickness = {thickness*1000:.2f} mm ({thickness:.6f} m)")
        
        # PARAM cards - Essential for flutter
        self._add_param_cards(damping)
        
        # AERO card - Reference conditions
        self._add_aero_card(rho_air, a_sound, length)
        
        # Material and property - CRITICAL FIX HERE
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
            "PARAM   WTMASS  0.00259",  # kg to N conversion
            f"PARAM   G       {damping:.3f}",
            "PARAM   KDAMP   -1",
            "PARAM   LMODES  10",
            "PARAM   VREF    1.0",
            "$"
        ])
    
    def _add_aero_card(self, rho_air, a_sound, ref_chord):
        """Add AERO reference card with proper reference chord"""
        # AERO card format:
        # AERO ACSID VELOCITY REFC RHOREF SYMXZ SYMXY
        self.cards.extend([
            "$ Aerodynamic reference conditions",
            f"AERO    0       1.0     {ref_chord:.3f}  {rho_air:.3E}1       1",
            "$"
        ])
    
    def _add_material_property(self, E, nu, rho, thickness):
        """Add material and property cards - CRITICAL FIX"""
        
        # MAT1 card - material properties
        self.cards.extend([
            "$ Material properties",
            f"MAT1    1       {E:.3E}        {nu:.3f} {rho:.1f}",
            "$"
        ])
        
        # PSHELL card - CRITICAL: proper format for thickness
        # Format: PSHELL PID MID T MID2 12I/T**3 MID3 TS/T NSM
        # Field 4 (T) is the thickness - MUST be properly formatted
        
        # Convert thickness to proper format
        t_str = f"{thickness:.6f}"  # Use 6 decimal places for precision
        
        # IMPORTANT: PSHELL format requires 8-character fields
        # PID=1, MID=1, T=thickness
        pshell_line = "PSHELL  1       1       " + f"{thickness:<8.6f}"
        
        self.cards.extend([
            "$ Shell property - thickness is CRITICAL for flutter",
            f"$ Thickness = {thickness*1000:.2f} mm",
            pshell_line,
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
        
        self.cards.append("$ Shell elements")
        
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
        self.cards.append("$ Boundary conditions - Simply supported")
        
        # Fix Z displacement on all edges for simply supported
        # Left edge (x=0)
        for j in range(ny + 1):
            grid_id = j + 1
            self.cards.append(f"SPC1    1       3       {grid_id}")
        
        # Right edge (x=L)
        for j in range(ny + 1):
            grid_id = nx * (ny + 1) + j + 1
            self.cards.append(f"SPC1    1       3       {grid_id}")
        
        # Bottom edge (y=0)
        for i in range(1, nx):  # Skip corners
            grid_id = i * (ny + 1) + 1
            self.cards.append(f"SPC1    1       3       {grid_id}")
        
        # Top edge (y=W)
        for i in range(1, nx):  # Skip corners
            grid_id = i * (ny + 1) + ny + 1
            self.cards.append(f"SPC1    1       3       {grid_id}")
        
        self.cards.append("$")
    
    def _add_aerodynamic_model(self, length, width):
        """Add aerodynamic panels and splines"""
        
        # CAERO1 - Doublet lattice aerodynamic panel
        self.cards.extend([
            "$ Aerodynamic panel definition",
            "CAERO1  1001    1002    0       1       10      5       1",
            f"+       0.0     0.0     0.0     {length:.3f}  0.0     {width:.3f}   0.0     0.0",
            "$ Spline to connect structure and aerodynamics",
            "SPLINE1 1       1001    1002    ALL",
            "$"
        ])
    
    def _add_flutter_setup(self, rho_air, mach):
        """Add flutter analysis cards"""
        
        # Eigenvalue extraction
        self.cards.extend([
            "$ Eigenvalue extraction",
            "EIGRL   10              0.1     100.0   10              MASS",
            "$"
        ])
        
        # FLFACT cards - parameter lists
        self.cards.extend([
            "$ Flutter parameters",
            "$ Mach numbers",
            "FLFACT  1       0.3     0.5     0.7     0.9     1.1     1.3     1.5",
            "$ Reduced frequencies",
            "FLFACT  2       0.001   0.01    0.1     0.3     0.5     1.0",
            "$ Air density",
            f"FLFACT  3       {rho_air:.3E}",
            "$ Velocities (m/s)",
            "FLFACT  4       50.     100.    150.    200.    250.    300.    350.",
            "FLFACT  4       400.    450.    500.    550.    600.",
            "$"
        ])
        
        # FLUTTER card - PK method
        self.cards.extend([
            "$ Flutter solution - PK method",
            "FLUTTER 20      PK      1       2       3       L       4",
            "+       1.0-4   1.0-3",
            "$"
        ])
        
        # MKAERO1 - aerodynamic matrix interpolation
        self.cards.extend([
            "$ Aerodynamic matrix generation",
            "MKAERO1 0.3     0.5     0.7     0.9     1.1     1.3     1.5",
            "MKAERO1 0.001   0.01    0.1     0.3     0.5     1.0",
            "$"
        ])
        
        # TABDMP1 - Structural damping
        self.cards.extend([
            "$ Structural damping table",
            "TABDMP1 30      CRIT",
            "+       0.0     0.02    100.0   0.02    ENDT",
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
