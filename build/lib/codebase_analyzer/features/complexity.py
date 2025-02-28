from pathlib import Path
from typing import Dict, Any, List, Optional
import ast
import radon.complexity as radon_cc
import radon.metrics as radon_metrics
from radon.visitors import ComplexityVisitor
import lizard

from .base import FeatureExtractor

class ComplexityFeatureExtractor(FeatureExtractor):
    """Extracts complexity-related features."""

    def extract(self, code: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        try:
            # Ensure code is properly formatted for radon
            code = code.strip() + '\n'
            tree = ast.parse(code)

            # Radon complexity
            radon_stats = ComplexityVisitor.from_code(code)
            # Lizard analysis
            lizard_stats = lizard.analyze_file.analyze_source_code(
                file_path.name if file_path else "temp.py", 
                code
            )

            return {
                'cyclomatic_complexity': {
                    'mean': self._calculate_mean_complexity(radon_stats.functions),
                    'max': self._calculate_max_complexity(radon_stats.functions),
                    'distribution': self._get_complexity_distribution(radon_stats.functions)
                },
                'cognitive_complexity': self._calculate_cognitive_complexity(tree),
                'halstead_metrics': self._calculate_halstead_metrics(code),
                'maintenance_index': radon_metrics.mi_visit(code, multi=True),
                'code_metrics': {
                    'loc': lizard_stats.nloc if lizard_stats.nloc else len(code.splitlines()),
                    'token_count': lizard_stats.token_count if lizard_stats.token_count else 0,
                    'function_count': len(lizard_stats.function_list),
                    'average_function_length': self._calculate_avg_function_length(lizard_stats)
                }
            }
        except Exception as e:
            print(f"Error in complexity extraction: {str(e)}")
            return self._get_default_metrics()

    def get_feature_names(self) -> List[str]:
        return [
            'cyclomatic_complexity.mean',
            'cyclomatic_complexity.max',
            'cyclomatic_complexity.distribution',
            'cognitive_complexity',
            'halstead_metrics.difficulty',
            'halstead_metrics.effort',
            'halstead_metrics.volume',
            'maintenance_index',
            'code_metrics.loc',
            'code_metrics.token_count',
            'code_metrics.function_count',
            'code_metrics.average_function_length'
        ]

    def _calculate_mean_complexity(self, functions: List[Any]) -> float:
        if not functions:
            return 1.0  # Default complexity for a function
        return sum(func.complexity for func in functions) / len(functions)

    def _calculate_max_complexity(self, functions: List[Any]) -> float:
        if not functions:
            return 1.0
        return max(func.complexity for func in functions)

    def _get_complexity_distribution(self, functions: List[Any]) -> Dict[str, int]:
        distribution = {'low': 0, 'medium': 0, 'high': 0, 'very_high': 0}
        for func in functions:
            if func.complexity <= 5:
                distribution['low'] += 1
            elif func.complexity <= 10:
                distribution['medium'] += 1
            elif func.complexity <= 20:
                distribution['high'] += 1
            else:
                distribution['very_high'] += 1
        if not functions:
            distribution['low'] = 1  # Assume simple function
        return distribution

    def _calculate_cognitive_complexity(self, tree: ast.AST) -> int:
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
        return max(visitor.complexity, 1)  # Ensure non-zero

    def _calculate_halstead_metrics(self, code: str) -> Dict[str, float]:
        try:
            h = radon_metrics.h_visit(code)
            return {
                'difficulty': h.difficulty,
                'effort': h.effort,
                'volume': h.volume,
                'vocabulary': h.vocabulary,
                'length': h.length
            }
        except Exception:
            return {'difficulty': 0.0, 'effort': 0.0, 'volume': 0.0, 'vocabulary': 0, 'length': 0}

    def _calculate_avg_function_length(self, stats: Any) -> float:
        if not stats.function_list:
            return 0.0
        return sum(func.nloc for func in stats.function_list) / len(stats.function_list)

    def _get_default_metrics(self) -> Dict[str, Any]:
        return {
            'cyclomatic_complexity': {
                'mean': 1.0,
                'max': 1.0,
                'distribution': {'low': 1, 'medium': 0, 'high': 0, 'very_high': 0}
            },
            'cognitive_complexity': 1,
            'halstead_metrics': {
                'difficulty': 0.0,
                'effort': 0.0,
                'volume': 0.0,
                'vocabulary': 0,
                'length': 0
            },
            'maintenance_index': 100.0,  # Default to max for empty/simple code
            'code_metrics': {
                'loc': 0,
                'token_count': 0,
                'function_count': 0,
                'average_function_length': 0.0
            }
        }