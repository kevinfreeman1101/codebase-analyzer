"""Module for analyzing dependency metrics in Python projects."""

import ast
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from pathlib import Path
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class DependencyMetrics:
    """Represents dependency metrics for a Python project."""
    direct_dependencies: Set[str]
    dependency_tree: Dict[str, List[str]]
    vulnerable_dependencies: List[Dict[str, str]]  # Added for vulnerability data

    def health_score(self) -> float:
        """Calculate a dependency health score."""
        base_score = 100.0
        penalty = len(self.direct_dependencies) * 2  # Base penalty for count
        vuln_penalty = len(self.vulnerable_dependencies) * 10  # Higher penalty for vulns
        return max(0.0, base_score - penalty - vuln_penalty)

class DependencyAnalyzer:
    """Analyzes Python project dependencies."""

    def analyze_project(self, project_path: Path) -> DependencyMetrics:
        """Analyze dependencies in a project directory.

        Args:
            project_path: Path to the project root directory.

        Returns:
            DependencyMetrics: Metrics including direct deps, tree, and vulnerabilities.
        """
        direct_deps = set()
        dependency_tree = {}
        vulnerable_deps = []

        # Find requirements.txt or similar files
        req_files = list(project_path.rglob("requirements*.txt"))
        if req_files:
            for req_file in req_files:
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                dep = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                                direct_deps.add(dep)
                except Exception as e:
                    logger.error(f"Failed to read {req_file}: {str(e)}")

        # Analyze code for imports
        for py_file in project_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            direct_deps.add(name.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module.split('.')[0] if node.module else ''
                        direct_deps.add(module)
            except (SyntaxError, UnicodeDecodeError, FileNotFoundError) as e:
                logger.warning(f"Skipping {py_file} due to parsing error: {str(e)}")

        # Build a simple dependency tree (direct deps only)
        dependency_tree = {dep: [] for dep in direct_deps}

        # Scan for vulnerabilities with safety
        if req_files:
            try:
                result = subprocess.run(
                    ["safety", "check", "--json", "--file", str(req_files[0])],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0 and result.stdout:
                    vuln_data = json.loads(result.stdout)
                    vulnerable_deps = [
                        {
                            "name": vuln["package"],
                            "version": vuln["installed_version"],
                            "vulnerability": vuln["advisory"],
                            "severity": vuln["severity"]
                        } for vuln in vuln_data.get("vulnerabilities", [])
                    ]
                elif result.returncode != 0:
                    logger.warning(f"Safety check failed: {result.stderr}")
            except Exception as e:
                logger.error(f"Dependency vulnerability scan failed: {str(e)}")

        return DependencyMetrics(
            direct_dependencies=direct_deps,
            dependency_tree=dependency_tree,
            vulnerable_dependencies=vulnerable_deps
        )