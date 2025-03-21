import ast
import sys
from typing import Set, List, Optional, Dict, Any
from .base_analyzer import BaseAnalyzer
from ..models.data_classes import FileInfo, FunctionInfo, ClassInfo, CodeSnippet
from ..utils.file_utils import safe_read_file

class PythonAnalyzer(BaseAnalyzer):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.functions: Dict[str, FunctionInfo] = {}
        self.classes: Dict[str, ClassInfo] = {}
        self.imports: Set[str] = set()
        self.content: Optional[str] = None
        self.ast_tree: Optional[ast.AST] = None

    def get_file_type(self) -> str:
        return 'python'

    def analyze(self) -> FileInfo:
        """Analyze the Python file and return FileInfo."""
        try:
            self.content = safe_read_file(self.file_path)
        except IOError as e:
            print(f"Skipping file due to error: {self.file_path} - {e}")
            self.content = ""

        if self.content:
            try:
                self.ast_tree = ast.parse(self.content)
                self._analyze_ast()
            except Exception as e:
                print(f"Error analyzing Python file {self.file_path}: {str(e)}")

        return FileInfo(
            path=self.file_path,
            type=self.get_file_type(),
            content=self.content or "",
            size=len(self.content or ""),
            dependencies=self.dependencies,
            functions=self.functions,
            classes=self.classes
        )

    def _analyze_ast(self):
        """Analyze the AST and collect information about the code."""
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

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a node."""
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1  # AND/OR increase complexity
        return complexity

    def _process_function(self, node: ast.FunctionDef) -> Optional[FunctionInfo]:
        """Process a function definition node."""
        if not self.content:
            return None

        try:
            params = [arg.arg for arg in node.args.args]
            returns = self._get_return_type(node)
            docstring = ast.get_docstring(node) or ""
            deps = self._get_dependencies(node)
            loc = node.end_lineno - node.lineno + 1
            code_snippet = self._get_code_snippet(node)
            complexity = self._calculate_complexity(node)

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

    def _process_class_attributes(self, node: ast.ClassDef) -> List[Dict[str, Any]]:
        """Extract class attributes from class body."""
        attributes = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                attr_name = item.target.id if isinstance(item.target, ast.Name) else None
                if attr_name:
                    attr_type = ast.unparse(item.annotation) if item.annotation else None
                    doc = None
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
        """Process a class definition node."""
        try:
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_info = self._process_function(item)
                    if method_info:
                        methods.append(method_info)

            attributes = self._process_class_attributes(node)
            base_classes = [ast.unparse(base) for base in node.bases]
            code_snippet = self._get_code_snippet(node)
            complexity = self._calculate_complexity(node)

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
        """Extract the actual code for a node."""
        if not self.content:
            return CodeSnippet("", 0, 0)

        start_line = node.lineno - 1
        end_line = node.end_lineno
        lines = self.content.split('\n')
        code_lines = lines[start_line:end_line]
        return CodeSnippet(
            content='\n'.join(code_lines),
            start_line=start_line + 1,
            end_line=end_line
        )

    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type annotation if present."""
        if node.returns:
            return ast.unparse(node.returns)
        return ""

    def _get_dependencies(self, node: ast.AST) -> Set[str]:
        """Extract dependencies from a node."""
        deps = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                deps.add(child.id)
        return deps - self.imports  # Exclude imports themselves

    def _process_import(self, node: ast.Import):
        """Process import statements."""
        for name in node.names:
            self.imports.add(name.name)
            self.dependencies.add(name.name)

    def _process_import_from(self, node: ast.ImportFrom):
        """Process from ... import statements."""
        module = node.module or ""
        for name in node.names:
            import_name = f"{module}.{name.name}"
            self.imports.add(import_name)
            self.dependencies.add(import_name)

    def get_external_dependencies(self) -> Set[str]:
        """Extract external dependencies (excluding standard library)."""
        stdlib_modules = set(sys.stdlib_module_names)
        return {dep.split('.')[0] for dep in self.dependencies 
                if dep.split('.')[0] not in stdlib_modules}