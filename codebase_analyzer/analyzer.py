"""Module for comprehensive codebase analysis and metric generation.

This module provides the CodebaseAnalyzer class, which orchestrates the analysis of a
project directory by leveraging specialized analyzers for complexity, quality,
dependencies, patterns, security, and performance, producing a detailed summary for LLM advisors.
"""

from datetime import datetime
from typing import Optional
from pathlib import Path
from .metrics.complexity_analyzer import ComplexityAnalyzer, ComplexityMetrics
from .metrics.quality_metrics import QualityAnalyzer, QualityMetrics
from .metrics.dependency_metrics import DependencyAnalyzer, DependencyMetrics
from .metrics.pattern_metrics import PatternAnalyzer, PatternMetrics
from .metrics.security_metrics import SecurityAnalyzer, SecurityMetrics
from .metrics.performance_metrics import PerformanceAnalyzer, PerformanceMetrics
from .models.data_classes import ProjectMetrics
from .recommendations.recommendation_engine import RecommendationEngine
from .formatters.summary_formatter import SummaryFormatter

class CodebaseAnalyzer:
    """Main class for analyzing codebases and generating metrics.

    Coordinates multiple analyzers to evaluate a project’s quality, complexity, security,
    performance, and dependency health, consolidating results into a unified report.
    """

    def __init__(self) -> None:
        """Initialize the CodebaseAnalyzer with component analyzers."""
        self.complexity_analyzer = ComplexityAnalyzer()
        self.quality_analyzer = QualityAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self.pattern_analyzer = PatternAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.project_metrics: Optional[ProjectMetrics] = None
        self.formatter = SummaryFormatter(Path.cwd())  # Default to current directory

    def analyze_project(self, project_path: Path) -> ProjectMetrics:
        """Perform comprehensive analysis of the project.

        Args:
            project_path: Path to the project root directory.

        Returns:
            ProjectMetrics: An object containing all analysis metrics.

        Raises:
            FileNotFoundError: If the project path does not exist.
        """
        if not project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")

        print("Starting comprehensive project analysis...")
        total_files = sum(1 for _ in project_path.rglob('*.py'))
        total_lines = sum(len(open(f).readlines()) for f in project_path.rglob('*.py') if f.is_file())

        print("Analyzing complexity metrics...")
        complexity_metrics = self.complexity_analyzer.analyze_project(project_path)

        print("Analyzing code quality...")
        quality_metrics = self.quality_analyzer.analyze_project(project_path)

        print("Analyzing dependencies...")
        dependency_metrics = self.dependency_analyzer.analyze_project(project_path)

        print("Analyzing code patterns...")
        pattern_metrics = self.pattern_analyzer.analyze_project(project_path)

        print("Analyzing security...")
        security_metrics = self.security_analyzer.analyze_project(project_path)

        print("Analyzing performance...")
        performance_metrics = self.performance_analyzer.analyze_project(project_path)

        self.project_metrics = ProjectMetrics(
            complexity=complexity_metrics,
            quality=quality_metrics,
            dependencies=dependency_metrics,
            patterns=pattern_metrics,
            security=security_metrics,
            performance=performance_metrics,
            timestamp=datetime.now(),
            project_path=project_path,
            total_files=total_files,
            total_lines=total_lines
        )

        return self.project_metrics

    def generate_summary(self) -> str:
        """Generate a detailed summary of the analysis for LLM advisors.

        Includes project overview, metric breakdowns with function-level complexity details,
        and recommendations to provide maximum context for understanding the codebase.

        Returns:
            str: Formatted summary string with comprehensive insights.
        """
        if not self.project_metrics:
            return "No analysis data available. Run analyze_project first."

        summary = []
        summary.append("CODEBASE ANALYSIS SUMMARY")
        summary.append("=" * 50)
        summary.append(f"Project Path: {self.project_metrics.project_path}")
        summary.append(f"Analysis Timestamp: {self.project_metrics.timestamp}")
        summary.append(f"Total Python Files: {self.project_metrics.total_files}")
        summary.append(f"Total Lines of Code: {self.project_metrics.total_lines}")
        summary.append("File Types Analyzed: Python (*.py)")
        summary.append(f"Overall Project Score: {self.project_metrics.calculate_overall_score():.1f}/100")
        summary.append("  - Weighted average of complexity, quality, security, and performance metrics")

        # Complexity Metrics
        summary.append("\nCOMPLEXITY METRICS")
        summary.append("-" * 30)
        summary.append(f"Average Cyclomatic Complexity: {self.project_metrics.complexity.cyclomatic_complexity:.2f}")
        summary.append(f"  - Measures decision points in code (lower is simpler)")
        summary.append(f"Maintainability Index: {self.project_metrics.complexity.maintainability_index:.1f}/100")
        summary.append("  - Higher values indicate better maintainability (<20 suggests complexity issues)")
        if self.project_metrics.complexity.complex_functions:
            summary.append("  Complex Functions (Top 3):")
            for func in self.project_metrics.complexity.complex_functions[:3]:
                summary.append(f"    - {func['name']} at {func['file_path']}:{func['line_number']}")
                summary.append(f"      Complexity: {func['complexity']}, Lines: {func['lines']}")
                summary.append(f"      Code Snippet: {func['code']}...")

        # Quality Metrics
        summary.append("\nQUALITY METRICS")
        summary.append("-" * 30)
        summary.append(f"Type Hint Coverage: {self.project_metrics.quality.type_hint_coverage:.1f}%")
        summary.append(f"  - Proportion of functions/variables with type annotations")
        summary.append(f"Documentation Coverage: {self.project_metrics.quality.documentation_coverage:.1f}%")
        summary.append(f"  - Percentage of modules, classes, and functions with docstrings")
        summary.append(f"Test Coverage (Estimated): {self.project_metrics.quality.test_coverage:.1f}%")
        summary.append(f"  - Rough estimate via assert statements; use `coverage.py` for precision")
        summary.append(f"Lint Score: {self.project_metrics.quality.lint_score:.1f}/100")
        summary.append(f"  - Reflects adherence to style guidelines (e.g., function length, error handling)")
        summary.append(f"Code-to-Comment Ratio: {self.project_metrics.quality.code_to_comment_ratio:.2f}")
        summary.append("  - Limited by AST; inline comments not captured")

        # Dependency Metrics
        summary.append("\nDEPENDENCY METRICS")
        summary.append("-" * 30)
        summary.append(f"Direct Dependencies: {len(self.project_metrics.dependencies.direct_dependencies)}")
        direct_deps = list(self.project_metrics.dependencies.direct_dependencies)[:3]
        if direct_deps:
            summary.append("  Examples of Direct Dependencies:")
            summary.extend(f"    - {dep}" for dep in direct_deps)
        summary.append(f"Dependency Health Score: {self.project_metrics.dependencies.health_score():.1f}/100")
        summary.append("  - Assesses outdated or risky dependencies")

        # Pattern Metrics
        summary.append("\nDESIGN PATTERN METRICS")
        summary.append("-" * 30)
        summary.append(f"Patterns Detected: {len(self.project_metrics.patterns.design_patterns)}")
        if self.project_metrics.patterns.design_patterns:
            summary.append("  Detected Patterns (Top 3):")
            for pattern in self.project_metrics.patterns.design_patterns[:3]:
                summary.append(f"    - {pattern.name} (Confidence: {pattern.confidence:.2f})")
                summary.append(f"      Locations: {', '.join(pattern.locations[:2])}")
                summary.append(f"      Description: {pattern.description}")

        # Security Metrics
        summary.append("\nSECURITY METRICS")
        summary.append("-" * 30)
        summary.append(f"Vulnerabilities Found: {len(self.project_metrics.security.vulnerabilities)}")
        summary.append(f"Security Score: {self.project_metrics.security.security_score:.1f}/100")
        if self.project_metrics.security.vulnerabilities:
            summary.append("  Identified Vulnerabilities (Top 3):")
            for vuln in self.project_metrics.security.vulnerabilities[:3]:
                summary.append(f"    - {vuln.type} at {vuln.location} (Severity: {vuln.severity})")
                summary.append(f"      Description: {vuln.description}")
                summary.append(f"      Recommendation: {vuln.recommendation}")
        if self.project_metrics.security.security_patterns:
            summary.append("  Security Patterns (Top 3):")
            for pattern in self.project_metrics.security.security_patterns[:3]:
                summary.append(f"    - {pattern.name} (Confidence: {pattern.confidence:.2f})")
                summary.append(f"      Locations: {', '.join(pattern.locations[:2])}")

        # Performance Metrics
        summary.append("\nPERFORMANCE METRICS")
        summary.append("-" * 30)
        summary.append(f"Hotspots Identified: {len(self.project_metrics.performance.hotspots)}")
        summary.append(f"Performance Score: {self.project_metrics.performance.performance_score:.1f}/100")
        if self.project_metrics.performance.hotspots:
            summary.append("  Performance Hotspots (Top 3):")
            for hotspot in self.project_metrics.performance.hotspots[:3]:
                summary.append(f"    - {hotspot.location} (Complexity: {hotspot.complexity})")
                summary.append(f"      Suggestion: {hotspot.optimization_suggestion}")
        if self.project_metrics.performance.loop_optimizations:
            summary.append("  Loop Optimization Opportunities (Top 3):")
            for opt in self.project_metrics.performance.loop_optimizations[:3]:
                summary.append(f"    - {opt.location} ({opt.loop_type}, Complexity: {opt.complexity})")
                summary.append(f"      Suggestion: {opt.suggestion}")
        if self.project_metrics.performance.memory_intensive_ops:
            summary.append("  Memory-Intensive Operations (Top 3):")
            summary.extend(f"    - {op}" for op in self.project_metrics.performance.memory_intensive_ops[:3])
        if self.project_metrics.performance.io_operations:
            summary.append("  I/O Operations (Top 3):")
            summary.extend(f"    - {op}" for op in self.project_metrics.performance.io_operations[:3])

        # Recommendations
        recommendations = self.recommendation_engine.generate_recommendations(self.project_metrics)
        if recommendations:
            summary.append("\nRECOMMENDATIONS FOR IMPROVEMENT")
            summary.append("=" * 30)
            summary.extend(f"  - {rec}" for rec in recommendations[:5])
            if len(recommendations) > 5:
                summary.append(f"  - {len(recommendations) - 5} additional recommendations available")

        return "\n".join(summary)