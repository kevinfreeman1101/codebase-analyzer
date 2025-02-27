from dataclasses import dataclass
from typing import Dict, List, Optional
import ast
from pathlib import Path
import radon.complexity as radon_cc
import radon.metrics as radon_metrics
from radon.visitors import ComplexityVisitor
import lizard

@dataclass
class ComplexityMetrics:
    cyclomatic_complexity: int
    cognitive_complexity: int
    maintainability_index: float
    halstead_metrics: Dict[str, float]
    lines_of_code: int
    nesting_depth: int

class ComplexityAnalyzer:
    """Analyzes code complexity metrics."""

    def analyze_project(self, project_path: Path) -> ComplexityMetrics:
        """Analyze complexity metrics for the entire project.

        Args:
            project_path: Path to the project root directory.

        Returns:
            ComplexityMetrics: Aggregated complexity metrics.
        """
        total_cc = 0
        total_cognitive = 0
        total_mi = 0.0
        total_loc = 0
        max_nesting = 0
        halstead = {'volume': 0.0, 'difficulty': 0.0, 'effort': 0.0, 'vocabulary': 0, 'length': 0}
        file_count = 0

        for file_path in project_path.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                radon_stats = ComplexityVisitor.from_code(code)
                lizard_stats = lizard.analyze_file.analyze_source_code(file_path.name, code)
                tree = ast.parse(code)

                # Include top-level control structures in cyclomatic complexity
                cc = sum(func.complexity for func in radon_stats.functions) + self._calculate_top_level_cc(tree)
                cognitive = self._calculate_cognitive_complexity(tree)
                mi = radon_metrics.mi_visit(code, multi=True)
                loc = lizard_stats.nloc
                nesting = self._calculate_nesting_depth(tree)

                total_cc += cc
                total_cognitive += cognitive
                total_mi += mi
                total_loc += loc
                max_nesting = max(max_nesting, nesting)

                h = radon_metrics.h_visit(code)
                for key in halstead:
                    halstead[key] += getattr(h, key, 0)

                file_count += 1
            except (SyntaxError, UnicodeDecodeError, FileNotFoundError):
                continue

        if file_count == 0:
            return ComplexityMetrics(
                cyclomatic_complexity=0,
                cognitive_complexity=0,
                maintainability_index=0.0,
                halstead_metrics={'volume': 0.0, 'difficulty': 0.0, 'effort': 0.0, 'vocabulary': 0, 'length': 0},
                lines_of_code=0,
                nesting_depth=0
            )

        return ComplexityMetrics(
            cyclomatic_complexity=total_cc,  # Total complexity, not averaged
            cognitive_complexity=total_cognitive,
            maintainability_index=total_mi / file_count if file_count > 0 else 0.0,
            halstead_metrics={k: v / file_count for k, v in halstead.items()},
            lines_of_code=total_loc,
            nesting_depth=max_nesting
        )

    def _calculate_top_level_cc(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for top-level control structures."""
        class TopLevelCCVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 0

            def visit_If(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_While(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_For(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_Try(self, node):
                self.complexity += 1
                self.generic_visit(node)

        visitor = TopLevelCCVisitor()
        visitor.visit(tree)
        return visitor.complexity

    def _calculate_cognitive_complexity(self, tree: ast.AST) -> int:
        """Calculate cognitive complexity of the AST."""
        class CognitiveComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 0
                self.nesting = 0

            def visit_If(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1

            def visit_While(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1

            def visit_For(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1

            def visit_Try(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1

        visitor = CognitiveComplexityVisitor()
        visitor.visit(tree)
        return visitor.complexity

    def _calculate_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate the maximum nesting depth of control structures."""
        class NestingVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_depth = 0
                self.max_depth = 0

            def _visit_control_structure(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_If(self, node):
                self._visit_control_structure(node)

            def visit_While(self, node):
                self._visit_control_structure(node)

            def visit_For(self, node):
                self._visit_control_structure(node)

            def visit_Try(self, node):
                self._visit_control_structure(node)

        visitor = NestingVisitor()
        visitor.visit(tree)
        return visitor.max_depth