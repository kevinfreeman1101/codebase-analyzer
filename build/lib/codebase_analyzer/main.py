import click
import sys
import traceback
from pathlib import Path
from .analyzer import CodebaseAnalyzer

@click.command()
@click.argument('directory', default='.', type=click.Path(exists=True))
def main(directory: str) -> None:
    """Entrypoint for the CLI tool to analyze a Python codebase."""
    print("Starting comprehensive project analysis...")
    analyzer = CodebaseAnalyzer()
    try:
        result = analyzer.analyze_project(Path(directory))
        summary = analyzer.generate_summary()
        print(summary)
        with open('summary.md', 'w', encoding='utf-8') as f:
            f.write(summary)
    except Exception as e:
        print(f"Error analyzing codebase: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()