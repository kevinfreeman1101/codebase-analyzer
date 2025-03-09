"""Module for analyzing code complexity metrics in Python projects."""

import ast
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ComplexityMetrics:
    """Represents complexity metrics for a Python project."""
    cyclomatic_complexity: float
    maintainability_index: float
    complex_functions: List[Dict[str, Any]]  # Added for detailed function stats

class ComplexityAnalyzer:
    """Analyzes code complexity metrics."""

    def analyze_project(self, project_path: Path) -> ComplexityMetrics:
        """Analyze complexity metrics for Python files in a project directory.

        Args:
            project_path: Path to the project root directory.

        Returns:
            ComplexityMetrics: Aggregated complexity metrics including function-level details.
        """
        total_complexity = 0.0
        total_lines = 0
        file_count = 0
        complex_functions = []

        for file_path in project_path.rglob("*.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                tree = ast.parse(content)
                complexity, funcs = self._analyze_complexity(tree, file_path)
                total_complexity += complexity
                total_lines += len(content.splitlines())
                file_count += 1
                complex_functions.extend(funcs)
            except (SyntaxError, UnicodeDecodeError, FileNotFoundError):
                continue

        if file_count == 0:
            return ComplexityMetrics(cyclomatic_complexity=0.0, maintainability_index=0.0, complex_functions=[])

        avg_complexity = total_complexity / file_count
        # Simplified maintainability index (100 - complexity penalty)
        maintainability = max(0.0, 100.0 - (avg_complexity * 5))  # Arbitrary scaling
        return ComplexityMetrics(
            cyclomatic_complexity=avg_complexity,
            maintainability_index=maintainability,
            complex_functions=complex_functions
        )

    def _analyze_complexity(self, tree: ast.AST, file_path: Path) -> tuple[float, List[Dict[str, Any]]]:
        """Analyze complexity of an AST and extract function-level details.

        Args:
            tree: The AST of the Python file.
            file_path: Path to the file being analyzed.

        Returns:
            tuple[float, List[Dict[str, Any]]]: Total complexity and list of complex functions.
        """
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self, file_path: Path):
                self.complexity = 1  # Base complexity
                self.functions = []
                self.file_path = file_path

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                func_complexity = 1  # Base for function
                lines = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                        func_complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        func_complexity += len(child.values) - 1
                self.complexity += func_complexity - 1  # Add to total, subtract base

                # Track functions with complexity > 5 or lines > 20
                if func_complexity > 5 or lines > 20:
                    self.functions.append({
                        "name": node.name,
                        "file_path": str(self.file_path),
                        "line_number": node.lineno,
                        "complexity": func_complexity,
                        "lines": lines,
                        "code": ast.unparse(node).splitlines()[0]  # First line as snippet
                    })
                self.generic_visit(node)

            def visit_If(self, node: ast.If) -> None:
                self.complexity += 1
                self.generic_visit(node)

            def visit_For(self, node: ast.For) -> None:
                self.complexity += 1
                self.generic_visit(node)

            def visit_While(self, node: ast.While) -> None:
                self.complexity += 1
                self.generic_visit(node)

            def visit_Try(self, node: ast.Try) -> None:
                self.complexity += 1
                self.generic_visit(node)

            def visit_With(self, node: ast.With) -> None:
                self.complexity += 1
                self.generic_visit(node)

            def visit_BoolOp(self, node: ast.BoolOp) -> None:
                self.complexity += len(node.values) - 1
                self.generic_visit(node)

        visitor = ComplexityVisitor(file_path)
        visitor.visit(tree)
        return visitor.complexity, visitor.functions