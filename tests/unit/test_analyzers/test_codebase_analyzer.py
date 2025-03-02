"""Tests for CodebaseAnalyzer."""

import pytest
from pathlib import Path
from codebase_analyzer.analyzer import CodebaseAnalyzer
from tests.helpers import TestHelper

class TestCodebaseAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()
        self.analyzer = CodebaseAnalyzer()

    def teardown_method(self):
        self.helper.cleanup_temp()

    def test_analyze_project_simple(self):
        """Test analyzing a simple project with one file."""
        files = {
            "main.py": "def main():\n    print('hello')"
        }
        project_dir = self.helper.create_temp_project(files)
    
        result = self.analyzer.analyze_project(project_dir)
    
        assert result.total_files == 1
        assert result.total_lines == 2
        assert result.complexity.cyclomatic_complexity >= 1.0  # At least one decision point
        assert result.quality.lint_score > 0

    def test_analyze_project_with_complexity(self):
        """Test analyzing a project with complex code."""
        files = {
            "complex.py": """
def complex_function(x):
    if x > 0:
        for i in range(10):
            print(i)
    return x
"""
        }
        project_dir = self.helper.create_temp_project(files)
    
        result = self.analyzer.analyze_project(project_dir)
    
        assert result.total_files == 1
        assert result.total_lines > 5
        assert result.complexity.cyclomatic_complexity > 1.0  # Multiple decision points

    def test_analyze_project_with_vulnerabilities(self):
        """Test analyzing a project with potential security issues."""
        files = {
            "vuln.py": """
def risky():
    eval('print(123)')  # Potential vulnerability
"""
        }
        project_dir = self.helper.create_temp_project(files)
    
        result = self.analyzer.analyze_project(project_dir)
    
        assert len(result.security.vulnerabilities) > 0

    def test_analyze_project_empty(self):
        """Test analyzing an empty project directory."""
        project_dir = self.helper.create_temp_project({})
        result = self.analyzer.analyze_project(project_dir)
    
        assert result.total_files == 0
        assert result.total_lines == 0

    def test_generate_summary_no_analysis(self):
        """Test generate_summary without prior analysis."""
        summary = self.analyzer.generate_summary()
        assert "No analysis data available" in summary

    def test_generate_summary_after_analysis(self):
        """Test generate_summary after analyzing a simple project."""
        files = {
            "main.py": "def main():\n    print('hello')"
        }
        project_dir = self.helper.create_temp_project(files)
    
        self.analyzer.analyze_project(project_dir)
        summary = self.analyzer.generate_summary()
    
        assert isinstance(summary, str)
        assert "CODEBASE ANALYSIS SUMMARY" in summary  # Match actual output case
        assert f"Total Python Files: {self.analyzer.project_metrics.total_files}" in summary
        assert "COMPLEXITY METRICS" in summary
        assert "QUALITY METRICS" in summary

    def test_analyze_project_invalid_path(self):
        """Test analyzing an invalid project path."""
        invalid_path = Path("/nonexistent/path")
        with pytest.raises(FileNotFoundError):
            self.analyzer.analyze_project(invalid_path)

    def test_analyze_project_with_errors(self, mocker):
        """Test analyzing a project with simulated analysis errors."""
        mocker.patch(
            'codebase_analyzer.metrics.complexity_analyzer.ComplexityAnalyzer.analyze_project',
            side_effect=Exception("Simulated complexity error")
        )
        files = {
            "main.py": "def main():\n    print('hello')"
        }
        project_dir = self.helper.create_temp_project(files)
    
        result = self.analyzer.analyze_project(project_dir)
        summary = self.analyzer.generate_summary()
    
        assert "ANALYSIS ERRORS" in summary
        assert "Simulated complexity error" in summary
        assert result.complexity.cyclomatic_complexity == 0.0  # Default value on error