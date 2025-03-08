import pytest
from pathlib import Path
from codebase_analyzer.analyzers.project_analyzer import ProjectAnalyzer

@pytest.fixture
def analyzer(tmp_path, mocker):
    """Fixture to provide a ProjectAnalyzer instance with root_path and mocked subprocess."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    mocker.patch(
        'subprocess.run',
        side_effect=[
            mocker.Mock(returncode=1, stdout="", stderr="Safety check failed"),
            mocker.Mock(returncode=1, stdout="", stderr="Pip outdated check failed"),
        ]
    )
    return ProjectAnalyzer(root_path=project_dir)

def test_project_analyzer_empty_directory(analyzer):
    """Test analyzing an empty project directory."""
    result = analyzer.analyze()
    assert isinstance(result, str)
    assert "File Distribution:\n" in result

def test_project_analyzer_with_files(analyzer):
    """Test analyzing a project with simple files."""
    files = {
        "main.py": "def main():\n    print('hello')",
        "utils.py": "def util():\n    return 42"
    }
    for fname, content in files.items():
        (analyzer.root_path / fname).write_text(content)
    result = analyzer.analyze()
    assert "File Distribution:\n- Python Files: 2 files" in result
    assert "Total Files: 2" in result

def test_project_analyzer_with_complex_structure(analyzer):
    """Test analyzing a project with nested structure."""
    files = {
        "src/main.py": "def main():\n    print('hello')",
        "src/utils/helper.py": "def helper():\n    return True",
        "tests/test_main.py": "def test_main():\n    assert True"
    }
    for fname, content in files.items():
        file_path = analyzer.root_path / fname
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    result = analyzer.analyze()
    assert "File Distribution:\n- Python Files: 3 files" in result
    assert "Total Files: 3" in result

def test_project_analyzer_with_non_python_files(analyzer):
    """Test analyzing a project with non-Python files."""
    files = {
        "main.py": "def main():\n    print('hello')",
        "README.md": "# Project\nDescription here",
        "requirements.txt": "requests==2.28.1"
    }
    for fname, content in files.items():
        (analyzer.root_path / fname).write_text(content)
    result = analyzer.analyze()
    assert "File Distribution:\n- Python Files: 1 files" in result
    assert "Total Files: 3" in result

def test_analyze_empty_project(analyzer):
    """Test analyzing an empty project (redundant but kept)."""
    result = analyzer.analyze()
    assert "File Distribution:\n" in result

def test_analyze_simple_project(analyzer):
    """Test analyzing a simple project."""
    files = {"app.py": "def run():\n    print('Running')"}
    for fname, content in files.items():
        (analyzer.root_path / fname).write_text(content)
    result = analyzer.analyze()
    assert "File Distribution:\n- Python Files: 1 files" in result
    assert "Total Files: 1" in result