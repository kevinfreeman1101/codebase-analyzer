"""Analyzer for entire Python projects."""

import logging
import subprocess
from typing import Dict, Optional
from pathlib import Path
from .python_analyzer import PythonAnalyzer
from .generic_analyzer import GenericAnalyzer
from ..formatters.summary_formatter import SummaryFormatter
from ..models.data_classes import FileInfo

logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    """Analyzes an entire project directory."""

    def __init__(self, root_path: Path):
        """Initialize the ProjectAnalyzer with project root.

        Args:
            root_path: Path to the project root directory.
        """
        self.root_path = root_path
        self.formatter: SummaryFormatter = SummaryFormatter(root_path)

    def analyze(self) -> str:
        """Analyze the project and return a summary.

        Returns:
            str: A formatted summary of the project analysis.
        """
        logger.info(f"Analyzing project at {self.root_path}")
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                file_info: Optional[FileInfo] = self._analyze_file(file_path)
                if file_info:
                    relative_path = file_path.relative_to(self.root_path)
                    self.formatter.add_source_file(str(relative_path), file_info)

        try:
            outdated = subprocess.run(
                ["pip", "list", "--outdated"],
                capture_output=True,
                text=True,
                check=False
            )
            self.formatter.dependency_health['outdated'] = outdated.stdout
        except subprocess.SubprocessError as e:
            logger.warning(f"Failed to check outdated packages: {str(e)}")

        try:
            vulnerabilities = subprocess.run(
                ["safety", "check"],
                capture_output=True,
                text=True,
                check=False
            )
            self.formatter.dependency_health['vulnerabilities'] = vulnerabilities.stdout
        except subprocess.SubprocessError as e:
            logger.warning(f"Failed to check vulnerabilities: {str(e)}")

        return self.formatter.generate_summary()

    def _analyze_file(self, file_path: Path) -> Optional[FileInfo]:
        """Analyze a single file within the project.

        Args:
            file_path: Path to the file to analyze.

        Returns:
            Optional[FileInfo]: File information if analysis succeeds or partially succeeds, None otherwise.
        """
        extension = file_path.suffix.lower()
        if extension == '.py':
            analyzer = PythonAnalyzer(file_path)
        else:
            analyzer = GenericAnalyzer(file_path)

        return analyzer.analyze()

    def _get_dependency_health(self) -> Dict[str, str]:
        """Check dependency health using external tools.

        Returns:
            Dict[str, str]: Dictionary containing outdated packages and vulnerability reports.
        """
        health = {'outdated': '', 'vulnerabilities': ''}

        try:
            outdated = subprocess.run(
                ["pip", "list", "--outdated"],
                capture_output=True,
                text=True,
                check=False
            )
            health['outdated'] = outdated.stdout
        except subprocess.SubprocessError as e:
            logger.warning(f"Failed to check outdated packages: {str(e)}")

        try:
            vulnerabilities = subprocess.run(
                ["safety", "check"],
                capture_output=True,
                text=True,
                check=False
            )
            health['vulnerabilities'] = vulnerabilities.stdout
        except subprocess.SubprocessError as e:
            logger.warning(f"Failed to check vulnerabilities: {str(e)}")

        return health