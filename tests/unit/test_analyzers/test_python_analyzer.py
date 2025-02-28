import pytest
from pathlib import Path
from codebase_analyzer.analyzers.python_analyzer import PythonAnalyzer
from codebase_analyzer.models.data_classes import FileInfo
from tests.helpers import TestHelper

class TestPythonAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()

    def teardown_method(self):
        self.helper.cleanup_temp()

    def test_analyze_empty_file(self):
        """Test analyzing an empty file."""
        content = ""
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert isinstance(result, FileInfo)
        assert len(result.functions) == 0
        assert len(result.classes) == 0

    def test_analyze_simple_function(self):
        """Test analyzing a file with a simple function."""
        content = """
def test_function():
    return True
"""
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert isinstance(result, FileInfo)
        assert len(result.functions) > 0
        assert "test_function" in result.functions

    def test_analyze_complex_function(self):
        """Test analyzing a file with a complex function."""
        content = """
def complex_function(x):
    if x > 0:
        for i in range(10):
            if i % 2 == 0:
                print(i)
    return x
"""
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert isinstance(result, FileInfo)
        assert "complex_function" in result.functions
        assert result.functions["complex_function"].complexity > 1

    def test_analyze_dependencies(self):
        """Test analyzing a file with dependencies."""
        content = """
import os
from datetime import datetime
import sys as system
"""
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert isinstance(result, FileInfo)
        assert "os" in result.dependencies
        assert "datetime.datetime" in result.dependencies
        assert "sys" in result.dependencies  # Checks module name, not alias

    def test_basic_analysis(self):
        """Test basic Python file analysis functionality."""
        content = 'def foo():\n    """Return a string."""\n    return "bar"'
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert isinstance(result, FileInfo), "Result should be a FileInfo object"
        assert "foo" in result.functions, "Function 'foo' should be detected"
        assert result.functions["foo"].name == "foo", "Function name should match"
        assert result.functions["foo"].docstring == "Return a string.", "Docstring should be extracted"
        assert result.functions["foo"].returns == "", "No return annotation expected"
        assert result.size == len('def foo():\n    """Return a string."""\n    return "bar"'), "Size should match content length"

    def test_unused_imports(self):
        """Test detection of unused imports."""
        content = 'import os\ndef foo():\n    return "bar"'
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert "os" in result.unused_imports, "Unused import 'os' should be detected"
        assert "foo" in result.functions, "Function 'foo' should still be analyzed"