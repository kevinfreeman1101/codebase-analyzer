import ast
from typing import Dict, Any, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class QualityMetrics:
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
        total_type_hints = 0.0
        total_doc_coverage = 0.0
        total_lint_score = 0.0
        total_lines = 0
        file_count = 0

        for file_path in project_path.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                tree = ast.parse(content)
                metrics = self.analyze_node(tree)
                
                total_type_hints += metrics.type_hint_coverage
                total_doc_coverage += metrics.documentation_coverage
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
            test_coverage=0.0,  # Still placeholder
            lint_score=total_lint_score / file_count,
            code_to_comment_ratio=total_lines / (file_count * 100)
        )

    def analyze_node(self, node: ast.AST) -> QualityMetrics:
        """Analyze quality metrics for an AST node."""
        type_coverage = self._calculate_type_hint_coverage(node)
        doc_coverage = self._calculate_documentation_coverage(node)
        test_cov = self._estimate_test_coverage(node)
        lint = self._calculate_lint_score(node)
        comment_ratio = self._calculate_code_comment_ratio(node)

        return QualityMetrics(
            type_hint_coverage=type_coverage,
            documentation_coverage=doc_coverage,
            test_coverage=test_cov,
            lint_score=lint,
            code_to_comment_ratio=comment_ratio
        )

    def _calculate_type_hint_coverage(self, node: ast.AST) -> float:
        """Calculate percentage of type-hinted functions and variables."""
        total_hints = 0
        total_possible = 0

        class TypeHintVisitor(ast.NodeVisitor):
            def __init__(self):
                self.hints = 0
                self.possible = 0

            def visit_FunctionDef(self, node):
                self.possible += 1  # Return type
                self.possible += len(node.args.args)  # Arguments

                if node.returns:
                    self.hints += 1

                for arg in node.args.args:
                    if arg.annotation:
                        self.hints += 1

                self.generic_visit(node)

            def visit_AnnAssign(self, node):
                self.possible += 1
                if node.annotation:
                    self.hints += 1

        visitor = TypeHintVisitor()
        visitor.visit(node)

        return (visitor.hints / visitor.possible * 100) if visitor.possible > 0 else 0

    def _calculate_documentation_coverage(self, node: ast.AST) -> float:
        """Calculate documentation coverage percentage."""
        total_docstrings = 0
        total_possible = 0

        class DocVisitor(ast.NodeVisitor):
            def __init__(self):
                self.docstrings = 0
                self.possible = 0

            def visit_FunctionDef(self, node):
                self.possible += 1
                if ast.get_docstring(node):
                    self.docstrings += 1
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                self.possible += 1
                if ast.get_docstring(node):
                    self.docstrings += 1
                self.generic_visit(node)

            def visit_Module(self, node):
                self.possible += 1
                if ast.get_docstring(node):
                    self.docstrings += 1
                self.generic_visit(node)

        visitor = DocVisitor()
        visitor.visit(node)

        return (visitor.docstrings / visitor.possible * 100) if visitor.possible > 0 else 0

    def _calculate_code_comment_ratio(self, node: ast.AST) -> float:
        """Calculate ratio of comments to code."""
        code_lines = 0
        comment_lines = 0

        class CommentVisitor(ast.NodeVisitor):
            def visit(self, node):
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
        issues = 0
        max_score = 100

        class LintVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                nonlocal issues
                # Check function length
                if len(node.body) > 50:  # Too long function
                    issues += 1
                # Check argument count
                if len(node.args.args) > 5:  # Too many arguments
                    issues += 1
                self.generic_visit(node)

            def visit_Try(self, node):
                nonlocal issues
                # Check for bare except
                for handler in node.handlers:
                    if handler.type is None:
                        issues += 1
                self.generic_visit(node)

        visitor = LintVisitor()
        visitor.visit(node)

        return max(0, max_score - (issues * 5))  # Deduct 5 points per issue

    def _estimate_test_coverage(self, node: ast.AST) -> float:
        """Estimate test coverage based on test file analysis."""
        # Placeholder - real implementation needs coverage tools
        return 0.0