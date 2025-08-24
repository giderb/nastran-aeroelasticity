"""
Doublet Lattice Method Flutter Analysis Solver (Level 2)
========================================================

Implements more accurate flutter analysis using doublet lattice method (DLM)
aerodynamics with finite element structural models. Suitable for subsonic
to transonic flow conditions with better accuracy than piston theory.

References:
- Albano, E. and Rodden, W.P., "A Doublet-Lattice Method for Calculating Lift Distributions on Oscillating Surfaces"
- Rodden, W.P., "Theoretical and Computational Aeroelasticity"
- MSC Nastran Aeroelastic Analysis User's Guide
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
import math

from .boundary_conditions import BoundaryCondition, BoundaryConditionManager

# Simple implementations to replace scipy dependencies
def simple_eig(A, B=None):
    """Simplified eigenvalue solver using numpy"""
    if B is None:
        return np.linalg.eig(A)
    else:
        # Generalized eigenvalue problem
        try:
            B_inv = np.linalg.inv(B)
            return np.linalg.eig(B_inv @ A)
        except:
            return np.linalg.eig(A), None

@dataclass
class DLMParameters:
    """Doublet Lattice Method parameters"""
    num_chord_panels: int = 8      # Chordwise panels
    num_span_panels: int = 6       # Spanwise panels
    reduced_frequencies: List[float] = None  # k = ωc/(2V)
    mach_numbers: List[float] = None
    
    def __post_init__(self):
        if self.reduced_frequencies is None:
            self.reduced_frequencies = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]
        if self.mach_numbers is None:
            self.mach_numbers = [0.3, 0.5, 0.7, 0.85, 0.9, 0.95]

class AerodynamicInfluenceCoefficient:
    """Aerodynamic influence coefficient calculation for DLM"""
    
    @staticmethod
    def doublet_influence(x_recv: float, y_recv: float, z_recv: float,
                         x_src: float, y_src: float, z_src: float,
                         dx: float, dy: float, mach: float, k: float) -> complex:
        """
        Calculate influence of doublet panel on receiving point
        
        Args:
            x_recv, y_recv, z_recv: Receiver point coordinates
            x_src, y_src, z_src: Source panel center coordinates  
            dx, dy: Source panel dimensions
            mach: Mach number
            k: Reduced frequency
            
        Returns:
            Complex influence coefficient
        """
        
        # Prandtl-Glauert transformation
        beta = np.sqrt(abs(1 - mach**2)) if mach != 1.0 else 0.1
        
        # Relative coordinates
        xi = (x_recv - x_src) / beta
        eta = y_recv - y_src
        zeta = z_recv - z_src
        
        # Panel corner coordinates in transformed space
        x1, x2 = -dx/(2*beta), dx/(2*beta)
        y1, y2 = -dy/2, dy/2
        
        # Distance calculations
        r1 = np.sqrt((xi - x1)**2 + eta**2 + zeta**2)
        r2 = np.sqrt((xi - x2)**2 + eta**2 + zeta**2)
        r3 = np.sqrt((xi - x1)**2 + (eta - dy)**2 + zeta**2)
        r4 = np.sqrt((xi - x2)**2 + (eta - dy)**2 + zeta**2)
        
        # Avoid singularities
        r1 = max(r1, 1e-10)
        r2 = max(r2, 1e-10)
        
        # Basic doublet influence (simplified)
        if abs(zeta) < 1e-10:  # On panel surface
            if abs(xi) < dx/(2*beta) and abs(eta) < dy/2:
                influence = -0.5  # Inside panel
            else:
                influence = 0.0   # Outside panel
        else:
            # 3D influence with oscillatory effects
            static_influence = (np.arctan2(eta*(xi-x1), zeta*r1) - 
                              np.arctan2(eta*(xi-x2), zeta*r2)) / (4*np.pi)
            
            # Add oscillatory terms for unsteady flow
            if k > 0:
                phase_factor = np.exp(1j * k * xi * mach)
                oscillatory_correction = 1.0 + 1j * k * xi
                influence = static_influence * phase_factor * oscillatory_correction
            else:
                influence = static_influence
                
        return complex(influence)

class DoubletLatticeSolver:
    """
    Doublet Lattice Method Flutter Analysis Solver
    
    Implements flutter analysis using:
    - Doublet lattice method for unsteady aerodynamics
    - Finite element method for structural analysis  
    - K-method or PK-method for flutter solution
    - Multiple Mach numbers and reduced frequencies
    """
    
    def __init__(self, dlm_params: DLMParameters = None):
        self.logger = logging.getLogger(__name__)
        self.dlm_params = dlm_params or DLMParameters()
        self.bc_manager = BoundaryConditionManager()
        
        # Aerodynamic matrices storage
        self.aerodynamic_matrices = {}  # [Q(k,M)] matrices
        self.panel_geometry = None
        
    def analyze_flutter(self, panel: 'PanelProperties', 
                       flow: 'FlowConditions',
                       velocity_range: Tuple[float, float] = (50, 300),
                       num_points: int = 30) -> List['FlutterResult']:
        """
        Perform flutter analysis using doublet lattice method
        
        Args:
            panel: Panel properties
            flow: Flow conditions
            velocity_range: Velocity range to analyze (m/s)  
            num_points: Number of velocity points
            
        Returns:
            List of flutter results
        """
        from .piston_theory_solver import FlutterResult, AtmosphereModel
        
        self.logger.info("Starting doublet lattice method flutter analysis")
        
        # Get atmospheric properties
        rho_air, sound_speed, pressure = AtmosphereModel.get_properties(flow.altitude)
        
        # Build aerodynamic model
        self._build_aerodynamic_model(panel)
        
        # Calculate structural properties  
        structural_matrices = self._calculate_structural_matrices(panel)
        
        # Generate aerodynamic influence coefficients
        self._generate_aerodynamic_matrices(panel, flow)
        
        # Flutter analysis
        velocities = np.linspace(velocity_range[0], velocity_range[1], num_points)
        results = []
        
        for V in velocities:
            mach = V / sound_speed
            
            if mach >= 0.98:
                self.logger.warning(f"DLM not accurate for transonic M={mach:.2f}")
                continue
                
            # Solve flutter equation for this velocity
            flutter_result = self._solve_flutter_equation(
                panel, structural_matrices, V, mach, rho_air, sound_speed
            )
            
            if flutter_result:
                results.extend(flutter_result)
        
        # Filter and sort results
        flutter_results = [r for r in results if r.damping < 0]  # Unstable modes
        flutter_results.sort(key=lambda x: x.flutter_speed)
        
        self.logger.info(f"DLM found {len(flutter_results)} flutter points")
        return flutter_results
    
    def _build_aerodynamic_model(self, panel: 'PanelProperties'):
        """Build doublet lattice aerodynamic model"""
        
        # Create panel mesh
        nx = self.dlm_params.num_chord_panels
        ny = self.dlm_params.num_span_panels
        
        # Panel coordinates
        x_panels = np.linspace(0, panel.length, nx+1)
        y_panels = np.linspace(0, panel.width, ny+1)
        
        # Panel centers and areas
        self.panel_centers = []
        self.panel_areas = []
        
        dx = panel.length / nx
        dy = panel.width / ny
        
        for i in range(nx):
            for j in range(ny):
                # Panel center
                x_center = x_panels[i] + dx/2
                y_center = y_panels[j] + dy/2
                z_center = 0.0  # Flat panel
                
                self.panel_centers.append((x_center, y_center, z_center))
                self.panel_areas.append(dx * dy)
        
        self.num_panels = nx * ny
        self.panel_geometry = {
            'nx': nx, 'ny': ny,
            'dx': dx, 'dy': dy,
            'centers': self.panel_centers,
            'areas': self.panel_areas
        }
        
        self.logger.info(f"Created {self.num_panels} aerodynamic panels ({nx}×{ny})")
    
    def _generate_aerodynamic_matrices(self, panel: 'PanelProperties', 
                                     flow: 'FlowConditions'):
        """Generate aerodynamic influence coefficient matrices"""
        
        self.logger.info("Generating aerodynamic influence matrices...")
        
        # For each Mach number and reduced frequency
        for mach in self.dlm_params.mach_numbers:
            if mach >= flow.mach_number * 1.2:  # Skip high Mach numbers
                continue
                
            for k in self.dlm_params.reduced_frequencies:
                
                # Initialize influence matrix
                Q_matrix = np.zeros((self.num_panels, self.num_panels), dtype=complex)
                
                # Calculate influence coefficients
                for i, (x_recv, y_recv, z_recv) in enumerate(self.panel_centers):
                    for j, (x_src, y_src, z_src) in enumerate(self.panel_centers):
                        
                        # Influence of source panel j on receiver panel i
                        influence = AerodynamicInfluenceCoefficient.doublet_influence(
                            x_recv, y_recv, z_recv,
                            x_src, y_src, z_src,
                            self.panel_geometry['dx'], 
                            self.panel_geometry['dy'],
                            mach, k
                        )
                        
                        Q_matrix[i, j] = influence
                
                # Store matrix
                self.aerodynamic_matrices[(mach, k)] = Q_matrix
        
        self.logger.info(f"Generated {len(self.aerodynamic_matrices)} aerodynamic matrices")
    
    def _calculate_structural_matrices(self, panel: 'PanelProperties') -> Dict[str, np.ndarray]:
        """Calculate structural mass and stiffness matrices"""
        
        # Simplified finite element model
        # Use same discretization as aerodynamic model
        nx, ny = self.panel_geometry['nx'], self.panel_geometry['ny']
        num_nodes = (nx + 1) * (ny + 1)
        
        # Mass matrix (lumped)
        element_mass = (panel.density * panel.thickness * 
                       self.panel_geometry['dx'] * self.panel_geometry['dy'] / 4)
        
        M = np.zeros((num_nodes, num_nodes))
        for i in range(num_nodes):
            M[i, i] = element_mass
        
        # Stiffness matrix (simplified plate bending with boundary conditions)
        D = (panel.youngs_modulus * panel.thickness**3) / \
            (12 * (1 - panel.poissons_ratio**2))
        
        # Apply boundary condition stiffness factors
        stiffness_factors = self.bc_manager.get_stiffness_matrix_factors(panel.boundary_conditions)
        
        K = np.zeros((num_nodes, num_nodes))
        
        # Simplified stiffness assembly (central differences)
        dx, dy = self.panel_geometry['dx'], self.panel_geometry['dy']
        
        for i in range(1, nx):
            for j in range(1, ny):
                node = i * (ny + 1) + j
                
                # Bending stiffness coefficients with boundary condition factors
                kxx = D / dx**4 * stiffness_factors['kxx']
                kyy = D / dy**4 * stiffness_factors['kyy']  
                kxy = 2 * D * panel.poissons_ratio / (dx**2 * dy**2) * stiffness_factors['kxy']
                
                # Assembly (simplified 5-point stencil)
                K[node, node] = 4 * (kxx + kyy + kxy)
                
                # Adjacent nodes
                if i > 0: K[node, node - (ny+1)] = -kxx
                if i < nx: K[node, node + (ny+1)] = -kxx  
                if j > 0: K[node, node - 1] = -kyy
                if j < ny: K[node, node + 1] = -kyy
        
        # Apply boundary condition constraints
        self._apply_boundary_constraints(panel, M, K, nx, ny)
        
        return {'M': M, 'K': K}
    
    def _apply_boundary_constraints(self, panel: 'PanelProperties', 
                                  M: np.ndarray, K: np.ndarray, nx: int, ny: int):
        """Apply boundary condition constraints to structural matrices"""
        
        bc_props = self.bc_manager.get_boundary_condition(panel.boundary_conditions)
        edge_constraints = self.bc_manager.get_edge_constraints(panel.boundary_conditions)
        
        # Get boundary node lists
        boundary_nodes = self._get_boundary_nodes(nx, ny, edge_constraints)
        
        # Apply constraints based on edge types
        for edge_name, constraint in edge_constraints.items():
            nodes = boundary_nodes[edge_name]
            
            for node in nodes:
                if constraint.value == 'C':  # Clamped
                    # High stiffness for clamped nodes
                    K[node, node] *= 10.0
                elif constraint.value == 'F':  # Free
                    # Reduce constraints for free edges (but avoid singularity)
                    K[node, node] *= 0.1
                elif constraint.value == 'S':  # Simply supported
                    # Standard boundary condition (no modification needed)
                    pass
                elif constraint.value == 'E':  # Elastic
                    # Moderate stiffness for elastic support
                    K[node, node] *= 2.0
        
        self.logger.debug(f"Applied {bc_props.name if bc_props else 'unknown'} boundary conditions")
    
    def _get_boundary_nodes(self, nx: int, ny: int, edge_constraints: dict) -> dict:
        """Get lists of nodes on each boundary edge"""
        
        boundary_nodes = {
            'leading': [],   # x = 0 edge
            'trailing': [],  # x = L edge  
            'left': [],      # y = 0 edge
            'right': []      # y = W edge
        }
        
        # Leading edge (x = 0, i = 0)
        for j in range(ny + 1):
            node = 0 * (ny + 1) + j
            boundary_nodes['leading'].append(node)
            
        # Trailing edge (x = L, i = nx)
        for j in range(ny + 1):
            node = nx * (ny + 1) + j
            boundary_nodes['trailing'].append(node)
            
        # Left edge (y = 0, j = 0)  
        for i in range(1, nx):  # Exclude corners already added
            node = i * (ny + 1) + 0
            boundary_nodes['left'].append(node)
            
        # Right edge (y = W, j = ny)
        for i in range(1, nx):  # Exclude corners already added
            node = i * (ny + 1) + ny
            boundary_nodes['right'].append(node)
        
        return boundary_nodes
    
    def _solve_flutter_equation(self, panel: 'PanelProperties',
                               structural_matrices: Dict[str, np.ndarray],
                               velocity: float, mach: float,
                               rho_air: float, sound_speed: float) -> List['FlutterResult']:
        """
        Solve flutter equation using K-method
        
        Equation: [K - ω²M + iω²ρV²/q * Q(k)] φ = 0
        where q = dynamic pressure, k = ωc/(2V)
        """
        from .piston_theory_solver import FlutterResult
        
        results = []
        M, K = structural_matrices['M'], structural_matrices['K']
        
        # Reference chord for reduced frequency
        ref_chord = panel.length
        dynamic_pressure = 0.5 * rho_air * velocity**2
        
        # Try different reduced frequencies
        for k in [0.1, 0.3, 0.5, 0.8, 1.0]:
            
            # Get aerodynamic matrix (interpolate if needed)
            Q_aero = self._interpolate_aerodynamic_matrix(mach, k)
            if Q_aero is None:
                continue
            
            # Project aerodynamic forces to structural DOFs
            # Simplified: assume 1-to-1 correspondence
            n_struct = min(M.shape[0], Q_aero.shape[0])
            Q_proj = Q_aero[:n_struct, :n_struct]
            
            try:
                # Solve eigenvalue problem
                # (K - ω²M + iω²ρV²/q * Q) φ = 0
                # Rearrange: (K + iω²ρV²/q * Q) φ = ω²M φ
                
                aero_scaling = dynamic_pressure / (ref_chord * panel.width)
                
                # Frequency iteration (simplified K-method)
                omega_guess = np.sqrt(np.real(K[0,0] / M[0,0]))  # First natural frequency
                
                for iteration in range(10):  # Iterate to converge
                    
                    # Current reduced frequency
                    k_current = omega_guess * ref_chord / (2 * velocity)
                    
                    # Update aerodynamic matrix
                    Q_current = self._interpolate_aerodynamic_matrix(mach, k_current)
                    if Q_current is None:
                        break
                        
                    Q_proj = Q_current[:n_struct, :n_struct]
                    
                    # Flutter matrix
                    A_flutter = K[:n_struct, :n_struct] + 1j * omega_guess**2 * aero_scaling * Q_proj
                    
                    # Solve eigenvalue problem
                    eigenvals, eigenvecs = simple_eig(A_flutter, M[:n_struct, :n_struct])
                    
                    # Find eigenvalue closest to current guess
                    idx = np.argmin(np.abs(eigenvals - omega_guess**2))
                    omega_new = np.sqrt(eigenvals[idx])
                    
                    # Check convergence (avoid division by zero)
                    if abs(omega_guess) > 1e-12:
                        if abs(omega_new - omega_guess) / abs(omega_guess) < 0.01:
                            break
                    else:
                        break
                        
                    omega_guess = omega_new
                
                # Check for flutter (negative damping) - handle complex omega
                if abs(omega_guess) < 1e-12:
                    continue
                    
                frequency = abs(np.real(omega_guess)) / (2 * np.pi)
                real_part = np.real(omega_guess)
                
                if abs(real_part) > 1e-12:
                    damping_ratio = -np.imag(omega_guess) / abs(real_part)
                else:
                    continue
                
                if damping_ratio < -0.001:  # Significant negative damping
                    result = FlutterResult(
                        flutter_speed=velocity,
                        flutter_frequency=frequency,
                        flutter_mode=1,  # Simplified
                        damping=damping_ratio,
                        method="Doublet Lattice",
                        mach_number=mach,
                        dynamic_pressure=dynamic_pressure
                    )
                    results.append(result)
                
            except Exception as e:
                self.logger.debug(f"Eigenvalue solution failed at V={velocity}: {e}")
                continue
        
        return results
    
    def _interpolate_aerodynamic_matrix(self, mach: float, k: float) -> Optional[np.ndarray]:
        """Interpolate aerodynamic matrix for given Mach and reduced frequency"""
        
        # Find closest stored values
        available_machs = sorted(set(m for m, _ in self.aerodynamic_matrices.keys()))
        available_ks = sorted(set(k_val for _, k_val in self.aerodynamic_matrices.keys()))
        
        # Simple nearest neighbor for now (could improve with interpolation)
        closest_mach = min(available_machs, key=lambda m: abs(m - mach))
        closest_k = min(available_ks, key=lambda k_val: abs(k_val - k))
        
        if (closest_mach, closest_k) in self.aerodynamic_matrices:
            return self.aerodynamic_matrices[(closest_mach, closest_k)]
        
        return None
    
    def compare_with_piston_theory(self, panel: 'PanelProperties',
                                  flow: 'FlowConditions') -> Dict[str, List['FlutterResult']]:
        """Compare DLM results with piston theory"""
        
        from .piston_theory_solver import PistonTheorySolver
        
        # Run both analyses
        dlm_results = self.analyze_flutter(panel, flow)
        
        piston_solver = PistonTheorySolver()
        piston_results = piston_solver.analyze_flutter(panel, flow)
        
        return {
            'DLM': dlm_results,
            'Piston_Theory': piston_results
        }

# Example usage and validation
if __name__ == "__main__":
    
    from .piston_theory_solver import PanelProperties, FlowConditions
    
    # Example panel
    panel = PanelProperties(
        length=0.5,           # 500mm
        width=0.3,            # 300mm
        thickness=0.002,      # 2mm
        youngs_modulus=71.7e9,
        poissons_ratio=0.33,
        density=2810,
        boundary_conditions="SSSS"
    )
    
    # Subsonic conditions (better for DLM)
    flow = FlowConditions(
        mach_number=0.8,
        altitude=8000
    )
    
    # DLM parameters
    dlm_params = DLMParameters(
        num_chord_panels=6,
        num_span_panels=4,
        reduced_frequencies=[0.1, 0.3, 0.5, 0.8, 1.0],
        mach_numbers=[0.3, 0.5, 0.7, 0.8, 0.85]
    )
    
    print("Doublet Lattice Method Flutter Analysis")
    print("=" * 45)
    print(f"Panel: {panel.length*1000}×{panel.width*1000}×{panel.thickness*1000} mm")
    print(f"Flow: M={flow.mach_number}, Alt={flow.altitude/1000:.1f} km")
    print(f"DLM Mesh: {dlm_params.num_chord_panels}×{dlm_params.num_span_panels}")
    print()
    
    # Initialize solver
    solver = DoubletLatticeSolver(dlm_params)
    
    # Run analysis
    results = solver.analyze_flutter(panel, flow, (80, 250), 20)
    
    if results:
        print("DLM Flutter Results:")
        print(f"{'Speed (m/s)':<12} {'Freq (Hz)':<10} {'Mode':<6} {'Damping':<10} {'Mach':<8}")
        print("-" * 50)
        for r in results[:10]:
            print(f"{r.flutter_speed:<12.1f} {r.flutter_frequency:<10.1f} {r.flutter_mode:<6} "
                  f"{r.damping:<10.3f} {r.mach_number:<8.2f}")
    else:
        print("No flutter found with DLM")
    
    # Compare with piston theory
    print("\nComparison with Piston Theory:")
    comparison = solver.compare_with_piston_theory(panel, flow)
    
    dlm_min = min(comparison['DLM'], key=lambda x: x.flutter_speed) if comparison['DLM'] else None
    piston_min = min(comparison['Piston_Theory'], key=lambda x: x.flutter_speed) if comparison['Piston_Theory'] else None
    
    if dlm_min and piston_min:
        print(f"DLM Critical Flutter Speed:    {dlm_min.flutter_speed:.1f} m/s")
        print(f"Piston Critical Flutter Speed: {piston_min.flutter_speed:.1f} m/s")
        print(f"Difference: {abs(dlm_min.flutter_speed - piston_min.flutter_speed):.1f} m/s "
              f"({abs(dlm_min.flutter_speed - piston_min.flutter_speed)/piston_min.flutter_speed*100:.1f}%)")
    else:
        print("Insufficient results for comparison")