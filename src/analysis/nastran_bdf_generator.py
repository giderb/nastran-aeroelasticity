"""
NASTRAN BDF Generator for Panel Flutter Analysis
"""

import numpy as np
from datetime import datetime

class NastranBDFGenerator:
    """Generate NASTRAN BDF files for panel flutter analysis"""
    
    def __init__(self):
        self.cards = []
    
    def generate_bdf(self, config):
        """Generate BDF content from configuration"""
        self.cards = []
        
        # Header
        self._add_header()
        
        # Executive control
        self._add_executive_control()
        
        # Case control
        self._add_case_control(config)
        
        # Bulk data
        self._add_bulk_data(config)
        
        return '\n'.join(self.cards)
    
    def _add_header(self):
        """Add BDF header"""
        self.cards.extend([
            "$ NASTRAN BDF File",
            f"$ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "$ Panel Flutter Analysis",
            "$"
        ])
    
    def _add_executive_control(self):
        """Add executive control section"""
        self.cards.extend([
            "ID PANEL,FLUTTER",
            "SOL 145",  # Flutter analysis
            "TIME 600",
            "CEND"
        ])
    
    def _add_case_control(self, config):
        """Add case control section"""
        self.cards.extend([
            "TITLE = Panel Flutter Analysis",
            "ECHO = NONE",
            "DISPLACEMENT = ALL",
            "SPCFORCE = ALL",
            "STRESS = ALL",
            "FORCE = ALL",
            "ESE = ALL",
            "METHOD = 1",
            "FMETHOD = 2",
            "SPC = 1",
            "BEGIN BULK"
        ])
    
    def _add_bulk_data(self, config):
        """Add bulk data section"""
        # Get geometry parameters
        geom = config.get('geometry', {})
        length = geom.get('length', 1.0)
        width = geom.get('width', 0.5)
        thickness = geom.get('thickness', 0.002)
        nx = geom.get('nx', 10)
        ny = geom.get('ny', 5)
        
        # Get material properties
        mat = config.get('material', {})
        E = mat.get('E', 70e9)
        nu = mat.get('nu', 0.3)
        rho = mat.get('rho', 2700)
        
        # Material card
        self.cards.append(f"MAT1    1       {E:.2E}        {nu:.3f} {rho:.3f}")
        
        # Shell property
        self.cards.append(f"PSHELL  1       1       {thickness:.4f}")
        
        # Generate grid points
        grid_id = 1
        dx = length / nx
        dy = width / ny
        
        for i in range(nx + 1):
            for j in range(ny + 1):
                x = i * dx
                y = j * dy
                z = 0.0
                self.cards.append(f"GRID    {grid_id:<8d}        {x:<8.3f}{y:<8.3f}{z:<8.3f}")
                grid_id += 1
        
        # Generate CQUAD4 elements
        elem_id = 1
        for i in range(nx):
            for j in range(ny):
                n1 = i * (ny + 1) + j + 1
                n2 = n1 + 1
                n3 = (i + 1) * (ny + 1) + j + 2
                n4 = n3 - 1
                self.cards.append(f"CQUAD4  {elem_id:<8d}1       {n1:<8d}{n2:<8d}{n3:<8d}{n4:<8d}")
                elem_id += 1
        
        # Boundary conditions
        boundary = config.get('boundary', 'Clamped-Free')
        if 'Clamped' in boundary:
            # Clamp left edge
            for j in range(ny + 1):
                grid_id = j + 1
                self.cards.append(f"SPC1    1       123456  {grid_id}")
        
        # Eigenvalue extraction
        self.cards.append("EIGRL   1               0       100")
        
        # Flutter cards
        self.cards.append("FLUTTER 2       PK      1       2       3")
        self.cards.append("MKAERO1 0.0     0.2     0.4     0.6     0.8     1.0")
        self.cards.append("MKAERO1 1.2     1.4     1.6     1.8     2.0")
        
        # End bulk
        self.cards.append("ENDDATA")
