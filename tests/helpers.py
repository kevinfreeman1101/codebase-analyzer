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
