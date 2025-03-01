"""Module for analyzing project directories and generating detailed summaries.

This module provides the ProjectAnalyzer class, which scans a project directory,
analyzes files using type-specific analyzers, and produces a formatted summary
including dependency health information for LLM consumption.
"""

import ast
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from .python_analyzer import PythonAnalyzer
from .generic_analyzer import GenericAnalyzer
from ..formatters.summary_formatter import SummaryFormatter
from ..utils.file_utils import should_analyze_file, get_file_type
from ..models.data_classes import FileInfo

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger: logging.Logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    """Analyzes an entire project directory and generates a detailed summary for LLM advisors.

    This class orchestrates the analysis of a project by scanning all files, applying appropriate
    analyzers based on file type, and formatting the results into a comprehensive summary.
    It supports dependency health checks and detailed logging for debugging purposes.
    """

    def __init__(self, root_path: Path) -> None:
        """Initialize the ProjectAnalyzer with the project root directory.

        Args:
            root_path: Path to the root directory of the project to analyze.
        """
        self.root_path: Path = root_path
        self.formatter: SummaryFormatter = SummaryFormatter(root_path)
        self.ignored_dirs: Set[str] = {'.git', '__pycache__', '.pytest_cache', 'node_modules', 'venv', '.venv'}
        self.dependency_health: Dict[str, str] = self._check_dependency_health()

    def analyze(self) -> str:
        """Analyze the project and return a formatted summary with dependency health.

        This method scans the project directory recursively, excluding ignored directories,
        and processes each file using PythonAnalyzer for .py files or GenericAnalyzer for others.
        It logs debugging information about file processing and handles exceptions gracefully,
        ensuring a robust summary suitable for LLM consumption.

        Returns:
            str: Formatted summary string containing project structure, metrics, and dependency health.
        """
        project_files: List[Path] = self._get_project_files()
        for file_path in project_files:
            file_info: Optional[FileInfo] = self._analyze_file(file_path)
            if file_info:
                relative_path: Path = file_path.relative_to(self.root_path)
                logger.debug(f"Processing file_info for {file_path}: {file_info.__dict__}")
                self.formatter.add_source_file(str(relative_path), file_info)
                if not file_info.functions:
                    logger.debug(f"Function missing docstring: {file_info.functions}")
                if file_info.classes:
                    logger.debug(f"Class methods: {[method.__dict__ for method in list(file_info.classes.values())[0].methods]}")
                    for class_info in file_info.classes.values():
                        for method in class_info.methods:
                            if not method.docstring:
                                logger.debug(f"Method missing docstring: {method.__dict__}")
        self.formatter.add_dependency_health(self.dependency_health)
        try:
            return self.formatter.format_summary()
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}", exc_info=True)
            return f"Error analyzing project: {str(e)}"

    def _analyze_file(self, file_path: Path) -> Optional[FileInfo]:
        """Analyze a single file and return its detailed information.

        Determines the file type and applies the appropriate analyzer (PythonAnalyzer for .py,
        GenericAnalyzer for others). Skips files that should not be analyzed based on predefined rules.

        Args:
            file_path: Path to the file to analyze.

        Returns:
            Optional[FileInfo]: File information if analysis succeeds, None otherwise.
        """
        if not should_analyze_file(str(file_path)):
            return None

        file_type: str = get_file_type(str(file_path))
        analyzer_class = PythonAnalyzer if file_type == 'python' else GenericAnalyzer
        analyzer = analyzer_class(str(file_path))
        return analyzer.analyze()

    def _get_project_files(self) -> List[Path]:
        """Get all project files recursively, excluding ignored directories.

        Walks the directory tree starting from root_path, filtering out directories specified
        in ignored_dirs, and collects all file paths.

        Returns:
            List[Path]: List of file paths in the project.
        """
        project_files: List[Path] = []
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            for file in files:
                file_path: Path = Path(root) / file
                project_files.append(file_path)
        return project_files

    def _extract_project_metadata(self) -> Dict[str, str]:
        """Extract project metadata from setup.py and __init__.py files for context.

        Parses setup.py for project details (name, version, etc.) and __init__.py for version
        information, providing context for the summary.

        Returns:
            Dict[str, str]: Metadata dictionary with keys like 'name', 'version', etc.
        """
        metadata: Dict[str, str] = {'name': '', 'version': '', 'description': '', 'author': '', 'python_version': ''}
        setup_info: Dict[str, str] = self._extract_setup_info()
        metadata.update(setup_info)

        init_file: Path = self.root_path / '__init__.py'
        if init_file.exists():
            with open(init_file, encoding='utf-8') as f:
                content: str = f.read()
                try:
                    tree: ast.AST = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id == '__version__':
                                    if isinstance(node.value, ast.Str):
                                        metadata['version'] = node.value.s
                except SyntaxError:
                    pass

        return metadata

    def _extract_setup_info(self) -> Dict[str, str]:
        """Extract information from setup.py for project context.

        Reads and parses setup.py to extract metadata such as name, version, and author.

        Returns:
            Dict[str, str]: Metadata extracted from setup.py.
        """
        setup_file: Path = self.root_path / 'setup.py'
        metadata: Dict[str, str] = {}
        if setup_file.exists():
            with open(setup_file, encoding='utf-8') as f:
                content: str = f.read()
                try:
                    tree: ast.AST = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'setup':
                            for keyword in node.keywords:
                                if keyword.arg in ['name', 'version', 'description', 'author', 'python_requires']:
                                    if isinstance(keyword.value, ast.Str):
                                        metadata[keyword.arg] = keyword.value.s
                                    elif isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                                        metadata[keyword.arg] = keyword.value.value
                except SyntaxError:
                    pass
        return metadata

    def _check_dependency_health(self) -> Dict[str, str]:
        """Check dependency health using pip and safety.

        Executes 'pip list --outdated' and 'safety check' to assess dependency status,
        capturing output for inclusion in the summary.

        Returns:
            Dict[str, str]: Health report with 'outdated' and 'vulnerabilities' keys.
        """
        health: Dict[str, str] = {'outdated': '', 'vulnerabilities': ''}
        try:
            result = subprocess.run(['pip', 'list', '--outdated'], capture_output=True, text=True)
            health['outdated'] = result.stdout.strip() or "All packages up-to-date"
        except Exception as e:
            health['outdated'] = f"Error checking outdated packages: {str(e)}"

        try:
            result = subprocess.run(['safety', 'check'], capture_output=True, text=True)
            health['vulnerabilities'] = result.stdout.strip() or "No vulnerabilities found"
        except Exception as e:
            health['vulnerabilities'] = f"Error checking vulnerabilities: {str(e)} (install `safety` with `pip install safety`)"
        return health