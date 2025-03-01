"""Module for analyzing Python files to extract detailed code structure and dependencies.

This module provides the PythonAnalyzer class, which inherits from BaseAnalyzer to
specialize in parsing Python source code. It extracts functions, classes, imports,
type hints, and complexity metrics, enabling comprehensive analysis for LLM advisors.
"""

import ast
import sys
from typing import Set, List, Optional, Dict, Any
from pathlib import Path
from .base_analyzer import BaseAnalyzer
from ..models.data_classes import FileInfo, FunctionInfo, ClassInfo, CodeSnippet
from ..utils.file_utils import safe_read_file

class PythonAnalyzer(BaseAnalyzer):
    """Analyzes Python files to extract detailed structural and dependency information.

    Inherits from BaseAnalyzer to provide specialized analysis for Python source code,
    including function and class definitions, imports, type hints, and code complexity.
    """

    def __init__(self, file_path: str) -> None:
        """Initialize the PythonAnalyzer with a file path.

        Args:
            file_path: Path to the Python file to analyze.
        """
        super().__init__(file_path)
        self.functions: Dict[str, FunctionInfo] = {}
        self.classes: Dict[str, ClassInfo] = {}
        self.imports: Set[str] = set()
        self.used_names: Set[str] = set()
        self.content: Optional[str] = None
        self.ast_tree: Optional[ast.AST] = None

    def get_file_type(self) -> str:
        """Return the file type identifier for Python files.

        Returns:
            str: 'python' to indicate the file type.
        """
        return 'python'

    def analyze(self) -> FileInfo:
        """Analyze the Python file and return detailed FileInfo for LLM understanding.

        Reads the file content, parses it into an AST, and extracts structural information
        such as functions, classes, dependencies, and unused imports.

        Returns:
            FileInfo: Comprehensive file data including dependencies, functions, and classes.
        """
        self.content = safe_read_file(self.file_path)
        if self.content is None:
            print(f"Error reading file: {self.file_path}")
            self.content = ""

        if self.content:
            try:
                self.ast_tree = ast.parse(self.content)
                self._analyze_ast()
            except Exception as e:
                print(f"Error analyzing Python file {self.file_path}: {str(e)}")

        unused_imports: Set[str] = self.get_unused_imports()
        return FileInfo(
            path=Path(self.file_path),
            type=self.get_file_type(),
            content=self.content or "",
            size=len(self.content or ""),
            dependencies=self.dependencies,
            functions=self.functions,
            classes=self.classes,
            unused_imports=unused_imports
        )

    def _analyze_ast(self) -> None:
        """Analyze the AST to collect code structure and usage information.

        Walks the AST to identify and process function definitions, class definitions,
        imports, and name usage for dependency and import analysis.
        """
        if not self.ast_tree:
            return

        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                self._process_function(node)
            elif isinstance(node, ast.ClassDef):
                self._process_class(node)
            elif isinstance(node, ast.Import):
                self._process_import(node)
            elif isinstance(node, ast.ImportFrom):
                self._process_import_from(node)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                self.used_names.add(node.id)

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a node.

        Counts decision points (if, for, while, try, etc.) to assess code complexity.

        Args:
            node: The AST node to analyze.

        Returns:
            int: Cyclomatic complexity score.
        """
        complexity: int = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _process_function(self, node: ast.FunctionDef) -> Optional[FunctionInfo]:
        """Process a function definition node and extract metadata.

        Extracts parameters, return type, docstring, dependencies, and complexity for a function.

        Args:
            node: The FunctionDef node from the AST.

        Returns:
            Optional[FunctionInfo]: Function metadata if successful, None if an error occurs.
        """
        if not self.content:
            return None

        try:
            params: List[str] = [arg.arg for arg in node.args.args]
            returns: str = self._get_return_type(node)
            docstring: str = ast.get_docstring(node) or ""
            deps: Set[str] = self._get_dependencies(node)
            loc: int = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 1
            code_snippet: CodeSnippet = self._get_code_snippet(node)
            complexity: int = self._calculate_complexity(node)

            function_info = FunctionInfo(
                name=node.name,
                params=params,
                returns=returns,
                docstring=docstring,
                dependencies=deps,
                loc=loc,
                code=code_snippet,
                file_path=self.file_path,
                complexity=complexity
            )

            self.functions[node.name] = function_info
            return function_info
        except Exception as e:
            print(f"Error processing function {node.name}: {str(e)}")
            return None

    def _process_class_attributes(self, node: ast.ClassDef) -> List[Dict[str, Optional[str]]]:
        """Extract class attributes from class body.

        Identifies annotated assignments and regular assignments to build attribute metadata.

        Args:
            node: The ClassDef node from the AST.

        Returns:
            List[Dict[str, Optional[str]]]: List of attribute metadata dictionaries.
        """
        attributes: List[Dict[str, Optional[str]]] = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                attr_name: Optional[str] = item.target.id if isinstance(item.target, ast.Name) else None
                if attr_name:
                    attr_type: Optional[str] = ast.unparse(item.annotation) if item.annotation else None
                    doc: Optional[str] = None
                    if item.value and isinstance(item.value, ast.Constant):
                        doc = item.value.value if isinstance(item.value.value, str) else None
                    attributes.append({
                        'name': attr_name,
                        'type_annotation': attr_type,
                        'docstring': doc
                    })
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append({
                            'name': target.id,
                            'type_annotation': None,
                            'docstring': None
                        })
        return attributes

    def _process_class(self, node: ast.ClassDef) -> Optional[ClassInfo]:
        """Process a class definition node and extract metadata.

        Captures methods, base classes, attributes, and complexity for a class.

        Args:
            node: The ClassDef node from the AST.

        Returns:
            Optional[ClassInfo]: Class metadata if successful, None if an error occurs.
        """
        try:
            methods: List[FunctionInfo] = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_info: Optional[FunctionInfo] = self._process_function(item)
                    if method_info:
                        methods.append(method_info)

            attributes: List[Dict[str, Optional[str]]] = self._process_class_attributes(node)
            base_classes: List[str] = [ast.unparse(base) for base in node.bases]
            code_snippet: CodeSnippet = self._get_code_snippet(node)
            complexity: int = self._calculate_complexity(node)

            class_info = ClassInfo(
                name=node.name,
                methods=methods,
                base_classes=base_classes,
                docstring=ast.get_docstring(node) or "",
                code=code_snippet,
                file_path=self.file_path,
                attributes=attributes,
                complexity=complexity
            )

            self.classes[node.name] = class_info
            return class_info
        except Exception as e:
            print(f"Error processing class {node.name}: {str(e)}")
            return None

    def _get_code_snippet(self, node: ast.AST) -> CodeSnippet:
        """Extract the actual code for a node to aid LLM code review.

        Args:
            node: The AST node to extract code from.

        Returns:
            CodeSnippet: Object containing the code content and line numbers.
        """
        if not self.content:
            return CodeSnippet("", 0, 0)

        start_line: int = node.lineno - 1
        end_line: int = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
        lines: List[str] = self.content.split('\n')
        code_lines: List[str] = lines[start_line:end_line]
        return CodeSnippet(
            content='\n'.join(code_lines),
            start_line=start_line + 1,
            end_line=end_line
        )

    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type annotation if present for type safety.

        Args:
            node: The FunctionDef node to inspect.

        Returns:
            str: Return type annotation string or empty if none.
        """
        if node.returns:
            return ast.unparse(node.returns)
        return ""

    def _get_dependencies(self, node: ast.AST) -> Set[str]:
        """Extract dependencies from a node, excluding imports.

        Identifies names used within the node that are loaded (not defined locally).

        Args:
            node: The AST node to analyze.

        Returns:
            Set[str]: Set of dependency names.
        """
        deps: Set[str] = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                deps.add(child.id)
        return deps - self.imports

    def _process_import(self, node: ast.Import) -> None:
        """Process import statements and track them.

        Adds imported module names to the imports and dependencies sets.

        Args:
            node: The Import node from the AST.
        """
        for name in node.names:
            self.imports.add(name.name)
            self.dependencies.add(name.name)

    def _process_import_from(self, node: ast.ImportFrom) -> None:
        """Process from ... import statements and track them.

        Adds fully qualified import names (e.g., module.name) to imports and dependencies.

        Args:
            node: The ImportFrom node from the AST.
        """
        module: str = node.module or ""
        for name in node.names:
            import_name: str = f"{module}.{name.name}"
            self.imports.add(import_name)
            self.dependencies.add(import_name)

    def get_external_dependencies(self) -> Set[str]:
        """Extract external dependencies excluding standard library modules.

        Filters dependencies to exclude Python standard library modules.

        Returns:
            Set[str]: Set of external dependency names (top-level module names).
        """
        stdlib_modules: Set[str] = set(sys.stdlib_module_names)
        return {dep.split('.')[0] for dep in self.dependencies 
                if dep.split('.')[0] not in stdlib_modules}

    def get_unused_imports(self) -> Set[str]:
        """Detect imports that are defined but not used in the code.

        Compares imported names against used names to identify unused imports.

        Returns:
            Set[str]: Set of unused import names.
        """
        return self.imports - self.used_names