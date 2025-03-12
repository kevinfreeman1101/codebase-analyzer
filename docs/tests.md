# Testing Guide

Here are the key test commands based on the current project structure:

1. Test Everything:
````bash
# Run all tests with coverage
pytest tests/ --cov=codebase_analyzer -v

# Run all tests with detailed coverage report
pytest tests/ --cov=codebase_analyzer --cov-report=term-missing -v

# Run all tests with HTML coverage report
pytest tests/ --cov=codebase_analyzer --cov-report=html -v

# Just unit tests
pytest tests/unit/ -v

# Just integration tests
pytest tests/integration/ -v

# Specific analyzer tests
pytest tests/unit/test_analyzers/ -v

# Specific feature tests
pytest tests/unit/test_features/ -v

# Single test file
pytest tests/unit/test_analyzers/test_python_analyzer.py -v

# Single test class
pytest tests/unit/test_analyzers/test_python_analyzer.py::TestPythonAnalyzer -v

# Single test method
pytest tests/unit/test_analyzers/test_python_analyzer.py::TestPythonAnalyzer::test_analyze_project_simple -v

# Stop on first failure
pytest tests/ -x

# Show local variables in tracebacks
pytest tests/ -l

# Show most common failures
pytest tests/ --maxfail=2

# Run only failed tests from last run
pytest tests/ --lf

# Run with benchmark
pytest tests/ --benchmark-only

# Run with full warnings
pytest tests/ -Wa

````bash

