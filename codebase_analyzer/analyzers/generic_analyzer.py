# /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/analyzers/generic_analyzer.py
from typing import Optional
from .base_analyzer import BaseAnalyzer
from ..models.data_classes import FileInfo
from ..utils.file_utils import safe_read_file  # Updated import

class GenericAnalyzer(BaseAnalyzer):
    """Analyzer for non-Python files."""

    def __init__(self, file_path: str, file_type: str):
        super().__init__(file_path)
        self._file_type = file_type

    def get_file_type(self) -> str:
        return self._file_type

    def analyze(self) -> Optional[FileInfo]:
        try:
            content = safe_read_file(self.file_path)
        except IOError as e:
            print(f"Skipping file due to error: {self.file_path} - {e}")
            return None
        
        if content is None:
            return None

        return FileInfo(
            path=self.file_path,
            type=self.get_file_type(),
            content=content,
            size=len(content),
            dependencies=self.dependencies
        )