from abc import ABC, abstractmethod
from typing import Dict, Set, Optional
from ..models.data_classes import FileInfo

class BaseAnalyzer(ABC):
    """Base class for file analyzers."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.dependencies: Set[str] = set()

    @abstractmethod
    def analyze(self) -> Optional[FileInfo]:
        """
        Analyze the file and return FileInfo object.

        Returns:
            FileInfo object or None if analysis fails
        """
        pass

    @abstractmethod
    def get_file_type(self) -> str:
        """
        Get the type of file this analyzer handles.

        Returns:
            String representing the file type
        """
        pass