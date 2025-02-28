from dataclasses import dataclass
from typing import Set, Dict, List
from pathlib import Path
from tests.helpers import TestHelper
from codebase_analyzer.analyzers.python_analyzer import PythonAnalyzer, FileInfo

class TestPythonAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()
        self.temp_file = self.helper.create_temp_file("")
        self.analyzer = PythonAnalyzer(self.temp_file)

    def test_analyze_empty_file(self):
        result = self.analyzer.analyze()
        assert result is not None, "Expected a FileInfo object for empty file"
        assert isinstance(result, FileInfo), "Result should be a FileInfo instance"
        assert len(result.functions) == 0
        assert len(result.classes) == 0

    def test_analyze_simple_function(self):
        content = """
def test_function():
    return True
"""
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert isinstance(result, FileInfo), "Result should be a FileInfo instance"
        assert len(result.functions) > 0
        assert "test_function" in result.functions
        assert result.functions["test_function"].complexity == 1
        self.helper.cleanup_temp(temp_file)

    def test_analyze_complex_function(self):
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
        assert isinstance(result, FileInfo), "Result should be a FileInfo instance"
        assert "complex_function" in result.functions
        assert result.functions["complex_function"].complexity >= 4
        self.helper.cleanup_temp(temp_file)

    def test_analyze_dependencies(self):
        content = """
import os
from datetime import datetime
import sys as system
"""
        temp_file = self.helper.create_temp_file(content)
        analyzer = PythonAnalyzer(temp_file)
        result = analyzer.analyze()
        assert isinstance(result, FileInfo), "Result should be a FileInfo instance"
        assert "os" in result.dependencies
        assert "datetime.datetime" in result.dependencies
        assert "sys" in result.dependencies
        self.helper.cleanup_temp(temp_file)

    def teardown_method(self):
        if hasattr(self, 'temp_file'):
            self.helper.cleanup_temp(self.temp_file)