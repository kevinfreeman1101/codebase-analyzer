"""Tests for QualityAnalyzer in quality_metrics.py."""

import pytest
from pathlib import Path
from codebase_analyzer.metrics.quality_metrics import QualityAnalyzer, QualityMetrics
from tests.helpers import TestHelper

class TestQualityAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()
        self.analyzer = QualityAnalyzer()

    def teardown_method(self):
        self.helper.cleanup_temp()

    def test_empty_file(self):
        """Test quality metrics for an empty file."""
        content = ""
        temp_file = self.helper.create_temp_file(content)
        with open(temp_file, 'r', encoding='utf-8') as f:
            tree = pytest.importorskip('ast').parse(f.read())
        result = self.analyzer.analyze_node(tree)
        assert isinstance(result, QualityMetrics)
        assert result.type_hint_coverage == 0.0
        assert result.documentation_coverage == 0.0
        assert result.test_coverage == 0.0
        assert result.lint_score == 100.0
        assert result.code_to_comment_ratio == 0.0

    def test_simple_function_with_test(self):
        """Test quality metrics for a file with a function and assert."""
        content = """
def test_func(x: int) -> bool:
    \"\"\"Test function.\"\"\"
    assert x > 0
    return True
"""
        temp_file = self.helper.create_temp_file(content)
        with open(temp_file, 'r', encoding='utf-8') as f:
            tree = pytest.importorskip('ast').parse(f.read())
        result = self.analyzer.analyze_node(tree)
        assert result.type_hint_coverage > 0  # Has type hints
        assert result.documentation_coverage > 0  # Has docstring
        assert result.test_coverage == 0.0  # Node-level is 0; project-level covers this
        assert result.lint_score == 100.0  # No lint issues
        assert result.code_to_comment_ratio == 0.0  # No comments preserved

    def test_project_with_tests(self, mocker):
        """Test quality metrics for a project with test-like code."""
        mocker.patch('subprocess.run', side_effect=[
            mocker.Mock(returncode=0, stdout=""),  # pytest run
            mocker.Mock(returncode=0, stdout="TOTAL 100 50 50%")  # coverage report
        ])
        files = {
            "main.py": "def func(x: int): return x * 2",
            "tests/test_main.py": """
def test_func():
    assert func(2) == 4
"""
        }
        project_dir = self.helper.create_temp_project(files)
        result = self.analyzer.analyze_project(Path(project_dir))
        assert result.type_hint_coverage > 0
        assert result.documentation_coverage == 0.0  # No docstrings
        assert result.test_coverage == 50.0  # Mocked coverage output
        assert result.lint_score == 100.0

    def test_mixed_functions(self):
        """Test quality metrics with mixed functions; coverage set at project level."""
        content = """
def func1(x):
    return x + 1

def test_func1():
    assert func1(2) == 3

def func2(y):
    return y * 2
"""
        temp_file = self.helper.create_temp_file(content)
        with open(temp_file, 'r', encoding='utf-8') as f:
            tree = pytest.importorskip('ast').parse(f.read())
        result = self.analyzer.analyze_node(tree)
        assert result.test_coverage == 0.0  # Node-level is 0; project-level needed
        assert result.type_hint_coverage == 0.0
        assert result.lint_score == 100.0

    def test_project_with_no_tests(self):
        """Test coverage when no test directory exists."""
        files = {
            "main.py": "def func(x: int): return x * 2"
        }
        project_dir = self.helper.create_temp_project(files)
        result = self.analyzer.analyze_project(Path(project_dir))
        assert result.test_coverage == 0.0  # No tests found
        assert result.type_hint_coverage > 0
        assert result.lint_score == 100.0