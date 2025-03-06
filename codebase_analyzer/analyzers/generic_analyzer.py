"""Analyzer for generic (non-Python) files, extracting basic metadata."""

from typing import Optional
from pathlib import Path
from ..models.data_classes import FileInfo
from ..utils.file_utils import safe_read_file
from .base_analyzer import BaseAnalyzer

class GenericAnalyzer(BaseAnalyzer):
    """Analyzes generic (non-Python) files to extract basic metadata."""

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    def get_file_type(self) -> str:
        """Return the type of file being analyzed.

        Returns:
            str: The file type based on extension (e.g., 'json', 'md', 'txt').
        """
        extension = self.file_path.suffix.lower().lstrip('.')
        return extension if extension else "unknown"

    def analyze(self) -> Optional[FileInfo]:
        """Analyze a generic file and return its metadata.

        Returns:
            Optional[FileInfo]: File information if successful, None otherwise.
        """
        content = safe_read_file(self.file_path)
        if content is None:
            return None

        return FileInfo(
            file_path=self.file_path,
            type=self.get_file_type(),
            size=len(content.encode('utf-8')),
            functions={},  # Empty dict for non-Python files
            classes={},    # Empty dict for non-Python files
            dependencies=set()  # No dependencies in non-Python files
        )