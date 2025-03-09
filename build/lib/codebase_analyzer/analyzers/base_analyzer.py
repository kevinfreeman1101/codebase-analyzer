"""Base class for file analyzers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ..models.data_classes import FileInfo

class BaseAnalyzer(ABC):
    """Abstract base class for file analyzers."""

    def __init__(self, file_path: Path) -> None:
        """Initialize the analyzer with a file path.

        Args:
            file_path: Path to the file to analyze.
        """
        self.file_path = file_path

    @abstractmethod
    def analyze(self) -> Optional[FileInfo]:
        """Analyze the file and return structured information.

        Returns:
            Optional[FileInfo]: File information if successful, None otherwise.
        """
        pass

    @abstractmethod
    def get_file_type(self) -> str:
        """Return the type of file being analyzed.

        Returns:
            str: The file type (e.g., 'python', 'json', etc.).
        """
        pass