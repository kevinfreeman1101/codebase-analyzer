from dataclasses import dataclass
from typing import Dict, List, Set, Optional
import ast
import re
from pathlib import Path

@dataclass
class DesignPattern:
    name: str
    confidence: float  # 0-1 score of detection confidence
    locations: List[str]  # Files/classes where pattern is used
    description: str
    implementation_notes: Optional[str] = None

@dataclass
class ArchitecturalStyle:
    name: str
    confidence: float
    evidence: List[str]
    suggestions: List[str]

@dataclass
class PatternMetrics:
    design_patterns: List[DesignPattern]
    architectural_style: ArchitecturalStyle
    api_patterns: Dict[str, float]
    database_patterns: Dict[str, float]
    anti_patterns: List[Dict[str, str]]

class PatternAnalyzer:
    """Analyzes code patterns and architectural styles."""

    def __init__(self):
        self.patterns: List[DesignPattern] = []
        self.api_patterns: Dict[str, float] = {}
        self.db_patterns: Dict[str, float] = {}
        self.anti_patterns: List[Dict[str, str]] = []

    def analyze_project(self, project_root: Path) -> PatternMetrics:
        """Analyze all patterns in the project."""
        self._detect_design_patterns(project_root)
        self._analyze_architecture(project_root)
        self._detect_api_patterns(project_root)
        self._detect_database_patterns(project_root)
        self._detect_anti_patterns(project_root)

        return PatternMetrics(
            design_patterns=self.patterns,
            architectural_style=self._determine_architecture_style(),
            api_patterns=self.api_patterns,
            database_patterns=self.db_patterns,
            anti_patterns=self.anti_patterns
        )

    def _detect_design_patterns(self, project_root: Path) -> None:
        """Detect common design patterns in the codebase."""
        patterns = {
            'singleton': self._detect_singleton_pattern,
            'factory': self._detect_factory_pattern,
            'strategy': self._detect_strategy_pattern,
            # Add others as implemented
        }

        for file_path in project_root.rglob('*.py'):
            try:
                with open(file_path) as f:
                    tree = ast.parse(f.read())
                    for pattern_name, detector in patterns.items():
                        result = detector(tree, file_path)
                        if result:
                            self.patterns.append(result)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _detect_singleton_pattern(self, tree: ast.AST, file_path: Path) -> Optional[DesignPattern]:
        """Detect Singleton pattern implementation."""
        class SingletonVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_private_constructor = False
                self.has_instance_var = False
                self.has_instance_method = False
                self.class_name = None

            def visit_ClassDef(self, node):
                self.class_name = node.name
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name == '__init__':
                            for decorator in item.decorator_list:
                                if isinstance(decorator, ast.Name) and decorator.id == 'private':
                                    self.has_private_constructor = True
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name) and target.id == '_instance':
                                self.has_instance_var = True
                    elif isinstance(item, ast.FunctionDef) and item.name == 'get_instance':
                        self.has_instance_method = True

        visitor = SingletonVisitor()
        visitor.visit(tree)

        if visitor.has_instance_var and visitor.has_instance_method:
            return DesignPattern(
                name="Singleton",
                confidence=0.9 if visitor.has_private_constructor else 0.7,
                locations=[str(file_path)],
                description=f"Singleton pattern detected in class {visitor.class_name}",
                implementation_notes="Implements instance control through get_instance method"
            )
        return None

    def _detect_factory_pattern(self, tree: ast.AST, file_path: Path) -> Optional[DesignPattern]:
        """Detect Factory pattern implementation."""
        class FactoryVisitor(ast.NodeVisitor):
            def __init__(self):
                self.creates_objects = False
                self.has_factory_method = False
                self.class_name = None
                self.created_types = set()

            def visit_ClassDef(self, node):
                self.class_name = node.name
                if 'Factory' in node.name:
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if any(x in item.name.lower() for x in ['create', 'get', 'make']):
                                self.has_factory_method = True
                                returns = self._find_return_types(item)
                                self.created_types.update(returns)

            def _find_return_types(self, node):
                returns = set()
                for child in ast.walk(node):
                    if isinstance(child, ast.Return):
                        if isinstance(child.value, ast.Call):
                            if isinstance(child.value.func, ast.Name):
                                returns.add(child.value.func.id)
                return returns

        visitor = FactoryVisitor()
        visitor.visit(tree)

        if visitor.has_factory_method and visitor.created_types:
            return DesignPattern(
                name="Factory",
                confidence=0.8,
                locations=[str(file_path)],
                description=f"Factory pattern detected in class {visitor.class_name}",
                implementation_notes=f"Creates objects of types: {', '.join(visitor.created_types)}"
            )
        return None

    def _detect_strategy_pattern(self, tree: ast.AST, file_path: Path) -> Optional[DesignPattern]:
        """Detect Strategy pattern implementation."""
        class StrategyVisitor(ast.NodeVisitor):
            def __init__(self):
                self.strategy_classes = set()
                self.context_class = None
                self.has_strategy_field = False

            def visit_ClassDef(self, node):
                if any(isinstance(base, ast.Name) and 'Strategy' in base.id 
                      for base in node.bases):
                    self.strategy_classes.add(node.name)
                for item in node.body:
                    if isinstance(item, ast.AnnAssign):
                        if isinstance(item.annotation, ast.Name):
                            if 'Strategy' in item.annotation.id:
                                self.context_class = node.name
                                self.has_strategy_field = True

        visitor = StrategyVisitor()
        visitor.visit(tree)

        if visitor.strategy_classes and visitor.has_strategy_field:
            return DesignPattern(
                name="Strategy",
                confidence=0.9,
                locations=[str(file_path)],
                description=f"Strategy pattern detected with context class {visitor.context_class}",
                implementation_notes=f"Strategy implementations: {', '.join(visitor.strategy_classes)}"
            )
        return None

    def _detect_observer_pattern(self, tree: ast.AST, file_path: Path) -> Optional[DesignPattern]:
        """Detect Observer pattern implementation."""
        class ObserverVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_observers = False
                self.has_notify = False
                self.class_name = None

            def visit_ClassDef(self, node):
                self.class_name = node.name
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        if any(isinstance(target, ast.Name) and 'observers' in target.id.lower() 
                               for target in item.targets):
                            self.has_observers = True
                    if isinstance(item, ast.FunctionDef):
                        if 'notify' in item.name.lower():
                            self.has_notify = True

        visitor = ObserverVisitor()
        visitor.visit(tree)

        if visitor.has_observers and visitor.has_notify:
            return DesignPattern(
                name="Observer",
                confidence=0.8,
                locations=[str(file_path)],
                description=f"Observer pattern detected in class {visitor.class_name}",
                implementation_notes="Uses observer list and notify method"
            )
        return None

    def _detect_decorator_pattern(self, tree: ast.AST, file_path: Path) -> Optional[DesignPattern]:
        """Detect Decorator pattern implementation."""
        class DecoratorVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_component = False
                self.has_decorator = False
                self.class_name = None

            def visit_ClassDef(self, node):
                self.class_name = node.name
                for base in node.bases:
                    if isinstance(base, ast.Name) and 'Component' in base.id:
                        self.has_component = True
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        if any(isinstance(target, ast.Name) and 'component' in target.id.lower() 
                               for target in item.targets):
                            self.has_decorator = True

        visitor = DecoratorVisitor()
        visitor.visit(tree)

        if visitor.has_component and visitor.has_decorator:
            return DesignPattern(
                name="Decorator",
                confidence=0.85,
                locations=[str(file_path)],
                description=f"Decorator pattern detected in class {visitor.class_name}",
                implementation_notes="Wraps a component object"
            )
        return None

    def _detect_adapter_pattern(self, tree: ast.AST, file_path: Path) -> Optional[DesignPattern]:
        """Detect Adapter pattern implementation."""
        class AdapterVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_adaptee = False
                self.has_adapted_method = False
                self.class_name = None

            def visit_ClassDef(self, node):
                self.class_name = node.name
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        if any(isinstance(target, ast.Name) and 'adaptee' in target.id.lower() 
                               for target in item.targets):
                            self.has_adaptee = True
                    if isinstance(item, ast.FunctionDef):
                        for call in ast.walk(item):
                            if isinstance(call, ast.Call):
                                if isinstance(call.func, ast.Attribute) and 'adaptee' in call.func.value.id.lower():
                                    self.has_adapted_method = True

        visitor = AdapterVisitor()
        visitor.visit(tree)

        if visitor.has_adaptee and visitor.has_adapted_method:
            return DesignPattern(
                name="Adapter",
                confidence=0.8,
                locations=[str(file_path)],
                description=f"Adapter pattern detected in class {visitor.class_name}",
                implementation_notes="Adapts an adaptee object"
            )
        return None

    def _analyze_architecture(self, project_root: Path) -> None:
        """Analyze the overall architectural style of the project."""
        self._evidence = []  # Collect evidence for architectural style
        self._analyze_layered_architecture(project_root)

    def _analyze_layered_architecture(self, project_root: Path) -> None:
        """Analyze if the project follows a layered architecture."""
        layers = {'presentation': False, 'business': False, 'data': False}
        for file_path in project_root.rglob('*.py'):
            file_name = file_path.name.lower()
            if 'view' in file_name or 'ui' in file_name:
                layers['presentation'] = True
                self._evidence.append(f"Presentation layer detected in {file_path}")
            elif 'service' in file_name or 'logic' in file_name:
                layers['business'] = True
                self._evidence.append(f"Business layer detected in {file_path}")
            elif 'model' in file_name or 'data' in file_name:
                layers['data'] = True
                self._evidence.append(f"Data layer detected in {file_path}")

    def _determine_architecture_style(self) -> ArchitecturalStyle:
        """Determine the predominant architectural style."""
        if hasattr(self, '_evidence') and self._evidence:
            confidence = min(1.0, len(self._evidence) * 0.3)  # Rough heuristic
            return ArchitecturalStyle(
                name="Layered",
                confidence=confidence,
                evidence=self._evidence,
                suggestions=["Ensure clear separation of concerns between layers"]
            )
        return ArchitecturalStyle(
            name="Unknown",
            confidence=0.5,
            evidence=["No clear architectural evidence found"],
            suggestions=["Consider defining a clear architecture"]
        )

    def _detect_api_patterns(self, project_root: Path) -> None:
        """Detect API-related patterns (placeholder)."""
        pass

    def _detect_database_patterns(self, project_root: Path) -> None:
        """Detect database-related patterns (placeholder)."""
        pass

    def _detect_anti_patterns(self, project_root: Path) -> None:
        """Detect anti-patterns (placeholder)."""
        pass

    def get_pattern_summary(self) -> str:
        """Generate a human-readable pattern summary."""
        summary = []
        summary.append("Pattern Analysis")
        summary.append("================")
        if self.patterns:
            summary.append("\nDesign Patterns Detected:")
            for pattern in sorted(self.patterns, key=lambda x: x.confidence, reverse=True):
                summary.append(f"\n{pattern.name} Pattern")
                summary.append(f"Confidence: {pattern.confidence:.1%}")
                summary.append(f"Location: {', '.join(pattern.locations)}")
                summary.append(f"Description: {pattern.description}")
                if pattern.implementation_notes:
                    summary.append(f"Notes: {pattern.implementation_notes}")
        arch_style = self._determine_architecture_style()
        summary.append(f"\nArchitectural Style: {arch_style.name}")
        summary.append(f"Confidence: {arch_style.confidence:.1%}")
        summary.append("\nEvidence:")
        for evidence in arch_style.evidence:
            summary.append(f"- {evidence}")
        if self.anti_patterns:
            summary.append("\nAnti-patterns Detected:")
            for anti in self.anti_patterns:
                summary.append(f"\n- {anti['name']}")
                summary.append(f"  Location: {anti['location']}")
                summary.append(f"  Suggestion: {anti['suggestion']}")
        return "\n".join(summary)