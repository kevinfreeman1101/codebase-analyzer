# codebase_analyzer/features/security.py
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import ast
import re
from dataclasses import dataclass

from .base import FeatureExtractor

@dataclass
class SecurityIssue:
    """Container for security issues found in code."""
    type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    line_number: int
    snippet: str
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID
    recommendation: Optional[str] = None

class SecurityFeatureExtractor(FeatureExtractor):
    """Extracts security-related features and identifies potential vulnerabilities."""

    def __init__(self):
        self.sensitive_patterns = {
            'password': r'password|passwd|pwd',
            'api_key': r'api[_-]?key|token|secret',
            'credentials': r'credential|auth[_-]?token',
            'private_key': r'private[_-]?key|secret[_-]?key',
            'social_security': r'ssn|social[_-]?security',
            'credit_card': r'credit[_-]?card|card[_-]?number'
        }

        self.vulnerability_patterns = {
            'sql_injection': (
                r'execute\s*\(|cursor\.execute|raw_input|input\s*\(.*\bquery\b',
                'high',
                'CWE-89'
            ),
            'command_injection': (
                r'os\.system|subprocess\.call|eval\(|exec\(',
                'critical',
                'CWE-78'
            ),
            'xss': (
                r'innerHTML|outerHTML|document\.write',
                'high',
                'CWE-79'
            ),
            'path_traversal': (
                r'\.\.\/|\.\.\\|\%2e\%2e\%2f',
                'high',
                'CWE-22'
            ),
            'insecure_deserialization': (
                r'pickle\.loads|yaml\.load|eval\(',
                'high',
                'CWE-502'
            )
        }

    def extract(self, code: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
            lines = code.split('\n')

            security_analysis = {
                'vulnerabilities': self._analyze_vulnerabilities(tree, lines),
                'sensitive_data': self._analyze_sensitive_data(tree, lines),
                'security_patterns': self._analyze_security_patterns(tree),
                'input_validation': self._analyze_input_validation(tree),
                'authentication': self._analyze_authentication(tree),
                'crypto_usage': self._analyze_crypto_usage(tree, lines),
                'security_score': 0.0  # Will be calculated at the end
            }

            security_analysis['security_score'] = self._calculate_security_score(
                security_analysis
            )

            return security_analysis
        except Exception as e:
            return self._get_default_metrics()

    def get_feature_names(self) -> List[str]:
        return [
            'vulnerabilities.count',
            'vulnerabilities.severity_distribution',
            'sensitive_data.exposure_count',
            'sensitive_data.types',
            'security_patterns.validation_score',
            'security_patterns.sanitization_score',
            'input_validation.coverage',
            'input_validation.strength',
            'authentication.methods',
            'authentication.strength',
            'crypto_usage.algorithms',
            'crypto_usage.strength',
            'security_score'
        ]

    def _analyze_vulnerabilities(self, tree: ast.AST, lines: List[str]) -> Dict[str, Any]:
        issues: List[SecurityIssue] = []
        
        class VulnerabilityVisitor(ast.NodeVisitor):
            def __init__(self, lines, patterns, issues):
                self.lines = lines
                self.patterns = patterns
                self.issues = issues

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = f"{node.func.value.id}.{node.func.attr}"
                else:
                    func_name = ""

                line_no = node.lineno - 1
                line_content = self.lines[line_no] if line_no < len(self.lines) else ""

                for vuln_type, (pattern, severity, cwe) in self.patterns.items():
                    if re.search(pattern, func_name) or re.search(pattern, line_content):
                        self.issues.append(SecurityIssue(
                            type=vuln_type,
                            severity=severity,
                            description=self._get_vulnerability_description(vuln_type),
                            line_number=node.lineno,
                            snippet=line_content.strip(),
                            cwe_id=cwe,
                            recommendation=self._get_recommendation(vuln_type)
                        ))

                self.generic_visit(node)

            def _get_vulnerability_description(self, vuln_type: str) -> str:
                descriptions = {
                    'sql_injection': 'Potential SQL injection vulnerability detected',
                    'command_injection': 'Possible command injection vulnerability',
                    'xss': 'Cross-site scripting vulnerability potential',
                    'path_traversal': 'Path traversal vulnerability detected',
                    'insecure_deserialization': 'Insecure deserialization detected'
                }
                return descriptions.get(vuln_type, 'Unknown vulnerability type')

            def _get_recommendation(self, vuln_type: str) -> str:
                recommendations = {
                    'sql_injection': 'Use parameterized queries or ORM',
                    'command_injection': 'Use subprocess.run with shell=False',
                    'xss': 'Use content security policy and input sanitization',
                    'path_traversal': 'Use os.path.normpath and validate paths',
                    'insecure_deserialization': 'Use json or other safe serializers'
                }
                return recommendations.get(vuln_type, 'Review and fix security issue')

        visitor = VulnerabilityVisitor(lines, self.vulnerability_patterns, issues)
        visitor.visit(tree)

        severity_distribution = {
            'low': 0,
            'medium': 0,
            'high': 0,
            'critical': 0
        }
        for issue in issues:
            severity_distribution[issue.severity] += 1

        return {
            'count': len(issues),
            'severity_distribution': severity_distribution,
            'details': [vars(issue) for issue in issues]
        }

    def _analyze_sensitive_data(self, tree: ast.AST, lines: List[str]) -> Dict[str, Any]:
        exposed_data: List[Dict[str, Any]] = []
        
        class SensitiveDataVisitor(ast.NodeVisitor):
            def __init__(self, lines, patterns, exposed_data):
                self.lines = lines
                self.patterns = patterns
                self.exposed_data = exposed_data

            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        line_no = target.lineno - 1
                        line_content = self.lines[line_no] if line_no < len(self.lines) else ""

                        for data_type, pattern in self.patterns.items():
                            if re.search(pattern, name, re.IGNORECASE):
                                self.exposed_data.append({
                                    'type': data_type,
                                    'line_number': target.lineno,
                                    'variable_name': name,
                                    'snippet': line_content.strip()
                                })

                self.generic_visit(node)

        visitor = SensitiveDataVisitor(lines, self.sensitive_patterns, exposed_data)
        visitor.visit(tree)

        return {
            'exposure_count': len(exposed_data),
            'types': list(set(item['type'] for item in exposed_data)),
            'details': exposed_data
        }

    def _analyze_security_patterns(self, tree: ast.AST) -> Dict[str, Any]:
        class SecurityPatternVisitor(ast.NodeVisitor):
            def __init__(self):
                self.validation_patterns = 0
                self.sanitization_patterns = 0
                self.encryption_patterns = 0
                self.secure_headers = 0
                self.csrf_protection = 0

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) or isinstance(node.func, ast.Attribute):
                    func_name = ast.unparse(node.func)
                    
                    # Check for input validation
                    if re.search(r'validate|clean|sanitize|escape', func_name, re.I):
                        self.validation_patterns += 1
                    
                    # Check for sanitization
                    if re.search(r'html\.escape|sanitize|bleach', func_name, re.I):
                        self.sanitization_patterns += 1
                    
                    # Check for encryption
                    if re.search(r'encrypt|hash|digest', func_name, re.I):
                        self.encryption_patterns += 1
                    
                    # Check for secure headers
                    if re.search(r'set_secure_headers|csp|hsts', func_name, re.I):
                        self.secure_headers += 1
                    
                    # Check for CSRF protection
                    if re.search(r'csrf|xsrf|token', func_name, re.I):
                        self.csrf_protection += 1

                self.generic_visit(node)

        visitor = SecurityPatternVisitor()
        visitor.visit(tree)

        return {
            'validation_score': min(visitor.validation_patterns / 5.0, 1.0),
            'sanitization_score': min(visitor.sanitization_patterns / 5.0, 1.0),
            'encryption_score': min(visitor.encryption_patterns / 5.0, 1.0),
            'secure_headers_score': min(visitor.secure_headers / 3.0, 1.0),
            'csrf_protection_score': min(visitor.csrf_protection / 2.0, 1.0)
        }

    def _analyze_input_validation(self, tree: ast.AST) -> Dict[str, Any]:
        class InputValidationVisitor(ast.NodeVisitor):
            def __init__(self):
                self.validation_count = 0
                self.input_points = 0
                self.validation_types = set()

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    # Count input points
                    if node.func.id in {'input', 'request', 'get', 'post'}:
                        self.input_points += 1
                    
                    # Count validation patterns
                    if node.func.id in {'isinstance', 'validate', 'clean'}:
                        self.validation_count += 1
                        self.validation_types.add(node.func.id)

                self.generic_visit(node)

        visitor = InputValidationVisitor()
        visitor.visit(tree)

        return {
            'coverage': visitor.validation_count / max(visitor.input_points, 1),
            'strength': len(visitor.validation_types) / 5.0,  # Normalized to 0-1
            'validation_types': list(visitor.validation_types)
        }

    def _analyze_authentication(self, tree: ast.AST) -> Dict[str, Any]:
        auth_patterns = {
            'basic_auth': r'basic_auth|authenticate',
            'token_auth': r'token_auth|jwt|bearer',
            'oauth': r'oauth|oidc',
            'session': r'session|cookie',
            'mfa': r'mfa|two_factor|2fa'
        }

        auth_methods: Set[str] = set()
        
        class AuthenticationVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) or isinstance(node.func, ast.Attribute):
                    func_name = ast.unparse(node.func)
                    
                    for auth_type, pattern in auth_patterns.items():
                        if re.search(pattern, func_name, re.I):
                            auth_methods.add(auth_type)

                self.generic_visit(node)

        visitor = AuthenticationVisitor()
        visitor.visit(tree)

        return {
            'methods': list(auth_methods),
            'strength': len(auth_methods) / len(auth_patterns),
            'mfa_enabled': 'mfa' in auth_methods
        }

    def _analyze_crypto_usage(self, tree: ast.AST, lines: List[str]) -> Dict[str, Any]:
        crypto_patterns = {
            'strong': {
                'aes': r'AES',
                'rsa': r'RSA',
                'bcrypt': r'bcrypt',
                'pbkdf2': r'pbkdf2',
                'argon2': r'argon2'
            },
            'weak': {
                'md5': r'md5',
                'sha1': r'sha1',
                'des': r'DES',
                'blowfish': r'blowfish'
            }
        }

        found_algorithms = {
            'strong': set(),
            'weak': set()
        }

        for line in lines:
            for strength, patterns in crypto_patterns.items():
                for algo, pattern in patterns.items():
                    if re.search(pattern, line, re.I):
                        found_algorithms[strength].add(algo)

        return {
            'algorithms': {
                'strong': list(found_algorithms['strong']),
                'weak': list(found_algorithms['weak'])
            },
            'strength': len(found_algorithms['strong']) / (
                len(found_algorithms['strong']) + len(found_algorithms['weak'])
            ) if any(found_algorithms.values()) else 0.0
        }

    def _calculate_security_score(self, analysis: Dict[str, Any]) -> float:
        weights = {
            'vulnerabilities': 0.3,
            'sensitive_data': 0.2,
            'security_patterns': 0.15,
            'input_validation': 0.15,
            'authentication': 0.1,
            'crypto_usage': 0.1
        }

        scores = {
            'vulnerabilities': 1.0 - min(analysis['vulnerabilities']['count'] / 10.0, 1.0),
            'sensitive_data': 1.0 - min(analysis['sensitive_data']['exposure_count'] / 5.0, 1.0),
            'security_patterns': sum(analysis['security_patterns'].values()) / len(analysis['security_patterns']),
            'input_validation': analysis['input_validation']['coverage'] * analysis['input_validation']['strength'],
            'authentication': analysis['authentication']['strength'],
            'crypto_usage': analysis['crypto_usage']['strength']
        }

        return sum(scores[k] * weights[k] for k in weights)

    def _get_default_metrics(self) -> Dict[str, Any]:
        return {
            'vulnerabilities': {
                'count': 0,
                'severity_distribution': {
                    'low': 0,
                    'medium': 0,
                    'high': 0,
                    'critical': 0
                },
                'details': []
            },
            'sensitive_data': {
                'exposure_count': 0,
                'types': [],
                'details': []
            },
            'security_patterns': {
                'validation_score': 0.0,
                'sanitization_score': 0.0,
                'encryption_score': 0.0,
                'secure_headers_score': 0.0,
                'csrf_protection_score': 0.0
            },
            'input_validation': {
                'coverage': 0.0,
                'strength': 0.0,
                'validation_types': []
            },
            'authentication': {
                'methods': [],
                'strength': 0.0,
                'mfa_enabled': False
            },
            'crypto_usage': {
                'algorithms': {
                    'strong': [],
                    'weak': []
                },
                'strength': 0.0
            },
            'security_score': 0.0
        }