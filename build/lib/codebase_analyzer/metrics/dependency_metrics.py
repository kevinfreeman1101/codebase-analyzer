from dataclasses import dataclass
from typing import Dict, List, Set, Optional
import ast
import pkg_resources
import importlib.metadata
import re
from pathlib import Path
import os

@dataclass
class DependencyInfo:
    name: str
    version_required: str
    version_installed: Optional[str]
    usage_count: int
    is_direct: bool
    license: Optional[str]
    security_advisories: List[str]

@dataclass
class DependencyMetrics:
    direct_dependencies: Dict[str, DependencyInfo]
    indirect_dependencies: Dict[str, DependencyInfo]
    internal_dependencies: Dict[str, List[str]]
    dependency_graph: Dict[str, Set[str]]
    circular_dependencies: List[List[str]]
    unused_imports: List[str]

    def health_score(self) -> float:
        """Calculate an overall dependency health score.

        Returns:
            float: A score from 0 to 100 based on dependency health.
        """
        if not self.direct_dependencies and not self.indirect_dependencies:
            return 100.0  # No dependencies, perfect score

        score = 100.0
        # Penalty for unused imports
        unused_penalty = len(self.unused_imports) * 5
        score -= unused_penalty

        # Penalty for circular dependencies
        circular_penalty = len(self.circular_dependencies) * 10
        score -= circular_penalty

        # Check for outdated or missing versions
        for dep in self.direct_dependencies.values():
            if dep.version_installed is None:
                score -= 10  # Missing installed version
            elif dep.version_required and dep.version_installed != dep.version_required:
                score -= 5  # Version mismatch

        # Penalty for security advisories
        security_penalty = sum(len(dep.security_advisories) * 15 for dep in self.direct_dependencies.values())
        score -= security_penalty

        return max(0.0, min(100.0, score))

class DependencyAnalyzer:
    """Analyzes project dependencies and their relationships."""

    def __init__(self):
        self.direct_deps: Dict[str, DependencyInfo] = {}
        self.indirect_deps: Dict[str, DependencyInfo] = {}
        self.internal_deps: Dict[str, List[str]] = {}
        self.dep_graph: Dict[str, Set[str]] = {}
        self.import_counts: Dict[str, int] = {}

    def analyze_project(self, project_root: str, requirements_files: List[str] = None) -> DependencyMetrics:
        """Analyze all dependencies in the project.

        Args:
            project_root: Path to the project root directory.
            requirements_files: Optional list of requirement file paths; defaults to searching for common files.

        Returns:
            DependencyMetrics: Object containing dependency analysis results.
        """
        if requirements_files is None:
            requirements_files = [
                str(Path(project_root) / 'requirements.txt'),
                str(Path(project_root) / 'requirements-dev.txt')
            ]
            requirements_files = [f for f in requirements_files if os.path.exists(f)]

        self._analyze_requirements(requirements_files)
        self._analyze_imports(project_root)
        self._check_security_advisories()
        circular_deps = self._detect_circular_dependencies()
        unused_imports = self._find_unused_imports()

        return DependencyMetrics(
            direct_dependencies=self.direct_deps,
            indirect_dependencies=self.indirect_deps,
            internal_dependencies=self.internal_deps,
            dependency_graph=self.dep_graph,
            circular_dependencies=circular_deps,
            unused_imports=unused_imports
        )

    def _analyze_requirements(self, requirements_files: List[str]) -> None:
        """Analyze requirements.txt and similar files."""
        for req_file in requirements_files:
            try:
                with open(req_file) as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            self._parse_requirement(line.strip())
            except FileNotFoundError:
                continue

    def _parse_requirement(self, req_line: str) -> None:
        """Parse a single requirement line."""
        pattern = r'^([a-zA-Z0-9-_.]+)(?:$.*$)?(?:[=<>!~]=?|@)(.+)$'
        match = re.match(pattern, req_line)

        if match:
            name, version = match.groups()
        else:
            name = req_line.split('[')[0].split('=')[0].strip()
            version = ''

        try:
            installed_version = pkg_resources.get_distribution(name).version
        except pkg_resources.DistributionNotFound:
            installed_version = None

        try:
            license_info = importlib.metadata.metadata(name).get('License')
        except importlib.metadata.PackageNotFoundError:
            license_info = None

        self.direct_deps[name] = DependencyInfo(
            name=name,
            version_required=version,
            version_installed=installed_version,
            usage_count=0,
            is_direct=True,
            license=license_info,
            security_advisories=[]
        )

    def _analyze_imports(self, project_root: str) -> None:
        """Analyze all imports in Python files."""
        class ImportVisitor(ast.NodeVisitor):
            def __init__(self):
                self.imports: Dict[str, int] = {}

            def visit_Import(self, node):
                for name in node.names:
                    base_name = name.name.split('.')[0]
                    self.imports[base_name] = self.imports.get(base_name, 0) + 1

            def visit_ImportFrom(self, node):
                if node.module:
                    base_name = node.module.split('.')[0]
                    self.imports[base_name] = self.imports.get(base_name, 0) + 1

        visitor = ImportVisitor()

        for root, _, files in os.walk(project_root):
            for file in files:
                if file.endswith('.py'):
                    try:
                        with open(os.path.join(root, file)) as f:
                            tree = ast.parse(f.read())
                            visitor.visit(tree)
                    except (SyntaxError, UnicodeDecodeError):
                        continue

        for name, count in visitor.imports.items():
            if name in self.direct_deps:
                self.direct_deps[name].usage_count = count
            elif name in self.indirect_deps:
                self.indirect_deps[name].usage_count = count

    def _check_security_advisories(self) -> None:
        """Check for known security vulnerabilities."""
        # Placeholder for advisory database API
        pass

    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies in the project."""
        def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
            def dfs(node: str, path: List[str], visited: Set[str]) -> List[List[str]]:
                if node in path:
                    cycle_start = path.index(node)
                    return [path[cycle_start:]]
                cycles = []
                if node in graph:
                    path.append(node)
                    visited.add(node)
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            cycles.extend(dfs(neighbor, path[:], visited))
                    path.pop()
                    visited.remove(node)
                return cycles

            visited: Set[str] = set()
            cycles: List[List[str]] = []
            for node in graph:
                if node not in visited:
                    cycles.extend(dfs(node, [], visited))
            return cycles

        return find_cycles(self.dep_graph)

    def _find_unused_imports(self) -> List[str]:
        """Find imports that are declared but not used."""
        return [
            name for name, info in self.direct_deps.items()
            if info.usage_count == 0
        ]

    def get_dependency_summary(self) -> str:
        """Generate a human-readable dependency summary."""
        summary = []
        summary.append("Dependency Analysis")
        summary.append("===================")

        summary.append("\nDirect Dependencies:")
        for dep in sorted(self.direct_deps.values(), key=lambda x: x.usage_count, reverse=True):
            summary.append(f"- {dep.name} (required: {dep.version_required}, "
                         f"installed: {dep.version_installed}, "
                         f"usage count: {dep.usage_count})")
            if dep.license:
                summary.append(f"  License: {dep.license}")
            if dep.security_advisories:
                summary.append("  Security Advisories:")
                for advisory in dep.security_advisories:
                    summary.append(f"  - {advisory}")

        if self.indirect_deps:
            summary.append("\nIndirect Dependencies:")
            for dep in sorted(self.indirect_deps.values(), key=lambda x: x.name):
                summary.append(f"- {dep.name} (installed: {dep.version_installed})")

        cycles = self._detect_circular_dependencies()
        if cycles:
            summary.append("\nCircular Dependencies Detected:")
            for cycle in cycles:
                summary.append(f"- {' -> '.join(cycle)}")

        unused = self._find_unused_imports()
        if unused:
            summary.append("\nUnused Dependencies:")
            for dep in sorted(unused):
                summary.append(f"- {dep}")

        return "\n".join(summary)