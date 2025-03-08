import pytest
from pathlib import Path
from codebase_analyzer.metrics.dependency_metrics import DependencyAnalyzer

def test_basic_dependencies(tmp_path):
    """Test analyzing basic dependencies in a project."""
    files = {"requirements.txt": "requests==2.28.1\nnumpy==1.23.5"}
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    analyzer = DependencyAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert len(result.direct_dependencies) == 2
    assert "requests" in result.direct_dependencies
    assert "numpy" in result.direct_dependencies

def test_vulnerable_dependencies(tmp_path, mocker):
    """Test detecting vulnerable dependencies."""
    files = {"requirements.txt": "requests==2.28.1\ncryptography==36.0.0"}
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for fname, content in files.items():
        (project_dir / fname).write_text(content)
    mocker.patch(
        'subprocess.run',
        return_value=mocker.Mock(returncode=0, stdout='{"vulnerabilities": [{"package": "cryptography", "installed_version": "36.0.0", "advisory": "CVE-2021-12345", "severity": "HIGH"}]}')
    )
    analyzer = DependencyAnalyzer()
    result = analyzer.analyze_project(project_dir)
    assert "cryptography" in [v["name"] for v in result.vulnerable_dependencies]