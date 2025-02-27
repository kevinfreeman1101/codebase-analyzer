from pathlib import Path
from typing import Dict, Optional, Set, Union, List
import mimetypes
import ast
import re
from .python_analyzer import PythonAnalyzer
from .generic_analyzer import GenericAnalyzer
from ..formatters.summary_formatter import SummaryFormatter
from ..utils.file_utils import safe_read_file, should_analyze_file, get_file_type
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    """Analyzes an entire project directory and generates a summary."""

    def __init__(self, root_path: Union[str, Path]):
        """Initialize the ProjectAnalyzer.

        Args:
            root_path: Path to the project root directory
        """
        self.root_path = Path(root_path)
        self.formatter = SummaryFormatter(self.root_path)
        self.dependencies = set()
        self.total_functions = 0
        self.documented_functions = 0
        self._extract_project_metadata()

    def _get_file_type(self, file_path: Path) -> str:
        """Determine the file type based on extension."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type:
            main_type = mime_type.split('/')[0]
            if main_type in ['text', 'application']:
                return mime_type.split('/')[-1]
            return main_type
        ext = file_path.suffix.lower()
        if ext in ['.md', '.rst']:
            return 'documentation'
        elif ext in ['.json', '.yaml', '.yml', '.toml']:
            return 'configuration'
        elif ext in ['.txt', '.log']:
            return 'text'
        return 'unknown'

    def _clean_dependencies(self, deps: Set[str]) -> Dict[str, Set[str]]:
        """Clean up and categorize dependencies."""
        categories = {
            'required': set(),
            'standard': set(),
            'development': set()
        }
        stdlib_modules = {
            'abc', 'argparse', 'ast', 'collections', 'dataclasses', 
            'datetime', 'enum', 'functools', 'importlib', 'inspect',
            'json', 'logging', 'mimetypes', 'os', 'pathlib', 'pickle',
            're', 'sys', 'time', 'tkinter', 'typing', 'unittest', 'warnings'
        }
        dev_packages = {
            'pytest', 'pylint', 'mypy', 'black', 'flake8', 'coverage',
            'tox', 'sphinx', 'doctest', 'unittest'
        }
        internal_modules = {
            'base_analyzer', 'generic_analyzer', 'python_analyzer', 'main',
            'analyzers', 'formatters', 'models', 'utils', 'codebase_analyzer'
        }
        for dep in deps:
            root_pkg = dep.split('.')[0]
            if root_pkg in stdlib_modules:
                categories['standard'].add(root_pkg)
            elif root_pkg in dev_packages:
                categories['development'].add(root_pkg)
            elif root_pkg not in internal_modules:
                categories['required'].add(root_pkg)
        return categories

    def _extract_setup_info(self, setup_path: Path) -> None:
        """Extract information from setup.py."""
        if not setup_path.exists():
            return
        try:
            with open(setup_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'setup':
                    for kw in node.keywords:
                        if kw.arg == 'python_requires':
                            if isinstance(kw.value, ast.Constant):
                                version_match = re.search(r'>=\s*(\d+\.\d+)', str(kw.value.value))
                                if version_match:
                                    self.formatter.set_python_version(version_match.group(1))
                        elif kw.arg == 'description':
                            if isinstance(kw.value, ast.Constant):
                                self.formatter.set_project_overview(str(kw.value.value))
        except Exception:
            pass

    def analyze(self) -> str:
        """Analyze the project and return a formatted summary."""
        try:
            for file_path in self._get_project_files():
                if any(part.startswith('.') or part == '__pycache__' 
                    for part in file_path.parts):
                    continue

                relative_path = file_path.relative_to(self.root_path)
                file_info = self._analyze_file(file_path)

                if file_info:
                    logger.debug(f"Processing file_info for {file_path}: {file_info}")
                    # Process classes
                    for class_info in file_info.get('classes', {}).values():
                        methods = class_info.get('methods', [])
                        logger.debug(f"Class methods: {methods}")
                        if isinstance(methods, list):
                            for method in methods:
                                self.total_functions += 1
                                if method.docstring:  # Direct attribute access for FunctionInfo
                                    self.documented_functions += 1
                                else:
                                    logger.debug(f"Method missing docstring: {method}")

                    # Process standalone functions
                    for func_info in file_info.get('functions', {}).values():
                        self.total_functions += 1
                        if func_info.get('docstring'):
                            self.documented_functions += 1
                        else:
                            logger.debug(f"Function missing docstring: {func_info}")

                    self.formatter.add_source_file(str(relative_path), file_info)
                    if file_info['dependencies']:
                        self.dependencies.update(file_info['dependencies'])

            return self.formatter.format_summary()
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}", exc_info=True)
            return f"Error analyzing project: {str(e)}"

    def _get_project_files(self) -> List[Path]:
        """Get all project files recursively.

        Returns:
            List of Path objects for all files in the project
        """
        files = []
        for path in self.root_path.rglob('*'):
            if path.is_file():
                files.append(path)
        return files

    def _analyze_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a single file and return its information.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dictionary containing file information or None if analysis fails
        """
        try:
            if not should_analyze_file(str(file_path)):
                return None

            if file_path.suffix == '.py':
                analyzer = PythonAnalyzer(str(file_path))
                file_info = analyzer.analyze()
                if file_info:
                    functions_dict = {}
                    for name, func in file_info.functions.items():
                        functions_dict[name] = {
                            'docstring': func.docstring,
                            'params': func.params,
                            'returns': func.returns,
                            'dependencies': func.dependencies,
                            'loc': func.loc,
                            'code': func.code,
                            'file_path': str(file_path)
                        }

                    classes_dict = {}
                    for name, cls in file_info.classes.items():
                        classes_dict[name] = {
                            'docstring': cls.docstring,
                            'methods': cls.methods,
                            'base_classes': cls.base_classes,
                            'attributes': cls.attributes,
                            'code': cls.code
                        }

                    return {
                        'type': 'python',
                        'size': file_info.size,
                        'content': file_info.content,
                        'dependencies': self._clean_dependencies(file_info.dependencies),
                        'functions': functions_dict,
                        'classes': classes_dict
                    }
            else:
                try:
                    content = safe_read_file(str(file_path))
                    return {
                        'type': get_file_type(str(file_path)),
                        'size': len(content.encode('utf-8')),
                        'content': None,
                        'dependencies': {},
                        'functions': {},
                        'classes': {}
                    }
                except IOError as e:
                    logger.warning(f"Skipping file {file_path}: {str(e)}")
                    return None
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}", exc_info=True)
            return None

    def _extract_project_metadata(self) -> None:
        """Extract project metadata from setup.py and __init__.py files."""
        metadata = {
            'name': self.root_path.name,
            'description': '',
            'python_version': '',
            'author': '',
            'version': ''
        }
        setup_path = self.root_path / 'setup.py'
        if setup_path.exists():
            try:
                with open(setup_path, 'r') as f:
                    content = f.read()
                description_match = re.search(r'description=["\'](.+?)["\']', content)
                if description_match:
                    metadata['description'] = description_match.group(1)
                version_match = re.search(r'version=["\'](.+?)["\']', content)
                if version_match:
                    metadata['version'] = version_match.group(1)
                author_match = re.search(r'author=["\'](.+?)["\']', content)
                if author_match:
                    metadata['author'] = author_match.group(1)
                python_requires = re.search(r'python_requires=["\'](.+?)["\']', content)
                if python_requires:
                    metadata['python_version'] = python_requires.group(1)
            except Exception as e:
                print(f"Error reading setup.py: {str(e)}")
        if not metadata['description']:
            init_path = self.root_path / '__init__.py'
            if init_path.exists():
                try:
                    with open(init_path, 'r') as f:
                        content = f.read()
                    module = ast.parse(content)
                    docstring = ast.get_docstring(module)
                    if docstring:
                        metadata['description'] = docstring.split('\n')[0]
                except Exception as e:
                    print(f"Error reading __init__.py: {str(e)}")
        self.formatter.update_project_overview(metadata)