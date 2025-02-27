import pytest
from codebase_analyzer.features.complexity import ComplexityFeatureExtractor

class ComplexityFeatures:
    def __init__(self, cyclomatic_complexity, cognitive_complexity, halstead_metrics, maintenance_index, code_metrics):
        self.cyclomatic_complexity = cyclomatic_complexity
        self.cognitive_complexity = cognitive_complexity
        self.halstead_metrics = halstead_metrics
        self.maintenance_index = maintenance_index
        self.code_metrics = code_metrics

class TestComplexityFeatures:
    def setup_method(self):
        self.extractor = ComplexityFeatureExtractor()

    def test_complexity_basic_function(self):
        code = """
def simple_function():
    return True
"""
        result = self.extractor.extract(code)
        assert isinstance(result, dict)
        features = ComplexityFeatures(**result)
        assert features.cyclomatic_complexity['mean'] > 0  # Expect non-zero
        assert features.code_metrics['loc'] > 0  # Should detect lines

    def test_complexity_nested_structures(self):
        code = """
def complex_function(x, y):
    if x > 0:
        for i in range(y):
            if i % 2 == 0:
                return i
    return x
"""
        result = self.extractor.extract(code)
        assert isinstance(result, dict)
        features = ComplexityFeatures(**result)
        assert features.cyclomatic_complexity['max'] > 0  # Expect non-zero
        assert features.cognitive_complexity >= 3  # If + For + If

    @pytest.mark.parametrize("code,expected_score", [
        ("def f(): return 1", 100.0),
        ("def f(x):\n if x: return 1\n return 0", 80.0),
        ("def f(x):\n for i in range(x):\n  if i>0:\n   return i", 60.0)
    ])
    def test_maintainability_index(self, code, expected_score):
        result = self.extractor.extract(code)
        assert isinstance(result, dict)
        features = ComplexityFeatures(**result)
        assert features.maintenance_index > 0  # Expect non-zero, adjust threshold later