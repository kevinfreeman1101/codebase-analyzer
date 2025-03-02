"""Analyzer for generic (non-Python) files to extract basic metadata."""

from typing import Optional, Set
from pathlib import Path
from .base_analyzer import BaseAnalyzer
from ..models.data_classes import FileInfo
from ..utils.file_utils import safe_read_file

class GenericAnalyzer(BaseAnalyzer):
    """Analyzes generic files that are not Python source code."""

    def get_file_type(self) -> str:
        """Determine the file type based on extension."""
        ext = self.file_path.suffix.lower().lstrip('.')
        if ext in ['md', 'rst', 'txt']:
            return 'documentation'
        elif ext in ['json', 'yaml', 'yml', 'ini', 'cfg']:
            return 'configuration'
        return 'text'

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
            classes={},    # Empty dict for non-Python files
            unused_imports=set()  # No imports in non-Python files
        )