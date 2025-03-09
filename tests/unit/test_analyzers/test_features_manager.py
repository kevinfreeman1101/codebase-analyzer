# Project Path: codebase_analyzer/tests/unit/test_analyzers/test_features_manager.py
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from codebase_analyzer.features.manager import FeatureExtractorManager

@pytest.fixture
def manager():
    """Fixture for FeatureExtractorManager with mocked extractors."""
    with patch.object(FeatureExtractorManager, '__init__', lambda self: None):
        mgr = FeatureExtractorManager()
        mgr.extractors = {
            'complexity': Mock(),
            'quality': Mock(),
            'security': Mock(),
            'performance': Mock()
        }
        return mgr

def test_init():
    """Test FeatureExtractorManager initialization."""
    mgr = FeatureExtractorManager()
    assert set(mgr.extractors.keys()) == {'complexity', 'quality', 'security', 'performance'}

def test_extract_all_success(manager):
    """Test extract_all with successful extractor runs."""
    mock_result = {
        'complexity': {'complexity_score': 0.8},
        'quality': {'quality_score': 0.7},
        'security': {'security_score': 0.9},
        'performance': {'performance_score': 0.6}
    }
    for name, extractor in manager.extractors.items():
        extractor.extract.return_value = mock_result[name]
    result = manager.extract_all("dummy code", Path("test.py"))
    assert len(result['results']) == 4
    assert result['overall_score'] == pytest.approx(0.75, 0.01)  # (0.8 + 0.7 + 0.9 + 0.6) * 0.25
    assert result['metadata']['file_path'] == "test.py"
    assert not result['metadata']['errors']

def test_extract_all_with_errors(manager):
    """Test extract_all when an extractor fails."""
    mock_result = {
        'complexity': {'error': 'default'},
        'quality': {'quality_score': 0.7},
        'security': {'security_score': 0.9},
        'performance': {'performance_score': 0.6}
    }
    manager.extractors['complexity'].extract.side_effect = Exception("fail")
    manager.extractors['complexity']._get_default_metrics.return_value = mock_result['complexity']
    for name, extractor in manager.extractors.items():
        if name != 'complexity':
            extractor.extract.return_value = mock_result[name]
    result = manager.extract_all("dummy code")
    assert result['results']['complexity']['error'] == 'default'
    assert len(result['metadata']['errors']) == 1
    assert result['metadata']['errors'][0]['extractor'] == 'complexity'
    assert result['overall_score'] == pytest.approx(0.55, 0.01)  # (0 + 0.7 + 0.9 + 0.6) * 0.25

def test_calculate_overall_score(manager):
    """Test overall score calculation."""
    results = {
        'complexity': {'complexity_score': 0.8},
        'quality': {'quality_score': 0.7},
        'security': {'security_score': 0.9},
        'performance': {'performance_score': 0.6}
    }
    score = manager._calculate_overall_score(results)
    assert score == pytest.approx(0.75, 0.01)

def test_generate_summary(manager):
    """Test summary generation with all metrics."""
    results = {
        'complexity': {'complexity_score': 0.8, 'complexity_metrics': {'time_complexity': 'O(n)', 'recursive_functions': ['func']}},
        'quality': {'quality_score': 0.7, 'metrics': {'documentation_score': 0.5, 'maintainability_index': 60}},
        'security': {'security_score': 0.9, 'vulnerabilities': {'count': 1}, 'sensitive_data': {'exposure_count': 1}},
        'performance': {'performance_score': 0.6, 'bottlenecks': {'count': 2}, 'caching_opportunities': {'opportunities_count': 1}}
    }
    summary = manager._generate_summary(results, 0.75)
    assert summary['overall_score'] == 0.75
    assert len(summary['key_metrics']['complexity']['highlights']) == 2
    assert len(summary['key_metrics']['security']['highlights']) == 2

def test_generate_recommendations(manager):
    """Test recommendation generation."""
    results = {
        'complexity': {'complexity_metrics': {'time_complexity': 'O(n^2)', 'recursive_functions': ['func']}},
        'quality': {'metrics': {'documentation_score': 0.5, 'maintainability_index': 60}},
        'security': {'vulnerabilities': {'severity_distribution': {'critical': 1}, 'count': 1}, 'sensitive_data': {'exposure_count': 1}},
        'performance': {'bottlenecks': {'count': 2}, 'caching_opportunities': {'opportunities_count': 1}}
    }
    recs = manager._generate_recommendations(results)
    assert any(r['priority'] == 'critical' for r in recs)
    assert len(recs) >= 7

def test_export_results_json(manager):
    """Test JSON export."""
    results = {'overall_score': 0.8}
    output = manager.export_results(results, 'json')
    assert '"overall_score": 0.8' in output

def test_export_results_html(manager):
    """Test HTML export with full report."""
    results = {
        'overall_score': 0.8,
        'metadata': {'timestamp': '2025-03-08T00:00:00', 'errors': [], 'analyzers_used': ['complexity']},
        'summary': {'key_metrics': {'complexity': {'score': 0.8, 'highlights': ['O(n)']}}},
        'results': {'complexity': {'complexity_score': 0.8}},
        'recommendations': [{'priority': 'high', 'title': 'Test', 'description': 'Desc', 'suggestion': 'Fix', 'category': 'complexity'}]
    }
    output = manager.export_results(results, 'html')
    assert '<title>Code Analysis Report</title>' in output
    assert '0.80' in output
    assert 'Test' in output

def test_export_results_invalid_format(manager):
    """Test invalid export format."""
    with pytest.raises(ValueError, match="Unsupported export format: invalid"):
        manager.export_results({}, 'invalid')

def test_export_results_to_file(manager, tmp_path):
    """Test export to file."""
    results = {'overall_score': 0.8}
    file_path = tmp_path / "output.json"
    manager.export_results(results, 'json', file_path)
    assert file_path.read_text() == '{"overall_score": 0.8}'