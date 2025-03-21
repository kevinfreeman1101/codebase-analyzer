"""Module for analyzing code quality metrics in Python projects."""

import ast
import subprocess
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class QualityMetrics:
    """Represents quality metrics for a Python project or file.

    Attributes:
        type_hint_coverage: Percentage of type-hinted elements.
        documentation_coverage: Percentage of documented elements.
        test_coverage: Percentage of code covered by tests.
        lint_score: Score based on code style issues (0-100).
        code_to_comment_ratio: Ratio of comment lines to code lines.
    """

    type_hint_coverage: float
    documentation_coverage: float
    test_coverage: float
    lint_score: float
    code_to_comment_ratio: float

    def quality_score(self) -> float:
        """Calculate an overall quality score from individual metrics.

        Returns:
            float: A score from 0 to 100.
        """
        weights = {
            'type_hint': 0.3,
            'doc': 0.3,
            'test': 0.2,
            'lint': 0.15,
            'comment': 0.05
        }
        score = (
            self.type_hint_coverage * weights['type_hint'] +
            self.documentation_coverage * weights['doc'] +
            self.test_coverage * weights['test'] +
            self.lint_score * weights['lint'] +
            (self.code_to_comment_ratio * 100 if self.code_to_comment_ratio <= 1 else 100) * weights['comment']
        )
        return min(100.0, max(0.0, score))

class QualityAnalyzer:
    """Analyzes code quality metrics."""

    def analyze_project(self, project_path: Path) -> QualityMetrics:
        """Analyze quality metrics for an entire project directory.

        Args:
            project_path: Path to the project root directory.

        Returns:
            QualityMetrics: Aggregated quality metrics for all Python files.
        """
        total_type_hints: float = 0.0
        total_doc_coverage: float = 0.0
        total_test_coverage: float = 0.0
        total_lint_score: float = 0.0
        total_lines: float = 0.0
        file_count: int = 0

        # Run coverage for the project if tests exist
        test_coverage = self._run_coverage(project_path)

        for file_path in project_path.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content: str = f.read()
                tree: ast.AST = ast.parse(content)
                metrics: QualityMetrics = self.analyze_node(tree)
                
                total_type_hints += metrics.type_hint_coverage
                total_doc_coverage += metrics.documentation_coverage
                # Use project-wide coverage instead of per-file heuristic
                total_lint_score += metrics.lint_score
                total_lines += metrics.code_to_comment_ratio * 100  # Rough estimate
                file_count += 1
            except (SyntaxError, UnicodeDecodeError, FileNotFoundError):
                continue

        if file_count == 0:
            return QualityMetrics(0.0, 0.0, 0.0, 0.0, 0.0)

        return QualityMetrics(
            type_hint_coverage=total_type_hints / file_count,
            documentation_coverage=total_doc_coverage / file_count,
            test_coverage=test_coverage,
            lint_score=total_lint_score / file_count,
            code_to_comment_ratio=total_lines / (file_count * 100)
        )

    def analyze_node(self, node: ast.AST) -> QualityMetrics:
        """Analyze quality metrics for an AST node excluding test coverage."""
        type_coverage: float = self._calculate_type_hint_coverage(node)
        doc_coverage: float = self._calculate_documentation_coverage(node)
        lint: float = self._calculate_lint_score(node)
        comment_ratio: float = self._calculate_code_comment_ratio(node)

        return QualityMetrics(
            type_hint_coverage=type_coverage,
            documentation_coverage=doc_coverage,
            test_coverage=0.0,  # Set at project level
            lint_score=lint,
            code_to_comment_ratio=comment_ratio
        )

    def _calculate_type_hint_coverage(self, node: ast.AST) -> float:
        """Calculate percentage of type-hinted functions and variables."""
        total_hints: int = 0
        total_possible: int = 0

        class TypeHintVisitor(ast.NodeVisitor):
            def __init__(self):
                self.hints: int = 0
                self.possible: int = 0

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                self.possible += 1  # Return type
                self.possible += len(node.args.args)  # Arguments

                if node.returns:
                    self.hints += 1

                for arg in node.args.args:
                    if arg.annotation:
                        self.hints += 1

                self.generic_visit(node)

            def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
                self.possible += 1
                if node.annotation:
                    self.hints += 1

        visitor = TypeHintVisitor()
        visitor.visit(node)

        return (visitor.hints / visitor.possible * 100) if visitor.possible > 0 else 0

    def _calculate_documentation_coverage(self, node: ast.AST) -> float:
        """Calculate documentation coverage percentage."""
        total_docstrings: int = 0
        total_possible: int = 0

        class DocVisitor(ast.NodeVisitor):
            def __init__(self):
                self.docstrings: int = 0
                self.possible: int = 0

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                self.possible += 1
                if ast.get_docstring(node):
                    self.docstrings += 1
                self.generic_visit(node)

            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                self.possible += 1
                if ast.get_docstring(node):
                    self.docstrings += 1
                self.generic_visit(node)

            def visit_Module(self, node: ast.Module) -> None:
                self.possible += 1
                if ast.get_docstring(node):
                    self.docstrings += 1
                self.generic_visit(node)

        visitor = DocVisitor()
        visitor.visit(node)

        return (visitor.docstrings / visitor.possible * 100) if visitor.possible > 0 else 0

    def _calculate_code_comment_ratio(self, node: ast.AST) -> float:
        """Calculate ratio of comments to code."""
        code_lines: int = 0
        comment_lines: int = 0

        class CommentVisitor(ast.NodeVisitor):
            def visit(self, node: ast.AST) -> None:
                if hasattr(node, 'lineno'):
                    nonlocal code_lines
                    code_lines += 1
                super().visit(node)

        visitor = CommentVisitor()
        visitor.visit(node)

        # Rough estimate since AST doesn't preserve comments
        return comment_lines / code_lines if code_lines > 0 else 0

    def _calculate_lint_score(self, node: ast.AST) -> float:
        """Calculate a lint score based on common code style issues."""
        issues: int = 0
        max_score: float = 100.0

        class LintVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                nonlocal issues
                # Check function length
                if len(node.body) > 50:  # Too long function
                    issues += 1
                # Check argument count
                if len(node.args.args) > 5:  # Too many arguments
                    issues += 1
                self.generic_visit(node)

            def visit_Try(self, node: ast.Try) -> None:
                nonlocal issues
                # Check for bare except
                for handler in node.handlers:
                    if handler.type is None:
                        issues += 1
                self.generic_visit(node)

        visitor = LintVisitor()
        visitor.visit(node)

        return max(0.0, max_score - (issues * 5))  # Deduct 5 points per issue

    def _estimate_test_coverage(self, node: ast.AST) -> float:
        """Deprecated: Use _run_coverage for project-level coverage instead."""
        return 0.0

    def _run_coverage(self, project_path: Path) -> float:
        """Run coverage.py on the project to get accurate test coverage.

        Args:
            project_path: Path to the project root directory.

        Returns:
            float: Test coverage percentage (0-100), or 0.0 if no tests or errors occur.
        """
        test_dir = project_path / "tests"
        if not test_dir.exists() or not any(test_dir.rglob("test_*.py")):
            return 0.0  # No tests found

        try:
            # Run pytest with coverage
            result = subprocess.run(
                ["coverage", "run", "-m", "pytest", str(test_dir)],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                return 0.0  # Test run failed

            # Generate coverage report
            report = subprocess.run(
                ["coverage", "report"],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                check=False
            )
            if report.returncode != 0:
                return 0.0  # Report generation failed

            # Parse the last line of the report for total coverage
            lines = report.stdout.strip().splitlines()
            if not lines or "TOTAL" not in lines[-1]:
                return 0.0

            total_line = lines[-1]
            coverage_percent = float(total_line.split()[-1].rstrip('%'))
            return coverage_percent
        except (subprocess.SubprocessError, ValueError, FileNotFoundError):
            return 0.0  # Handle missing coverage tool or parsing errors gracefully