from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Set, Optional
from pathlib import Path

@dataclass
class CodeSnippet:
    """Represents a snippet of code extracted from a file."""
    content: str
    start_line: int
    end_line: int

@dataclass
class FunctionInfo:
    """Detailed information about a function in the codebase."""
    name: str
    params: List[str]
    returns: str
    docstring: str
    dependencies: Set[str]
    loc: int
    code: CodeSnippet
    file_path: str
    complexity: int = 1

@dataclass
class ClassInfo:
    """Detailed information about a class in the codebase."""
    name: str
    methods: List[FunctionInfo]
    base_classes: List[str]
    docstring: str
    code: CodeSnippet
    file_path: str
    attributes: List[Dict[str, Optional[str]]]
    complexity: int = 1

@dataclass
class FileInfo:
    """Comprehensive information about a file for LLM analysis."""
    path: Path
    type: str
    content: str
    size: int
    dependencies: Set[str]
    functions: Dict[str, FunctionInfo]
    classes: Dict[str, ClassInfo]
    unused_imports: Set[str] = field(default_factory=set)

@dataclass
class ProjectMetrics:
    """Aggregated metrics for the entire project."""
    complexity: 'ComplexityMetrics'
    quality: 'QualityMetrics'
    dependencies: 'DependencyMetrics'
    patterns: 'PatternMetrics'
    security: 'SecurityMetrics'
    performance: 'PerformanceMetrics'
    timestamp: datetime
    project_path: Path
    total_files: int
    total_lines: int

    def calculate_overall_score(self) -> float:
        """Calculate weighted overall project score.

        Returns:
            float: A score from 0 to 100 representing overall project health.
        """
        weights = {
            'complexity': 0.15,
            'quality': 0.20,
            'security': 0.25,
            'performance': 0.20,
            'patterns': 0.10,
            'dependencies': 0.10
        }

        scores = {
            'complexity': self.complexity.maintainability_index / 100,
            'quality': self.quality.quality_score() / 100,
            'security': self.security.security_score / 100,
            'performance': self.performance.performance_score / 100,  # Changed () to attribute access
            'patterns': sum(p.confidence for p in self.patterns.design_patterns) / max(len(self.patterns.design_patterns), 1),
            'dependencies': self.dependencies.health_score() / 100
        }

        overall_score = sum(weights[metric] * scores[metric] for metric in weights)
        return min(100.0, max(0.0, overall_score * 100))