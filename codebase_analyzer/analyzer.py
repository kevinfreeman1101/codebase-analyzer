from datetime import datetime
from typing import Dict, Optional
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
    """Main class for analyzing codebases and generating metrics."""

    def __init__(self):
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
        """Generate a human-readable summary of the analysis.

        Returns:
            str: Formatted summary string.
        """
        if not self.project_metrics:
            return "No analysis data available. Run analyze_project first."

        summary = []
        summary.append("Codebase Analysis Summary")
        summary.append("=========================")
        summary.append(f"Project Path: {self.project_metrics.project_path}")
        summary.append(f"Analysis Timestamp: {self.project_metrics.timestamp}")
        summary.append(f"Total Files: {self.project_metrics.total_files}")
        summary.append(f"Total Lines: {self.project_metrics.total_lines}")
        
        summary.append("\nComplexity Metrics")
        summary.append(f"  Cyclomatic Complexity: {self.project_metrics.complexity.cyclomatic_complexity}")
        summary.append(f"  Maintainability Index: {self.project_metrics.complexity.maintainability_index:.1f}")

        summary.append("\nQuality Metrics")
        summary.append(f"  Type Hint Coverage: {self.project_metrics.quality.type_hint_coverage:.1f}%")
        summary.append(f"  Documentation Coverage: {self.project_metrics.quality.documentation_coverage:.1f}%")

        summary.append("\nDependency Metrics")
        summary.append(f"  Direct Dependencies: {len(self.project_metrics.dependencies.direct_dependencies)}")

        summary.append("\nPattern Metrics")
        summary.append(f"  Design Patterns Detected: {len(self.project_metrics.patterns.design_patterns)}")

        summary.append("\nSecurity Metrics")
        summary.append(f"  Vulnerabilities Found: {len(self.project_metrics.security.vulnerabilities)}")
        summary.append(f"  Security Score: {self.project_metrics.security.security_score:.1f}")

        summary.append("\nPerformance Metrics")
        summary.append(f"  Hotspots Identified: {len(self.project_metrics.performance.hotspots)}")
        
        summary.append(f"\nOverall Project Score: {self.project_metrics.calculate_overall_score():.1f}/100")
        
        recommendations = self.recommendation_engine.generate_recommendations(self.project_metrics)
        if recommendations:
            summary.append("\nRecommendations")
            summary.append("---------------")
            summary.extend(recommendations)

        return "\n".join(summary)