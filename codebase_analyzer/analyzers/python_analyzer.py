"""Analyzer for Python files to extract detailed metrics."""

import ast
import logging
from typing import Optional, Set, Dict, List
from pathlib import Path
from .base_analyzer import BaseAnalyzer
from ..models.data_classes import FileInfo, FunctionInfo, ClassInfo, CodeSnippet
from ..utils.file_utils import safe_read_file

logger = logging.getLogger(__name__)

class PythonAnalyzer(BaseAnalyzer):
    """Analyzes Python source files."""

    def get_file_type(self) -> str:
        return "python"

    def analyze(self) -> Optional[FileInfo]:
        """Analyze a Python file and return its metadata.

        Returns:
            Optional[FileInfo]: File information if successful, None if critical errors occur.
        """
        content = safe_read_file(self.file_path)
        if content is None:
            logger.error(f"Failed to read file: {self.file_path}")
            return None

        try:
            tree = ast.parse(content)
        except (SyntaxError, ValueError) as e:
            logger.warning(f"Syntax error in {self.file_path}: {str(e)}")
            return FileInfo(
                path=Path(self.file_path),
                type=self.get_file_type(),
                content=content,
                size=len(content.encode('utf-8')),
                dependencies=set(),
                functions={},
                classes={},
                unused_imports=set()
            )

        functions: Dict[str, FunctionInfo] = {}
        classes: Dict[str, ClassInfo] = {}
        imports: Set[str] = set()
        used_names: Set[str] = set()

        class Visitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.functions = functions
                self.classes = classes
                self.imports = imports
                self.used_names = used_names

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                code = CodeSnippet(ast.unparse(node), node.lineno, node.end_lineno or node.lineno)
                params = [arg.arg for arg in node.args.args]
                returns = ast.unparse(node.returns) if node.returns else "None"
                docstring = ast.get_docstring(node) or ""
                complexity = self.analyzer._calculate_complexity(node)
                self.functions[node.name] = FunctionInfo(
                    name=node.name,
                    params=params,
                    returns=returns,
                    docstring=docstring,
                    dependencies=self.analyzer._extract_dependencies(node),
                    loc=node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 1,
                    code=code,
                    file_path=str(self.analyzer.file_path),
                    complexity=complexity
                )
                for child in ast.walk(node):
                    if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                        self.used_names.add(child.id)
                self.generic_visit(node)

            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                class_methods = {}
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        code = CodeSnippet(ast.unparse(item), item.lineno, item.end_lineno or item.lineno)
                        params = [arg.arg for arg in item.args.args]
                        returns = ast.unparse(item.returns) if item.returns else "None"
                        docstring = ast.get_docstring(item) or ""
                        complexity = self.analyzer._calculate_complexity(item)
                        class_methods[item.name] = FunctionInfo(
                            name=item.name,
                            params=params,
                            returns=returns,
                            docstring=docstring,
                            dependencies=self.analyzer._extract_dependencies(item),
                            loc=item.end_lineno - item.lineno + 1 if hasattr(item, 'end_lineno') else 1,
                            code=code,
                            file_path=str(self.analyzer.file_path),
                            complexity=complexity
                        )
                        for child in ast.walk(item):
                            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                                self.used_names.add(child.id)
                code = CodeSnippet(ast.unparse(node), node.lineno, node.end_lineno or node.lineno)
                bases = [ast.unparse(base) for base in node.bases]
                docstring = ast.get_docstring(node) or ""
                complexity = self.analyzer._calculate_complexity(node)
                self.classes[node.name] = ClassInfo(
                    name=node.name,
                    methods=class_methods,
                    base_classes=bases,
                    docstring=docstring,
                    code=code,
                    file_path=str(self.analyzer.file_path),
                    attributes=self.analyzer._extract_attributes(node),
                    complexity=complexity
                )
                self.generic_visit(node)

            def visit_Import(self, node: ast.Import) -> None:
                for name in node.names:
                    self.imports.add(name.name.split('.')[0])
                self.generic_visit(node)

            def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
                if node.module:
                    self.imports.add(node.module.split('.')[0])
                self.generic_visit(node)

            def visit_Name(self, node: ast.Name) -> None:
                if isinstance(node.ctx, ast.Load):
                    self.used_names.add(node.id)
                self.generic_visit(node)

        visitor = Visitor(self)
        visitor.visit(tree)

        unused_imports = imports - used_names

        return FileInfo(
            path=Path(self.file_path),
            type=self.get_file_type(),
            content=content,
            size=len(content.encode('utf-8')),
            dependencies=imports,
            functions=functions,
            classes=classes,
            unused_imports=unused_imports
        )

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity for a node."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _extract_dependencies(self, node: ast.AST) -> Set[str]:
        """Extract dependencies used within a node."""
        deps = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                deps.add(child.id)
        return deps

    def _extract_attributes(self, node: ast.ClassDef) -> List[Dict[str, Optional[str]]]:
        """Extract attributes from a class definition."""
        attrs = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                attrs.append({
                    "name": item.target.id if isinstance(item.target, ast.Name) else "unknown",
                    "type": ast.unparse(item.annotation) if item.annotation else None
                })
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attrs.append({"name": target.id, "type": None})
        return attrs