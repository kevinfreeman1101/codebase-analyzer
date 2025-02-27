# codebase_analyzer/features/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass

@dataclass
class CodeFeatures:
    """Container for extracted code features."""
    complexity_metrics: Dict[str, float]
    quality_metrics: Dict[str, float]
    pattern_metrics: Dict[str, Any]
    security_metrics: Dict[str, float]
    performance_metrics: Dict[str, float]
    dependency_metrics: Dict[str, Any]
    test_metrics: Dict[str, float]
    documentation_metrics: Dict[str, float]

class FeatureExtractor(ABC):
    """Base class for all feature extractors."""

    @abstractmethod
    def extract(self, code: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        """Extract features from code."""
        pass

    @abstractmethod
    def get_feature_names(self) -> List[str]:
        """Get list of features this extractor provides."""
        pass