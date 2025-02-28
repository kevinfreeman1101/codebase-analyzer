import click
import sys
from pathlib import Path
from .analyzer import CodebaseAnalyzer

@click.command()
@click.argument('directory', default='.', type=click.Path(exists=True))
def main(directory: str) -> None:
    """Entrypoint for the CLI tool to analyze a Python codebase."""
    analyzer = CodebaseAnalyzer()
    try:
        result = analyzer.analyze_project(Path(directory))
        summary = analyzer.generate_summary()
        print(summary)
        # Save to file as in the old output
        with open('summary.md', 'w') as f:
            f.write(summary)
    except Exception as e:
        print(f"Error analyzing codebase: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()