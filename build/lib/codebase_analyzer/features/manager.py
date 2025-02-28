# codebase_analyzer/features/manager.py
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
import concurrent.futures
from datetime import datetime
import json

from .base import FeatureExtractor
from .complexity import ComplexityFeatureExtractor
from .quality import QualityFeatureExtractor
from .security import SecurityFeatureExtractor
from .performance import PerformanceFeatureExtractor

class FeatureExtractorManager:
    """Coordinates multiple feature extractors and aggregates their results."""

    def __init__(self):
        self.extractors: Dict[str, FeatureExtractor] = {
            'complexity': ComplexityFeatureExtractor(),
            'quality': QualityFeatureExtractor(),
            'security': SecurityFeatureExtractor(),
            'performance': PerformanceFeatureExtractor()
        }
        
    def extract_all(self, code: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Extracts all features from the given code using all registered extractors.
        
        Args:
            code: The source code to analyze
            file_path: Optional path to the source file
            
        Returns:
            Dictionary containing all extracted features and metadata
        """
        results = {}
        errors = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_extractor = {
                executor.submit(self._extract_safely, name, extractor, code, file_path): name
                for name, extractor in self.extractors.items()
            }

            for future in concurrent.futures.as_completed(future_to_extractor):
                extractor_name = future_to_extractor[future]
                try:
                    result = future.result()
                    results[extractor_name] = result
                except Exception as e:
                    errors.append({
                        'extractor': extractor_name,
                        'error': str(e)
                    })
                    results[extractor_name] = self._get_default_metrics(extractor_name)

        return self._create_analysis_report(results, errors, file_path)

    def _extract_safely(self, name: str, extractor: FeatureExtractor, 
                       code: str, file_path: Optional[Path]) -> Dict[str, Any]:
        """Safely extracts features using the given extractor with error handling."""
        try:
            return extractor.extract(code, file_path)
        except Exception as e:
            raise Exception(f"Error in {name} extractor: {str(e)}")

    def _get_default_metrics(self, extractor_name: str) -> Dict[str, Any]:
        """Returns default metrics for a given extractor when analysis fails."""
        try:
            return self.extractors[extractor_name]._get_default_metrics()
        except Exception:
            return {'error': 'Failed to get default metrics'}

    def _create_analysis_report(self, results: Dict[str, Any], 
                              errors: List[Dict[str, str]], 
                              file_path: Optional[Path]) -> Dict[str, Any]:
        """Creates a comprehensive analysis report with all results and metadata."""
        overall_score = self._calculate_overall_score(results)
        
        return {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'file_path': str(file_path) if file_path else None,
                'analyzers_used': list(self.extractors.keys()),
                'errors': errors
            },
            'overall_score': overall_score,
            'summary': self._generate_summary(results, overall_score),
            'results': results,
            'recommendations': self._generate_recommendations(results)
        }

    def _calculate_overall_score(self, results: Dict[str, Any]) -> float:
        """Calculates the overall code quality score from all metrics."""
        weights = {
            'complexity': 0.25,
            'quality': 0.25,
            'security': 0.25,
            'performance': 0.25
        }

        scores = {
            name: results[name].get(f'{name}_score', 0.0)
            for name in weights.keys()
        }

        return sum(scores[k] * weights[k] for k in weights)

    def _generate_summary(self, results: Dict[str, Any], 
                         overall_score: float) -> Dict[str, Any]:
        """Generates a high-level summary of the analysis results."""
        return {
            'overall_score': overall_score,
            'key_metrics': {
                'complexity': {
                    'score': results['complexity'].get('complexity_score', 0.0),
                    'highlights': self._get_complexity_highlights(results['complexity'])
                },
                'quality': {
                    'score': results['quality'].get('quality_score', 0.0),
                    'highlights': self._get_quality_highlights(results['quality'])
                },
                'security': {
                    'score': results['security'].get('security_score', 0.0),
                    'highlights': self._get_security_highlights(results['security'])
                },
                'performance': {
                    'score': results['performance'].get('performance_score', 0.0),
                    'highlights': self._get_performance_highlights(results['performance'])
                }
            }
        }

    def _get_complexity_highlights(self, results: Dict[str, Any]) -> List[str]:
        """Extracts key complexity insights from results."""
        highlights = []
        if 'complexity_metrics' in results:
            metrics = results['complexity_metrics']
            if metrics.get('time_complexity', 'O(1)') != 'O(1)':
                highlights.append(f"Time complexity: {metrics['time_complexity']}")
            if metrics.get('recursive_functions'):
                highlights.append(f"Found {len(metrics['recursive_functions'])} recursive functions")
        return highlights

    def _get_quality_highlights(self, results: Dict[str, Any]) -> List[str]:
        """Extracts key quality insights from results."""
        highlights = []
        if 'metrics' in results:
            metrics = results['metrics']
            if 'documentation_score' in metrics:
                highlights.append(f"Documentation coverage: {metrics['documentation_score']*100:.1f}%")
            if 'maintainability_index' in metrics:
                highlights.append(f"Maintainability index: {metrics['maintainability_index']:.1f}")
        return highlights

    def _get_security_highlights(self, results: Dict[str, Any]) -> List[str]:
        """Extracts key security insights from results."""
        highlights = []
        if 'vulnerabilities' in results:
            vuln = results['vulnerabilities']
            if vuln['count'] > 0:
                highlights.append(f"Found {vuln['count']} potential security issues")
        if 'sensitive_data' in results:
            sensitive = results['sensitive_data']
            if sensitive['exposure_count'] > 0:
                highlights.append(f"Found {sensitive['exposure_count']} sensitive data exposures")
        return highlights

    def _get_performance_highlights(self, results: Dict[str, Any]) -> List[str]:
        """Extracts key performance insights from results."""
        highlights = []
        if 'bottlenecks' in results:
            bottlenecks = results['bottlenecks']
            if bottlenecks['count'] > 0:
                highlights.append(f"Found {bottlenecks['count']} performance bottlenecks")
        if 'caching_opportunities' in results:
            caching = results['caching_opportunities']
            if caching['opportunities_count'] > 0:
                highlights.append(f"Found {caching['opportunities_count']} caching opportunities")
        return highlights

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates prioritized recommendations based on analysis results."""
        recommendations = []
        
        # Add recommendations from each analyzer
        for analyzer_name, analyzer_results in results.items():
            if analyzer_name == 'complexity':
                recommendations.extend(self._get_complexity_recommendations(analyzer_results))
            elif analyzer_name == 'quality':
                recommendations.extend(self._get_quality_recommendations(analyzer_results))
            elif analyzer_name == 'security':
                recommendations.extend(self._get_security_recommendations(analyzer_results))
            elif analyzer_name == 'performance':
                recommendations.extend(self._get_performance_recommendations(analyzer_results))

        # Sort recommendations by priority
        recommendations.sort(key=lambda x: {
            'critical': 0,
            'high': 1,
            'medium': 2,
            'low': 3
        }[x['priority']])

        return recommendations

    def _get_complexity_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates recommendations for complexity issues."""
        recommendations = []
        
        if 'complexity_metrics' in results:
            metrics = results['complexity_metrics']
            
            # Check for high complexity
            if 'O(n^' in metrics.get('time_complexity', ''):
                recommendations.append({
                    'category': 'complexity',
                    'priority': 'high',
                    'title': 'High Time Complexity Detected',
                    'description': f"Found code with {metrics['time_complexity']} complexity",
                    'suggestion': 'Consider optimizing algorithms or using more efficient data structures'
                })

            # Check for recursive functions
            if metrics.get('recursive_functions'):
                recommendations.append({
                    'category': 'complexity',
                    'priority': 'medium',
                    'title': 'Recursive Functions Found',
                    'description': f"Found {len(metrics['recursive_functions'])} recursive functions",
                    'suggestion': 'Evaluate if iteration could be more efficient'
                })

        return recommendations

    def _get_quality_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates recommendations for code quality issues."""
        recommendations = []
        
        if 'metrics' in results:
            metrics = results['metrics']
            
            # Check documentation coverage
            doc_score = metrics.get('documentation_score', 0)
            if doc_score < 0.7:
                recommendations.append({
                    'category': 'quality',
                    'priority': 'medium',
                    'title': 'Low Documentation Coverage',
                    'description': f"Documentation coverage is {doc_score*100:.1f}%",
                    'suggestion': 'Add docstrings and comments to improve code clarity'
                })

            # Check maintainability
            maint_index = metrics.get('maintainability_index', 0)
            if maint_index < 65:
                recommendations.append({
                    'category': 'quality',
                    'priority': 'high',
                    'title': 'Low Maintainability Score',
                    'description': f"Maintainability index is {maint_index:.1f}",
                    'suggestion': 'Refactor complex functions and improve code organization'
                })

        return recommendations

    def _get_security_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates recommendations for security issues."""
        recommendations = []
        
        if 'vulnerabilities' in results:
            vulns = results['vulnerabilities']
            
            # Check for critical vulnerabilities
            if vulns['severity_distribution'].get('critical', 0) > 0:
                recommendations.append({
                    'category': 'security',
                    'priority': 'critical',
                    'title': 'Critical Security Vulnerabilities',
                    'description': f"Found {vulns['severity_distribution']['critical']} critical vulnerabilities",
                    'suggestion': 'Immediately address critical security issues'
                })

            # Check for sensitive data exposure
            if results.get('sensitive_data', {}).get('exposure_count', 0) > 0:
                recommendations.append({
                    'category': 'security',
                    'priority': 'high',
                    'title': 'Sensitive Data Exposure',
                    'description': 'Found potential sensitive data exposure',
                    'suggestion': 'Review and secure sensitive data handling'
                })

        return recommendations

    def _get_performance_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates recommendations for performance issues."""
        recommendations = []
        
        if 'bottlenecks' in results:
            bottlenecks = results['bottlenecks']
            
            # Check for performance bottlenecks
            if bottlenecks['count'] > 0:
                recommendations.append({
                    'category': 'performance',
                    'priority': 'high',
                    'title': 'Performance Bottlenecks Detected',
                    'description': f"Found {bottlenecks['count']} performance bottlenecks",
                    'suggestion': 'Optimize identified bottlenecks'
                })

            # Check for caching opportunities
            if results.get('caching_opportunities', {}).get('opportunities_count', 0) > 0:
                recommendations.append({
                    'category': 'performance',
                    'priority': 'medium',
                    'title': 'Caching Opportunities',
                    'description': 'Found opportunities for implementing caching',
                    'suggestion': 'Implement caching for frequently accessed data'
                })

        return recommendations

    def export_results(self, results: Dict[str, Any], 
                      format: str = 'json', 
                      output_path: Optional[Path] = None) -> Optional[str]:
        """
        Exports analysis results in the specified format.
        
        Args:
            results: Analysis results to export
            format: Output format ('json' or 'html')
            output_path: Optional path to save the output
            
        Returns:
            Exported content as string if no output_path is provided
        """
        if format == 'json':
            content = json.dumps(results, indent=2)
        elif format == 'html':
            content = self._generate_html_report(results)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        if output_path:
            output_path = Path(output_path)
            output_path.write_text(content)
            return None
        
        return content

    def _generate_html_report(self, results: Dict[str, Any]) -> str:
        """Generates an HTML report from analysis results."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Code Analysis Report</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .score {{ 
                    font-size: 24px; 
                    font-weight: bold;
                    padding: 20px;
                    background: #f5f5f5;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .section {{ 
                    margin: 30px 0;
                    padding: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .recommendation {{ 
                    border-left: 4px solid #ccc; 
                    padding: 15px;
                    margin: 15px 0;
                    background: #f9f9f9;
                }}
                .critical {{ border-color: #ff0000; background: #fff5f5; }}
                .high {{ border-color: #ff9900; background: #fff9f0; }}
                .medium {{ border-color: #ffcc00; background: #fffbf0; }}
                .low {{ border-color: #99cc00; background: #f5fff0; }}
                .metric-card {{
                    display: inline-block;
                    width: calc(50% - 40px);
                    margin: 10px;
                    padding: 15px;
                    background: #f5f5f5;
                    border-radius: 6px;
                }}
                .highlight {{
                    padding: 10px;
                    margin: 5px 0;
                    background: #e9ecef;
                    border-radius: 4px;
                }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .timestamp {{
                    color: #666;
                    font-size: 0.9em;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Code Analysis Report</h1>
                <div class="timestamp">
                    Generated on: {results['metadata']['timestamp']}
                </div>

                {self._generate_score_section(results)}
                {self._generate_metrics_section(results)}
                {self._generate_recommendations_section(results)}
                {self._generate_details_section(results)}

                <div class="section">
                    <h2>Analysis Metadata</h2>
                    {self._generate_metadata_section(results['metadata'])}
                </div>
            </div>
        </body>
        </html>
        """

    def _generate_score_section(self, results: Dict[str, Any]) -> str:
        """Generates the overall score section of the HTML report."""
        return f"""
        <div class="score">
            Overall Code Quality Score: {results['overall_score']:.2f} / 1.00
        </div>
        """

    def _generate_metrics_section(self, results: Dict[str, Any]) -> str:
        """Generates the metrics section of the HTML report."""
        metrics = results['summary']['key_metrics']

        metrics_html = ""
        for category, data in metrics.items():
            highlights = "\n".join([
                f'<div class="highlight">{highlight}</div>'
                for highlight in data['highlights']
            ])

            metrics_html += f"""
            <div class="metric-card">
                <h3>{category.title()}</h3>
                <p>Score: {data['score']:.2f}</p>
                {highlights}
            </div>
            """

        return f"""
        <div class="section">
            <h2>Key Metrics</h2>
            {metrics_html}
        </div>
        """

    def _generate_recommendations_section(self, results: Dict[str, Any]) -> str:
        """Generates the recommendations section of the HTML report."""
        recommendations_html = ""
        for rec in results['recommendations']:
            recommendations_html += f"""
            <div class="recommendation {rec['priority']}">
                <h3>{rec['title']}</h3>
                <p><strong>Priority:</strong> {rec['priority'].title()}</p>
                <p><strong>Category:</strong> {rec['category'].title()}</p>
                <p><strong>Description:</strong> {rec['description']}</p>
                <p><strong>Suggestion:</strong> {rec['suggestion']}</p>
            </div>
            """

        return f"""
        <div class="section">
            <h2>Recommendations</h2>
            {recommendations_html}
        </div>
        """

    def _generate_details_section(self, results: Dict[str, Any]) -> str:
        """Generates the detailed results section of the HTML report."""
        details_html = ""
        for analyzer, data in results['results'].items():
            # Filter out internal keys and complex objects
            filtered_data = {
                k: v for k, v in data.items()
                if isinstance(v, (str, int, float, bool)) or 
                (isinstance(v, dict) and not k.startswith('_'))
            }

            details_html += f"""
            <div class="section">
                <h3>{analyzer.title()} Analysis Details</h3>
                <pre>{json.dumps(filtered_data, indent=2)}</pre>
            </div>
            """

        return f"""
        <div class="section">
            <h2>Detailed Analysis Results</h2>
            {details_html}
        </div>
        """

    def _generate_metadata_section(self, metadata: Dict[str, Any]) -> str:
        """Generates the metadata section of the HTML report."""
        error_html = ""
        if metadata['errors']:
            error_html = "<h3>Errors</h3><ul>" + "".join([
                f"<li>{error['extractor']}: {error['error']}</li>"
                for error in metadata['errors']
            ]) + "</ul>"

        return f"""
        <p><strong>File analyzed:</strong> {metadata['file_path'] or 'Unknown'}</p>
        <p><strong>Analyzers used:</strong> {', '.join(metadata['analyzers_used'])}</p>
        {error_html}
        """