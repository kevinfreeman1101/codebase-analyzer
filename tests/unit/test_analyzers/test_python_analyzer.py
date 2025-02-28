import pytest
from pathlib import Path
from codebase_analyzer.analyzers.python_analyzer import PythonAnalyzer, FileInfo
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
        assert "sys" in result.dependencies  # Fixed to check module name, not alias