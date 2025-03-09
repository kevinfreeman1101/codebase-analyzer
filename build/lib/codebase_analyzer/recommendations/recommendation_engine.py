"""Module for generating recommendations based on codebase analysis."""

from typing import List, Any
from dataclasses import dataclass
from codebase_analyzer.models.data_classes import Recommendation, ProjectMetrics

@dataclass
class RecommendationEngine:
    """Generates actionable recommendations based on project metrics."""
    recommendations: List[Recommendation] = None

    def __post_init__(self):
        self.recommendations = []

    def generate_recommendations(self, metrics: ProjectMetrics) -> List[str]:
        """Generate a list of recommendation strings from project metrics.

        Args:
            metrics: ProjectMetrics object containing analysis results.

        Returns:
            List[str]: Formatted recommendation strings.
        """
        self.recommendations.clear()
        self._analyze_complexity_metrics(metrics.complexity)
        self._analyze_quality_metrics(metrics.quality)
        self._analyze_dependency_metrics(metrics.dependencies)
        self._analyze_pattern_metrics(metrics.patterns)
        self._analyze_security_metrics(metrics.security)
        self._analyze_performance_metrics(metrics.performance)

        return [f"[{r.priority}] {r.category}: {r.description}\n  Suggestion: {r.suggestion}" 
                for r in self.recommendations]

    def _analyze_complexity_metrics(self, metrics: Any) -> None:
        """Analyze complexity metrics and provide recommendations."""
        if metrics.cyclomatic_complexity > 10:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Complexity",
                description="High average cyclomatic complexity detected",
                suggestion="Refactor complex functions to reduce decision points"
            ))
        if metrics.maintainability_index < 50:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Complexity",
                description="Low maintainability index",
                suggestion="Simplify code structure and improve readability"
            ))
        if metrics.complex_functions:
            high_complexity = [f for f in metrics.complex_functions if f["complexity"] > 10]
            if high_complexity:
                self.recommendations.append(Recommendation(
                    priority="HIGH",
                    category="Complexity",
                    description=f"{len(high_complexity)} functions with excessive complexity",
                    suggestion=f"Refactor functions like {high_complexity[0]['name']} at {high_complexity[0]['file_path']}:{high_complexity[0]['line_number']}"
                ))

    def _analyze_quality_metrics(self, metrics: Any) -> None:
        """Analyze quality metrics and provide recommendations."""
        if metrics.type_hint_coverage < 50:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Quality",
                description="Low type hint coverage",
                suggestion="Add type annotations to improve code reliability and IDE support"
            ))
        if metrics.documentation_coverage < 50:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Quality",
                description="Insufficient documentation coverage",
                suggestion="Add docstrings to functions, classes, and modules"
            ))
        if metrics.test_coverage < 50:
            self.recommendations.append(Recommendation(
                priority="HIGH",
                category="Quality",
                description="Insufficient test coverage",
                suggestion="Increase unit test coverage to ensure code reliability"
            ))
        if metrics.lint_score < 75:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Quality",
                description="Low lint score",
                suggestion="Address style issues like long functions or bare excepts"
            ))

    def _analyze_dependency_metrics(self, metrics: Any) -> None:
        """Analyze dependency metrics and provide recommendations."""
        if metrics.health_score() < 75:
            self.recommendations.append(Recommendation(
                priority="HIGH",
                category="Dependencies",
                description="Low dependency health score",
                suggestion="Update or replace outdated/vulnerable dependencies"
            ))

    def _analyze_pattern_metrics(self, metrics: Any) -> None:
        """Analyze pattern metrics and provide recommendations."""
        if not metrics.design_patterns:
            self.recommendations.append(Recommendation(
                priority="LOW",
                category="Patterns",
                description="No design patterns detected",
                suggestion="Consider applying appropriate design patterns for better structure"
            ))

    def _analyze_security_metrics(self, metrics: Any) -> None:
        """Analyze security metrics and provide recommendations."""
        if len(metrics.vulnerabilities) > 0:
            self.recommendations.append(Recommendation(
                priority="HIGH",
                category="Security",
                description=f"{len(metrics.vulnerabilities)} security vulnerabilities detected",
                suggestion="Address critical vulnerabilities immediately (e.g., eval usage)"
            ))
        if metrics.security_score < 75:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Security",
                description="Low security score",
                suggestion="Review code for insecure practices and apply security patterns"
            ))

    def _analyze_performance_metrics(self, metrics: Any) -> None:
        """Analyze performance metrics and provide recommendations."""
        if len(metrics.hotspots) > 0:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Performance",
                description=f"{len(metrics.hotspots)} performance hotspots identified",
                suggestion=f"Optimize functions like {metrics.hotspots[0].location}"
            ))
        if metrics.performance_score < 75:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Performance",
                description="Low performance score",
                suggestion="Review hotspots and optimize loops or I/O operations"
            ))