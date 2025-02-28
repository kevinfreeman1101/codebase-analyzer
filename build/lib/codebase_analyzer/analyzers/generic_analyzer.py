from typing import Optional, Dict
from pathlib import Path
from .base_analyzer import BaseAnalyzer
from ..utils.file_utils import safe_read_file, get_file_type
from ..models.data_classes import FileInfo

class GenericAnalyzer(BaseAnalyzer):
    """Analyzer for generic non-Python files."""

    def get_file_type(self) -> str:
        """Determine the file type based on its extension or content."""
        return get_file_type(self.file_path)

    def analyze(self) -> Optional[FileInfo]:
        """Analyze a generic file and return its metadata.

        Returns:
            Optional[FileInfo]: File information if successful, None otherwise.
        """
        content = safe_read_file(self.file_path)
        if content is None:
            return None

        return FileInfo(
            path=Path(self.file_path),
            type=self.get_file_type(),
            content=content,
            size=len(content.encode('utf-8')),
            dependencies=self.dependencies,
            functions={},  # Empty dict for non-Python files
            classes={}     # Empty dict for non-Python files
        )