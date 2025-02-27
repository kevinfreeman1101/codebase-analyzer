# codebase_analyzer/features/quality.py
from pathlib import Path
from typing import Dict, Any, List, Optional
import ast
import re

from .base import FeatureExtractor

class QualityFeatureExtractor(FeatureExtractor):
    """Extracts code quality features including documentation, naming conventions,
    code structure, type hints, and test coverage metrics."""

    def extract(self, code: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
            return {
                'documentation': self._analyze_documentation(tree, code),
                'naming': self._analyze_naming(tree),
                'structure': self._analyze_structure(tree),
                'type_hints': self._analyze_type_hints(tree),
                'test_coverage': self._analyze_test_coverage(code) if file_path else None,
                'code_smells': self._analyze_code_smells(tree, code)
            }
        except Exception as e:
            return self._get_default_metrics()

    def get_feature_names(self) -> List[str]:
        return [
            'documentation.docstring_coverage',
            'documentation.comment_ratio',
            'documentation.quality_score',
            'naming.convention_adherence',
            'naming.consistency_score',
            'structure.function_length',
            'structure.class_length',
            'structure.nesting_depth',
            'type_hints.coverage',
            'type_hints.consistency',
            'test_coverage.percentage',
            'test_coverage.quality',
            'code_smells.count',
            'code_smells.severity'
        ]

    def _analyze_documentation(self, tree: ast.AST, code: str) -> Dict[str, Any]:
        class DocVisitor(ast.NodeVisitor):
            def __init__(self):
                self.total_functions = 0
                self.documented_functions = 0
                self.total_classes = 0
                self.documented_classes = 0
                self.docstring_quality_scores = []

            def visit_FunctionDef(self, node):
                self.total_functions += 1
                if docstring := ast.get_docstring(node):
                    self.documented_functions += 1
                    self.docstring_quality_scores.append(
                        self._assess_docstring_quality(docstring)
                    )
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                self.total_classes += 1
                if docstring := ast.get_docstring(node):
                    self.documented_classes += 1
                    self.docstring_quality_scores.append(
                        self._assess_docstring_quality(docstring)
                    )
                self.generic_visit(node)

            def _assess_docstring_quality(self, docstring: str) -> float:
                score = 0.0
                # Check for common docstring sections
                if re.search(r'Args:|Parameters:', docstring): score += 0.2
                if re.search(r'Returns:|Yields:', docstring): score += 0.2
                if re.search(r'Raises:|Exceptions:', docstring): score += 0.2
                if re.search(r'Examples?:', docstring): score += 0.2
                # Check for descriptive content
                if len(docstring.split()) >= 10: score += 0.2
                return score

        visitor = DocVisitor()
        visitor.visit(tree)

        # Calculate comment ratio
        lines = code.split('\n')
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))

        return {
            'docstring_coverage': self._calculate_coverage(
                visitor.documented_functions + visitor.documented_classes,
                visitor.total_functions + visitor.total_classes
            ),
            'comment_ratio': comment_lines / len(lines) if lines else 0.0,
            'quality_score': sum(visitor.docstring_quality_scores) / len(visitor.docstring_quality_scores)
            if visitor.docstring_quality_scores else 0.0
        }

    def _analyze_naming(self, tree: ast.AST) -> Dict[str, Any]:
        class NamingVisitor(ast.NodeVisitor):
            def __init__(self):
                self.names = {'function': [], 'class': [], 'variable': []}
                self.convention_scores = []

            def visit_FunctionDef(self, node):
                self.names['function'].append(node.name)
                self.convention_scores.append(
                    self._check_naming_convention(node.name, 'function')
                )
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                self.names['class'].append(node.name)
                self.convention_scores.append(
                    self._check_naming_convention(node.name, 'class')
                )
                self.generic_visit(node)

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    self.names['variable'].append(node.id)
                    self.convention_scores.append(
                        self._check_naming_convention(node.id, 'variable')
                    )
                self.generic_visit(node)

            def _check_naming_convention(self, name: str, type_: str) -> float:
                if not name:
                    return 0.0

                score = 0.0
                
                if type_ == 'function':
                    # Snake case for functions
                    if re.match(r'^[a-z][a-z0-9_]*$', name):
                        score = 1.0
                elif type_ == 'class':
                    # PascalCase for classes
                    if re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                        score = 1.0
                elif type_ == 'variable':
                    # Snake case for variables
                    if re.match(r'^[a-z][a-z0-9_]*$', name):
                        score = 1.0
                    # UPPER_CASE for constants
                    elif re.match(r'^[A-Z][A-Z0-9_]*$', name):
                        score = 1.0

                return score

            def get_consistency_score(self) -> float:
                scores = []
                for names in self.names.values():
                    if names:
                        # Check if all names in the category follow the same pattern
                        patterns = {self._get_name_pattern(name) for name in names}
                        scores.append(1.0 if len(patterns) == 1 else 0.0)
                return sum(scores) / len(scores) if scores else 1.0

            def _get_name_pattern(self, name: str) -> str:
                if re.match(r'^[a-z][a-z0-9_]*$', name):
                    return 'snake_case'
                if re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                    return 'PascalCase'
                if re.match(r'^[A-Z][A-Z0-9_]*$', name):
                    return 'UPPER_CASE'
                return 'other'

        visitor = NamingVisitor()
        visitor.visit(tree)

        return {
            'convention_adherence': sum(visitor.convention_scores) / len(visitor.convention_scores)
            if visitor.convention_scores else 1.0,
            'consistency_score': visitor.get_consistency_score()
        }

    def _analyze_structure(self, tree: ast.AST) -> Dict[str, Any]:
        class StructureVisitor(ast.NodeVisitor):
            def __init__(self):
                self.function_lengths = []
                self.class_lengths = []
                self.nesting_depths = []
                self.current_nesting = 0

            def visit_FunctionDef(self, node):
                self.function_lengths.append(len(node.body))
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                self.class_lengths.append(len(node.body))
                self.generic_visit(node)

            def visit_If(self, node):
                self._handle_nesting(node)

            def visit_For(self, node):
                self._handle_nesting(node)

            def visit_While(self, node):
                self._handle_nesting(node)

            def _handle_nesting(self, node):
                self.current_nesting += 1
                self.nesting_depths.append(self.current_nesting)
                self.generic_visit(node)
                self.current_nesting -= 1

        visitor = StructureVisitor()
        visitor.visit(tree)

        return {
            'function_length': {
                'mean': self._safe_mean(visitor.function_lengths),
                'max': max(visitor.function_lengths) if visitor.function_lengths else 0
            },
            'class_length': {
                'mean': self._safe_mean(visitor.class_lengths),
                'max': max(visitor.class_lengths) if visitor.class_lengths else 0
            },
            'nesting_depth': {
                'mean': self._safe_mean(visitor.nesting_depths),
                'max': max(visitor.nesting_depths) if visitor.nesting_depths else 0
            }
        }

    def _analyze_type_hints(self, tree: ast.AST) -> Dict[str, Any]:
        class TypeHintVisitor(ast.NodeVisitor):
            def __init__(self):
                self.total_annotations = 0
                self.total_annotatable = 0
                self.consistent_annotations = 0
                self.function_annotations = {}

            def visit_FunctionDef(self, node):
                # Check return annotation
                self.total_annotatable += 1
                if node.returns:
                    self.total_annotations += 1

                # Check argument annotations
                arg_annotations = []
                for arg in node.args.args:
                    self.total_annotatable += 1
                    if arg.annotation:
                        self.total_annotations += 1
                        arg_annotations.append(True)
                    else:
                        arg_annotations.append(False)

                # Check annotation consistency within function
                if arg_annotations:
                    if all(arg_annotations) or not any(arg_annotations):
                        self.consistent_annotations += 1
                    self.function_annotations[node.name] = arg_annotations

                self.generic_visit(node)

        visitor = TypeHintVisitor()
        visitor.visit(tree)

        return {
            'coverage': self._calculate_coverage(
                visitor.total_annotations,
                visitor.total_annotatable
            ),
            'consistency': self._calculate_coverage(
                visitor.consistent_annotations,
                len(visitor.function_annotations)
            ) if visitor.function_annotations else 1.0
        }

    def _analyze_test_coverage(self, code: str) -> Dict[str, Any]:
        test_patterns = {
            'assertions': r'assert\s+|self\.assert\w+',
            'test_functions': r'def test_\w+',
            'test_classes': r'class Test\w+',
            'mocks': r'mock\.|patch\.|MagicMock|Mock\(',
            'fixtures': r'@pytest\.fixture|@fixture'
        }

        scores = {}
        lines = code.split('\n')
        
        for pattern_name, pattern in test_patterns.items():
            matches = sum(1 for line in lines if re.search(pattern, line))
            scores[pattern_name] = min(matches / 5.0, 1.0)  # Normalize to 0-1

        return {
            'percentage': sum(scores.values()) / len(scores),
            'quality': self._calculate_test_quality(scores),
            'patterns': scores
        }

    def _analyze_code_smells(self, tree: ast.AST, code: str) -> Dict[str, Any]:
        class SmellVisitor(ast.NodeVisitor):
            def __init__(self):
                self.smells = []
                self.current_function = None

            def visit_FunctionDef(self, node):
                self.current_function = node.name
                # Check function length
                if len(node.body) > 20:
                    self.smells.append({
                        'type': 'long_function',
                        'severity': 'medium',
                        'location': f'function {node.name}'
                    })
                
                # Check number of arguments
                if len(node.args.args) > 5:
                    self.smells.append({
                        'type': 'too_many_arguments',
                        'severity': 'medium',
                        'location': f'function {node.name}'
                    })
                
                self.generic_visit(node)
                self.current_function = None

            def visit_ClassDef(self, node):
                # Check class length
                if len(node.body) > 30:
                    self.smells.append({
                        'type': 'large_class',
                        'severity': 'high',
                        'location': f'class {node.name}'
                    })
                self.generic_visit(node)

        visitor = SmellVisitor()
        visitor.visit(tree)

        # Additional code smell checks
        lines = code.split('\n')
        
        # Check for duplicate code (simple check)
        seen_lines = set()
        for line in lines:
            stripped = line.strip()
            if len(stripped) > 20:  # Only check substantial lines
                if stripped in seen_lines:
                    visitor.smells.append({
                        'type': 'duplicate_code',
                        'severity': 'high',
                        'location': 'multiple locations'
                    })
                seen_lines.add(stripped)

        return {
            'count': len(visitor.smells),
            'severity': self._calculate_smell_severity(visitor.smells),
            'details': visitor.smells
        }

    def _calculate_coverage(self, covered: int, total: int) -> float:
        return covered / total if total > 0 else 1.0

    def _safe_mean(self, values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    def _calculate_test_quality(self, scores: Dict[str, float]) -> float:
        weights = {
            'assertions': 0.3,
            'test_functions': 0.2,
            'test_classes': 0.2,
            'mocks': 0.15,
            'fixtures': 0.15
        }
        return sum(scores[k] * weights.get(k, 0) for k in scores)

    def _calculate_smell_severity(self, smells: List[Dict[str, str]]) -> float:
        if not smells:
            return 0.0
            
        severity_scores = {
            'low': 0.3,
            'medium': 0.6,
            'high': 1.0
        }
        
        total_score = sum(severity_scores[smell['severity']] for smell in smells)
        return total_score / len(smells)

    def _get_default_metrics(self) -> Dict[str, Any]:
        return {
            'documentation': {
                'docstring_coverage': 0.0,
                'comment_ratio': 0.0,
                'quality_score': 0.0
            },
            'naming': {
                'convention_adherence': 0.0,
                'consistency_score': 0.0
            },
            'structure': {
                'function_length': {
                    'mean': 0.0,
                    'max': 0
                },
                'class_length': {
                    'mean': 0.0,
                    'max': 0
                },
                'nesting_depth': {
                    'mean': 0.0,
                    'max': 0
                }
            },
            'type_hints': {
                'coverage': 0.0,
                'consistency': 0.0
            },
            'test_coverage': {
                'percentage': 0.0,
                'quality': 0.0,
                'patterns': {
                    'assertions': 0.0,
                    'test_functions': 0.0,
                    'test_classes': 0.0,
                    'mocks': 0.0,
                    'fixtures': 0.0
                }
            },
            'code_smells': {
                'count': 0,
                'severity': 0.0,
                'details': []
            }
        }