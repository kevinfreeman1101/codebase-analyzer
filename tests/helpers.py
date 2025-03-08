"""Helper utilities for unit tests."""

import shutil
from pathlib import Path
import tempfile

class TestHelper:
    """Helper class for creating temporary test environments."""

    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir

    def create_temp_file(self, content: str) -> Path:
        """Create a temporary file with given content."""
        fd, path = tempfile.mkstemp(dir=str(self.temp_dir), suffix=".py")
        with open(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        return Path(path)

    def create_temp_project(self, files: dict) -> Path:
        """Create a temporary project directory with given files."""
        project_dir = self.temp_dir / "project"
        project_dir.mkdir(exist_ok=True)
        for rel_path, content in files.items():
            file_path = project_dir / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return project_dir

    def cleanup_temp(self):
        """No-op since cleanup is handled by the fixture."""
        pass