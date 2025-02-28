from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path
from ..models.data_classes import ProjectMetrics

@dataclass
class Recommendation:
    priority: str
    category: str
    description: str
    suggestion: str

class RecommendationEngine:
    """Generates actionable recommendations based on codebase metrics."""

    def __init__(self):
        self.recommendations: List[Recommendation] = []

    def generate_recommendations(self, metrics: ProjectMetrics) -> List[str]:
        """Generate comprehensive recommendations based on all metrics."""
        self.recommendations = []
        self._analyze_security_metrics(metrics.security)
        self._analyze_complexity_metrics(metrics.complexity)
        self._analyze_quality_metrics(metrics.quality)
        self._analyze_dependency_metrics(metrics.dependencies)
        self._analyze_performance_metrics(metrics.performance)
        self._analyze_pattern_metrics(metrics.patterns)

        return [self._format_recommendation(r) for r in self.recommendations]

    def _analyze_security_metrics(self, metrics: Any) -> None:
        """Analyze security metrics and provide recommendations."""
        if len(metrics.vulnerabilities) > 0:
            self.recommendations.append(Recommendation(
                priority="HIGH",
                category="Security",
                description=f"Found {len(metrics.vulnerabilities)} security vulnerabilities",
                suggestion="Address vulnerabilities: " + ", ".join(v.type for v in metrics.vulnerabilities)
            ))
        if metrics.security_score < 70:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Security",
                description="Low security score detected",
                suggestion="Review security practices and implement additional protections"
            ))

    def _analyze_complexity_metrics(self, metrics: Any) -> None:
        """Analyze complexity metrics and provide recommendations."""
        if metrics.cyclomatic_complexity > 10:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Complexity",
                description="High cyclomatic complexity detected",
                suggestion="Refactor complex functions to reduce decision points"
            ))
        if metrics.maintainability_index < 50:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Complexity",
                description="Low maintainability index",
                suggestion="Simplify code structure and improve readability"
            ))
        if metrics.nesting_depth > 5:
            self.recommendations.append(Recommendation(
                priority="LOW",
                category="Complexity",
                description="Excessive nesting detected",
                suggestion="Reduce nesting levels by extracting logic into separate functions"
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
        if metrics.documentation_coverage < 70:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Quality",
                description="Insufficient documentation coverage",
                suggestion="Add docstrings to functions, classes, and modules"
            ))
        if metrics.test_coverage < 80:
            self.recommendations.append(Recommendation(
                priority="HIGH",
                category="Quality",
                description="Insufficient test coverage",
                suggestion="Increase unit test coverage to ensure code reliability"
            ))

    def _analyze_dependency_metrics(self, metrics: Any) -> None:
        """Analyze dependency metrics and provide recommendations."""
        if metrics.circular_dependencies:
            self.recommendations.append(Recommendation(
                priority="HIGH",
                category="Dependencies",
                description=f"Found {len(metrics.circular_dependencies)} circular dependencies",
                suggestion="Refactor code to eliminate circular imports"
            ))
        if metrics.unused_imports:
            self.recommendations.append(Recommendation(
                priority="LOW",
                category="Dependencies",
                description=f"Found {len(metrics.unused_imports)} unused imports",
                suggestion="Remove unused imports: " + ", ".join(metrics.unused_imports)
            ))
        if metrics.health_score() < 80:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Dependencies",
                description="Dependency health score below threshold",
                suggestion="Review dependency versions and security advisories"
            ))

    def _analyze_performance_metrics(self, metrics: Any) -> None:
        """Analyze performance metrics and provide recommendations."""
        if metrics.hotspots:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Performance",
                description=f"Found {len(metrics.hotspots)} performance hotspots",
                suggestion="Optimize identified hotspots: " + ", ".join(h.location for h in metrics.hotspots)
            ))
        if metrics.loop_optimizations:
            self.recommendations.append(Recommendation(
                priority="LOW",
                category="Performance",
                description=f"Found {len(metrics.loop_optimizations)} loop optimization opportunities",
                suggestion="Apply suggestions: " + ", ".join(o.suggestion for o in metrics.loop_optimizations)
            ))
        if metrics.performance_score < 70:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Performance",
                description="Low performance score detected",
                suggestion="Profile and optimize code execution"
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
        if metrics.anti_patterns:
            self.recommendations.append(Recommendation(
                priority="MEDIUM",
                category="Patterns",
                description=f"Found {len(metrics.anti_patterns)} anti-patterns",
                suggestion="Refactor to eliminate anti-patterns"
            ))

    def _format_recommendation(self, rec: Recommendation) -> str:
        """Format a recommendation into a readable string."""
        return f"[{rec.priority}] {rec.category}: {rec.description}\n  Suggestion: {rec.suggestion}"