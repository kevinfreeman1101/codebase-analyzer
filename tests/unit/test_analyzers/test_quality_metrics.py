import pytest
from pathlib import Path
from codebase_analyzer.metrics.quality_metrics import QualityAnalyzer

def test_empty_file(tmp_path):
    """Test quality analysis of a project with an empty file."""
    files = {"empty.py": ""}
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = QualityAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.test_coverage == 0.0

def test_simple_function_with_test(tmp_path, mocker):
    """Test quality analysis of a project with a function and test."""
    files = {
        "app.py": "def simple():\n    return 42",
        "tests/test_app.py": "from app import simple\ndef test_simple():\n    assert simple() == 42"
    }
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for fname, content in files.items():
        file_path = project_dir / fname
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    mocker.patch(
        'subprocess.run',
        side_effect=[
            mocker.Mock(returncode=0, stdout=""),
            mocker.Mock(returncode=0, stdout="Name Stmts Miss Cover\nTOTAL 2 0 100%")
        ]
    )
    analyzer = QualityAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.test_coverage == 100.0

def test_project_with_tests(tmp_path, mocker):
    """Test quality analysis of a project with tests."""
    files = {
        "main.py": "def main():\n    print('hello')",
        "tests/test_main.py": "from main import main\ndef test_main():\n    assert True"
    }
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for fname, content in files.items():
        file_path = project_dir / fname
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    mocker.patch(
        'subprocess.run',
        side_effect=[
            mocker.Mock(returncode=0, stdout=""),
            mocker.Mock(returncode=0, stdout="Name Stmts Miss Cover\nTOTAL 2 0 100%")
        ]
    )
    analyzer = QualityAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.test_coverage == 100.0

def test_mixed_functions(tmp_path, mocker):
    """Test quality analysis of a project with mixed coverage."""
    files = {
        "utils.py": "def covered():\n    return 1\ndef uncovered():\n    pass",
        "tests/test_utils.py": "from utils import covered\ndef test_covered():\n    assert covered() == 1"
    }
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for fname, content in files.items():
        file_path = project_dir / fname
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    mocker.patch(
        'subprocess.run',
        side_effect=[
            mocker.Mock(returncode=0, stdout=""),
            mocker.Mock(returncode=0, stdout="Name Stmts Miss Cover\nTOTAL 4 2 50%")
        ]
    )
    analyzer = QualityAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.test_coverage == 50.0

def test_project_with_no_tests(tmp_path):
    """Test quality analysis of a project with no tests."""
    files = {"app.py": "def func():\n    return 'no tests'"}
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = QualityAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert result.test_coverage == 0.0