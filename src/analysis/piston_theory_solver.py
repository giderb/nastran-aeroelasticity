"""
Piston Theory Flutter Analysis Solver (Level 1)
===============================================

Implements simplified flutter analysis using piston theory aerodynamics
and analytical structural models. Suitable for preliminary design and
high-speed (supersonic) flow conditions.

References:
- Ashley, H. and Zartarian, G., "Piston Theory - A New Aerodynamic Tool for the Aeroelastician"
- Dowell, E.H., "A Modern Course in Aeroelasticity"
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math

from .boundary_conditions import BoundaryCondition, BoundaryConditionManager

# Simple implementations to replace scipy dependencies
def simple_eig(A, B=None):
    """Simplified eigenvalue solver using numpy"""
    if B is None:
        return np.linalg.eig(A)
    else:
        # Generalized eigenvalue problem: solve A*x = lambda*B*x
        try:
            B_inv = np.linalg.inv(B)
            return np.linalg.eig(B_inv @ A)
        except:
            return np.linalg.eig(A), None

def simple_brentq(f, a, b, xtol=1e-12, maxiter=100):
    """Simple Brent's method root finding"""
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("Function must have different signs at bounds")
    
    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa
    
    c = a
    fc = fa
    
    for i in range(maxiter):
        if abs(b - a) < xtol:
            return b
        
        if abs(fc - fb) > 1e-15 and abs(fa - fb) > 1e-15:
            # Inverse quadratic interpolation
            s = a * fb * fc / ((fa - fb) * (fa - fc)) + \
                b * fa * fc / ((fb - fa) * (fb - fc)) + \
                c * fa * fb / ((fc - fa) * (fc - fb))
        else:
            # Secant method
            s = b - fb * (b - a) / (fb - fa)
        
        fs = f(s)
        
        if fs * fb < 0:
            a, fa = b, fb
        else:
            fa = fs
        
        b, fb = s, fs
        c, fc = a, fa
    
    return b

@dataclass
class FlutterResult:
    """Results from flutter analysis"""
    flutter_speed: float  # m/s
    flutter_frequency: float  # Hz
    flutter_mode: int
    damping: float
    method: str
    mach_number: float
    dynamic_pressure: float  # Pa

@dataclass 
class PanelProperties:
    """Panel geometric and material properties"""
    length: float  # m
    width: float   # m  
    thickness: float  # m
    youngs_modulus: float  # Pa
    poissons_ratio: float
    density: float  # kg/m³
    boundary_conditions: BoundaryCondition = BoundaryCondition.SSSS
    
    def __post_init__(self):
        """Post-initialization to handle legacy string boundary conditions"""
        if isinstance(self.boundary_conditions, str):
            # Convert legacy string format to BoundaryCondition enum
            bc_manager = BoundaryConditionManager()
            parsed_bc = bc_manager.parse_boundary_condition(self.boundary_conditions)
            if parsed_bc:
                self.boundary_conditions = parsed_bc
            else:
                logging.warning(f"Unknown boundary condition '{self.boundary_conditions}', defaulting to SSSS")
                self.boundary_conditions = BoundaryCondition.SSSS

@dataclass
class FlowConditions:
    """Flow environment properties"""
    mach_number: float
    altitude: float  # m
    temperature: float = 288.15  # K (ISA standard)
    
class AtmosphereModel:
    """Standard atmosphere model for air properties"""
    
    @staticmethod
    def get_properties(altitude: float) -> Tuple[float, float, float]:
        """
        Get air properties at altitude
        
        Returns:
            density (kg/m³), sound_speed (m/s), pressure (Pa)
        """
        # ISA Standard Atmosphere
        if altitude <= 11000:  # Troposphere
            T = 288.15 - 0.0065 * altitude
            p = 101325 * (T / 288.15) ** 5.2561
        else:  # Stratosphere (simplified)
            T = 216.65
            p = 22632 * np.exp(-0.0001577 * (altitude - 11000))
            
        rho = p / (287.0 * T)  # R = 287 J/(kg·K) for air
        a = np.sqrt(1.4 * 287.0 * T)  # Sound speed
        
        return rho, a, p

class PistonTheorySolver:
    """
    Piston Theory Flutter Analysis Solver
    
    Implements flutter analysis using:
    - Piston theory for aerodynamic forces
    - Rayleigh-Ritz method for structural analysis
    - Simply supported boundary conditions
    - Multiple structural modes
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bc_manager = BoundaryConditionManager()
        
    def analyze_flutter(self, panel: PanelProperties, 
                       flow: FlowConditions,
                       velocity_range: Tuple[float, float] = (50, 500),
                       num_points: int = 50) -> List[FlutterResult]:
        """
        Perform flutter analysis using piston theory
        
        Args:
            panel: Panel properties
            flow: Flow conditions  
            velocity_range: Velocity range to analyze (m/s)
            num_points: Number of velocity points
            
        Returns:
            List of flutter results
        """
        self.logger.info("Starting piston theory flutter analysis")
        
        # Get atmospheric properties
        rho_air, sound_speed, pressure = AtmosphereModel.get_properties(flow.altitude)
        
        # Calculate panel properties
        D = self._calculate_flexural_rigidity(panel)
        natural_frequencies = self._calculate_natural_frequencies(panel, D)
        
        # Velocity sweep
        velocities = np.linspace(velocity_range[0], velocity_range[1], num_points)
        results = []
        
        for V in velocities:
            mach = V / sound_speed
            
            # Skip very low Mach numbers for piston theory
            if mach < 0.3:
                continue
                
            if mach < 0.5:
                self.logger.debug(f"Piston theory not accurate for M={mach:.2f} < 0.5")
                
            # Analyze each structural mode
            for mode_idx, omega_n in enumerate(natural_frequencies[:5]):  # First 5 modes
                result = self._analyze_mode(panel, flow, V, mach, omega_n, 
                                          mode_idx + 1, rho_air, sound_speed)
                if result:
                    results.append(result)
        
        # Sort by flutter speed
        flutter_results = [r for r in results if r.damping < 0]  # Unstable modes
        flutter_results.sort(key=lambda x: x.flutter_speed)
        
        self.logger.info(f"Found {len(flutter_results)} flutter points")
        return flutter_results
    
    def _calculate_flexural_rigidity(self, panel: PanelProperties) -> float:
        """Calculate flexural rigidity D = Et³/(12(1-ν²))"""
        return (panel.youngs_modulus * panel.thickness**3) / \
               (12 * (1 - panel.poissons_ratio**2))
    
    def _calculate_natural_frequencies(self, panel: PanelProperties, D: float) -> List[float]:
        """
        Calculate natural frequencies for panel with specified boundary conditions
        
        Uses classical plate theory with boundary condition corrections:
        ω_mn = π²√(D/(ρt)) * λ_mn * √((m/a)² + (n/b)²)
        where λ_mn is the boundary condition factor
        """
        frequencies = []
        
        # Get boundary condition properties
        bc_props = self.bc_manager.get_boundary_condition(panel.boundary_conditions)
        
        # Define modes based on boundary condition
        if panel.boundary_conditions in [BoundaryCondition.CFFF, BoundaryCondition.SFFF]:
            # Cantilever-like modes - bending and torsion modes dominate
            modes = [(1,0), (2,0), (3,0), (0,1), (1,1), (4,0), (0,2), (2,1), (1,2)]
        elif panel.boundary_conditions == BoundaryCondition.FFFF:
            # Free-free includes rigid body modes (exclude them)
            modes = [(1,1), (1,2), (2,1), (2,2), (1,3), (3,1), (2,3), (3,2)]
        else:
            # Standard modes for most boundary conditions
            modes = [(1,1), (1,2), (2,1), (2,2), (1,3), (3,1), (2,3), (3,2), (3,3)]
        
        # Base coefficient 
        base_coeff = np.pi**2 * np.sqrt(D / (panel.density * panel.thickness))
        
        for m, n in modes:
            # Get frequency factor for this boundary condition and mode
            freq_factor = self.bc_manager.get_natural_frequency_factors(
                panel.boundary_conditions, (m, n)
            )
            
            if panel.boundary_conditions in [BoundaryCondition.CFFF, BoundaryCondition.SFFF] and n == 0:
                # Special case for cantilever bending modes
                # Use beam theory: ω = λ²√(EI/(ρAL⁴)) where λ depends on mode
                cantilever_factors = {1: 1.875, 2: 4.694, 3: 7.855, 4: 10.996}
                if m in cantilever_factors:
                    # Convert to plate bending frequency
                    I = panel.width * panel.thickness**3 / 12  # Moment of inertia per unit width
                    A = panel.width * panel.thickness  # Area per unit width
                    lambda_m = cantilever_factors[m]
                    freq = (lambda_m**2 / (2 * np.pi * panel.length**2)) * np.sqrt(
                        panel.youngs_modulus * I / (panel.density * A)
                    )
                else:
                    freq = base_coeff * freq_factor * np.sqrt((m/panel.length)**2 + (n/panel.width)**2)
            else:
                # Standard plate modes with boundary condition correction
                freq = base_coeff * freq_factor * np.sqrt((m/panel.length)**2 + (n/panel.width)**2)
            
            frequencies.append(freq)
        
        # Log boundary condition effect
        if bc_props:
            self.logger.debug(f"Using {bc_props.name} boundary condition")
            self.logger.debug(f"Structural stiffness factor: {bc_props.structural_stiffness}")
            
        return frequencies
    
    def _analyze_mode(self, panel: PanelProperties, flow: FlowConditions,
                     velocity: float, mach: float, omega_n: float, 
                     mode_num: int, rho_air: float, sound_speed: float) -> Optional[FlutterResult]:
        """
        Analyze flutter for a specific structural mode
        
        Uses piston theory: Δp = (2ρ_air * V / β) * (∂w/∂t + V * ∂w/∂x)
        where β = √(M² - 1) for supersonic, β = √(1 - M²) for subsonic
        """
        
        try:
            # Piston theory parameter (avoid numerical issues)
            if mach > 1.05:  # Clear supersonic
                beta = np.sqrt(mach**2 - 1)
            elif mach < 0.95:  # Clear subsonic
                beta = np.sqrt(abs(1 - mach**2))
            else:  # Transonic region - avoid piston theory
                return None
            
            # Generalized aerodynamic force coefficient with boundary condition effects
            # Base piston theory coefficient
            aero_coeff_base = (2 * rho_air * velocity) / beta
            
            # Apply boundary condition correction to aerodynamic coefficient
            # Different mode shapes have different aerodynamic effectiveness
            bc_props = self.bc_manager.get_boundary_condition(panel.boundary_conditions)
            
            if panel.boundary_conditions == BoundaryCondition.CFFF:
                # Cantilever configuration - reduced aerodynamic effectiveness
                aero_efficiency = 0.7  # Reduced due to constrained leading edge
            elif panel.boundary_conditions == BoundaryCondition.CCCC:
                # Clamped all edges - higher aerodynamic effectiveness in center
                aero_efficiency = 0.9
            elif panel.boundary_conditions == BoundaryCondition.FFFF:
                # Free all edges - maximum aerodynamic effectiveness
                aero_efficiency = 1.1
            else:
                # Standard simply supported and mixed conditions
                aero_efficiency = 1.0
            
            aero_coeff = aero_coeff_base * aero_efficiency
            
            # Modal mass with boundary condition effects
            # Different boundary conditions affect the effective modal mass
            if panel.boundary_conditions == BoundaryCondition.SSSS:
                modal_mass = panel.density * panel.thickness * panel.length * panel.width / 4
            elif panel.boundary_conditions == BoundaryCondition.CCCC:
                modal_mass = panel.density * panel.thickness * panel.length * panel.width / 4 * 1.1  # Slight increase
            elif panel.boundary_conditions == BoundaryCondition.CFFF:
                modal_mass = panel.density * panel.thickness * panel.length * panel.width / 4 * 0.8  # Reduced effective mass
            elif panel.boundary_conditions == BoundaryCondition.FFFF:
                modal_mass = panel.density * panel.thickness * panel.length * panel.width / 4 * 0.9  # Slightly reduced
            else:
                # Interpolate for mixed conditions
                modal_mass = panel.density * panel.thickness * panel.length * panel.width / 4
            
            # Aerodynamic damping and stiffness
            c_aero = aero_coeff * panel.length * panel.width / 4  # Modal aerodynamic damping
            k_aero = c_aero * velocity * np.pi / panel.length    # Modal aerodynamic stiffness
            
            # Modal structural stiffness
            k_struct = modal_mass * omega_n**2
            
            # Flutter equation: s²m + s*c_aero + (k_struct - k_aero) = 0
            # where s = iω (assuming harmonic motion)
            
            # Solve characteristic equation
            a = modal_mass
            b = c_aero
            c = k_struct - k_aero
            
            # Discriminant
            discriminant = b**2 - 4*a*c
            
            if discriminant >= 0:
                # Real roots - no flutter
                damping_ratio = b / (2 * np.sqrt(a * c)) if c > 0 else float('inf')
                frequency = np.sqrt(c / a) / (2 * np.pi) if c > 0 else 0
            else:
                # Complex roots - potential flutter
                freq_rad = np.sqrt(abs(c) / a)
                frequency = freq_rad / (2 * np.pi)
                damping_ratio = -b / (2 * a * freq_rad)
            
            # Check for flutter (negative damping)
            if damping_ratio < 0:
                dynamic_pressure = 0.5 * rho_air * velocity**2
                
                return FlutterResult(
                    flutter_speed=velocity,
                    flutter_frequency=frequency,
                    flutter_mode=mode_num,
                    damping=damping_ratio,
                    method="Piston Theory",
                    mach_number=mach,
                    dynamic_pressure=dynamic_pressure
                )
                
        except Exception as e:
            self.logger.error(f"Error analyzing mode {mode_num} at V={velocity}: {e}")
            
        return None
    
    def find_critical_flutter_speed(self, panel: PanelProperties,
                                   flow: FlowConditions,
                                   velocity_range: Tuple[float, float] = (50, 500)) -> Optional[FlutterResult]:
        """
        Find the critical (lowest) flutter speed using root finding
        
        Returns:
            Critical flutter result or None if no flutter found
        """
        
        def flutter_equation(V):
            """Flutter boundary condition (zero damping)"""
            results = self.analyze_flutter(panel, flow, (V, V+1), 2)
            if results:
                return min([r.damping for r in results])
            return 1.0  # Stable (positive damping)
        
        try:
            # Find root where damping crosses zero
            
            # Check bounds
            if flutter_equation(velocity_range[0]) * flutter_equation(velocity_range[1]) > 0:
                self.logger.warning("No flutter found in velocity range")
                return None
                
            # Find critical flutter speed
            V_flutter = simple_brentq(flutter_equation, velocity_range[0], velocity_range[1])
            
            # Get detailed results at flutter speed
            results = self.analyze_flutter(panel, flow, (V_flutter-5, V_flutter+5), 11)
            critical_result = min(results, key=lambda x: abs(x.damping)) if results else None
            
            return critical_result
            
        except Exception as e:
            self.logger.error(f"Error finding critical flutter speed: {e}")
            return None

class PistonTheoryValidator:
    """Validation class for piston theory results"""
    
    @staticmethod
    def validate_against_reference(panel: PanelProperties, 
                                 flow: FlowConditions,
                                 expected_flutter_speed: float,
                                 tolerance: float = 0.15) -> bool:
        """
        Validate piston theory results against reference data
        
        Args:
            panel: Panel properties
            flow: Flow conditions
            expected_flutter_speed: Reference flutter speed (m/s)
            tolerance: Acceptable relative error
            
        Returns:
            True if within tolerance
        """
        solver = PistonTheorySolver()
        result = solver.find_critical_flutter_speed(panel, flow)
        
        if not result:
            return False
            
        relative_error = abs(result.flutter_speed - expected_flutter_speed) / expected_flutter_speed
        return relative_error <= tolerance

# Example usage and validation
if __name__ == "__main__":
    
    # Example panel (aluminum aircraft panel)
    panel = PanelProperties(
        length=0.5,           # 500mm
        width=0.3,            # 300mm  
        thickness=0.002,      # 2mm
        youngs_modulus=71.7e9, # Al 7075-T6
        poissons_ratio=0.33,
        density=2810,         # kg/m³
        boundary_conditions="SSSS"
    )
    
    # High altitude supersonic conditions
    flow = FlowConditions(
        mach_number=2.0,
        altitude=10000  # 10 km
    )
    
    # Analyze flutter
    solver = PistonTheorySolver()
    
    print("Piston Theory Flutter Analysis")
    print("=" * 40)
    print(f"Panel: {panel.length*1000}×{panel.width*1000}×{panel.thickness*1000} mm")
    print(f"Material: E={panel.youngs_modulus/1e9:.1f} GPa, ρ={panel.density} kg/m³")
    print(f"Flow: M={flow.mach_number}, Alt={flow.altitude/1000:.1f} km")
    print()
    
    # Find critical flutter speed
    critical_result = solver.find_critical_flutter_speed(panel, flow)
    
    if critical_result:
        print(f"Critical Flutter Speed: {critical_result.flutter_speed:.1f} m/s")
        print(f"Flutter Frequency: {critical_result.flutter_frequency:.1f} Hz") 
        print(f"Flutter Mode: {critical_result.flutter_mode}")
        print(f"Mach Number at Flutter: {critical_result.mach_number:.2f}")
        print(f"Dynamic Pressure: {critical_result.dynamic_pressure/1000:.1f} kPa")
    else:
        print("No flutter found in analysis range")
    
    # Full analysis
    print("\nDetailed Analysis:")
    results = solver.analyze_flutter(panel, flow, (100, 400), 30)
    
    if results:
        print(f"{'Speed (m/s)':<12} {'Freq (Hz)':<10} {'Mode':<6} {'Damping':<10} {'Mach':<8}")
        print("-" * 50)
        for r in results[:10]:  # First 10 results
            print(f"{r.flutter_speed:<12.1f} {r.flutter_frequency:<10.1f} {r.flutter_mode:<6} "
                  f"{r.damping:<10.3f} {r.mach_number:<8.2f}")