import pytest
from pathlib import Path
from codebase_analyzer.analyzer import CodebaseAnalyzer

@pytest.fixture
def temp_project(tmp_path):
    """Fixture to create a fresh temp project per test."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    yield project_dir

def test_analyze_project_simple(temp_project):
    """Test analyzing a simple project with one file."""
    files = {"main.py": "def main():\n    print('hello')"}
    project_dir = temp_project
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = CodebaseAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.total_files == 1
    assert result.total_lines == 2
    assert result.complexity.cyclomatic_complexity >= 1.0
    assert result.quality.lint_score > 0

def test_analyze_project_with_complexity(temp_project):
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
    project_dir = temp_project
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = CodebaseAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.total_files == 1
    assert result.total_lines == 6
    assert result.complexity.cyclomatic_complexity > 1.0

def test_analyze_project_with_vulnerabilities(temp_project):
    """Test analyzing a project with potential security issues."""
    files = {
        "vuln.py": """
def risky():
    eval('print(123)')  # Potential vulnerability
"""
    }
    project_dir = temp_project
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = CodebaseAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert len(result.security.vulnerabilities) > 0

def test_analyze_project_empty(temp_project):
    """Test analyzing an empty project directory."""
    project_dir = temp_project
    analyzer = CodebaseAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.total_files == 0
    assert result.total_lines == 0

def test_generate_summary_no_analysis():
    """Test generate_summary without prior analysis."""
    analyzer = CodebaseAnalyzer()
    summary = analyzer.generate_summary()
    assert "No analysis data available" in summary

def test_generate_summary_after_analysis(temp_project):
    """Test generate_summary after analyzing a simple project."""
    files = {"main.py": "def main():\n    print('hello')"}
    project_dir = temp_project
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = CodebaseAnalyzer()
    analyzer.analyze_project(project_dir)
    summary = analyzer.generate_summary()
    assert isinstance(summary, str)
    assert "CODEBASE ANALYSIS SUMMARY" in summary
    assert f"Total Python Files: {analyzer.project_metrics.total_files}" in summary
    assert "COMPLEXITY METRICS" in summary
    assert "QUALITY METRICS" in summary

def test_analyze_project_invalid_path():
    """Test analyzing an invalid project path."""
    analyzer = CodebaseAnalyzer()
    invalid_path = Path("/nonexistent/path")
    with pytest.raises(FileNotFoundError):
        analyzer.analyze_project(invalid_path)

def test_analyze_project_with_errors(temp_project, mocker):
    """Test analyzing a project with simulated analysis errors."""
    mocker.patch(
        'codebase_analyzer.metrics.complexity_analyzer.ComplexityAnalyzer.analyze_project',
        side_effect=Exception("Simulated complexity error")
    )
    files = {"main.py": "def main():\n    print('hello')"}
    project_dir = temp_project
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = CodebaseAnalyzer()
    result = analyzer.analyze_project(project_dir)
    summary = analyzer.generate_summary()
    assert "ANALYSIS ERRORS" in summary
    assert "Simulated complexity error" in summary
    assert result.complexity.cyclomatic_complexity == 0.0