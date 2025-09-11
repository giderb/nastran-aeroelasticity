"""
Multi-Solver Flutter Analysis Framework
======================================

Integrates multiple flutter analysis methods:
- Level 1: Piston Theory (fast, supersonic)  
- Level 2: Doublet Lattice Method (accurate, subsonic/transonic)
- Level 3: NASTRAN (high fidelity, all conditions)

Provides solver selection, comparison, and validation capabilities.
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt

from .piston_theory_solver import PistonTheorySolver, PanelProperties, FlowConditions, FlutterResult
from .doublet_lattice_solver import DoubletLatticeSolver, DLMParameters
from .nastran_solver import NastranSolver, NastranConfig

class SolverMethod(Enum):
    """Available flutter analysis methods"""
    PISTON_THEORY = "piston_theory"
    DOUBLET_LATTICE = "doublet_lattice"  
    NASTRAN = "nastran"
    AUTO = "auto"  # Automatic method selection

@dataclass
class SolverRecommendation:
    """Solver method recommendation based on conditions"""
    recommended_method: SolverMethod
    confidence: float  # 0-1 scale
    reason: str
    alternative_methods: List[SolverMethod]

@dataclass
class ComparisonResult:
    """Results from multi-solver comparison"""
    methods: List[str]
    flutter_speeds: List[float]
    flutter_frequencies: List[float]  
    relative_differences: Dict[str, float]
    recommended_result: FlutterResult
    confidence_level: str

class MultiSolverFramework:
    """Main framework for multi-solver flutter analysis"""
    
    def __init__(self):
        """Initialize the multi-solver framework"""
        self.solvers = {
            SolverMethod.PISTON_THEORY: PistonTheorySolver,
            SolverMethod.DOUBLET_LATTICE: DoubletLatticeSolver,
            SolverMethod.NASTRAN: NastranSolver
        }
        self.logger = logging.getLogger(__name__)
    
    def get_available_solvers(self) -> List[str]:
        """Get list of available solver methods"""
        return [method.value for method in SolverMethod if method != SolverMethod.AUTO]
    
    def recommend_solver(self, mach: float, altitude: float = 0, 
                        panel_aspect_ratio: float = 1.0) -> SolverRecommendation:
        """Recommend best solver based on flow conditions"""
        
        if mach > 1.2:
            # Supersonic - Piston Theory is best
            return SolverRecommendation(
                recommended_method=SolverMethod.PISTON_THEORY,
                confidence=0.95,
                reason="Piston theory is most accurate for supersonic flow",
                alternative_methods=[SolverMethod.NASTRAN]
            )
        elif mach < 0.6:
            # Subsonic - Doublet Lattice is best
            return SolverRecommendation(
                recommended_method=SolverMethod.DOUBLET_LATTICE,
                confidence=0.90,
                reason="Doublet lattice method is ideal for subsonic flow",
                alternative_methods=[SolverMethod.NASTRAN, SolverMethod.PISTON_THEORY]
            )
        else:
            # Transonic - NASTRAN is most reliable
            return SolverRecommendation(
                recommended_method=SolverMethod.NASTRAN,
                confidence=0.85,
                reason="NASTRAN provides best accuracy in transonic regime",
                alternative_methods=[SolverMethod.DOUBLET_LATTICE]
            )
    
    def run_analysis(self, method: Union[str, SolverMethod], config: Dict) -> FlutterResult:
        """Run flutter analysis with specified method"""
        
        if isinstance(method, str):
            method = SolverMethod(method)
        
        if method == SolverMethod.AUTO:
            # Auto-select based on conditions
            mach = config.get('flow_conditions', {}).get('mach', 0.6)
            recommendation = self.recommend_solver(mach)
            method = recommendation.recommended_method
            self.logger.info(f"Auto-selected {method.value}: {recommendation.reason}")
        
        # Create and run appropriate solver
        if method == SolverMethod.PISTON_THEORY:
            return self._run_piston_theory(config)
        elif method == SolverMethod.DOUBLET_LATTICE:
            return self._run_doublet_lattice(config)
        elif method == SolverMethod.NASTRAN:
            return self._run_nastran(config)
        else:
            raise ValueError(f"Unknown solver method: {method}")
    
    def _run_piston_theory(self, config: Dict) -> FlutterResult:
        """Run piston theory analysis"""
        solver = PistonTheorySolver()
        
        # Extract parameters
        panel = PanelProperties(
            length=config['geometry']['length'],
            width=config['geometry']['width'],
            thickness=config['geometry']['thickness'],
            elastic_modulus=config['material']['E'],
            poisson_ratio=config['material']['nu'],
            density=config['material']['rho'],
            damping_ratio=config['material'].get('damping', 0.02)
        )
        
        flow = FlowConditions(
            mach=config['analysis']['mach'],
            altitude=config['analysis'].get('altitude', 0),
            air_density=config['analysis'].get('density', 1.225)
        )
        
        return solver.solve_flutter(panel, flow)
    
    def _run_doublet_lattice(self, config: Dict) -> FlutterResult:
        """Run doublet lattice analysis"""
        solver = DoubletLatticeSolver()
        
        params = DLMParameters(
            nx=config['geometry'].get('nx', 10),
            ny=config['geometry'].get('ny', 5),
            length=config['geometry']['length'],
            width=config['geometry']['width']
        )
        
        # Configure and run solver
        solver.setup_geometry(params)
        solver.set_flow_conditions(
            mach=config['analysis']['mach'],
            altitude=config['analysis'].get('altitude', 0)
        )
        
        return solver.solve_flutter()
    
    def _run_nastran(self, config: Dict) -> FlutterResult:
        """Run NASTRAN analysis"""
        solver = NastranSolver()
        
        nastran_config = NastranConfig(
            sol_sequence=145,  # Flutter analysis
            output_format='f06'
        )
        
        solver.configure(nastran_config)
        return solver.solve(config)
    
    def compare_methods(self, config: Dict, 
                        methods: Optional[List[SolverMethod]] = None) -> ComparisonResult:
        """Compare results from multiple solver methods"""
        
        if methods is None:
            # Use all applicable methods
            mach = config.get('analysis', {}).get('mach', 0.6)
            if mach > 1.2:
                methods = [SolverMethod.PISTON_THEORY, SolverMethod.NASTRAN]
            elif mach < 0.6:
                methods = [SolverMethod.DOUBLET_LATTICE, SolverMethod.NASTRAN]
            else:
                methods = [SolverMethod.NASTRAN, SolverMethod.DOUBLET_LATTICE]
        
        results = {}
        for method in methods:
            try:
                result = self.run_analysis(method, config)
                results[method.value] = result
            except Exception as e:
                self.logger.warning(f"Failed to run {method.value}: {e}")
        
        # Extract and compare results
        flutter_speeds = []
        flutter_frequencies = []
        
        for method_name, result in results.items():
            flutter_speeds.append(result.critical_velocity)
            flutter_frequencies.append(result.critical_frequency)
        
        # Calculate relative differences
        mean_speed = np.mean(flutter_speeds)
        relative_diffs = {}
        for method_name, speed in zip(results.keys(), flutter_speeds):
            relative_diffs[method_name] = abs(speed - mean_speed) / mean_speed * 100
        
        # Determine confidence level
        max_diff = max(relative_diffs.values())
        if max_diff < 5:
            confidence = "High - All methods agree within 5%"
        elif max_diff < 10:
            confidence = "Medium - Methods agree within 10%"
        else:
            confidence = "Low - Significant variation between methods"
        
        # Select recommended result (from most reliable method)
        if SolverMethod.NASTRAN.value in results:
            recommended = results[SolverMethod.NASTRAN.value]
        else:
            recommended = list(results.values())[0]
        
        return ComparisonResult(
            methods=list(results.keys()),
            flutter_speeds=flutter_speeds,
            flutter_frequencies=flutter_frequencies,
            relative_differences=relative_diffs,
            recommended_result=recommended,
            confidence_level=confidence
        )

class FlutterSolverFactory:
    """Factory for creating flutter analysis solvers"""
    
    @staticmethod
    def create_solver(method: SolverMethod, **kwargs):
        """Create solver instance based on method"""
        
        if method == SolverMethod.PISTON_THEORY:
            return PistonTheorySolver()
            
        elif method == SolverMethod.DOUBLET_LATTICE:
            dlm_params = kwargs.get('dlm_params', DLMParameters())
            return DoubletLatticeSolver(dlm_params)
            
        elif method == SolverMethod.NASTRAN:
            # Use new NASTRAN solver with configuration
            nastran_config = kwargs.get('nastran_config', NastranConfig())
            return NastranSolver(nastran_config)
                
        else:
            raise ValueError(f"Unknown solver method: {method}")

class SolverSelector:
    """Intelligent solver selection based on problem characteristics"""
    
    @staticmethod  
    def recommend_solver(panel: PanelProperties, 
                        flow: FlowConditions,
                        analysis_requirements: Dict = None) -> SolverRecommendation:
        """
        Recommend best solver method based on problem characteristics
        
        Args:
            panel: Panel properties
            flow: Flow conditions
            analysis_requirements: Analysis requirements (accuracy, speed, etc.)
            
        Returns:
            Solver recommendation with reasoning
        """
        
        requirements = analysis_requirements or {}
        
        # Default scoring
        piston_score = 0.0
        dlm_score = 0.0
        nastran_score = 0.0
        
        reasons = []
        
        # Mach number considerations
        if flow.mach_number > 1.2:
            piston_score += 0.4
            nastran_score += 0.3  # NASTRAN also good for supersonic
            dlm_score -= 0.2
            reasons.append(f"Supersonic flow (M={flow.mach_number:.1f}) favors piston theory and NASTRAN")
            
        elif 0.3 <= flow.mach_number <= 0.95:
            dlm_score += 0.4
            nastran_score += 0.35  # NASTRAN excellent for subsonic/transonic
            piston_score += 0.1
            reasons.append(f"Subsonic/transonic flow (M={flow.mach_number:.1f}) favors DLM and NASTRAN")
            
        elif flow.mach_number < 0.3:
            dlm_score += 0.2
            nastran_score += 0.25  # NASTRAN good for all conditions
            reasons.append(f"Low subsonic flow (M={flow.mach_number:.1f}) suitable for DLM/NASTRAN")
        
        # Panel geometry considerations
        aspect_ratio = panel.length / panel.width
        if aspect_ratio > 3.0:
            piston_score += 0.2
            reasons.append(f"High aspect ratio ({aspect_ratio:.1f}) suitable for piston theory")
        elif aspect_ratio < 1.5:
            dlm_score += 0.2
            reasons.append(f"Low aspect ratio ({aspect_ratio:.1f}) suitable for DLM")
        
        # Thickness ratio
        thickness_ratio = panel.thickness / panel.length
        if thickness_ratio < 0.01:
            piston_score += 0.2
            dlm_score += 0.3
            reasons.append("Thin panel suitable for simplified theories")
        else:
            nastran_score += 0.2
            reasons.append("Thick panel may require full FEM analysis")
        
        # Analysis requirements
        if requirements.get('speed_priority', False):
            piston_score += 0.3
            reasons.append("Fast analysis requested")
            
        if requirements.get('accuracy_priority', False):
            dlm_score += 0.2
            nastran_score += 0.3
            reasons.append("High accuracy requested")
            
        if requirements.get('preliminary_design', True):
            piston_score += 0.2
            dlm_score += 0.1
            reasons.append("Preliminary design phase")
        
        # NASTRAN always gets base score for completeness
        nastran_score += 0.1
        
        # Determine recommendation
        scores = {
            SolverMethod.PISTON_THEORY: piston_score,
            SolverMethod.DOUBLET_LATTICE: dlm_score,
            SolverMethod.NASTRAN: nastran_score
        }
        
        # Sort by score
        sorted_methods = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        recommended = sorted_methods[0][0]
        confidence = min(sorted_methods[0][1], 1.0)
        
        # Alternative methods (score > 0.3)
        alternatives = [method for method, score in sorted_methods[1:] if score > 0.3]
        
        reason = "; ".join(reasons[:3])  # Top 3 reasons
        
        return SolverRecommendation(
            recommended_method=recommended,
            confidence=confidence,
            reason=reason,
            alternative_methods=alternatives
        )

class MultiSolverAnalyzer:
    """Multi-solver flutter analysis with comparison capabilities"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results_cache = {}
        
    def analyze_with_multiple_solvers(self, 
                                    panel: PanelProperties,
                                    flow: FlowConditions,
                                    methods: List[SolverMethod] = None,
                                    velocity_range: Tuple[float, float] = (50, 300),
                                    num_points: int = 30,
                                    nastran_config: NastranConfig = None) -> Dict[str, List[FlutterResult]]:
        """
        Run flutter analysis with multiple solvers
        
        Args:
            panel: Panel properties
            flow: Flow conditions  
            methods: List of methods to use (None = auto-select)
            velocity_range: Velocity range for analysis
            
        Returns:
            Dictionary of results by method
        """
        
        if methods is None:
            # Auto-select appropriate methods
            recommendation = SolverSelector.recommend_solver(panel, flow)
            methods = [recommendation.recommended_method] + recommendation.alternative_methods
            methods = methods[:2]  # Limit to 2 methods for performance
        
        results = {}
        
        for method in methods:
            try:
                self.logger.info(f"Running analysis with {method.value}")
                
                # Create solver
                if method == SolverMethod.PISTON_THEORY:
                    solver = FlutterSolverFactory.create_solver(method)
                    method_results = solver.analyze_flutter(panel, flow, velocity_range, num_points)
                    
                elif method == SolverMethod.DOUBLET_LATTICE:
                    # Optimize DLM parameters based on panel size
                    dlm_params = self._optimize_dlm_parameters(panel, flow)
                    solver = FlutterSolverFactory.create_solver(method, dlm_params=dlm_params)
                    method_results = solver.analyze_flutter(panel, flow, velocity_range, num_points)
                    
                elif method == SolverMethod.NASTRAN:
                    # NASTRAN integration with full capability
                    if nastran_config is None:
                        # Use optimized config if none provided
                        nastran_config = self._optimize_nastran_parameters(panel, flow)
                    else:
                        # Merge GUI config with optimized parameters
                        optimized = self._optimize_nastran_parameters(panel, flow)
                        # Keep GUI settings for paths, memory, cpu_time, but use optimized analysis parameters
                        nastran_config.method = optimized.method
                        nastran_config.num_modes = optimized.num_modes
                        nastran_config.frequency_range = optimized.frequency_range
                        nastran_config.mach_numbers = optimized.mach_numbers
                        nastran_config.density_ratios = optimized.density_ratios
                    
                    solver = FlutterSolverFactory.create_solver(method, nastran_config=nastran_config)
                    
                    # Check if NASTRAN is available
                    if solver.is_available():
                        method_results = solver.analyze_flutter(panel, flow, velocity_range, num_points)
                    else:
                        self.logger.warning("NASTRAN not available - using simulation mode")
                        method_results = solver.analyze_flutter(panel, flow, velocity_range, num_points)
                    
                else:
                    continue
                
                results[method.value] = method_results
                self.logger.info(f"{method.value}: Found {len(method_results)} flutter points")
                
            except Exception as e:
                self.logger.error(f"Error with {method.value} solver: {e}")
                results[method.value] = []
        
        return results
    
    def _optimize_dlm_parameters(self, panel: PanelProperties, flow: FlowConditions) -> DLMParameters:
        """Optimize DLM parameters based on panel and flow conditions"""
        
        # Base parameters
        base_chord_panels = 8
        base_span_panels = 6
        
        # Adjust based on aspect ratio
        aspect_ratio = panel.length / panel.width
        if aspect_ratio > 2.0:
            chord_panels = int(base_chord_panels * 1.2)
            span_panels = max(4, int(base_span_panels * 0.8))
        elif aspect_ratio < 0.8:
            chord_panels = max(6, int(base_chord_panels * 0.8))
            span_panels = int(base_span_panels * 1.2)
        else:
            chord_panels = base_chord_panels
            span_panels = base_span_panels
        
        # Adjust reduced frequencies based on Mach number
        if flow.mach_number > 0.8:
            k_values = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.2]
        else:
            k_values = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5]
        
        # Mach number range around flight condition
        mach_values = [
            max(0.1, flow.mach_number - 0.2),
            max(0.2, flow.mach_number - 0.1), 
            flow.mach_number,
            min(0.95, flow.mach_number + 0.1),
            min(0.98, flow.mach_number + 0.2)
        ]
        
        return DLMParameters(
            num_chord_panels=chord_panels,
            num_span_panels=span_panels,
            reduced_frequencies=k_values,
            mach_numbers=mach_values
        )
    
    def _optimize_nastran_parameters(self, panel: PanelProperties, flow: FlowConditions) -> NastranConfig:
        """Optimize NASTRAN parameters based on panel and flow conditions"""
        
        # Determine optimal flutter analysis method
        if flow.mach_number > 1.1:
            method = "PK"  # PK method good for supersonic
        elif flow.mach_number > 0.7:
            method = "K"   # K method for transonic
        else:
            method = "KE"  # KE method for subsonic
        
        # Mach number range
        mach_range = [
            max(0.1, flow.mach_number - 0.3),
            flow.mach_number - 0.1,
            flow.mach_number,
            flow.mach_number + 0.1,
            min(2.0, flow.mach_number + 0.3)
        ]
        
        # Density ratios (typically sea level)
        density_ratios = [1.0]
        
        # Number of modes based on panel size
        panel_area = panel.length * panel.width
        if panel_area > 1.0:
            num_modes = 30
        elif panel_area > 0.1:
            num_modes = 20
        else:
            num_modes = 15
        
        # Frequency range based on panel properties
        # Rough estimate of first natural frequency
        import math
        D = (panel.youngs_modulus * panel.thickness**3) / (12 * (1 - panel.poissons_ratio**2))
        rho = panel.density * panel.thickness
        f1_approx = (math.pi**2 / (2 * panel.length**2)) * math.sqrt(D / rho) / (2 * math.pi)
        
        freq_range = (max(0.1, f1_approx * 0.1), min(2000.0, f1_approx * 10))
        
        return NastranConfig(
            method=method,
            num_modes=num_modes,
            frequency_range=freq_range,
            mach_numbers=mach_range,
            density_ratios=density_ratios,
            memory="4gb",  # Conservative memory setting
            cpu_time=1800  # 30 minutes max
        )
    
    def compare_results(self, results: Dict[str, List[FlutterResult]]) -> ComparisonResult:
        """
        Compare results from multiple solvers
        
        Args:
            results: Dictionary of results by solver method
            
        Returns:
            Comprehensive comparison analysis
        """
        
        # Extract critical flutter speeds for each method
        critical_results = {}
        
        for method, method_results in results.items():
            if method_results:
                # Find lowest flutter speed
                critical = min(method_results, key=lambda r: r.flutter_speed)
                critical_results[method] = critical
        
        if len(critical_results) < 2:
            self.logger.warning("Need at least 2 methods for meaningful comparison")
            return None
        
        # Calculate relative differences
        methods = list(critical_results.keys())
        flutter_speeds = [critical_results[m].flutter_speed for m in methods]
        flutter_frequencies = [critical_results[m].flutter_frequency for m in methods]
        
        # Reference speed (average)
        ref_speed = np.mean(flutter_speeds)
        
        relative_diffs = {}
        for method, speed in zip(methods, flutter_speeds):
            relative_diffs[method] = abs(speed - ref_speed) / ref_speed * 100
        
        # Determine confidence level and recommended result
        max_difference = max(relative_diffs.values())
        
        if max_difference < 5:
            confidence = "High"
        elif max_difference < 15:
            confidence = "Medium"  
        elif max_difference < 30:
            confidence = "Low"
        else:
            confidence = "Very Low"
        
        # Recommend most conservative (lowest) flutter speed
        recommended_method = min(critical_results.keys(), 
                               key=lambda m: critical_results[m].flutter_speed)
        recommended_result = critical_results[recommended_method]
        
        return ComparisonResult(
            methods=methods,
            flutter_speeds=flutter_speeds,
            flutter_frequencies=flutter_frequencies,
            relative_differences=relative_diffs,
            recommended_result=recommended_result,
            confidence_level=confidence
        )
    
    def plot_comparison(self, results: Dict[str, List[FlutterResult]], 
                       comparison: ComparisonResult = None):
        """Create comparison plots of flutter results"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Flutter speeds
        if comparison:
            methods = comparison.methods
            speeds = comparison.flutter_speeds
            frequencies = comparison.flutter_frequencies
            
            ax1.bar(methods, speeds, alpha=0.7)
            ax1.set_ylabel('Flutter Speed (m/s)')
            ax1.set_title('Critical Flutter Speed Comparison')
            ax1.tick_params(axis='x', rotation=45)
            
            # Add relative differences as text
            for i, (method, speed) in enumerate(zip(methods, speeds)):
                diff = comparison.relative_differences[method]
                ax1.text(i, speed + max(speeds)*0.02, f'{diff:.1f}%', 
                        ha='center', va='bottom', fontsize=9)
            
            ax2.bar(methods, frequencies, alpha=0.7, color='orange')
            ax2.set_ylabel('Flutter Frequency (Hz)')
            ax2.set_title('Critical Flutter Frequency Comparison')
            ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def generate_report(self, panel: PanelProperties, flow: FlowConditions,
                       results: Dict[str, List[FlutterResult]], 
                       comparison: ComparisonResult) -> str:
        """Generate comprehensive analysis report"""
        
        report = []
        report.append("MULTI-SOLVER FLUTTER ANALYSIS REPORT")
        report.append("=" * 50)
        report.append("")
        
        # Panel information
        report.append("PANEL CONFIGURATION:")
        report.append(f"  Length: {panel.length*1000:.1f} mm")
        report.append(f"  Width: {panel.width*1000:.1f} mm")
        report.append(f"  Thickness: {panel.thickness*1000:.1f} mm")
        report.append(f"  Material: E={panel.youngs_modulus/1e9:.1f} GPa, ρ={panel.density} kg/m³")
        report.append(f"  Boundary: {panel.boundary_conditions}")
        report.append("")
        
        # Flow conditions
        report.append("FLOW CONDITIONS:")
        report.append(f"  Mach Number: {flow.mach_number}")
        report.append(f"  Altitude: {flow.altitude/1000:.1f} km")
        report.append("")
        
        # Solver recommendations
        recommendation = SolverSelector.recommend_solver(panel, flow)
        report.append("SOLVER RECOMMENDATION:")
        report.append(f"  Recommended: {recommendation.recommended_method.value}")
        report.append(f"  Confidence: {recommendation.confidence:.1%}")
        report.append(f"  Reason: {recommendation.reason}")
        report.append("")
        
        # Results comparison
        if comparison:
            report.append("RESULTS COMPARISON:")
            report.append(f"  Methods Analyzed: {', '.join(comparison.methods)}")
            report.append(f"  Confidence Level: {comparison.confidence_level}")
            report.append("")
            
            report.append("  Critical Flutter Results:")
            for i, method in enumerate(comparison.methods):
                speed = comparison.flutter_speeds[i]
                freq = comparison.flutter_frequencies[i]
                diff = comparison.relative_differences[method]
                report.append(f"    {method}: {speed:.1f} m/s, {freq:.1f} Hz ({diff:+.1f}%)")
            
            report.append("")
            report.append(f"  RECOMMENDED RESULT: {comparison.recommended_result.flutter_speed:.1f} m/s")
            report.append(f"  (Most conservative estimate from {comparison.recommended_result.method})")
        
        return "\n".join(report)

# Example usage
if __name__ == "__main__":
    
    # Example panel
    panel = PanelProperties(
        length=0.5,           # 500mm
        width=0.3,            # 300mm
        thickness=0.002,      # 2mm
        youngs_modulus=71.7e9,
        poissons_ratio=0.33,
        density=2810
    )
    
    # Test different flow conditions
    flow_conditions = [
        FlowConditions(mach_number=0.7, altitude=8000),   # Subsonic
        FlowConditions(mach_number=1.5, altitude=10000),  # Supersonic
    ]
    
    analyzer = MultiSolverAnalyzer()
    
    for flow in flow_conditions:
        print(f"\nAnalyzing Flow Condition: M={flow.mach_number}, Alt={flow.altitude}m")
        print("-" * 60)
        
        # Get solver recommendation
        recommendation = SolverSelector.recommend_solver(panel, flow)
        print(f"Recommended Solver: {recommendation.recommended_method.value}")
        print(f"Confidence: {recommendation.confidence:.1%}")
        print(f"Reason: {recommendation.reason}")
        print()
        
        # Run multi-solver analysis
        methods = [SolverMethod.PISTON_THEORY, SolverMethod.DOUBLET_LATTICE]
        results = analyzer.analyze_with_multiple_solvers(panel, flow, methods)
        
        # Compare results
        comparison = analyzer.compare_results(results)
        
        if comparison:
            print("Comparison Results:")
            for i, method in enumerate(comparison.methods):
                speed = comparison.flutter_speeds[i]
                diff = comparison.relative_differences[method]
                print(f"  {method}: {speed:.1f} m/s ({diff:+.1f}%)")
            
            print(f"\nRecommended: {comparison.recommended_result.flutter_speed:.1f} m/s")
            print(f"Confidence: {comparison.confidence_level}")
        
        print("\n" + "="*60)