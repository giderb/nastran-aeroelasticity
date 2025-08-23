"""
Analysis Runner
==============

High-level analysis runner that orchestrates the flutter analysis process
and provides progress tracking and error handling for the GUI.
"""

import threading
import time
import logging
from typing import Callable, Optional
from dataclasses import dataclass

from .flutter_engine import (
    FlutterAnalysisEngine, 
    FlutterAnalysisConfig, 
    GeometryConfig, 
    MaterialConfig,
    FlutterResults,
    AnalysisValidator
)


@dataclass
class AnalysisProgress:
    """Progress tracking for analysis"""
    step: str
    progress: float  # 0-100
    timestamp: float


class AnalysisRunner:
    """High-level analysis runner with progress tracking"""
    
    def __init__(self, progress_callback: Optional[Callable[[str, float], None]] = None):
        self.progress_callback = progress_callback
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.should_stop = False
        self.current_engine = None
        
    def run_flutter_analysis(self, config: FlutterAnalysisConfig, 
                           geometry: GeometryConfig, 
                           material: MaterialConfig) -> FlutterResults:
        """Run complete flutter analysis with validation and error handling"""
        
        if self.is_running:
            raise RuntimeError("Analysis is already running")
            
        self.is_running = True
        self.should_stop = False
        
        try:
            # Phase 1: Validation (0-10%)
            self._update_progress("Validating inputs...", 0)
            validation_errors = self._validate_inputs(config, geometry, material)
            
            if validation_errors:
                error_msg = "Validation failed:\n" + "\n".join(validation_errors)
                self.logger.error(error_msg)
                return FlutterResults(
                    velocities=None,
                    frequencies=None,
                    dampings=None,
                    flutter_velocity=None,
                    flutter_frequency=None,
                    flutter_mode=None,
                    analysis_successful=False,
                    error_message=error_msg
                )
            
            self._update_progress("Validation complete", 10)
            
            if self.should_stop:
                return self._create_cancelled_result()
            
            # Phase 2: Setup (10-20%)
            self._update_progress("Setting up analysis engine...", 12)
            try:
                self.current_engine = FlutterAnalysisEngine(config)
                self._update_progress("Configuring model...", 15)
                
                if not self.current_engine.setup_analysis(geometry, material):
                    error_msg = "Failed to setup analysis model - check input parameters"
                    self.logger.error(error_msg)
                    return FlutterResults(
                        velocities=None,
                        frequencies=None,
                        dampings=None,
                        flutter_velocity=None,
                        flutter_frequency=None,
                        flutter_mode=None,
                        analysis_successful=False,
                        error_message=error_msg
                    )
            except Exception as e:
                error_msg = f"Failed to initialize analysis engine: {str(e)}"
                self.logger.error(error_msg)
                return FlutterResults(
                    velocities=None,
                    frequencies=None,
                    dampings=None,
                    flutter_velocity=None,
                    flutter_frequency=None,
                    flutter_mode=None,
                    analysis_successful=False,
                    error_message=error_msg
                )
            
            self._update_progress("Model setup complete", 20)
            
            if self.should_stop:
                return self._create_cancelled_result()
            
            # Phase 3: Analysis (20-100%)
            self._update_progress("Starting flutter analysis...", 22)
            
            def engine_progress_callback(step: str, progress: float):
                # Map engine progress (0-100) to our remaining range (22-100)
                mapped_progress = 22 + (progress / 100.0) * 78
                self._update_progress(step, mapped_progress)
                return not self.should_stop  # Return whether to continue
            
            results = self.current_engine.run_analysis(engine_progress_callback)
            
            if self.should_stop:
                return self._create_cancelled_result()
            
            # Phase 4: Finalization (100%)
            if results.analysis_successful:
                self._update_progress("Analysis completed successfully!", 100)
                self.logger.info("Flutter analysis completed successfully")
            else:
                self.logger.error(f"Analysis failed: {results.error_message}")
                
            return results
            
        except Exception as e:
            error_msg = f"Unexpected error during analysis: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return FlutterResults(
                velocities=None,
                frequencies=None,
                dampings=None,
                flutter_velocity=None,
                flutter_frequency=None,
                flutter_mode=None,
                analysis_successful=False,
                error_message=error_msg
            )
        
        finally:
            self.is_running = False
            if self.current_engine:
                self.current_engine.cleanup()
                self.current_engine = None
    
    def run_async(self, config: FlutterAnalysisConfig, 
                  geometry: GeometryConfig, 
                  material: MaterialConfig,
                  completion_callback: Callable[[FlutterResults], None]):
        """Run analysis asynchronously in a separate thread"""
        
        def analysis_thread():
            try:
                results = self.run_flutter_analysis(config, geometry, material)
                completion_callback(results)
            except Exception as e:
                self.logger.error(f"Error in analysis thread: {e}", exc_info=True)
                error_results = FlutterResults(
                    velocities=None,
                    frequencies=None,
                    dampings=None,
                    flutter_velocity=None,
                    flutter_frequency=None,
                    flutter_mode=None,
                    analysis_successful=False,
                    error_message=str(e)
                )
                completion_callback(error_results)
        
        thread = threading.Thread(target=analysis_thread, daemon=True)
        thread.start()
        return thread
    
    def stop_analysis(self):
        """Request analysis to stop"""
        self.should_stop = True
        self.logger.info("Analysis stop requested")
    
    def _validate_inputs(self, config: FlutterAnalysisConfig, 
                        geometry: GeometryConfig, 
                        material: MaterialConfig) -> list:
        """Validate all analysis inputs"""
        all_errors = []
        
        # Validate configuration
        config_errors = AnalysisValidator.validate_config(config)
        all_errors.extend(config_errors)
        
        # Validate geometry
        geometry_errors = AnalysisValidator.validate_geometry(geometry)
        all_errors.extend(geometry_errors)
        
        # Validate material
        material_errors = AnalysisValidator.validate_material(material)
        all_errors.extend(material_errors)
        
        return all_errors
    
    def _update_progress(self, step: str, progress: float):
        """Update progress and call callback"""
        if self.progress_callback:
            self.progress_callback(step, progress)
        
        self.logger.debug(f"Progress: {progress:.1f}% - {step}")
    
    def _create_cancelled_result(self) -> FlutterResults:
        """Create result object for cancelled analysis"""
        return FlutterResults(
            velocities=None,
            frequencies=None,
            dampings=None,
            flutter_velocity=None,
            flutter_frequency=None,
            flutter_mode=None,
            analysis_successful=False,
            error_message="Analysis was cancelled by user"
        )


class BatchAnalysisRunner:
    """Runner for batch/parametric analysis studies"""
    
    def __init__(self, progress_callback: Optional[Callable[[str, float], None]] = None):
        self.progress_callback = progress_callback
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.should_stop = False
        
    def run_parametric_study(self, base_config: FlutterAnalysisConfig,
                           geometry: GeometryConfig,
                           material: MaterialConfig,
                           parameter_variations: dict) -> dict:
        """Run parametric study varying specified parameters"""
        
        if self.is_running:
            raise RuntimeError("Batch analysis is already running")
            
        self.is_running = True
        self.should_stop = False
        results = {}
        
        try:
            # Calculate total number of cases
            total_cases = 1
            for param_values in parameter_variations.values():
                total_cases *= len(param_values)
            
            self.logger.info(f"Starting parametric study with {total_cases} cases")
            
            case_num = 0
            
            # Generate all parameter combinations
            param_names = list(parameter_variations.keys())
            param_values_list = list(parameter_variations.values())
            
            import itertools
            for param_combination in itertools.product(*param_values_list):
                if self.should_stop:
                    break
                    
                case_num += 1
                case_progress = (case_num - 1) / total_cases * 100
                
                # Create modified configuration
                case_config = self._create_case_config(
                    base_config, geometry, material,
                    param_names, param_combination
                )
                
                case_name = self._create_case_name(param_names, param_combination)
                self._update_progress(f"Running case {case_num}/{total_cases}: {case_name}", 
                                    case_progress)
                
                # Run single analysis
                runner = AnalysisRunner()
                case_results = runner.run_flutter_analysis(
                    case_config['config'], 
                    case_config['geometry'], 
                    case_config['material']
                )
                
                results[case_name] = {
                    'parameters': dict(zip(param_names, param_combination)),
                    'results': case_results
                }
                
            final_progress = case_num / total_cases * 100
            self._update_progress(f"Parametric study complete: {case_num}/{total_cases} cases", 
                                final_progress)
            
        except Exception as e:
            self.logger.error(f"Parametric study failed: {e}", exc_info=True)
            
        finally:
            self.is_running = False
            
        return results
    
    def _create_case_config(self, base_config, base_geometry, base_material,
                           param_names, param_values):
        """Create configuration for a specific parameter case"""
        import copy
        
        # Deep copy base configurations
        case_config = copy.deepcopy(base_config)
        case_geometry = copy.deepcopy(base_geometry)
        case_material = copy.deepcopy(base_material)
        
        # Apply parameter variations
        for param_name, param_value in zip(param_names, param_values):
            if hasattr(case_config, param_name):
                setattr(case_config, param_name, param_value)
            elif hasattr(case_geometry, param_name):
                setattr(case_geometry, param_name, param_value)
            elif hasattr(case_material, param_name):
                setattr(case_material, param_name, param_value)
        
        return {
            'config': case_config,
            'geometry': case_geometry,
            'material': case_material
        }
    
    def _create_case_name(self, param_names, param_values):
        """Create descriptive name for analysis case"""
        parts = []
        for name, value in zip(param_names, param_values):
            if isinstance(value, float):
                parts.append(f"{name}={value:.3g}")
            else:
                parts.append(f"{name}={value}")
        return "_".join(parts)
    
    def _update_progress(self, step: str, progress: float):
        """Update progress and call callback"""
        if self.progress_callback:
            self.progress_callback(step, progress)
        
        self.logger.debug(f"Batch Progress: {progress:.1f}% - {step}")
    
    def stop_analysis(self):
        """Request batch analysis to stop"""
        self.should_stop = True
        self.logger.info("Batch analysis stop requested")


# Analysis result utilities
class ResultsAnalyzer:
    """Analyze and summarize flutter analysis results"""
    
    @staticmethod
    def analyze_flutter_margin(results: FlutterResults, operating_velocity: float) -> dict:
        """Analyze flutter safety margin"""
        analysis = {
            'flutter_detected': results.flutter_velocity is not None,
            'operating_velocity': operating_velocity,
            'flutter_velocity': results.flutter_velocity,
            'flutter_frequency': results.flutter_frequency,
            'safety_margin': None,
            'safety_factor': None,
            'safety_status': 'unknown'
        }
        
        if results.flutter_velocity is not None:
            analysis['safety_margin'] = results.flutter_velocity - operating_velocity
            analysis['safety_factor'] = results.flutter_velocity / operating_velocity
            
            if analysis['safety_factor'] > 1.5:
                analysis['safety_status'] = 'safe'
            elif analysis['safety_factor'] > 1.2:
                analysis['safety_status'] = 'marginal'
            else:
                analysis['safety_status'] = 'unsafe'
        else:
            analysis['safety_status'] = 'safe'  # No flutter detected
            
        return analysis
    
    @staticmethod
    def find_critical_modes(results: FlutterResults) -> list:
        """Identify critical flutter modes"""
        # This would analyze mode shapes and identify which structural modes
        # are most critical for flutter. For now, return placeholder.
        return [{'mode': 1, 'type': 'bending', 'criticality': 'high'}]
    
    @staticmethod
    def generate_summary_report(results: FlutterResults, 
                              operating_velocity: float = 200.0) -> str:
        """Generate comprehensive analysis summary"""
        if not results.analysis_successful:
            return f"Analysis Failed: {results.error_message}"
        
        margin_analysis = ResultsAnalyzer.analyze_flutter_margin(results, operating_velocity)
        
        report = []
        report.append("FLUTTER ANALYSIS SUMMARY")
        report.append("=" * 50)
        
        if results.flutter_velocity is not None:
            report.append(f"Flutter Speed: {results.flutter_velocity:.1f} m/s")
            report.append(f"Flutter Frequency: {results.flutter_frequency:.2f} Hz")
            report.append(f"Operating Speed: {operating_velocity:.1f} m/s")
            report.append(f"Safety Margin: {margin_analysis['safety_margin']:.1f} m/s")
            report.append(f"Safety Factor: {margin_analysis['safety_factor']:.2f}")
            report.append(f"Safety Status: {margin_analysis['safety_status'].upper()}")
        else:
            report.append("No flutter detected in analysis range")
            report.append(f"Maximum analysis speed: {results.velocities.max():.1f} m/s")
            report.append("Safety Status: SAFE")
        
        report.append("")
        report.append("RECOMMENDATIONS:")
        
        if margin_analysis['safety_status'] == 'unsafe':
            report.append("- IMMEDIATE ACTION REQUIRED: Flutter speed too low")
            report.append("- Consider structural modifications or operating limit reduction")
        elif margin_analysis['safety_status'] == 'marginal':
            report.append("- Caution advised: Limited safety margin")
            report.append("- Consider detailed analysis and monitoring")
        else:
            report.append("- Structure appears safe for intended operation")
            report.append("- Continue with normal design process")
        
        return "\n".join(report)