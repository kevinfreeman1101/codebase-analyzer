"""Data classes for storing analysis results."""

from dataclasses import dataclass
from typing import Dict, Set, Optional, List
from pathlib import Path
from datetime import datetime

@dataclass
class FunctionInfo:
    """Stores information about a function."""
    loc: int = 0
    docstring: Optional[str] = None
    params: List[str] = None
    complexity: float = 0.0
    returns: Optional[str] = None

    def __post_init__(self):
        if self.params is None:
            self.params = []
        if self.returns is None:
            self.returns = "None"

@dataclass
class MethodInfo:
    """Stores information about a class method."""
    loc: int = 0
    docstring: Optional[str] = None

@dataclass
class ClassInfo:
    """Stores information about a class, including its methods."""
    methods: Dict[str, MethodInfo] = None
    docstring: Optional[str] = None

    def __post_init__(self):
        if self.methods is None:
            self.methods = {}

@dataclass
class FileInfo:
    """Stores information about a file, including functions and classes."""
    file_path: Path = None
    type: str = "unknown"
    size: float = 0.0
    functions: Dict[str, FunctionInfo] = None
    classes: Dict[str, ClassInfo] = None
    dependencies: Set[str] = None
    unused_imports: Set[str] = None

    def __post_init__(self):
        if self.functions is None:
            self.functions = {}
        if self.classes is None:
            self.classes = {}
        if self.dependencies is None:
            self.dependencies = set()
        if self.unused_imports is None:
            self.unused_imports = set()

@dataclass
class ProjectMetrics:
    """Stores project-level metrics."""
    complexity: 'ComplexityMetrics' = None
    quality: 'QualityMetrics' = None
    dependencies: 'DependencyMetrics' = None
    patterns: 'PatternMetrics' = None
    security: 'SecurityMetrics' = None
    performance: 'PerformanceMetrics' = None
    timestamp: datetime = None
    project_path: Path = None
    total_files: int = 0
    total_lines: int = 0
    total_size: float = 0.0
    function_count: int = 0
    class_count: int = 0
    documented_count: int = 0

    def __post_init__(self):
        if self.complexity is None:
            from codebase_analyzer.metrics.complexity_analyzer import ComplexityMetrics
            self.complexity = ComplexityMetrics(0.0, 0.0, [])
        if self.quality is None:
            from codebase_analyzer.metrics.quality_metrics import QualityMetrics
            self.quality = QualityMetrics(0.0, 0.0, 0.0, 0.0, 0.0)
        if self.dependencies is None:
            from codebase_analyzer.metrics.dependency_metrics import DependencyMetrics
            self.dependencies = DependencyMetrics(set(), {}, [])
        if self.patterns is None:
            from codebase_analyzer.metrics.pattern_metrics import PatternMetrics
            self.patterns = PatternMetrics([])
        if self.security is None:
            from codebase_analyzer.metrics.security_metrics import SecurityMetrics
            self.security = SecurityMetrics([], 0.0, [])
        if self.performance is None:
            from codebase_analyzer.metrics.performance_metrics import PerformanceMetrics
            self.performance = PerformanceMetrics([], 0.0, [], [], [])
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def calculate_overall_score(self) -> float:
        """Calculate an overall score based on available metrics.

        Returns:
            float: Overall score out of 100.
        """
        # Weights for each metric
        weights = {
            'complexity': 0.2,
            'quality': 0.3,
            'security': 0.3,
            'performance': 0.2
        }

        # Normalize scores (assuming each metric has a score out of 100)
        complexity_score = 100 - (self.complexity.cyclomatic_complexity * 10)  # Simplified
        quality_score = self.quality.test_coverage * 100
        security_score = 100 - (self.security.security_score * 20)  # Use security_score for local version
        performance_score = self.performance.performance_score  # Already a normalized score (0-100)

        # Weighted average
        total_score = (
            weights['complexity'] * complexity_score +
            weights['quality'] * quality_score +
            weights['security'] * security_score +
            weights['performance'] * performance_score
        )

        return max(0.0, min(100.0, total_score))

@dataclass
class Recommendation:
    """Stores a recommendation for improving the codebase."""
    category: str = "general"
    description: str = ""
    priority: int = 1
    suggestion: str = ""  # Added to match RecommendationEngine usage
    details: Dict[str, str] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}