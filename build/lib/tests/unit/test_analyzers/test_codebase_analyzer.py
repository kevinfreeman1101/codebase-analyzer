from datetime import datetime
from pathlib import Path
from tests.helpers import TestHelper
from codebase_analyzer.analyzer import CodebaseAnalyzer, ProjectMetrics

class TestCodebaseAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()
        self.analyzer = CodebaseAnalyzer()

    def test_analyze_project_simple(self):
        """Test analyzing a simple project with one Python file."""
        files = {
            "main.py": "def main():\n    print('hello')\n\nif __name__ == '__main__':\n    main()"
        }
        project_dir = self.helper.create_temp_project(files)

        result = self.analyzer.analyze_project(project_dir)

        # Basic assertions
        assert isinstance(result, ProjectMetrics)
        assert result.project_path == project_dir
        assert result.total_files == 1
        assert result.total_lines == 5
        assert isinstance(result.timestamp, datetime)  # Corrected to datetime class

        # Metric-specific assertions
        assert result.complexity.cyclomatic_complexity >= 2  # if + main call
        assert result.complexity.maintainability_index > 0
        assert result.quality.type_hint_coverage >= 0
        assert result.dependencies.direct_dependencies is not None
        assert result.patterns.design_patterns is not None
        assert result.security.vulnerabilities is not None
        assert result.performance.hotspots is not None

        # Score is calculated
        score = result.calculate_overall_score()
        assert 0 <= score <= 100

    def test_analyze_project_with_complexity(self):
        """Test analyzing a project with complex code."""
        files = {
            "app.py": """
def complex_func(x):
    if x > 0:
        for i in range(10):
            print(i)
    return x
"""
        }
        project_dir = self.helper.create_temp_project(files)

        result = self.analyzer.analyze_project(project_dir)

        assert result.complexity.cyclomatic_complexity >= 3  # if + for + base
        assert result.complexity.cognitive_complexity >= 2  # if + for
        assert result.complexity.nesting_depth >= 2

    def test_analyze_project_with_vulnerabilities(self):
        """Test analyzing a project with security vulnerabilities."""
        files = {
            "app.py": "import os\nos.system('ls')\n"
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
        assert isinstance(summary, str)
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
        assert "Codebase Analysis Summary" in summary
        assert str(project_dir) in summary
        assert "Total Files: 1" in summary
        assert "Total Lines: 2" in summary

    def test_analyze_project_invalid_path(self):
        """Test analyze_project with an invalid path."""
        invalid_path = Path("/nonexistent/path")
        try:
            self.analyzer.analyze_project(invalid_path)
            assert False, "Expected an exception for invalid path"
        except FileNotFoundError:
            assert True