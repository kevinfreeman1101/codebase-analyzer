import pytest
from pathlib import Path
from codebase_analyzer.analyzers.python_analyzer import PythonAnalyzer

def test_analyze_empty_file(tmp_path):
    """Test analyzing an empty Python file."""
    file_path = tmp_path / "empty.py"
    file_path.write_text("")
    analyzer = PythonAnalyzer(file_path)
    result = analyzer.analyze()
    assert len(result.functions) == 0
    assert result.size == 0

def test_analyze_simple_function(tmp_path):
    """Test analyzing a file with a simple function."""
    content = "def simple():\n    print('hi')"
    file_path = tmp_path / "simple.py"
    file_path.write_text(content)
    analyzer = PythonAnalyzer(file_path)
    result = analyzer.analyze()
    assert "simple" in result.functions
    assert result.functions["simple"].loc == 2
    assert result.functions["simple"].complexity == 1

def test_analyze_complex_function(tmp_path):
    """Test analyzing a file with a complex function."""
    content = """
def complex(x):
    if x > 0:
        for i in range(5):
            print(i)
    return x
"""
    file_path = tmp_path / "complex.py"
    file_path.write_text(content)
    analyzer = PythonAnalyzer(file_path)
    result = analyzer.analyze()
    assert "complex" in result.functions
    assert result.functions["complex"].loc == 5
    assert result.functions["complex"].complexity == 3

def test_analyze_dependencies(tmp_path):
    """Test analyzing a file with imports."""
    content = "import os\nimport sys\n\ndef func():\n    pass"
    file_path = tmp_path / "deps.py"
    file_path.write_text(content)
    analyzer = PythonAnalyzer(file_path)
    result = analyzer.analyze()
    assert "os" in result.dependencies
    assert "sys" in result.dependencies

def test_basic_analysis(tmp_path):
    """Test basic analysis of a Python file."""
    content = "def basic():\n    x = 1\n    return x"
    file_path = tmp_path / "basic.py"
    file_path.write_text(content)
    analyzer = PythonAnalyzer(file_path)
    result = analyzer.analyze()
    assert "basic" in result.functions
    assert result.functions["basic"].loc == 3
    assert result.functions["basic"].complexity == 1

def test_unused_imports(tmp_path):
    """Test detecting unused imports."""
    content = "import math\n\ndef func():\n    print('no math')"
    file_path = tmp_path / "unused.py"
    file_path.write_text(content)
    analyzer = PythonAnalyzer(file_path)
    result = analyzer.analyze()
    assert "math" in result.unused_imports

def test_malformed_file(tmp_path):
    """Test analyzing a malformed Python file."""
    content = "def func()\n    print('missing colon')"
    file_path = tmp_path / "malformed.py"
    file_path.write_text(content)
    analyzer = PythonAnalyzer(file_path)
    result = analyzer.analyze()
    assert len(result.functions) == 0