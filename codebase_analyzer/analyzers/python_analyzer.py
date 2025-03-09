"""Analyzer for Python source files, extracting functions, classes, and dependencies."""

from typing import Dict, Optional, Set
from pathlib import Path
import ast
from ..models.data_classes import FileInfo, FunctionInfo, ClassInfo, MethodInfo
from .base_analyzer import BaseAnalyzer

class PythonAnalyzer(BaseAnalyzer):
    """Analyzes Python source files to extract functions, classes, and dependencies."""

    def __init__(self, file_path: Path, dependencies: Optional[Set[str]] = None) -> None:
        super().__init__(file_path)
        self.dependencies: Set[str] = dependencies if dependencies is not None else set()

    def get_file_type(self) -> str:
        """Return the type of file being analyzed.

        Returns:
            str: The file type ('python').
        """
        return "python"

    def analyze(self) -> Optional[FileInfo]:
        """Analyze the Python source file and return structured information.

        Returns:
            Optional[FileInfo]: FileInfo object with analysis results, or None if analysis fails.
        """
        source = self._read_file()
        if source is None:
            return FileInfo(
                file_path=self.file_path,
                type=self.get_file_type(),
                size=0 if not self.file_path.exists() else self.file_path.stat().st_size,
                lines=0,
                functions={},
                classes={},
                dependencies=self.dependencies,
                skipped=True
            )

        try:
            lines = len(source.splitlines())
            if not source.strip():  # Empty file
                return FileInfo(
                    file_path=self.file_path,
                    type=self.get_file_type(),
                    size=self.file_path.stat().st_size,
                    lines=lines,
                    functions={},
                    classes={},
                    dependencies=self.dependencies,
                    skipped=False
                )

            tree = ast.parse(source)
            functions: Dict[str, FunctionInfo] = {}
            classes: Dict[str, ClassInfo] = {}
            imported_names: Set[str] = set()
            alias_names: Dict[str, str] = {}  # Map alias to original name
            used_names: Set[str] = set()

            # First pass: Collect imports and track used names
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        module = name.name.split('.')[0]
                        imported_names.add(module)
                        if name.asname:
                            alias_names[name.asname] = module
                        else:
                            alias_names[module] = module
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module.split('.')[0]
                        imported_names.add(module)
                        for name in node.names:
                            if name.asname:
                                alias_names[name.asname] = name.name
                            else:
                                alias_names[name.name] = name.name
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    current = node
                    while isinstance(current, ast.Attribute):
                        current = current.value
                    if isinstance(current, ast.Name):
                        used_names.add(current.id)

            self.dependencies.update(imported_names)
            unused_imports = {name for name in imported_names if not any(used_name in alias_names and alias_names[used_name] == name for used_name in used_names)}

            # Second pass: Analyze functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    params = [arg.arg for arg in node.args.args]
                    complexity = 1
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                            complexity += 1
                    returns = "None"
                    for child in ast.walk(node):
                        if isinstance(child, ast.Return):
                            if child.value is None:
                                returns = "None"
                            elif isinstance(child.value, ast.Constant):
                                if isinstance(child.value.value, (int, float)):
                                    returns = "int" if isinstance(child.value.value, int) else "float"
                                elif isinstance(child.value.value, str):
                                    returns = "str"
                                elif isinstance(child.value.value, bool):
                                    returns = "bool"
                            break
                    functions[node.name] = FunctionInfo(
                        loc=self._count_lines(node),
                        docstring=ast.get_docstring(node),
                        params=params,
                        complexity=complexity,
                        returns=returns
                    )
                elif isinstance(node, ast.ClassDef):
                    methods = {}
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            methods[child.name] = MethodInfo(
                                loc=self._count_lines(child),
                                docstring=ast.get_docstring(child)
                            )
                    classes[node.name] = ClassInfo(
                        methods=methods,
                        docstring=ast.get_docstring(node)
                    )

            return FileInfo(
                file_path=self.file_path,
                type=self.get_file_type(),
                size=self.file_path.stat().st_size,
                lines=lines,
                functions=functions,
                classes=classes,
                dependencies=self.dependencies,
                unused_imports=unused_imports,
                skipped=False
            )
        except (SyntaxError, FileNotFoundError):
            return FileInfo(
                file_path=self.file_path,
                type=self.get_file_type(),
                size=0 if not self.file_path.exists() else self.file_path.stat().st_size,
                lines=0,
                functions={},
                classes={},
                dependencies=self.dependencies,
                skipped=True
            )

    def _read_file(self) -> Optional[str]:
        """Read the file content safely.

        Returns:
            Optional[str]: File content, or None if reading fails.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (IOError, UnicodeDecodeError):
            return None

    def _count_lines(self, node: ast.AST) -> int:
        """Count the number of lines in an AST node.

        Args:
            node: AST node to analyze.

        Returns:
            int: Number of lines in the node.
        """
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            return node.end_lineno - node.lineno + 1
        return 0