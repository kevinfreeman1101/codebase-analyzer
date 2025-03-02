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
        assert result.test_coverage > 0  # Has assert
        assert result.lint_score == 100.0  # No lint issues
        assert result.code_to_comment_ratio == 0.0  # No comments preserved

    def test_project_with_tests(self):
        """Test quality metrics for a project with test-like code."""
        files = {
            "main.py": "def func(x: int): return x * 2",
            "test_main.py": """
def test_func():
    assert func(2) == 4
"""
        }
        project_dir = self.helper.create_temp_project(files)
        result = self.analyzer.analyze_project(Path(project_dir))
        assert result.type_hint_coverage > 0
        assert result.documentation_coverage == 0.0  # No docstrings
        assert result.test_coverage > 0  # Assert in test file
        assert result.lint_score == 100.0