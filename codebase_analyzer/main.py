import click
import sys
from typing import Optional
from pathlib import Path
from .analyzers.python_analyzer import PythonAnalyzer
from .analyzers.generic_analyzer import GenericAnalyzer
from .formatters.summary_formatter import SummaryFormatter

class CodebaseAnalyzerCLI:
    """CLI tool for analyzing a codebase."""

    def __init__(self, directory: str):
        """Initialize the analyzer with a target directory."""
        self.directory = Path(directory)
        self.formatter = SummaryFormatter(self.directory)

    def analyze(self) -> None:
        """Analyze the codebase and generate a summary."""
        print("Analyzing codebase...")
        if not self.directory.exists():
            print(f"Error: Directory '{self.directory}' does not exist.")
            sys.exit(1)

        for file_path in self.directory.rglob('*'):
            if file_path.is_file():
                self._analyze_file(file_path)

        summary = self.formatter.format_summary()
        print(summary)

    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single file and update the formatter."""
        from .utils.file_utils import should_analyze_file, get_file_type

        if not should_analyze_file(str(file_path)):
            return

        file_type = get_file_type(str(file_path))
        analyzer_class = PythonAnalyzer if file_type == 'python' else GenericAnalyzer
        analyzer = analyzer_class(str(file_path))
        file_info = analyzer.analyze()

        if file_info:
            relative_path = file_path.relative_to(self.directory)
            self.formatter.add_source_file(str(relative_path), file_info)

@click.command()
@click.argument('directory', default='.', type=click.Path(exists=True))
def main(directory: str) -> None:
    """Entrypoint for the CLI tool."""
    analyzer = CodebaseAnalyzerCLI(directory)
    analyzer.analyze()

if __name__ == "__main__":
    main()