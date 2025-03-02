"""Data classes for representing analysis results and recommendations."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Set, Optional, Any
from pathlib import Path

@dataclass
class CodeSnippet:
    """Represents a snippet of code with its location."""
    content: str
    start_line: int
    end_line: int

@dataclass
class FunctionInfo:
    """Detailed information about a function."""
    name: str
    params: List[str]
    returns: str
    docstring: str
    dependencies: Set[str]
    loc: int
    code: CodeSnippet
    file_path: str
    complexity: int

@dataclass
class ClassInfo:
    """Detailed information about a class."""
    name: str
    methods: List[FunctionInfo]
    base_classes: List[str]
    docstring: str
    code: CodeSnippet
    file_path: str
    attributes: List[Dict[str, Optional[str]]]
    complexity: int

@dataclass
class FileInfo:
    """Comprehensive information about a file."""
    path: Path
    type: str
    content: str
    size: int
    dependencies: Set[str]
    functions: Dict[str, FunctionInfo]
    classes: Dict[str, ClassInfo]
    unused_imports: Set[str]

@dataclass
class ComplexityMetrics:
    """Represents complexity metrics for a Python project."""
    cyclomatic_complexity: float
    maintainability_index: float
    complex_functions: List[Dict[str, Any]]

@dataclass
class QualityMetrics:
    """Represents quality metrics for a Python project."""
    type_hint_coverage: float
    documentation_coverage: float
    test_coverage: float
    lint_score: float
    code_to_comment_ratio: float

    def quality_score(self) -> float:
        """Calculate an overall quality score."""
        weights = {'type_hint': 0.3, 'doc': 0.3, 'test': 0.2, 'lint': 0.15, 'comment': 0.05}
        score = (
            self.type_hint_coverage * weights['type_hint'] +
            self.documentation_coverage * weights['doc'] +
            self.test_coverage * weights['test'] +
            self.lint_score * weights['lint'] +
            (self.code_to_comment_ratio * 100 if self.code_to_comment_ratio <= 1 else 100) * weights['comment']
        )
        return min(100.0, max(0.0, score))

@dataclass
class DependencyMetrics:
    """Represents dependency metrics for a Python project."""
    direct_dependencies: Set[str]
    dependency_tree: Dict[str, List[str]]

    def health_score(self) -> float:
        """Calculate a dependency health score (placeholder)."""
        return 100.0 - (len(self.direct_dependencies) * 2)  # Simplified scoring

@dataclass
class Pattern:
    """Represents a detected design pattern or security pattern."""
    name: str
    locations: List[str]
    confidence: float
    description: str = ""

@dataclass
class PatternMetrics:
    """Represents pattern metrics for a Python project."""
    design_patterns: List[Pattern]

@dataclass
class Vulnerability:
    """Represents a security vulnerability."""
    type: str
    location: str
    severity: str
    description: str
    recommendation: str

@dataclass
class SecurityMetrics:
    """Represents security metrics for a Python project."""
    vulnerabilities: List[Vulnerability]
    security_score: float
    security_patterns: List[Pattern]

@dataclass
class PerformanceHotspot:
    """Represents a performance hotspot in the code."""
    location: str
    complexity: int
    execution_count_estimate: int
    optimization_suggestion: str

@dataclass
class LoopOptimization:
    """Represents a loop optimization opportunity."""
    location: str
    loop_type: str
    complexity: int
    suggestion: str

@dataclass
class PerformanceMetrics:
    """Represents performance metrics for a Python project."""
    hotspots: List[PerformanceHotspot]
    performance_score: float
    loop_optimizations: List[LoopOptimization]
    memory_intensive_ops: List[str]
    io_operations: List[str]

@dataclass
class Recommendation:
    """Represents a recommendation for code improvement."""
    priority: str  # e.g., "HIGH", "MEDIUM", "LOW"
    category: str  # e.g., "Complexity", "Quality"
    description: str
    suggestion: str

@dataclass
class ProjectMetrics:
    """Aggregates all metrics for a project."""
    complexity: ComplexityMetrics
    quality: QualityMetrics
    dependencies: DependencyMetrics
    patterns: PatternMetrics
    security: SecurityMetrics
    performance: PerformanceMetrics
    timestamp: datetime
    project_path: Path
    total_files: int
    total_lines: int

    def calculate_overall_score(self) -> float:
        """Calculate an overall project score from individual metrics."""
        weights = {
            "complexity": 0.2,
            "quality": 0.3,
            "security": 0.3,
            "performance": 0.2
        }
        complexity_score = max(0.0, min(100.0, self.complexity.maintainability_index))
        quality_score = self.quality.quality_score()
        security_score = self.security.security_score
        performance_score = self.performance.performance_score
        dependency_score = self.dependencies.health_score()

        overall_score = (
            complexity_score * weights["complexity"] +
            quality_score * weights["quality"] +
            security_score * weights["security"] +
            performance_score * weights["performance"] +
            dependency_score * 0.1  # Lower weight for dependencies
        ) / 1.1  # Normalize to 100
        return round(overall_score, 1)