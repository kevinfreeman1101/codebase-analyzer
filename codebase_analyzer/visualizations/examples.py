# codebase_analyzer/visualizations/examples.py
from pathlib import Path
from typing import Dict, Any

def generate_visualization_report(metrics: Dict[str, Any], output_dir: str = 'analysis_output') -> Path:
    """
    Example usage of the MetricVisualizer class.

    Args:
        metrics: Dictionary containing all analysis metrics
        output_dir: Directory to store visualization outputs

    Returns:
        Path to the generated HTML report
    """
    # Initialize visualizer
    visualizer = MetricVisualizer(Path(output_dir))

    # Generate all visualizations
    generated_files = visualizer.generate_visualizations(metrics)

    # Generate and return HTML report
    report_path = visualizer.generate_html_report()

    print(f"Generated {len(generated_files)} visualizations:")
    for file in generated_files:
        print(f"- {file.name}")

    return report_path

# Integration with main analyzer
class CodebaseAnalyzer:
    def __init__(self):
        self.visualizer = MetricVisualizer(Path('analysis_output'))

    def analyze_project(self, project_path: Path, generate_visuals: bool = True) -> Dict[str, Any]:
        """
        Analyze project and optionally generate visualizations.

        Args:
            project_path: Path to the project to analyze
            generate_visuals: Whether to generate visualization reports

        Returns:
            Dictionary containing analysis results and paths to generated files
        """
        # Perform analysis (existing code)
        metrics = self._analyze_metrics(project_path)

        # Generate visualizations if requested
        if generate_visuals:
            visualization_paths = self.visualizer.generate_visualizations(metrics)
            report_path = self.visualizer.generate_html_report()

            metrics['visualization_results'] = {
                'report_path': report_path,
                'visualization_files': visualization_paths
            }

        return metrics

# Command-line interface integration
def main():
    """Command-line interface for running analysis with visualizations."""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze codebase and generate visualizations')
    parser.add_argument('project_path', type=str, help='Path to the project to analyze')
    parser.add_argument('--output-dir', type=str, default='analysis_output',
                       help='Directory to store analysis results and visualizations')
    parser.add_argument('--no-visuals', action='store_true',
                       help='Skip generation of visualizations')

    args = parser.parse_args()

    analyzer = CodebaseAnalyzer()
    results = analyzer.analyze_project(
        Path(args.project_path),
        generate_visuals=not args.no_visuals
    )

    if not args.no_visuals:
        print(f"\nAnalysis complete! View the report at: "
              f"{results['visualization_results']['report_path']}")

    return 0

if __name__ == '__main__':
    exit(main())