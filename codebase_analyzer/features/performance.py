# codebase_analyzer/features/performance.py
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import ast
import re
from dataclasses import dataclass
from collections import defaultdict

from .base import FeatureExtractor

@dataclass
class PerformanceIssue:
    """Container for performance issues found in code."""
    type: str
    severity: str  # 'low', 'medium', 'high'
    description: str
    line_number: int
    snippet: str
    recommendation: Optional[str] = None
    estimated_impact: Optional[str] = None

class PerformanceFeatureExtractor(FeatureExtractor):
    """Extracts performance-related features and identifies potential bottlenecks."""

    def __init__(self):
        self.performance_patterns = {
            'nested_loops': (
                r'for.*\s+for',
                'high',
                'Nested loops detected - potential O(n²) or worse complexity'
            ),
            'large_memory': (
                r'\.read$\)|load\(.*$|\.readlines\(\)',
                'medium',
                'Loading large data into memory'
            ),
            'inefficient_concat': (
                r'\s*\+\s*'.join(['\w+' for _ in range(3)]),
                'low',
                'Inefficient string concatenation'
            ),
            'global_state': (
                r'global\s+\w+',
                'medium',
                'Global state usage may impact performance'
            )
        }

    def extract(self, code: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
            lines = code.split('\n')

            performance_analysis = {
                'complexity_metrics': self._analyze_complexity(tree),
                'memory_patterns': self._analyze_memory_usage(tree, lines),
                'io_operations': self._analyze_io_operations(tree),
                'caching_opportunities': self._analyze_caching(tree),
                'bottlenecks': self._analyze_bottlenecks(tree, lines),
                'async_patterns': self._analyze_async_patterns(tree),
                'performance_score': 0.0  # Will be calculated at the end
            }

            performance_analysis['performance_score'] = self._calculate_performance_score(
                performance_analysis
            )

            return performance_analysis
        except Exception as e:
            return self._get_default_metrics()

    def get_feature_names(self) -> List[str]:
        return [
            'complexity_metrics.time_complexity',
            'complexity_metrics.space_complexity',
            'memory_patterns.allocation_count',
            'memory_patterns.large_objects',
            'io_operations.sync_ops',
            'io_operations.async_ops',
            'caching_opportunities.count',
            'caching_opportunities.impact',
            'bottlenecks.count',
            'bottlenecks.severity',
            'async_patterns.usage',
            'performance_score'
        ]

    def _analyze_complexity(self, tree: ast.AST) -> Dict[str, Any]:
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.loop_depths = []
                self.current_depth = 0
                self.recursive_functions = set()
                self.comprehensions = 0
                self.generators = 0

            def visit_For(self, node):
                self._handle_loop(node)

            def visit_While(self, node):
                self._handle_loop(node)

            def _handle_loop(self, node):
                self.current_depth += 1
                self.loop_depths.append(self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_ListComp(self, node):
                self.comprehensions += 1
                self.generic_visit(node)

            def visit_GeneratorExp(self, node):
                self.generators += 1
                self.generic_visit(node)

            def visit_FunctionDef(self, node):
                # Check for recursion
                class RecursionDetector(ast.NodeVisitor):
                    def __init__(self, func_name):
                        self.func_name = func_name
                        self.is_recursive = False

                    def visit_Call(self, node):
                        if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
                            self.is_recursive = True
                        self.generic_visit(node)

                detector = RecursionDetector(node.name)
                detector.visit(node)
                if detector.is_recursive:
                    self.recursive_functions.add(node.name)
                
                self.generic_visit(node)

        visitor = ComplexityVisitor()
        visitor.visit(tree)

        max_depth = max(visitor.loop_depths) if visitor.loop_depths else 0
        time_complexity = self._estimate_time_complexity(max_depth, bool(visitor.recursive_functions))

        return {
            'time_complexity': time_complexity,
            'space_complexity': self._estimate_space_complexity(visitor),
            'loop_depths': visitor.loop_depths,
            'recursive_functions': list(visitor.recursive_functions),
            'comprehensions': visitor.comprehensions,
            'generators': visitor.generators
        }

    def _analyze_memory_usage(self, tree: ast.AST, lines: List[str]) -> Dict[str, Any]:
        class MemoryVisitor(ast.NodeVisitor):
            def __init__(self):
                self.allocations = []
                self.large_objects = []
                self.current_function = None

            def visit_FunctionDef(self, node):
                self.current_function = node.name
                self.generic_visit(node)
                self.current_function = None

            def visit_List(self, node):
                self.allocations.append({
                    'type': 'list',
                    'function': self.current_function,
                    'line': node.lineno
                })
                self.generic_visit(node)

            def visit_Dict(self, node):
                self.allocations.append({
                    'type': 'dict',
                    'function': self.current_function,
                    'line': node.lineno
                })
                self.generic_visit(node)

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    # Check for large data structure creation
                    if node.func.id in {'list', 'dict', 'set'}:
                        self.large_objects.append({
                            'type': node.func.id,
                            'function': self.current_function,
                            'line': node.lineno
                        })
                self.generic_visit(node)

        visitor = MemoryVisitor()
        visitor.visit(tree)

        return {
            'allocation_count': len(visitor.allocations),
            'large_objects': len(visitor.large_objects),
            'allocation_details': visitor.allocations,
            'large_object_details': visitor.large_objects
        }

    def _analyze_io_operations(self, tree: ast.AST) -> Dict[str, Any]:
        class IOVisitor(ast.NodeVisitor):
            def __init__(self):
                self.sync_ops = []
                self.async_ops = []
                self.file_operations = []
                self.network_operations = []

            def visit_Call(self, node):
                if isinstance(node.func, ast.Attribute):
                    # File operations
                    if node.func.attr in {'open', 'read', 'write', 'close'}:
                        self.file_operations.append({
                            'operation': node.func.attr,
                            'line': node.lineno
                        })
                    # Network operations
                    elif node.func.attr in {'get', 'post', 'request', 'connect'}:
                        self.network_operations.append({
                            'operation': node.func.attr,
                            'line': node.lineno
                        })

                    # Async operations
                    if node.func.attr.startswith('async_'):
                        self.async_ops.append({
                            'operation': node.func.attr,
                            'line': node.lineno
                        })
                    else:
                        self.sync_ops.append({
                            'operation': node.func.attr,
                            'line': node.lineno
                        })

                self.generic_visit(node)

        visitor = IOVisitor()
        visitor.visit(tree)

        return {
            'sync_ops': len(visitor.sync_ops),
            'async_ops': len(visitor.async_ops),
            'file_operations': visitor.file_operations,
            'network_operations': visitor.network_operations,
            'io_ratio': len(visitor.async_ops) / (len(visitor.sync_ops) + len(visitor.async_ops))
            if visitor.sync_ops or visitor.async_ops else 0.0
        }

    def _analyze_caching(self, tree: ast.AST) -> Dict[str, Any]:
        class CachingVisitor(ast.NodeVisitor):
            def __init__(self):
                self.cache_opportunities = []
                self.existing_caches = []
                self.repeated_calls = defaultdict(int)

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    self.repeated_calls[node.func.id] += 1
                    
                    # Check for existing caching decorators
                    if hasattr(node, 'decorator_list'):
                        for decorator in node.decorator_list:
                            if isinstance(decorator, ast.Name) and decorator.id in {'lru_cache', 'cache'}:
                                self.existing_caches.append({
                                    'function': node.func.id,
                                    'line': node.lineno
                                })

                self.generic_visit(node)

            def get_opportunities(self):
                return [
                    {'function': func, 'calls': count}
                    for func, count in self.repeated_calls.items()
                    if count > 2  # Threshold for suggesting caching
                ]

        visitor = CachingVisitor()
        visitor.visit(tree)

        opportunities = visitor.get_opportunities()
        return {
            'opportunities_count': len(opportunities),
            'existing_caches': len(visitor.existing_caches),
            'cache_opportunities': opportunities,
            'existing_cache_details': visitor.existing_caches,
            'impact_score': min(len(opportunities) / 5.0, 1.0)
        }

    def _analyze_bottlenecks(self, tree: ast.AST, lines: List[str]) -> Dict[str, Any]:
        issues: List[PerformanceIssue] = []
        
        class BottleneckVisitor(ast.NodeVisitor):
            def __init__(self, lines, patterns, issues):
                self.lines = lines
                self.patterns = patterns
                self.issues = issues

            def visit(self, node):
                if hasattr(node, 'lineno'):
                    line_no = node.lineno - 1
                    if line_no < len(self.lines):
                        line_content = self.lines[line_no]
                        
                        for issue_type, (pattern, severity, description) in self.patterns.items():
                            if re.search(pattern, line_content):
                                self.issues.append(PerformanceIssue(
                                    type=issue_type,
                                    severity=severity,
                                    description=description,
                                    line_number=node.lineno,
                                    snippet=line_content.strip(),
                                    recommendation=self._get_recommendation(issue_type)
                                ))
                
                super().generic_visit(node)

            def _get_recommendation(self, issue_type: str) -> str:
                recommendations = {
                    'nested_loops': 'Consider restructuring using more efficient algorithms or data structures',
                    'large_memory': 'Use streaming or chunked reading for large data',
                    'inefficient_concat': 'Use join() or string builders for multiple concatenations',
                    'global_state': 'Consider dependency injection or local state management'
                }
                return recommendations.get(issue_type, 'Review and optimize the code')

        visitor = BottleneckVisitor(lines, self.performance_patterns, issues)
        visitor.visit(tree)

        severity_distribution = {
            'low': 0,
            'medium': 0,
            'high': 0
        }
        for issue in issues:
            severity_distribution[issue.severity] += 1

        return {
            'count': len(issues),
            'severity_distribution': severity_distribution,
            'details': [vars(issue) for issue in issues]
        }

    def _analyze_async_patterns(self, tree: ast.AST) -> Dict[str, Any]:
        class AsyncVisitor(ast.NodeVisitor):
            def __init__(self):
                self.async_functions = []
                self.await_expressions = []
                self.async_with_blocks = []
                self.async_for_loops = []

            def visit_AsyncFunctionDef(self, node):
                self.async_functions.append({
                    'name': node.name,
                    'line': node.lineno
                })
                self.generic_visit(node)

            def visit_Await(self, node):
                self.await_expressions.append({
                    'line': node.lineno
                })
                self.generic_visit(node)

            def visit_AsyncWith(self, node):
                self.async_with_blocks.append({
                    'line': node.lineno
                })
                self.generic_visit(node)

            def visit_AsyncFor(self, node):
                self.async_for_loops.append({
                    'line': node.lineno
                })
                self.generic_visit(node)

        visitor = AsyncVisitor()
        visitor.visit(tree)

        total_async_constructs = (
            len(visitor.async_functions) +
            len(visitor.await_expressions) +
            len(visitor.async_with_blocks) +
            len(visitor.async_for_loops)
        )

        return {
            'async_functions': visitor.async_functions,
            'await_expressions': visitor.await_expressions,
            'async_with_blocks': visitor.async_with_blocks,
            'async_for_loops': visitor.async_for_loops,
            'total_async_constructs': total_async_constructs,
            'async_usage_score': min(total_async_constructs / 10.0, 1.0)
        }

    def _estimate_time_complexity(self, max_loop_depth: int, has_recursion: bool) -> str:
        if has_recursion:
            return "O(n^k) - recursive"
        elif max_loop_depth == 0:
            return "O(1)"
        elif max_loop_depth == 1:
            return "O(n)"
        else:
            return f"O(n^{max_loop_depth})"

    def _estimate_space_complexity(self, visitor: ComplexityVisitor) -> str:
        if visitor.recursive_functions:
            return "O(n) - recursive stack"
        elif visitor.comprehensions or visitor.generators:
            return "O(n) - data structures"
        else:
            return "O(1)"

    def _calculate_performance_score(self, analysis: Dict[str, Any]) -> float:
        weights = {
            'complexity': 0.25,
            'memory': 0.2,
            'io': 0.2,
            'caching': 0.15,
            'bottlenecks': 0.1,
            'async': 0.1
        }

        scores = {
            'complexity': self._score_complexity(analysis['complexity_metrics']),
            'memory': self._score_memory(analysis['memory_patterns']),
            'io': self._score_io(analysis['io_operations']),
            'caching': analysis['caching_opportunities']['impact_score'],
            'bottlenecks': 1.0 - min(analysis['bottlenecks']['count'] / 10.0, 1.0),
            'async': analysis['async_patterns']['async_usage_score']
        }

        return sum(scores[k] * weights[k] for k in weights)

    def _score_complexity(self, complexity_metrics: Dict[str, Any]) -> float:
        # Lower score for higher complexity
        if 'O(n^k)' in complexity_metrics['time_complexity']:
            time_score = 0.2  # Recursive complexity
        elif 'O(1)' in complexity_metrics['time_complexity']:
            time_score = 1.0  # Constant time
        elif 'O(n)' in complexity_metrics['time_complexity']:
            time_score = 0.8  # Linear time
        else:
            # Extract power from O(n^x) and score accordingly
            power = int(complexity_metrics['time_complexity'].split('^')[1][0])
            time_score = max(0.1, 1.0 - (power - 1) * 0.2)

        # Score space complexity
        if 'O(1)' in complexity_metrics['space_complexity']:
            space_score = 1.0
        else:
            space_score = 0.7  # O(n) or recursive

        return (time_score * 0.6 + space_score * 0.4)

    def _score_memory(self, memory_patterns: Dict[str, Any]) -> float:
        # Lower score for more allocations and large objects
        allocation_score = 1.0 - min(memory_patterns['allocation_count'] / 50.0, 1.0)
        large_objects_score = 1.0 - min(memory_patterns['large_objects'] / 10.0, 1.0)

        return (allocation_score * 0.7 + large_objects_score * 0.3)

    def _score_io(self, io_operations: Dict[str, Any]) -> float:
        # Higher score for more async operations
        async_ratio = io_operations['io_ratio']
        operation_count = io_operations['sync_ops'] + io_operations['async_ops']

        # Penalize high number of I/O operations
        operation_score = 1.0 - min(operation_count / 20.0, 1.0)

        return (async_ratio * 0.6 + operation_score * 0.4)

    def _get_default_metrics(self) -> Dict[str, Any]:
        return {
            'complexity_metrics': {
                'time_complexity': 'O(1)',
                'space_complexity': 'O(1)',
                'loop_depths': [],
                'recursive_functions': [],
                'comprehensions': 0,
                'generators': 0
            },
            'memory_patterns': {
                'allocation_count': 0,
                'large_objects': 0,
                'allocation_details': [],
                'large_object_details': []
            },
            'io_operations': {
                'sync_ops': 0,
                'async_ops': 0,
                'file_operations': [],
                'network_operations': [],
                'io_ratio': 0.0
            },
            'caching_opportunities': {
                'opportunities_count': 0,
                'existing_caches': 0,
                'cache_opportunities': [],
                'existing_cache_details': [],
                'impact_score': 0.0
            },
            'bottlenecks': {
                'count': 0,
                'severity_distribution': {
                    'low': 0,
                    'medium': 0,
                    'high': 0
                },
                'details': []
            },
            'async_patterns': {
                'async_functions': [],
                'await_expressions': [],
                'async_with_blocks': [],
                'async_for_loops': [],
                'total_async_constructs': 0,
                'async_usage_score': 0.0
            },
            'performance_score': 0.0
        }