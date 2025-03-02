"""Tests for DependencyAnalyzer in dependency_metrics.py."""

import pytest
from pathlib import Path
from codebase_analyzer.metrics.dependency_metrics import DependencyAnalyzer, DependencyMetrics
from tests.helpers import TestHelper

class TestDependencyAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()
        self.analyzer = DependencyAnalyzer()

    def teardown_method(self):
        self.helper.cleanup_temp()

    def test_basic_dependencies(self):
        """Test dependency analysis with a simple project."""
        files = {
            "main.py": "import os\nprint('hello')",
            "requirements.txt": "numpy>=1.24.3"
        }
        project_dir = self.helper.create_temp_project(files)
        result = self.analyzer.analyze_project(project_dir)
        assert "os" in result.direct_dependencies
        assert "numpy" in result.direct_dependencies
        assert result.health_score() > 0

    def test_vulnerable_dependencies(self, mocker):
        """Test detection of vulnerable dependencies."""
        mocker.patch(
            'subprocess.run',
            return_value=mocker.Mock(
                returncode=0,
                stdout='{"vulnerabilities": [{"package": "numpy", "installed_version": "1.24.3", "advisory": "CVE-XXXX", "severity": "HIGH"}]}'
            )
        )
        files = {
            "requirements.txt": "numpy>=1.24.3"
        }
        project_dir = self.helper.create_temp_project(files)
        result = self.analyzer.analyze_project(project_dir)
        assert "numpy" in result.direct_dependencies
        assert len(result.vulnerable_dependencies) == 1
        assert result.vulnerable_dependencies[0]["name"] == "numpy"
        assert result.vulnerable_dependencies[0]["severity"] == "HIGH"
        assert result.health_score() < 100.0