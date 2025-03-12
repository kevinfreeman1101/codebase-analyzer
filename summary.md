CODEBASE ANALYSIS SUMMARY
==================================================
Project Path: .
Analysis Timestamp: 2025-03-11 23:02:40.144166
Total Python Files: 99
Total Lines of Code: 12821
File Types Analyzed: Python (*.py)
Overall Project Score: 0.0/100
  - Weighted average of complexity, quality, security, and performance metrics

COMPLEXITY METRICS
------------------------------
Average Cyclomatic Complexity: 29.18
  - Measures decision points in code (lower is simpler)
Maintainability Index: 0.0/100
  - Higher values indicate better maintainability (<20 suggests complexity issues)
  Complex Functions (Top 3):
    - test_simple_function_with_test at tests/unit/test_analyzers/test_quality_metrics.py:16
      Complexity: 2, Lines: 22
      Code Snippet: def test_simple_function_with_test(tmp_path, mocker):...
    - test_project_with_tests at tests/unit/test_analyzers/test_quality_metrics.py:39
      Complexity: 2, Lines: 22
      Code Snippet: def test_project_with_tests(tmp_path, mocker):...
    - test_mixed_functions at tests/unit/test_analyzers/test_quality_metrics.py:62
      Complexity: 2, Lines: 22
      Code Snippet: def test_mixed_functions(tmp_path, mocker):...

QUALITY METRICS
------------------------------
Type Hint Coverage: 35.5%
  - Proportion of functions/variables with type annotations
Documentation Coverage: 40.5%
  - Percentage of modules, classes, and functions with docstrings
Test Coverage: 0.0%
  - Measured via coverage.py; 0% if no tests or errors occurred
Lint Score: 99.9/100
  - Reflects adherence to style guidelines (e.g., function length, error handling)
Code-to-Comment Ratio: 0.00
  - Limited by AST; inline comments not captured

DEPENDENCY METRICS
------------------------------
Direct Dependencies: 67
  Examples of Direct Dependencies:
    - typing
    - pickle
    - numpy
Dependency Health Score: 0.0/100
  - Assesses outdated or risky dependencies; lower with vulnerabilities

DESIGN PATTERN METRICS
------------------------------
Patterns Detected: 0

SECURITY METRICS
------------------------------
Vulnerabilities Found: 0
Security Score: 100.0/100
  Security Patterns (Top 3):
    - InputValidation (Confidence: 0.60)
      Locations: codebase_analyzer/main.py
    - InputValidation (Confidence: 0.60)
      Locations: codebase_analyzer/__main__.py
    - InputValidation (Confidence: 0.60)
      Locations: codebase_analyzer/analyzer.py

PERFORMANCE METRICS
------------------------------
Hotspots Identified: 23
Performance Score: 0.0/100
  Performance Hotspots (Top 3):
    - codebase_analyzer/formatters/summary_formatter.py:119 (Complexity: 7)
      Suggestion: Consider list comprehension or vectorization
    - codebase_analyzer/metrics/dependency_metrics.py:58 (Complexity: 6)
      Suggestion: Consider list comprehension or vectorization
    - codebase_analyzer/metrics/pattern_metrics.py:86 (Complexity: 10)
      Suggestion: Consider list comprehension or vectorization
  Loop Optimization Opportunities (Top 3):
    - codebase_analyzer/examples/feature_extractor_examples.py:139 (For, Complexity: 2)
      Suggestion: Replace with list comprehension
    - codebase_analyzer/formatters/comprehensive_formatter.py:123 (For, Complexity: 2)
      Suggestion: Replace with list comprehension
    - codebase_analyzer/formatters/comprehensive_formatter.py:146 (For, Complexity: 2)
      Suggestion: Replace with list comprehension
  Memory-Intensive Operations (Top 3):
    - tests/unit/test_analyzers/test_dependency_metrics.py:31 - Large list comprehension
    - codebase_analyzer/visualizations/metric_visualizer.py:55 - Large list comprehension
    - codebase_analyzer/visualizations/metric_visualizer.py:126 - Large list comprehension
  I/O Operations (Top 3):
    - tests/conftest.py:33 - full_path.write_text
    - tests/helpers.py:17 - f.write
    - tests/helpers.py:28 - f.write

RECOMMENDATIONS FOR IMPROVEMENT
==============================
  - [MEDIUM] Complexity: High average cyclomatic complexity detected
  Suggestion: Refactor complex functions to reduce decision points
  - [MEDIUM] Complexity: Low maintainability index
  Suggestion: Simplify code structure and improve readability
  - [HIGH] Complexity: 22 functions with excessive complexity
  Suggestion: Refactor functions like generate_summary at codebase_analyzer/analyzer.py:130
  - [MEDIUM] Quality: Low type hint coverage
  Suggestion: Add type annotations to improve code reliability and IDE support
  - [MEDIUM] Quality: Insufficient documentation coverage
  Suggestion: Add docstrings to functions, classes, and modules
  - 5 additional recommendations available