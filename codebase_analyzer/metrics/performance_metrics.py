import ast
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PerformanceHotspot:
    location: str
    complexity: int
    execution_count_estimate: int
    optimization_suggestion: str

@dataclass
class LoopOptimization:
    location: str
    loop_type: str
    complexity: int
    suggestion: str

@dataclass
class PerformanceMetrics:
    hotspots: List[PerformanceHotspot]
    performance_score: float
    loop_optimizations: List[LoopOptimization]
    memory_intensive_ops: List[str]
    io_operations: List[str]

class PerformanceAnalyzer:
    """Analyzes code for performance metrics and optimization opportunities."""

    def __init__(self):
        self.hotspots: List[PerformanceHotspot] = []
        self.loop_optimizations: List[LoopOptimization] = []
        self.memory_ops: List[str] = []
        self.io_ops: List[str] = []

    def analyze_project(self, project_root: Path) -> PerformanceMetrics:
        """Analyze the project for performance characteristics."""
        self._identify_hotspots(project_root)
        self._identify_optimization_opportunities(project_root)
        self._detect_memory_intensive_operations(project_root)
        self._detect_io_operations(project_root)
        score = self._calculate_performance_score()

        return PerformanceMetrics(
            hotspots=self.hotspots,
            performance_score=score,
            loop_optimizations=self.loop_optimizations,
            memory_intensive_ops=self.memory_ops,
            io_operations=self.io_ops
        )

    def _identify_hotspots(self, project_root: Path) -> None:
        """Identify potential performance hotspots."""
        for file_path in project_root.rglob('*.py'):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    self._analyze_hotspots(tree, file_path)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _analyze_hotspots(self, tree: ast.AST, file_path: Path) -> None:
        """Analyze AST for performance hotspots."""
        class HotspotVisitor(ast.NodeVisitor):
            def __init__(self, hotspots: List[PerformanceHotspot], file_path: Path):
                self.hotspots = hotspots
                self.file_path = file_path

            def visit_For(self, node):
                complexity = self._calculate_complexity(node)
                if complexity > 5:  # Arbitrary threshold
                    self.hotspots.append(PerformanceHotspot(
                        location=f"{self.file_path}:{node.lineno}",
                        complexity=complexity,
                        execution_count_estimate=10,  # Placeholder
                        optimization_suggestion="Consider list comprehension or vectorization"
                    ))
                self.generic_visit(node)

            def visit_While(self, node):
                complexity = self._calculate_complexity(node)
                if complexity > 5:
                    self.hotspots.append(PerformanceHotspot(
                        location=f"{self.file_path}:{node.lineno}",
                        complexity=complexity,
                        execution_count_estimate=10,  # Placeholder
                        optimization_suggestion="Evaluate loop termination condition"
                    ))
                self.generic_visit(node)

            def _calculate_complexity(self, node: ast.AST) -> int:
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While, ast.If)):
                        complexity += 1
                return complexity

        visitor = HotspotVisitor(self.hotspots, file_path)
        visitor.visit(tree)

    def _identify_optimization_opportunities(self, project_root: Path) -> None:
        """Identify opportunities for performance optimization."""
        for file_path in project_root.rglob('*.py'):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    self._analyze_optimizations(tree, file_path)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _analyze_optimizations(self, tree: ast.AST, file_path: Path) -> None:
        """Analyze AST for optimization opportunities."""
        class OptimizationVisitor(ast.NodeVisitor):
            def __init__(self, optimizations: List[LoopOptimization], file_path: Path):
                self.optimizations = optimizations
                self.file_path = file_path

            def visit_For(self, node):
                complexity = self._calculate_complexity(node)
                if isinstance(node.body, list) and len(node.body) == 1:
                    # Check for list.append calls
                    if (isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Call) and 
                        isinstance(node.body[0].value.func, ast.Attribute) and 
                        node.body[0].value.func.attr == 'append'):
                        self.optimizations.append(LoopOptimization(
                            location=f"{self.file_path}:{node.lineno}",
                            loop_type="For",
                            complexity=complexity,
                            suggestion="Replace with list comprehension"
                        ))
                self.generic_visit(node)

            def visit_While(self, node):
                complexity = self._calculate_complexity(node)
                if len(node.body) > 10:  # Long loops
                    self.optimizations.append(LoopOptimization(
                        location=f"{self.file_path}:{node.lineno}",
                        loop_type="While",
                        complexity=complexity,
                        suggestion="Consider breaking into smaller loops"
                    ))
                self.generic_visit(node)

            def _calculate_complexity(self, node: ast.AST) -> int:
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While, ast.If)):
                        complexity += 1
                return complexity

        visitor = OptimizationVisitor(self.loop_optimizations, file_path)
        visitor.visit(tree)

    def _detect_memory_intensive_operations(self, project_root: Path) -> None:
        """Detect memory-intensive operations."""
        for file_path in project_root.rglob('*.py'):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    self._analyze_memory_ops(tree, file_path)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _analyze_memory_ops(self, tree: ast.AST, file_path: Path) -> None:
        """Analyze AST for memory-intensive operations."""
        class MemoryVisitor(ast.NodeVisitor):
            def __init__(self, memory_ops: List[str], file_path: Path):
                self.memory_ops = memory_ops
                self.file_path = file_path

            def visit_ListComp(self, node):
                self.memory_ops.append(f"{self.file_path}:{node.lineno} - Large list comprehension")
                self.generic_visit(node)

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id in ['deepcopy', 'copy']:
                    self.memory_ops.append(f"{self.file_path}:{node.lineno} - Deep copy operation")
                self.generic_visit(node)

        visitor = MemoryVisitor(self.memory_ops, file_path)
        visitor.visit(tree)

    def _detect_io_operations(self, project_root: Path) -> None:
        """Detect I/O operations."""
        for file_path in project_root.rglob('*.py'):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    self._analyze_io_ops(tree, file_path)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _analyze_io_ops(self, tree: ast.AST, file_path: Path) -> None:
        """Analyze AST for I/O operations."""
        class IOVisitor(ast.NodeVisitor):
            def __init__(self, io_ops: List[str], file_path: Path):
                self.io_ops = io_ops
                self.file_path = file_path

            def visit_Call(self, node):
                if isinstance(node.func, ast.Attribute):
                    func_name = ast.unparse(node.func)
                    if any(x in func_name for x in ['open', 'read', 'write', 'print']):
                        self.io_ops.append(f"{self.file_path}:{node.lineno} - {func_name}")
                self.generic_visit(node)

        visitor = IOVisitor(self.io_ops, file_path)
        visitor.visit(tree)

    def _calculate_performance_score(self) -> float:
        """Calculate an overall performance score."""
        if not (self.hotspots or self.loop_optimizations or self.memory_ops or self.io_ops):
            return 100.0

        hotspot_penalty = len(self.hotspots) * 10
        loop_penalty = len(self.loop_optimizations) * 5
        memory_penalty = len(self.memory_ops) * 8
        io_penalty = len(self.io_ops) * 5

        raw_score = 100 - (hotspot_penalty + loop_penalty + memory_penalty + io_penalty)
        return max(0.0, min(100.0, raw_score))