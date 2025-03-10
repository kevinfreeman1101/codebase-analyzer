from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import logging
from .metrics.complexity_analyzer import ComplexityAnalyzer, ComplexityMetrics
from .metrics.quality_metrics import QualityAnalyzer, QualityMetrics
from .metrics.security_metrics import SecurityAnalyzer, SecurityMetrics
from .metrics.performance_metrics import PerformanceAnalyzer, PerformanceMetrics
from .models.data_classes import ProjectMetrics
from .recommendations.recommendation_engine import RecommendationEngine
from .analyzers.project_analyzer import ProjectAnalyzer
from .formatters.summary_formatter import SummaryFormatter

from collections import namedtuple
from collections import namedtuple
from collections import namedtuple
from collections import namedtuple
from collections import namedtuple
from collections import namedtuple
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodebaseAnalyzer:
    def __init__(self) -> None:
        """Initialize the CodebaseAnalyzer with component analyzers."""
        self.complexity_analyzer = ComplexityAnalyzer()
        self.quality_analyzer = QualityAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.project_metrics: Optional[ProjectMetrics] = None
        self.project_analyzer: Optional[ProjectAnalyzer] = None
        self.errors: List[str] = []
        self.formatter = SummaryFormatter(Path.cwd())

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
        total_lines = sum(file_info.lines for file_info in analysis_result["results"].values())
        result = {
            "total_files": total_files,
            "total_lines": total_lines,
            "results": analysis_result["results"],
            "summary": analysis_result["summary"],
            "dependency_health": analysis_result["dependency_health"]
        }
        complexity_result = self.complexity_analyzer.analyze_project(project_path)
        quality_result = self.quality_analyzer.analyze_project(project_path)
        security_result = self.security_analyzer.analyze_project(project_path)
        performance_result = self.performance_analyzer.analyze_project(project_path)
        result["performance"] = {"performance_score": performance_result.performance_score}
        result["security"] = {"vulnerabilities": security_result.vulnerabilities}
        result["quality"] = {"lint_score": quality_result.lint_score}
        result["complexity"] = {"cyclomatic_complexity": complexity_result.cyclomatic_complexity}
        return result

    def generate_summary(self) -> str:
        """Generate a summary of the analysis results."""
        if not self.project_analyzer:
            return "No analysis data available"
        if self.errors:
            return "Errors during analysis:\n- " + "\n- ".join(self.errors)
        if not hasattr(self, 'last_result'):  # Store result to persist metrics and summary
            self.last_result = self.analyze_project(Path(self.project_analyzer.root_path))
            self.project_metrics = namedtuple("Metrics", ["total_files"])(self.last_result.get("total_files", 0))  # Sync metrics as object
        complexity_summary = f"COMPLEXITY METRICS\nAverage Cyclomatic Complexity: {self.last_result['complexity']['cyclomatic_complexity']}"
        quality_summary = f"QUALITY METRICS\nAverage Lint Score: {self.last_result['quality']['lint_score']}"
        return f"CODEBASE ANALYSIS SUMMARY\nTotal Python Files: {self.project_metrics.total_files}\n{complexity_summary}\n{quality_summary}\n" + self.last_result["summary"]
