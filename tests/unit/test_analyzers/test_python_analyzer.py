import pytest
from pathlib import Path
from codebase_analyzer.analyzers.python_analyzer import PythonAnalyzer
from tests.helpers import TestHelper

class TestPythonAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()
        self.analyzer = PythonAnalyzer(Path("/tmp/dummy.py"))  # Dummy path, overridden in tests

    def teardown_method(self):
        self.helper.cleanup_temp()

    def test_analyze_empty_file(self):
        """Test analyzing an empty Python file."""
        content = ""
        temp_file = self.helper.create_temp_file(content)
        self.analyzer.file_path = Path(temp_file)
        result = self.analyzer.analyze()
        assert result is not None
        assert result.functions == {}
        assert result.classes == {}
        assert result.dependencies == set()

    def test_analyze_simple_function(self):
        """Test analyzing a file with a simple function."""
        content = """
def simple(x):
    return x + 1
"""
        temp_file = self.helper.create_temp_file(content)
        self.analyzer.file_path = Path(temp_file)
        result = self.analyzer.analyze()
        assert "simple" in result.functions
        assert result.functions["simple"].params == ["x"]
        assert result.functions["simple"].returns == "None"

    def test_analyze_complex_function(self):
        """Test analyzing a file with a complex function."""
        content = """
def complex_func(x):
    if x > 0:
        for i in range(x):
            print(i)
    return x
"""
        temp_file = self.helper.create_temp_file(content)
        self.analyzer.file_path = Path(temp_file)
        result = self.analyzer.analyze()
        assert "complex_func" in result.functions
        assert result.functions["complex_func"].complexity > 2

    def test_analyze_dependencies(self):
        """Test analyzing a file with dependencies."""
        content = """
import os
from math import sqrt
def func():
    os.path.join('a', 'b')
    return sqrt(4)
"""
        temp_file = self.helper.create_temp_file(content)
        self.analyzer.file_path = Path(temp_file)
        result = self.analyzer.analyze()
        assert "os" in result.dependencies
        assert "math" in result.dependencies

    def test_basic_analysis(self):
        """Test basic analysis with a class and function."""
        content = """
class MyClass:
    def method(self):
        pass
def standalone():
    pass
"""
        temp_file = self.helper.create_temp_file(content)
        self.analyzer.file_path = Path(temp_file)
        result = self.analyzer.analyze()
        assert "MyClass" in result.classes
        assert "method" in result.classes["MyClass"].methods
        assert "standalone" in result.functions

    def test_unused_imports(self):
        """Test detection of unused imports."""
        content = """
import os
import math
def func():
    return os.path.join('a', 'b')
"""
        temp_file = self.helper.create_temp_file(content)
        self.analyzer.file_path = Path(temp_file)
        result = self.analyzer.analyze()
        assert "os" in result.dependencies
        assert "math" in result.unused_imports

    def test_malformed_file(self):
        """Test handling of a malformed Python file."""
        content = "def func(): return 1\n    print('indentation error')"
        temp_file = self.helper.create_temp_file(content)
        self.analyzer.file_path = Path(temp_file)
        result = self.analyzer.analyze()
        assert result is not None
        assert result.functions == {}
        assert result.classes == {}