# Example usage in a Python script
from codebase_analyzer import CodebaseAnalyzer
from pathlib import Path

# Initialize analyzer
analyzer = CodebaseAnalyzer()

# Analyze project with visualizations
project_path = Path('/path/to/your/project')
results = analyzer.analyze_project(project_path)

# Access visualization paths
report_path = results['visualization_results']['report_path']
print(f"View the analysis report at: {report_path}")

# Access specific visualizations
visualization_files = results['visualization_results']['visualization_files']
for viz_file in visualization_files:
    print(f"Generated visualization: {viz_file.name}")


"""
# COMMAND LINE USAGE
# Basic usage
python -m codebase_analyzer /path/to/your/project

# Specify custom output directory
python -m codebase_analyzer /path/to/your/project --output-dir ./my_analysis

# Skip visualization generation
python -m codebase_analyzer /path/to/your/project --no-visuals
"""