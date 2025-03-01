import ast
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class Vulnerability:
    type: str
    description: str
    severity: str
    location: str
    recommendation: str

@dataclass
class SecurityPattern:
    name: str
    confidence: float
    locations: List[str]
    description: str

@dataclass
class SecurityMetrics:
    vulnerabilities: List[Vulnerability]
    security_score: float
    security_patterns: List[SecurityPattern]

class SecurityAnalyzer:
    """Analyzes code for security vulnerabilities and patterns."""

    def __init__(self) -> None:
        self.vulnerabilities: List[Vulnerability] = []
        self.patterns: List[SecurityPattern] = []

    def analyze_project(self, project_root: Path) -> SecurityMetrics:
        """Analyze the project for security issues.

        Args:
            project_root: Path to the project root directory.

        Returns:
            SecurityMetrics: Object containing vulnerabilities, score, and patterns.
        """
        self._detect_vulnerabilities(project_root)
        self._detect_security_patterns(project_root)
        score: float = self._calculate_security_score()

        return SecurityMetrics(
            vulnerabilities=self.vulnerabilities,
            security_score=score,
            security_patterns=self.patterns
        )

    def _detect_vulnerabilities(self, project_root: Path) -> None:
        """Detect common security vulnerabilities in Python files."""
        for file_path in project_root.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content: str = f.read()
                    tree: ast.AST = ast.parse(content)
                    self._check_for_insecure_functions(tree, file_path)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _check_for_insecure_functions(self, tree: ast.AST, file_path: Path) -> None:
        """Check for use of insecure functions in the AST.

        Args:
            tree: The AST of the Python file.
            file_path: Path to the file being analyzed.
        """
        insecure_funcs: Dict[str, tuple[str, str, str]] = {
            'os.system': ('Command Injection', 'HIGH', 'Use subprocess with shell=False'),
            'eval': ('Code Injection', 'CRITICAL', 'Avoid eval; use ast.literal_eval if needed'),
            'exec': ('Code Injection', 'CRITICAL', 'Avoid exec'),
            'input': ('Input Vulnerability', 'MEDIUM', 'Use safer input methods for Python 2'),
        }

        class InsecureFunctionVisitor(ast.NodeVisitor):
            def __init__(self, vulnerabilities: List[Vulnerability], file_path: Path):
                self.vulnerabilities: List[Vulnerability] = vulnerabilities
                self.file_path: Path = file_path

            def visit_Call(self, node: ast.Call) -> None:
                if isinstance(node.func, ast.Attribute):
                    func_name: str = f"{ast.unparse(node.func.value)}.{node.func.attr}"
                elif isinstance(node.func, ast.Name):
                    func_name: str = node.func.id
                else:
                    func_name: Optional[str] = None

                if func_name in insecure_funcs:
                    vuln_type, severity, recommendation = insecure_funcs[func_name]
                    self.vulnerabilities.append(Vulnerability(
                        type=vuln_type,
                        description=f"Use of insecure function: {func_name}",
                        severity=severity,
                        location=f"{self.file_path}:{node.lineno}",
                        recommendation=recommendation
                    ))
                self.generic_visit(node)

        visitor = InsecureFunctionVisitor(self.vulnerabilities, file_path)
        visitor.visit(tree)

    def _detect_security_patterns(self, project_root: Path) -> None:
        """Detect implementation of security patterns in Python files."""
        patterns: Dict[str, callable] = {
            'Authentication': self._check_authentication_pattern,
            'InputValidation': self._check_input_validation,
        }

        for file_path in project_root.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content: str = f.read()
                    tree: ast.AST = ast.parse(content)
                    for pattern_name, detector in patterns.items():
                        result: Optional[SecurityPattern] = detector(tree, file_path)
                        if result:
                            self.patterns.append(result)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _check_authentication_pattern(self, tree: ast.AST, file_path: Path) -> Optional[SecurityPattern]:
        """Check for authentication pattern in the AST.

        Args:
            tree: The AST of the Python file.
            file_path: Path to the file being analyzed.

        Returns:
            Optional[SecurityPattern]: Detected pattern or None if not found.
        """
        class AuthVisitor(ast.NodeVisitor):
            def __init__(self) -> None:
                self.auth_detected: bool = False

            def visit_Import(self, node: ast.Import) -> None:
                for name in node.names:
                    if name.name in ['flask_login', 'django.contrib.auth']:
                        self.auth_detected = True
                self.generic_visit(node)

            def visit_Call(self, node: ast.Call) -> None:
                if isinstance(node.func, ast.Attribute):
                    func_name: str = ast.unparse(node.func)
                    if 'login' in func_name.lower() or 'authenticate' in func_name.lower():
                        self.auth_detected = True
                self.generic_visit(node)

        visitor = AuthVisitor()
        visitor.visit(tree)

        if visitor.auth_detected:
            return SecurityPattern(
                name="Authentication",
                confidence=0.7,
                locations=[str(file_path)],
                description="Evidence of authentication mechanisms detected"
            )
        return None

    def _check_input_validation(self, tree: ast.AST, file_path: Path) -> Optional[SecurityPattern]:
        """Check for input validation pattern in the AST.

        Args:
            tree: The AST of the Python file.
            file_path: Path to the file being analyzed.

        Returns:
            Optional[SecurityPattern]: Detected pattern or None if not found.
        """
        class ValidationVisitor(ast.NodeVisitor):
            def __init__(self) -> None:
                self.validation_detected: bool = False

            def visit_Call(self, node: ast.Call) -> None:
                if isinstance(node.func, ast.Attribute):
                    func_name: str = ast.unparse(node.func)
                    if any(x in func_name.lower() for x in ['validate', 'sanitize', 'escape']):
                        self.validation_detected = True
                self.generic_visit(node)

            def visit_If(self, node: ast.If) -> None:
                if isinstance(node.test, ast.Compare):
                    self.validation_detected = True
                self.generic_visit(node)

        visitor = ValidationVisitor()
        visitor.visit(tree)

        if visitor.validation_detected:
            return SecurityPattern(
                name="InputValidation",
                confidence=0.6,
                locations=[str(file_path)],
                description="Evidence of input validation detected"
            )
        return None

    def _calculate_security_score(self) -> float:
        """Calculate an overall security score based on vulnerabilities and patterns.

        Returns:
            float: Score from 0 to 100.
        """
        if not self.vulnerabilities and not self.patterns:
            return 100.0

        vuln_score: int = 0
        for vuln in self.vulnerabilities:
            if vuln.severity == 'CRITICAL':
                vuln_score += 30
            elif vuln.severity == 'HIGH':
                vuln_score += 20
            elif vuln.severity == 'MEDIUM':
                vuln_score += 10
            else:
                vuln_score += 5

        pattern_score: int = len(self.patterns) * 10
        raw_score: float = 100 - vuln_score + pattern_score
        return max(0.0, min(100.0, raw_score))