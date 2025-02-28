# Codebase Analyzer

A Python tool to analyze Python codebases, providing metrics on complexity, quality, dependencies, patterns, security, and performance.
Use this tool to:

- Identify potential issues and improve the overall quality of your codebase.
- Generate condensed code summaries for providing quick context to LLM code advisors (try this with Grok3 to supercharge your development speed!)

## Features

- Comprehensive analysis of Python projects
- Metrics include cyclomatic complexity, maintainability, security vulnerabilities, and performance hotspots
- Detailed summaries with actionable recommendations
- Extensible architecture for adding new analyzers

## Installation

```bash
pip install -r requirements.txt
python setup.py install
```

## Usage

```python
from codebase_analyzer.analyzer import CodebaseAnalyzer
from pathlib import Path

analyzer = CodebaseAnalyzer()
metrics = analyzer.analyze_project(Path("/path/to/project"))
print(analyzer.generate_summary())
```

## Running Tests

```bash
pytest tests/
```

## Requirements

- Python 3.8+
- Dependencies: ast, bandit, pkg_resources, importlib.metadata, and others (see requirements.txt)

## Contributing

- Fork the repository
- Submit pull requests to the main branch
- Ensure tests pass (pytest tests/)
