from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import logging
from .metrics.complexity_analyzer import ComplexityAnalyzer, ComplexityMetrics
from .metrics.quality_metrics import QualityAnalyzer, QualityMetrics
from .metrics.dependency_metrics import DependencyAnalyzer, DependencyMetrics
from .metrics.pattern_metrics import PatternAnalyzer, PatternMetrics
from .metrics.security_metrics import SecurityAnalyzer, SecurityMetrics
from .metrics.performance_metrics import PerformanceAnalyzer, PerformanceMetrics
from .models.data_classes import ProjectMetrics
from .recommendations.recommendation_engine import RecommendationEngine
from .formatters.summary_formatter import SummaryFormatter
from .analyzers.project_analyzer import ProjectAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodebaseAnalyzer:
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
        self.project_analyzer: Optional[ProjectAnalyzer] = None
        self.errors: List[str] = []

    def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """Analyze the project directory and return structured results."""
        if not project_path.exists():
            error_msg = f"Project path does not exist: {project_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        logger.info("Starting comprehensive project analysis...")
        self.errors.clear()
        self.project_analyzer = ProjectAnalyzer(str(project_path))
        analysis_result = self.project_analyzer.analyze()

        total_files = len(analysis_result["results"])
        total_lines = sum(
            getattr(r, "lines", 0) for r in analysis_result["results"].values() if not getattr(r, "skipped", False)
        )

        # Use PatternAnalyzer to get pattern metrics
        pattern_metrics = self.pattern_analyzer.analyze_project(project_path)

        self.project_metrics = ProjectMetrics(
            complexity=ComplexityMetrics(0.0, 0.0, []),
            quality=QualityMetrics(0.0, 0.0, 0.0, 0.0, 0.0),
            dependencies=DependencyMetrics(set(), analysis_result["dependency_health"], []),
            patterns=pattern_metrics,
            security=SecurityMetrics([], 0.0, []),
            performance=PerformanceMetrics([], 0.0, [], [], []),
            timestamp=datetime.now(),
            project_path=project_path,
            total_files=total_files,
            total_lines=total_lines
        )

        return analysis_result

    def generate_summary(self) -> str:
        """Generate a detailed summary of the analysis."""
        if not self.project_analyzer or not self.project_metrics:
            return "No analysis data available. Run analyze_project first."

        analysis_result = self.project_analyzer.analyze()  # Re-run for latest summary
        summary = analysis_result["summary"]
        if self.errors:
            summary += "\n\nANALYSIS ERRORS\n" + "-" * 30
            summary += "\n".join(f"  - {error}" for error in self.errors[:5])
            if len(self.errors) > 5:
                summary += f"\n  - {len(self.errors) - 5} additional errors logged"
        return summary