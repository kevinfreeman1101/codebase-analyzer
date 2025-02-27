# codebase_analyzer/main.py
import os
from pathlib import Path
from typing import Dict
import click

from .analyzers.python_analyzer import PythonAnalyzer
from .analyzers.generic_analyzer import GenericAnalyzer
from .recommendations.recommendation_engine import RecommendationEngine
from .formatters.summary_formatter import SummaryFormatter
from .utils.file_utils import generate_tree_structure, save_to_file

class CodebaseAnalyzer:
    def __init__(self, root_dir: str, output_dir: str, max_tokens: int = 8000):
        self.root_dir = Path(root_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.max_tokens = max_tokens
        self.files: Dict[str, dict] = {}
        self.recommendation_engine = RecommendationEngine()

        self.analyzable_extensions = {
            '.py': ('python', PythonAnalyzer),
            '.pyw': ('python', PythonAnalyzer),
            '.pyi': ('python', PythonAnalyzer),
            '.pyx': ('python', PythonAnalyzer),
            '.pxd': ('python', PythonAnalyzer),
            '.pxi': ('python', PythonAnalyzer),
            '.txt': ('text', GenericAnalyzer),
            '.md': ('markdown', GenericAnalyzer),
            '.rst': ('rst', GenericAnalyzer),
            '.json': ('json', GenericAnalyzer),
            '.yaml': ('yaml', GenericAnalyzer),
            '.yml': ('yaml', GenericAnalyzer),
            '.html': ('html', GenericAnalyzer),
            '.htm': ('html', GenericAnalyzer),
            '.css': ('css', GenericAnalyzer),
            '.js': ('javascript', GenericAnalyzer),
            '.ts': ('typescript', GenericAnalyzer),
            '.xml': ('xml', GenericAnalyzer),
            '.csv': ('csv', GenericAnalyzer),
            '.ini': ('ini', GenericAnalyzer),
            '.conf': ('ini', GenericAnalyzer),
        }

        self.special_files = {
            'requirements.txt': ('requirements', GenericAnalyzer),
            'Pipfile': ('pipfile', GenericAnalyzer),
            'poetry.lock': ('poetry', GenericAnalyzer),
        }

    def analyze(self) -> Dict[str, dict]:
        """Analyze the codebase and return file info."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                self._analyze_file(file_path)
        return self.files

    def _analyze_file(self, file_path: str) -> None:
        """Analyze a single file."""
        from .utils.file_utils import should_analyze_file

        if not should_analyze_file(file_path):
            return

        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_name)[1].lower()

        analyzer_info = (self.special_files.get(file_name) or 
                        self.analyzable_extensions.get(ext))
        
        if analyzer_info:
            file_type, analyzer_class = analyzer_info
            analyzer = (analyzer_class(file_path) if analyzer_class == PythonAnalyzer 
                       else analyzer_class(file_path, file_type))
            file_info = analyzer.analyze()
            if file_info:
                self.files[file_path] = file_info.__dict__

    def generate_summary(self, format: str = 'markdown') -> str:
        """Generate a summary of the codebase."""
        formatter = SummaryFormatter(self.root_dir)
        complex_functions = []

        for file_path, info in self.files.items():
            formatter.add_source_file(file_path, info)
            if info['type'] == 'python':
                for func in info.get('functions', {}).values():
                    if (func.complexity or 0) > 15:  # Direct attribute access with default
                        complex_functions.append({
                            'name': func.name,
                            'complexity': func.complexity or 0,
                            'file_path': file_path
                        })

        metrics = {
            'security': {'vulnerabilities': [], 'pattern_coverage': 0.8},
            'performance': {'hotspots': [], 'caching_opportunities': []},
            'quality': {
                'test_coverage': 0.6,  # Placeholder, improve later
                'documentation_coverage': sum(1 for info in self.files.values() 
                                            for func in info.get('functions', {}).values()
                                            if func.docstring) / 
                                        sum(len(info.get('functions', {})) 
                                            for info in self.files.values()) if self.files else 0,
                'untested_files': [],
                'undocumented_files': [f for f, info in self.files.items() 
                                     if not any(func.docstring 
                                               for func in info.get('functions', {}).values())]
            },
            'complexity': {'complex_functions': complex_functions},
            'dependencies': {'outdated_dependencies': []},
            'patterns': {'anti_patterns': []}
        }
        recommendations = self.recommendation_engine.generate_recommendations(metrics)
        summary = formatter.format_summary()
        if format == 'markdown':
            return f"{summary}\n\n{self.recommendation_engine.export_recommendations('markdown')}"
        elif format == 'html':
            return f"{summary}\n\n{self.recommendation_engine.export_recommendations('html')}"
        return summary

    def save_summary(self, filename: str, format: str = 'markdown') -> bool:
        """Save the summary to a file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.output_dir / filename
        summary = self.generate_summary(format)
        return save_to_file(summary, str(file_path))

@click.command()
@click.argument('root_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output-dir', default='./summaries', type=click.Path(file_okay=False, dir_okay=True),
              help='Directory to save the summary (default: ./summaries)')
@click.option('--max-tokens', default=8000, type=int,
              help='Maximum tokens for summary (default: 8000)')
@click.option('--format', default='markdown', type=click.Choice(['markdown', 'html', 'text']),
              help='Output format (default: markdown)')
def main(root_dir: str, output_dir: str, max_tokens: int, format: str) -> None:
    """Analyze a Python codebase and generate a summary for LLMs."""
    analyzer = CodebaseAnalyzer(root_dir, output_dir, max_tokens)
    click.echo("Analyzing codebase...")
    analyzer.analyze()
    project_name = Path(root_dir).name
    filename = f"{project_name}_summary.{format if format != 'text' else 'txt'}"
    if analyzer.save_summary(filename, format):
        click.echo(f"Summary saved to {os.path.join(output_dir, filename)}")
    else:
        click.echo("Failed to save summary", err=True)

if __name__ == '__main__':
    main()