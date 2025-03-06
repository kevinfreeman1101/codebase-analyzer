"""Analyzer for entire projects, orchestrating file-level analysis."""

import json
from typing import Dict, Optional, Set
from pathlib import Path
from hashlib import sha256
import subprocess
from ..formatters.summary_formatter import SummaryFormatter
from ..utils.file_utils import safe_read_file
from .python_analyzer import PythonAnalyzer
from .generic_analyzer import GenericAnalyzer

class ProjectAnalyzer:
    """Analyzes a project directory, coordinating file analysis and formatting results."""

    def __init__(self, root_path: Path):
        """Initialize ProjectAnalyzer with the project root path.

        Args:
            root_path: Path to the project root directory.
        """
        self.root_path = Path(root_path).resolve()
        self.formatter = SummaryFormatter(self.root_path)
        self.dependencies: Set[str] = set()
        self.dependency_cache_file = self.root_path / ".dependency_cache.json"

    def _hash_requirements(self) -> str:
        """Generate a SHA256 hash of requirements.txt if it exists."""
        req_file = self.root_path / "requirements.txt"
        if not req_file.exists():
            return ""
        content = safe_read_file(req_file)
        return sha256(content.encode('utf-8')).hexdigest() if content else ""

    def _load_dependency_cache(self) -> Optional[Dict[str, str]]:
        """Load cached dependency check results."""
        if self.dependency_cache_file.exists():
            try:
                with open(self.dependency_cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def _save_dependency_cache(self, req_hash: str, outdated: str, vulnerabilities: str) -> None:
        """Save dependency check results to cache."""
        cache = {
            "requirements_hash": req_hash,
            "outdated": outdated,
            "vulnerabilities": vulnerabilities
        }
        try:
            with open(self.dependency_cache_file, 'w') as f:
                json.dump(cache, f)
        except IOError:
            pass  # Silently fail if cache write fails

    def _check_dependency_health(self) -> tuple[str, str]:
        """Check dependency health using safety and pip for outdated packages."""
        req_hash = self._hash_requirements()
        if req_hash:
            # Check cache
            cache = self._load_dependency_cache()
            if cache and cache.get("requirements_hash") == req_hash:
                return cache["outdated"], cache["vulnerabilities"]

        # Run safety check if no cache or cache miss
        vulnerabilities = ""
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                vulnerabilities = result.stdout
            else:
                vulnerabilities = result.stderr or "Safety check failed"
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            vulnerabilities = f"Safety check error: {str(e)}"

        # Check for outdated packages
        outdated = ""
        try:
            result = subprocess.run(
                ["pip", "list", "--outdated"],
                capture_output=True,
                text=True,
                timeout=30
            )
            outdated = result.stdout if result.returncode == 0 else result.stderr
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            outdated = f"Pip outdated check error: {str(e)}"

        # Cache the results
        if req_hash:
            self._save_dependency_cache(req_hash, outdated, vulnerabilities)

        return outdated, vulnerabilities

    def analyze(self) -> Optional[str]:
        """Analyze the project directory and generate a summary.

        Returns:
            Optional[str]: Formatted summary of the project analysis, or None if analysis fails.
        """
        if not self.root_path.exists() or not self.root_path.is_dir():
            return None

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.root_path)
                analyzer: Optional[PythonAnalyzer | GenericAnalyzer] = None

                if file_path.suffix == '.py':
                    analyzer = PythonAnalyzer(file_path, self.dependencies)
                else:
                    analyzer = GenericAnalyzer(file_path)

                file_info = analyzer.analyze()
                if file_info:
                    self.formatter.add_source_file(str(relative_path), file_info)

        outdated, vulnerabilities = self._check_dependency_health()
        self.formatter.dependency_health['outdated'] = outdated
        self.formatter.dependency_health['vulnerabilities'] = vulnerabilities

        return self.formatter.generate_summary()