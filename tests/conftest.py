# tests/conftest.py
import pytest
from pathlib import Path
import tempfile
import shutil
from tests.helpers import TestHelper

@pytest.fixture(scope="session")
def temp_dir():
    """Provide a session-scoped temporary directory."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture(scope="session")
def helper(temp_dir):
    """Provide a TestHelper instance with a session-scoped temp directory."""
    return TestHelper(temp_dir)

@pytest.fixture
def sample_codebase():
    """Creates a temporary sample codebase for testing."""
    temp_dir = tempfile.mkdtemp()
    sample_files = {
        'main.py': 'def main():\n    print("Hello")\n\nif __name__ == "__main__":\n    main()',
        'utils/helper.py': 'def helper():\n    return True',
        'tests/test_main.py': 'def test_main():\n    assert True'
    }

    for file_path, content in sample_files.items():
        full_path = Path(temp_dir) / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)

    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def analyzer():
    """Creates a CodebaseAnalyzer instance."""
    from codebase_analyzer.analyzer import CodebaseAnalyzer
    return CodebaseAnalyzer()