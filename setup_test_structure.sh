#!/bin/bash
# setup_test_structure.sh

# Create test directory structure
mkdir -p tests/unit/test_analyzers
mkdir -p tests/integration

# Create __init__.py files
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/unit/test_analyzers/__init__.py
touch tests/integration/__init__.py

# Create test configuration files
echo "pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1
pytest-benchmark>=4.0.0
black>=23.7.0
flake8>=6.1.0
mypy>=1.4.1" > requirements-dev.txt

# Create pytest.ini
echo "[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=codebase_analyzer --cov-report=term-missing

filterwarnings =
    ignore::DeprecationWarning
    ignore::UserWarning" > tests/pytest.ini

# Create initial test files
cat > tests/helpers.py << 'EOL'
from pathlib import Path
import tempfile
import shutil

class TestHelper:
    @staticmethod
    def create_temp_file(content: str, suffix: str = '.py') -> Path:
        """Create a temporary file with given content."""
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp.write(content.encode('utf-8'))
        temp.close()
        return Path(temp.name)
    
    @staticmethod
    def create_temp_project(files: dict[str, str]) -> Path:
        """Create a temporary project directory with specified files."""
        temp_dir = Path(tempfile.mkdtemp())
        for file_path, content in files.items():
            full_path = temp_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
        return temp_dir
    
    @staticmethod
    def cleanup_temp(path: Path):
        """Clean up temporary files/directories."""
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
EOL

# Make the script executable
chmod +x setup_test_structure.sh