import tempfile
import shutil
from typing import Dict
from pathlib import Path

class TestHelper:
    """Helper class for creating temporary test files and directories."""

    def __init__(self):
        self.temp_dir = None

    def create_temp_file(self, content: str) -> str:
        """Create a temporary file with given content."""
        if not self.temp_dir:
            self.temp_dir = tempfile.mkdtemp()
        temp_file = tempfile.NamedTemporaryFile(dir=self.temp_dir, delete=False)
        temp_file.write(content.encode('utf-8'))
        temp_file.close()
        return temp_file.name

    def create_temp_project(self, files: Dict[str, str]) -> Path:
        """Create a temporary project directory with specified files."""
        if not self.temp_dir:
            self.temp_dir = tempfile.mkdtemp()
        temp_dir_path = Path(self.temp_dir)
        
        for file_path, content in files.items():
            full_path = temp_dir_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
        
        return temp_dir_path

    def cleanup_temp(self):
        """Clean up temporary files and directories."""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir = None