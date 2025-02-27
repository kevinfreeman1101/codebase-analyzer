# examples/feature_extractor_examples.py

from pathlib import Path
from codebase_analyzer.features.manager import FeatureExtractorManager

def basic_analysis_example():
    """Basic example of analyzing a simple code snippet."""
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def process_data(items):
    result = []
    for item in items:
        for subitem in item:
            result.append(subitem * 2)
    return result

def unsafe_eval(user_input):
    return eval(user_input)
    """

    manager = FeatureExtractorManager()
    results = manager.extract_all(code)

    # Export as JSON
    json_output = manager.export_results(results, format='json')
    print("JSON Analysis Results:")
    print(json_output)

    # Export as HTML
    html_output_path = Path("analysis_report.html")
    manager.export_results(results, format='html', output_path=html_output_path)
    print(f"\nHTML report generated at: {html_output_path.absolute()}")

def analyze_project_file():
    """Example of analyzing a real project file."""
    file_path = Path("example_project/main.py")

    if not file_path.exists():
        # Create example file if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("""
import json
from typing import Dict, List

class DataProcessor:
    def __init__(self):
        self._cache = {}

    def process_items(self, items: List[Dict]) -> List[Dict]:
        results = []
        for item in items:
            # Nested loops for demonstration
            for key, value in item.items():
                if isinstance(value, list):
                    for subvalue in value:
                        results.append({
                            'key': key,
                            'value': subvalue,
                            'processed': True
                        })
        return results

    def load_data(self, filepath: str) -> Dict:
        # Potential security issue - no path validation
        with open(filepath) as f:
            return json.load(f)
        """)

    manager = FeatureExtractorManager()

    # Analyze the file
    with open(file_path) as f:
        code = f.read()

    results = manager.extract_all(code, file_path)

    # Generate reports in different formats
    reports_dir = Path("analysis_reports")
    reports_dir.mkdir(exist_ok=True)

    # JSON report
    json_path = reports_dir / "analysis.json"
    manager.export_results(results, format='json', output_path=json_path)

    # HTML report
    html_path = reports_dir / "analysis.html"
    manager.export_results(results, format='html', output_path=html_path)

    print(f"Reports generated in: {reports_dir.absolute()}")

def analyze_with_custom_output():
    """Example of analyzing code and customizing the output."""
    code = """
# Global variable usage
CACHE = {}

def compute_expensive_operation(x):
    # Potential performance issue - no caching
    return sum(i * i for i in range(x))

def process_user_data(user_input: str) -> str:
    # Security vulnerability - using exec
    exec(f"result = {user_input}")
    return locals().get('result', '')

class DataManager:
    def __init__(self):
        # Missing type hints
        self.data = []

    def add_items(self, items):
        # Nested loops
        for item in items:
            for subitem in item:
                self.data.append(subitem)

    def get_items(self):
        # Missing return type hint
        return self.data
    """

    manager = FeatureExtractorManager()
    results = manager.extract_all(code)

    # Custom report generation
    def generate_summary_report(results: Dict) -> str:
        summary = []
        summary.append("=== Code Analysis Summary ===")
        summary.append(f"Overall Score: {results['overall_score']:.2f}\n")

        summary.append("Key Findings:")
        for category, data in results['summary']['key_metrics'].items():
            summary.append(f"\n{category.upper()}:")
            summary.append(f"Score: {data['score']:.2f}")
            for highlight in data['highlights']:
                summary.append(f"- {highlight}")

        summary.append("\nTop Recommendations:")
        for rec in results['recommendations'][:3]:  # Top 3 recommendations
            summary.append(f"\n{rec['priority'].upper()}: {rec['title']}")
            summary.append(f"- {rec['suggestion']}")

        return "\n".join(summary)

    # Generate and save custom summary
    summary_report = generate_summary_report(results)
    summary_path = Path("analysis_reports/summary.txt")
    summary_path.parent.mkdir(exist_ok=True)
    summary_path.write_text(summary_report)

    print("Custom Summary Report:")
    print(summary_report)

def main():
    """Run all examples."""
    print("\n=== Running Basic Analysis Example ===")
    basic_analysis_example()

    print("\n=== Running Project File Analysis Example ===")
    analyze_project_file()

    print("\n=== Running Custom Output Analysis Example ===")
    analyze_with_custom_output()

if __name__ == "__main__":
    main()