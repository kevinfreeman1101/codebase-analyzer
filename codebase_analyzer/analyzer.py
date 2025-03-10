import logging
from pathlib import Path
from codebase_analyzer.analyzers.project_analyzer import ProjectAnalyzer
from codebase_analyzer.features.manager import FeatureExtractorManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CodebaseAnalyzer:
    def __init__(self, root_path="."):
        path = Path(root_path)
        logging.info("Initializing CodebaseAnalyzer with root_path: %s", path)
        self.project_analyzer = ProjectAnalyzer(root_path=path)
        self.feature_manager = FeatureExtractorManager()
        self.results = {}
        logging.info("CodebaseAnalyzer initialized")

    def analyze_project(self, project_path):
        logging.info("Starting analyze_project with path: %s (type: %s)", project_path, type(project_path))
        path = Path(project_path)
        logging.info("Converted path to: %s", path)
        if not path.exists():
            logging.error("Path does not exist: %s", path)
            raise FileNotFoundError(f"Project path does not exist: {path}")
        logging.info("Path exists, proceeding with analysis")
        
        # Use root_path set in ProjectAnalyzer, no need to pass path
        project_metrics = self.project_analyzer.analyze()
        logging.info("Project metrics collected: %s", project_metrics.keys())
        
        feature_metrics = self.feature_manager.extract_all(path)
        logging.info("Feature metrics collected: %s", feature_metrics.keys())
        
        self.results = {
            "project_metrics": project_metrics,
            "feature_metrics": feature_metrics,
            "total_files": project_metrics.get("total_files", 0),
            "total_lines": project_metrics.get("total_lines", 0)
        }
        logging.info("Finished analyzing project")
        return self.results

    def generate_summary(self):
        logging.info("Generating summary from results: %s", self.results.keys())
        summary = f"Total Files: {self.results.get('total_files', 0)}\nTotal Lines: {self.results.get('total_lines', 0)}"
        return summary
