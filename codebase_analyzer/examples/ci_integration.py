# examples/ci_integration.py

from pathlib import Path
from typing import Dict, Any
from codebase_analyzer.features.manager import FeatureExtractorManager

def check_analysis_results(results: Dict[str, Any]) -> bool:
    """
    Checks if analysis results meet quality thresholds.
    Returns True if all checks pass, False otherwise.
    """
    # Define quality thresholds
    thresholds = {
        'overall_score': 0.7,
        'complexity_score': 0.65,
        'quality_score': 0.7,
        'security_score': 0.8,
        'performance_score': 0.65
    }

    # Check overall score
    if results['overall_score'] < thresholds['overall_score']:
        print(f"❌ Overall score {results['overall_score']:.2f} below threshold {thresholds['overall_score']}")
        return False

    # Check individual scores
    for category, data in results['summary']['key_metrics'].items():
        threshold = thresholds.get(f'{category}_score')
        if threshold and data['score'] < threshold:
            print(f"❌ {category.title()} score {data['score']:.2f} below threshold {threshold}")
            return False

    # Check for critical security issues
    security_results = results['results']['security']
    if security_results.get('vulnerabilities', {}).get('severity_distribution', {}).get('critical', 0) > 0:
        print("❌ Critical security vulnerabilities found")
        return False

    return True

def analyze_project_for_ci(project_dir: Path, output_dir: Path) -> bool:
    """
    Analyzes a project directory and generates reports for CI/CD pipeline.
    Returns True if all quality checks pass, False otherwise.
    """
    manager = FeatureExtractorManager()
    all_passed = True

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Analyze all Python files
    for python_file in project_dir.rglob("*.py"):
        if "test" not in str(python_file) and "venv" not in str(python_file):
            print(f"\nAnalyzing: {python_file}")

            # Read and analyze file
            code = python_file.read_text()
            results = manager.extract_all(code, python_file)

            # Generate reports
            file_basename = python_file.stem
            manager.export_results(
                results,
                format='html',
                output_path=output_dir / f"{file_basename}_analysis.html"
            )
            manager.export_results(
                results,
                format='json',
                output_path=output_dir / f"{file_basename}_analysis.json"
            )

            # Check results
            if not check_analysis_results(results):
                all_passed = False
                print(f"❌ Quality checks failed for {python_file}")
            else:
                print(f"✅ Quality checks passed for {python_file}")

    return all_passed

def main():
    """Example usage in CI pipeline."""
    project_dir = Path("example_project")
    output_dir = Path("ci_reports")

    print("Running code analysis for CI...")
    passed = analyze_project_for_ci(project_dir, output_dir)

    if not passed:
        print("\n❌ CI checks failed! Please review the analysis reports.")
        exit(1)
    else:
        print("\n✅ All CI checks passed!")

if __name__ == "__main__":
    main()