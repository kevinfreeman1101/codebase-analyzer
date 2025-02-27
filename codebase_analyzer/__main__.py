import sys
from pathlib import Path
from .analyzers.project_analyzer import ProjectAnalyzer

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m codebase_analyzer <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    if not Path(project_path).exists():
        print(f"Error: Path '{project_path}' does not exist")
        sys.exit(1)

    analyzer = ProjectAnalyzer(project_path)
    summary = analyzer.analyze()

    # Write to file and print to console
    output_file = Path(project_path) / "codebase_summary.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)

    print(summary)
    print(f"\nSummary saved to: {output_file}")

if __name__ == "__main__":
    main()