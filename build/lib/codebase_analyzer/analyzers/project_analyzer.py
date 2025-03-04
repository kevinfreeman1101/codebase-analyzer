import ast
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from .python_analyzer import PythonAnalyzer
from .generic_analyzer import GenericAnalyzer
from ..formatters.summary_formatter import SummaryFormatter
from ..utils.file_utils import should_analyze_file, get_file_type
from ..models.data_classes import FileInfo

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    """Analyzes an entire project directory and generates a summary."""

    def __init__(self, root_path: Path):
        """Initialize the ProjectAnalyzer.

        Args:
            root_path: Path to the project root directory
        """
        self.root_path = root_path
        self.formatter = SummaryFormatter(root_path)
        self.ignored_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', 'venv', '.venv'}

    def analyze(self) -> str:
        """Analyze the project and return a formatted summary."""
        project_files = self._get_project_files()
        for file_path in project_files:
            file_info = self._analyze_file(file_path)
            if file_info:
                relative_path = file_path.relative_to(self.root_path)
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
        try:
            return self.formatter.format_summary()
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}", exc_info=True)
            return f"Error analyzing project: {str(e)}"

    def _analyze_file(self, file_path: Path) -> Optional[FileInfo]:
        """Analyze a single file and return its information.

        Args:
            file_path: Path to the file to analyze

        Returns:
            FileInfo containing file information or None if analysis fails
        """
        if not should_analyze_file(str(file_path)):
            return None

        file_type = get_file_type(str(file_path))
        analyzer_class = PythonAnalyzer if file_type == 'python' else GenericAnalyzer
        analyzer = analyzer_class(str(file_path))
        return analyzer.analyze()

    def _get_project_files(self) -> List[Path]:
        """Get all project files recursively.

        Returns:
            List of Path objects for all files in the project
        """
        project_files = []
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            for file in files:
                file_path = Path(root) / file
                project_files.append(file_path)
        return project_files

    def _extract_project_metadata(self) -> Dict[str, str]:
        """Extract project metadata from setup.py and __init__.py files."""
        metadata = {'name': '', 'version': '', 'description': '', 'author': '', 'python_version': ''}
        setup_info = self._extract_setup_info()
        metadata.update(setup_info)

        init_file = self.root_path / '__init__.py'
        if init_file.exists():
            with open(init_file) as f:
                content = f.read()
                try:
                    tree = ast.parse(content)
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
        """Extract information from setup.py."""
        setup_file = self.root_path / 'setup.py'
        metadata = {}
        if setup_file.exists():
            with open(setup_file) as f:
                content = f.read()
                try:
                    tree = ast.parse(content)
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