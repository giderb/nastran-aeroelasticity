"""
GUI Analysis Module
==================

Advanced flutter analysis engine and runner for the Panel Flutter GUI application.
Provides comprehensive panel flutter analysis with NASTRAN integration.
"""

from .flutter_engine import (
    FlutterAnalysisEngine,
    FlutterAnalysisConfig, 
    GeometryConfig,
    MaterialConfig,
    FlutterResults,
    AnalysisValidator
)

from .analysis_runner import (
    AnalysisRunner,
    BatchAnalysisRunner,
    AnalysisProgress,
    ResultsAnalyzer
)

__all__ = [
    'FlutterAnalysisEngine',
    'FlutterAnalysisConfig',
    'GeometryConfig', 
    'MaterialConfig',
    'FlutterResults',
    'AnalysisValidator',
    'AnalysisRunner',
    'BatchAnalysisRunner',
    'AnalysisProgress',
    'ResultsAnalyzer'
]