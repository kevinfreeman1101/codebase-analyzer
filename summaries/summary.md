CODEBASE SUMMARY
===============

Root: /mnt/Egg/code/python/apps/codebase-analyzer

Project Overview
--------------
Name: codebase-analyzer

Summary Statistics
------------------
Directories: 9
Total Files: 268
Total Size: 1256.3 KB
Classes: 364
Functions: 1276
Documented: 1554 (95% of functions)

File Distribution:
- Toml Files: 2 files
- Unknown Files: 22 files
- Documentation Files: 24 files
- Sh Files: 2 files
- Python Files: 200 files
- Archive Files: 2 files
- Conf Files: 2 files
- Configuration Files: 6 files
- Ini Files: 2 files
- Tag Files: 4 files
- Yml Files: 2 files

Directory Structure
------------------
├─ .github
│  ├─ workflows
   ├─ tests.yml
├─ .pytest_cache
│  ├─ v
│  ├─ cache
   ├─ lastfailed
   ├─ nodeids
   ├─ stepwise
│  ├─ .gitignore
│  ├─ CACHEDIR.TAG
│  ├─ README.md
├─ .vscode
│  ├─ settings.json
├─ build
│  ├─ lib
   ├─ codebase_analyzer
│  ├─ analyzers
│  ├─ __init__.py
│  ├─ base_analyzer.py
│  ├─ generic_analyzer.py
│  ├─ project_analyzer.py
│  ├─ python_analyzer.py
│  ├─ features
│  ├─ __init__.py
│  ├─ base.py
│  ├─ complexity.py
│  ├─ manager.py
│  ├─ performance.py
│  ├─ quality.py
│  ├─ security.py
│  ├─ formatters
│  ├─ __init__.py
│  ├─ comprehensive_formatter.py
│  ├─ summary_formatter.py
│  ├─ metrics
│  ├─ __init__.py
│  ├─ complexity_analyzer.py
│  ├─ dependency_metrics.py
│  ├─ pattern_metrics.py
│  ├─ performance_metrics.py
│  ├─ quality_metrics.py
│  ├─ security_metrics.py
│  ├─ models
│  ├─ __init__.py
│  ├─ data_classes.py
│  ├─ recommendations
│  ├─ __init__.py
│  ├─ ml_engine.py
│  ├─ prompt_manager.py
│  ├─ recommendation_engine.py
│  ├─ utils
│  ├─ __init__.py
│  ├─ file_utils.py
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ analyzer.py
│  ├─ main.py
   ├─ tests
   ├─ integration
│  ├─ __init__.py
│  ├─ test_integration.py
   ├─ unit
│  ├─ test_analyzers
│  ├─ __init__.py
│  ├─ test_codebase_analyzer.py
│  ├─ test_project_analyzer.py
│  ├─ test_python_analyzer.py
│  ├─ __init__.py
   ├─ __init__.py
   ├─ conftest.py
   ├─ helpers.py
├─ codebase_analyzer
│  ├─ analyzers
│  ├─ __init__.py
│  ├─ base_analyzer.py
│  ├─ generic_analyzer.py
│  ├─ project_analyzer.py
│  ├─ python_analyzer.py
│  ├─ examples
│  ├─ prompts
│  ├─ templates.json
│  ├─ ci_integration.py
│  ├─ feature_extractor_examples.py
│  ├─ prompt_example.py
│  ├─ recommendations_example.py
│  ├─ features
│  ├─ __init__.py
│  ├─ base.py
│  ├─ complexity.py
│  ├─ manager.py
│  ├─ performance.py
│  ├─ quality.py
│  ├─ security.py
│  ├─ formatters
│  ├─ __init__.py
│  ├─ comprehensive_formatter.py
│  ├─ summary_formatter.py
│  ├─ metrics
│  ├─ __init__.py
│  ├─ complexity_analyzer.py
│  ├─ dependency_metrics.py
│  ├─ pattern_metrics.py
│  ├─ performance_metrics.py
│  ├─ quality_metrics.py
│  ├─ security_metrics.py
│  ├─ models
│  ├─ __init__.py
│  ├─ data_classes.py
│  ├─ recommendations
│  ├─ __init__.py
│  ├─ ml_engine.py
│  ├─ prompt_manager.py
│  ├─ recommendation_engine.py
│  ├─ utils
│  ├─ __init__.py
│  ├─ file_utils.py
│  ├─ visualizations
│  ├─ examples.py
│  ├─ metric_visualizer.py
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ analyzer.py
│  ├─ main.py
├─ codebase_analyzer.egg-info
│  ├─ PKG-INFO
│  ├─ SOURCES.txt
│  ├─ dependency_links.txt
│  ├─ entry_points.txt
│  ├─ requires.txt
│  ├─ top_level.txt
├─ summaries
│  ├─ summary.md
├─ tests
│  ├─ .pytest_cache
│  ├─ v
│  ├─ cache
   ├─ lastfailed
   ├─ nodeids
   ├─ stepwise
│  ├─ .gitignore
│  ├─ CACHEDIR.TAG
│  ├─ README.md
│  ├─ integration
│  ├─ __init__.py
│  ├─ test_integration.py
│  ├─ unit
│  ├─ test_analyzers
│  ├─ __init__.py
│  ├─ test_codebase_analyzer.py
│  ├─ test_dependency_metrics.py
│  ├─ test_features_manager.py
│  ├─ test_project_analyzer.py
│  ├─ test_python_analyzer.py
│  ├─ test_quality_metrics.py
│  ├─ test_features
│  ├─ test_complexity_features.py
│  ├─ __init__.py
│  ├─ __init__.py
│  ├─ conftest.py
│  ├─ helpers.py
│  ├─ pytest.ini
├─ .coverage
├─ .dependency_cache.json
├─ .gitignore
├─ README.md
├─ example_usage.py
├─ logging.conf
├─ pyproject.toml
├─ requirements-dev.txt
├─ requirements.txt
├─ requirements.txt.archive
├─ setup.py
├─ setup_test_structure.sh
├─ summary.md

Source Files
------------

pyproject.toml
  Size: 0.2 KB
  (Empty or initialization file)

.gitignore
  Size: 0.4 KB
  (Empty or initialization file)

.coverage
  Size: 52.4 KB
  (Empty or initialization file)

README.md
  Size: 1.4 KB
  (Empty or initialization file)

summary.md
  Size: 61.1 KB
  (Empty or initialization file)

setup_test_structure.sh
  Size: 1.9 KB
  (Empty or initialization file)

setup.py
  Size: 0.4 KB
  (Empty or initialization file)

requirements-dev.txt
  Size: 0.2 KB
  (Empty or initialization file)

requirements.txt.archive
  Size: 0.3 KB
  (Empty or initialization file)

logging.conf
  Size: 0.3 KB
  (Empty or initialization file)

example_usage.py
  Size: 0.9 KB
  (Empty or initialization file)

requirements.txt
  Size: 1.5 KB
  (Empty or initialization file)

.dependency_cache.json
  Size: 1.1 KB
  (Empty or initialization file)

tests/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

tests/conftest.py
  Size: 1.3 KB
  Functions:
    - temp_dir (Lines: 5, Documented: Yes)
    - helper (Lines: 3, Documented: Yes)
    - sample_codebase (Lines: 16, Documented: Yes)
    - analyzer (Lines: 4, Documented: Yes)

tests/pytest.ini
  Size: 0.2 KB
  (Empty or initialization file)

tests/helpers.py
  Size: 1.1 KB
  Functions:
    - __init__ (Lines: 2, Documented: No)
    - create_temp_file (Lines: 6, Documented: Yes)
    - create_temp_project (Lines: 10, Documented: Yes)
    - cleanup_temp (Lines: 3, Documented: Yes)
  Classes:
    - TestHelper (Methods: 4, Documented: Yes)

tests/unit/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

tests/unit/test_features/test_complexity_features.py
  Size: 2.0 KB
  Functions:
    - __init__ (Lines: 6, Documented: No)
    - setup_method (Lines: 2, Documented: No)
    - test_complexity_basic_function (Lines: 10, Documented: No)
    - test_complexity_nested_structures (Lines: 14, Documented: No)
    - test_maintainability_index (Lines: 5, Documented: No)
  Classes:
    - ComplexityFeatures (Methods: 1, Documented: No)
    - TestComplexityFeatures (Methods: 4, Documented: No)

tests/unit/test_analyzers/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

tests/unit/test_analyzers/test_quality_metrics.py
  Size: 3.5 KB
  Functions:
    - test_empty_file (Lines: 10, Documented: Yes)
    - test_simple_function_with_test (Lines: 22, Documented: Yes)
    - test_project_with_tests (Lines: 22, Documented: Yes)
    - test_mixed_functions (Lines: 22, Documented: Yes)
    - test_project_with_no_tests (Lines: 10, Documented: Yes)

tests/unit/test_analyzers/test_features_manager.py
  Size: 5.7 KB
  Functions:
    - manager (Lines: 11, Documented: Yes)
    - test_init (Lines: 4, Documented: Yes)
    - test_extract_all_success (Lines: 15, Documented: Yes)
    - test_extract_all_with_errors (Lines: 18, Documented: Yes)
    - test_calculate_overall_score (Lines: 10, Documented: Yes)
    - test_generate_summary (Lines: 12, Documented: Yes)
    - test_generate_recommendations (Lines: 11, Documented: Yes)
    - test_export_results_json (Lines: 5, Documented: Yes)
    - test_export_results_html (Lines: 13, Documented: Yes)
    - test_export_results_invalid_format (Lines: 4, Documented: Yes)
    - test_export_results_to_file (Lines: 6, Documented: Yes)

tests/unit/test_analyzers/test_python_analyzer.py
  Size: 2.7 KB
  Functions:
    - test_analyze_empty_file (Lines: 8, Documented: Yes)
    - test_analyze_simple_function (Lines: 10, Documented: Yes)
    - test_analyze_complex_function (Lines: 16, Documented: Yes)
    - test_analyze_dependencies (Lines: 9, Documented: Yes)
    - test_basic_analysis (Lines: 10, Documented: Yes)
    - test_unused_imports (Lines: 8, Documented: Yes)
    - test_malformed_file (Lines: 8, Documented: Yes)

tests/unit/test_analyzers/test_project_analyzer.py
  Size: 3.0 KB
  Functions:
    - analyzer (Lines: 12, Documented: Yes)
    - test_project_analyzer_empty_directory (Lines: 5, Documented: Yes)
    - test_project_analyzer_with_files (Lines: 11, Documented: Yes)
    - test_project_analyzer_with_complex_structure (Lines: 14, Documented: Yes)
    - test_project_analyzer_with_non_python_files (Lines: 12, Documented: Yes)
    - test_analyze_empty_project (Lines: 4, Documented: Yes)
    - test_analyze_simple_project (Lines: 8, Documented: Yes)

tests/unit/test_analyzers/test_codebase_analyzer.py
  Size: 4.0 KB
  Functions:
    - temp_project (Lines: 5, Documented: Yes)
    - test_analyze_project_simple (Lines: 12, Documented: Yes)
    - test_analyze_project_with_complexity (Lines: 19, Documented: Yes)
    - test_analyze_project_with_vulnerabilities (Lines: 14, Documented: Yes)
    - test_analyze_project_empty (Lines: 7, Documented: Yes)
    - test_generate_summary_no_analysis (Lines: 5, Documented: Yes)
    - test_generate_summary_after_analysis (Lines: 14, Documented: Yes)
    - test_analyze_project_invalid_path (Lines: 6, Documented: Yes)
    - test_analyze_project_with_errors (Lines: 16, Documented: Yes)

tests/unit/test_analyzers/test_dependency_metrics.py
  Size: 1.4 KB
  Functions:
    - test_basic_dependencies (Lines: 12, Documented: Yes)
    - test_vulnerable_dependencies (Lines: 14, Documented: Yes)

tests/.pytest_cache/.gitignore
  Size: 0.0 KB
  (Empty or initialization file)

tests/.pytest_cache/README.md
  Size: 0.3 KB
  (Empty or initialization file)

tests/.pytest_cache/CACHEDIR.TAG
  Size: 0.2 KB
  (Empty or initialization file)

tests/.pytest_cache/v/cache/lastfailed
  Size: 3.3 KB
  (Empty or initialization file)

tests/.pytest_cache/v/cache/nodeids
  Size: 6.3 KB
  (Empty or initialization file)

tests/.pytest_cache/v/cache/stepwise
  Size: 0.0 KB
  (Empty or initialization file)

tests/integration/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

tests/integration/test_integration.py
  Size: 1.2 KB
  Functions:
    - setup_method (Lines: 2, Documented: No)
    - test_full_analysis (Lines: 31, Documented: Yes)
  Classes:
    - TestIntegration (Methods: 2, Documented: No)

summaries/summary.md
  Size: 4.0 KB
  (Empty or initialization file)

.github/workflows/tests.yml
  Size: 0.8 KB
  (Empty or initialization file)

codebase_analyzer.egg-info/entry_points.txt
  Size: 0.1 KB
  (Empty or initialization file)

codebase_analyzer.egg-info/SOURCES.txt
  Size: 2.0 KB
  (Empty or initialization file)

codebase_analyzer.egg-info/requires.txt
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer.egg-info/PKG-INFO
  Size: 0.1 KB
  (Empty or initialization file)

codebase_analyzer.egg-info/top_level.txt
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer.egg-info/dependency_links.txt
  Size: 0.0 KB
  (Empty or initialization file)

.vscode/settings.json
  Size: 0.1 KB
  (Empty or initialization file)

.pytest_cache/.gitignore
  Size: 0.0 KB
  (Empty or initialization file)

.pytest_cache/README.md
  Size: 0.3 KB
  (Empty or initialization file)

.pytest_cache/CACHEDIR.TAG
  Size: 0.2 KB
  (Empty or initialization file)

.pytest_cache/v/cache/lastfailed
  Size: 3.7 KB
  (Empty or initialization file)

.pytest_cache/v/cache/nodeids
  Size: 3.9 KB
  (Empty or initialization file)

.pytest_cache/v/cache/stepwise
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer/__init__.py
  Size: 0.1 KB
  (Empty or initialization file)

codebase_analyzer/main.py
  Size: 0.8 KB
  Functions:
    - main (Lines: 14, Documented: Yes)

codebase_analyzer/__main__.py
  Size: 0.1 KB
  (Empty or initialization file)

codebase_analyzer/analyzer.py
  Size: 3.7 KB
  Functions:
    - __init__ (Lines: 12, Documented: Yes)
    - analyze_project (Lines: 34, Documented: Yes)
    - generate_summary (Lines: 13, Documented: Yes)
  Classes:
    - CodebaseAnalyzer (Methods: 3, Documented: No)

codebase_analyzer/visualizations/examples.py
  Size: 2.9 KB
  Functions:
    - generate_visualization_report (Lines: 25, Documented: Yes)
    - main (Lines: 24, Documented: Yes)
    - __init__ (Lines: 2, Documented: No)
    - analyze_project (Lines: 25, Documented: Yes)
  Classes:
    - CodebaseAnalyzer (Methods: 2, Documented: No)

codebase_analyzer/visualizations/metric_visualizer.py
  Size: 13.6 KB
  Functions:
    - __init__ (Lines: 10, Documented: No)
    - generate_visualizations (Lines: 14, Documented: Yes)
    - _generate_score_dashboard (Lines: 36, Documented: Yes)
    - _generate_complexity_heatmap (Lines: 36, Documented: Yes)
    - _generate_dependency_graph (Lines: 41, Documented: Yes)
    - _generate_security_radar (Lines: 49, Documented: Yes)
    - _generate_performance_timeline (Lines: 34, Documented: Yes)
    - _generate_quality_metrics_sunburst (Lines: 71, Documented: Yes)
    - _generate_pattern_distribution (Lines: 38, Documented: Yes)
    - generate_html_report (Lines: 40, Documented: Yes)
    - plot_sunburst (Lines: 38, Documented: No)
  Classes:
    - MetricVisualizer (Methods: 10, Documented: Yes)

codebase_analyzer/utils/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer/utils/file_utils.py
  Size: 3.6 KB
  Functions:
    - should_analyze_file (Lines: 20, Documented: Yes)
    - get_file_type (Lines: 26, Documented: Yes)
    - safe_read_file (Lines: 26, Documented: Yes)
    - save_to_file (Lines: 16, Documented: Yes)
    - generate_tree_structure (Lines: 19, Documented: Yes)

codebase_analyzer/models/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer/models/data_classes.py
  Size: 4.4 KB
  Functions:
    - __post_init__ (Lines: 3, Documented: No)
    - calculate_overall_score (Lines: 29, Documented: Yes)
  Classes:
    - FunctionInfo (Methods: 1, Documented: Yes)
    - MethodInfo (Methods: 0, Documented: Yes)
    - ClassInfo (Methods: 1, Documented: Yes)
    - FileInfo (Methods: 0, Documented: No)
    - ProjectMetrics (Methods: 2, Documented: Yes)
    - Recommendation (Methods: 1, Documented: Yes)

codebase_analyzer/examples/ci_integration.py
  Size: 3.2 KB
  Functions:
    - check_analysis_results (Lines: 33, Documented: Yes)
    - analyze_project_for_ci (Lines: 41, Documented: Yes)
    - main (Lines: 13, Documented: Yes)

codebase_analyzer/examples/feature_extractor_examples.py
  Size: 5.0 KB
  Functions:
    - basic_analysis_example (Lines: 31, Documented: Yes)
    - analyze_project_file (Lines: 56, Documented: Yes)
    - analyze_with_custom_output (Lines: 62, Documented: Yes)
    - main (Lines: 10, Documented: Yes)
    - generate_summary_report (Lines: 18, Documented: No)

codebase_analyzer/examples/recommendations_example.py
  Size: 0.9 KB
  Classes:
    - CustomModel (Methods: 0, Documented: No)

codebase_analyzer/examples/prompt_example.py
  Size: 0.6 KB
  (Empty or initialization file)

codebase_analyzer/examples/prompts/templates.json
  Size: 3.8 KB
  (Empty or initialization file)

codebase_analyzer/formatters/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer/formatters/comprehensive_formatter.py
  Size: 12.8 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - _setup_colors (Lines: 14, Documented: Yes)
    - format_analysis (Lines: 24, Documented: Yes)
    - _format_project_overview (Lines: 16, Documented: Yes)
    - _format_executive_summary (Lines: 21, Documented: Yes)
    - _format_complexity_analysis (Lines: 21, Documented: Yes)
    - _format_quality_analysis (Lines: 20, Documented: Yes)
    - _format_security_analysis (Lines: 23, Documented: Yes)
    - _format_performance_analysis (Lines: 20, Documented: Yes)
    - _format_dependency_analysis (Lines: 20, Documented: Yes)
    - _format_pattern_analysis (Lines: 19, Documented: Yes)
    - _format_recommendations (Lines: 17, Documented: Yes)
    - _format_score (Lines: 11, Documented: Yes)
    - _format_header (Lines: 8, Documented: Yes)
    - _get_critical_findings (Lines: 20, Documented: Yes)
    - _get_prioritized_recommendations (Lines: 24, Documented: Yes)
    - _group_by_severity (Lines: 10, Documented: Yes)
  Classes:
    - FormattingOptions (Methods: 0, Documented: Yes)
    - ComprehensiveFormatter (Methods: 17, Documented: Yes)

codebase_analyzer/formatters/summary_formatter.py
  Size: 7.1 KB
  Functions:
    - __init__ (Lines: 28, Documented: Yes)
    - add_source_file (Lines: 45, Documented: Yes)
    - generate_summary (Lines: 63, Documented: Yes)
    - _format_file_structure (Lines: 17, Documented: Yes)
  Classes:
    - SummaryFormatter (Methods: 4, Documented: Yes)

codebase_analyzer/metrics/__init__.py
  Size: 0.6 KB
  (Empty or initialization file)

codebase_analyzer/metrics/dependency_metrics.py
  Size: 4.1 KB
  Functions:
    - health_score (Lines: 6, Documented: Yes)
    - analyze_project (Lines: 74, Documented: Yes)
  Classes:
    - DependencyMetrics (Methods: 1, Documented: Yes)
    - DependencyAnalyzer (Methods: 1, Documented: Yes)

codebase_analyzer/metrics/security_metrics.py
  Size: 8.4 KB
  Functions:
    - __init__ (Lines: 2, Documented: No)
    - analyze_project (Lines: 18, Documented: Yes)
    - _detect_vulnerabilities (Lines: 10, Documented: Yes)
    - _check_for_insecure_functions (Lines: 40, Documented: Yes)
    - _detect_security_patterns (Lines: 18, Documented: Yes)
    - _check_authentication_pattern (Lines: 38, Documented: Yes)
    - _check_input_validation (Lines: 37, Documented: Yes)
    - _calculate_security_score (Lines: 23, Documented: Yes)
    - visit_Call (Lines: 6, Documented: No)
    - visit_Import (Lines: 5, Documented: No)
    - visit_If (Lines: 4, Documented: No)
  Classes:
    - Vulnerability (Methods: 0, Documented: No)
    - SecurityPattern (Methods: 0, Documented: No)
    - SecurityMetrics (Methods: 0, Documented: No)
    - SecurityAnalyzer (Methods: 8, Documented: Yes)
    - InsecureFunctionVisitor (Methods: 2, Documented: No)
    - AuthVisitor (Methods: 3, Documented: No)
    - ValidationVisitor (Methods: 3, Documented: No)

codebase_analyzer/metrics/quality_metrics.py
  Size: 9.9 KB
  Functions:
    - quality_score (Lines: 21, Documented: Yes)
    - analyze_project (Lines: 45, Documented: Yes)
    - analyze_node (Lines: 14, Documented: Yes)
    - _calculate_type_hint_coverage (Lines: 32, Documented: Yes)
    - _calculate_documentation_coverage (Lines: 32, Documented: Yes)
    - _calculate_code_comment_ratio (Lines: 17, Documented: Yes)
    - _calculate_lint_score (Lines: 28, Documented: Yes)
    - _estimate_test_coverage (Lines: 3, Documented: Yes)
    - _run_coverage (Lines: 46, Documented: Yes)
    - __init__ (Lines: 3, Documented: No)
    - visit_FunctionDef (Lines: 9, Documented: No)
    - visit_AnnAssign (Lines: 4, Documented: No)
    - visit_ClassDef (Lines: 5, Documented: No)
    - visit_Module (Lines: 5, Documented: No)
    - visit (Lines: 5, Documented: No)
    - visit_Try (Lines: 7, Documented: No)
  Classes:
    - QualityMetrics (Methods: 1, Documented: Yes)
    - QualityAnalyzer (Methods: 8, Documented: Yes)
    - TypeHintVisitor (Methods: 3, Documented: No)
    - DocVisitor (Methods: 4, Documented: No)
    - CommentVisitor (Methods: 1, Documented: No)
    - LintVisitor (Methods: 2, Documented: No)

codebase_analyzer/metrics/pattern_metrics.py
  Size: 15.5 KB
  Functions:
    - __init__ (Lines: 4, Documented: No)
    - analyze_project (Lines: 16, Documented: Yes)
    - _detect_design_patterns (Lines: 19, Documented: Yes)
    - _detect_singleton_pattern (Lines: 36, Documented: Yes)
    - _detect_factory_pattern (Lines: 40, Documented: Yes)
    - _detect_strategy_pattern (Lines: 31, Documented: Yes)
    - _detect_observer_pattern (Lines: 31, Documented: Yes)
    - _detect_decorator_pattern (Lines: 31, Documented: Yes)
    - _detect_adapter_pattern (Lines: 33, Documented: Yes)
    - _analyze_architecture (Lines: 4, Documented: Yes)
    - _analyze_layered_architecture (Lines: 14, Documented: Yes)
    - _determine_architecture_style (Lines: 16, Documented: Yes)
    - _detect_api_patterns (Lines: 3, Documented: Yes)
    - _detect_database_patterns (Lines: 3, Documented: Yes)
    - _detect_anti_patterns (Lines: 3, Documented: Yes)
    - get_pattern_summary (Lines: 27, Documented: Yes)
    - visit_ClassDef (Lines: 12, Documented: No)
    - _find_return_types (Lines: 8, Documented: No)
  Classes:
    - DesignPattern (Methods: 0, Documented: No)
    - ArchitecturalStyle (Methods: 0, Documented: No)
    - PatternMetrics (Methods: 0, Documented: No)
    - PatternAnalyzer (Methods: 16, Documented: Yes)
    - SingletonVisitor (Methods: 2, Documented: No)
    - FactoryVisitor (Methods: 3, Documented: No)
    - StrategyVisitor (Methods: 2, Documented: No)
    - ObserverVisitor (Methods: 2, Documented: No)
    - DecoratorVisitor (Methods: 2, Documented: No)
    - AdapterVisitor (Methods: 2, Documented: No)

codebase_analyzer/metrics/complexity_analyzer.py
  Size: 4.8 KB
  Functions:
    - analyze_project (Lines: 38, Documented: Yes)
    - _analyze_complexity (Lines: 65, Documented: Yes)
    - __init__ (Lines: 4, Documented: No)
    - visit_FunctionDef (Lines: 21, Documented: No)
    - visit_If (Lines: 3, Documented: No)
    - visit_For (Lines: 3, Documented: No)
    - visit_While (Lines: 3, Documented: No)
    - visit_Try (Lines: 3, Documented: No)
    - visit_With (Lines: 3, Documented: No)
    - visit_BoolOp (Lines: 3, Documented: No)
  Classes:
    - ComplexityMetrics (Methods: 0, Documented: Yes)
    - ComplexityAnalyzer (Methods: 2, Documented: Yes)
    - ComplexityVisitor (Methods: 8, Documented: No)

codebase_analyzer/metrics/performance_metrics.py
  Size: 12.0 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - analyze_project (Lines: 22, Documented: Yes)
    - _identify_hotspots (Lines: 10, Documented: Yes)
    - _analyze_hotspots (Lines: 43, Documented: Yes)
    - _identify_optimization_opportunities (Lines: 10, Documented: Yes)
    - _analyze_optimizations (Lines: 47, Documented: Yes)
    - _detect_memory_intensive_operations (Lines: 10, Documented: Yes)
    - _analyze_memory_ops (Lines: 23, Documented: Yes)
    - _detect_io_operations (Lines: 10, Documented: Yes)
    - _analyze_io_ops (Lines: 21, Documented: Yes)
    - _calculate_performance_score (Lines: 16, Documented: Yes)
    - visit_For (Lines: 14, Documented: No)
    - visit_While (Lines: 10, Documented: No)
    - _calculate_complexity (Lines: 6, Documented: No)
    - visit_ListComp (Lines: 3, Documented: No)
    - visit_Call (Lines: 6, Documented: No)
  Classes:
    - PerformanceHotspot (Methods: 0, Documented: Yes)
    - LoopOptimization (Methods: 0, Documented: Yes)
    - PerformanceMetrics (Methods: 0, Documented: Yes)
    - PerformanceAnalyzer (Methods: 11, Documented: Yes)
    - HotspotVisitor (Methods: 4, Documented: No)
    - OptimizationVisitor (Methods: 4, Documented: No)
    - MemoryVisitor (Methods: 3, Documented: No)
    - IOVisitor (Methods: 2, Documented: No)

codebase_analyzer/recommendations/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer/recommendations/ml_engine.py
  Size: 8.4 KB
  Functions:
    - analyze (Lines: 15, Documented: Yes)
    - train (Lines: 3, Documented: Yes)
    - save (Lines: 7, Documented: Yes)
    - load (Lines: 6, Documented: Yes)
    - __init__ (Lines: 4, Documented: No)
    - _process_features (Lines: 6, Documented: Yes)
    - _initialize_feature_extractors (Lines: 8, Documented: Yes)
    - _extract_complexity_features (Lines: 7, Documented: Yes)
    - _call_llm_api (Lines: 8, Documented: Yes)
    - _load_prompt_templates (Lines: 5, Documented: Yes)
    - _initialize_models (Lines: 12, Documented: Yes)
    - add_model (Lines: 3, Documented: Yes)
    - remove_model (Lines: 3, Documented: Yes)
    - _aggregate_recommendations (Lines: 21, Documented: Yes)
    - _merge_recommendations (Lines: 14, Documented: Yes)
  Classes:
    - MLRecommendation (Methods: 0, Documented: Yes)
    - ModelInterface (Methods: 4, Documented: Yes)
    - LocalMLModel (Methods: 8, Documented: Yes)
    - LLMInterface (Methods: 3, Documented: Yes)
    - ClaudeInterface (Methods: 6, Documented: Yes)
    - MLRecommendationEngine (Methods: 7, Documented: Yes)

codebase_analyzer/recommendations/prompt_manager.py
  Size: 4.1 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - _load_templates (Lines: 17, Documented: Yes)
    - _merge_templates (Lines: 10, Documented: Yes)
    - _initialize_variables (Lines: 8, Documented: Yes)
    - set_variable (Lines: 3, Documented: Yes)
    - get_prompt (Lines: 18, Documented: Yes)
    - _get_template (Lines: 10, Documented: Yes)
    - add_template (Lines: 9, Documented: Yes)
    - list_templates (Lines: 5, Documented: Yes)
    - _collect_templates (Lines: 9, Documented: Yes)
  Classes:
    - PromptManager (Methods: 10, Documented: Yes)

codebase_analyzer/recommendations/recommendation_engine.py
  Size: 6.5 KB
  Functions:
    - __post_init__ (Lines: 2, Documented: No)
    - generate_recommendations (Lines: 19, Documented: Yes)
    - _analyze_complexity_metrics (Lines: 25, Documented: Yes)
    - _analyze_quality_metrics (Lines: 30, Documented: Yes)
    - _analyze_dependency_metrics (Lines: 9, Documented: Yes)
    - _analyze_pattern_metrics (Lines: 9, Documented: Yes)
    - _analyze_security_metrics (Lines: 16, Documented: Yes)
    - _analyze_performance_metrics (Lines: 16, Documented: Yes)
  Classes:
    - RecommendationEngine (Methods: 8, Documented: Yes)

codebase_analyzer/analyzers/base_analyzer.py
  Size: 0.9 KB
  Functions:
    - __init__ (Lines: 7, Documented: Yes)
    - analyze (Lines: 7, Documented: Yes)
    - get_file_type (Lines: 7, Documented: Yes)
  Classes:
    - BaseAnalyzer (Methods: 3, Documented: Yes)

codebase_analyzer/analyzers/project_analyzer.py
  Size: 8.9 KB
  Functions:
    - __init__ (Lines: 11, Documented: Yes)
    - _hash_requirements (Lines: 13, Documented: Yes)
    - _load_dependency_cache (Lines: 17, Documented: Yes)
    - _save_dependency_cache (Lines: 16, Documented: Yes)
    - _check_dependency_health (Lines: 69, Documented: Yes)
    - analyze (Lines: 48, Documented: Yes)
  Classes:
    - ProjectAnalyzer (Methods: 6, Documented: Yes)

codebase_analyzer/analyzers/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer/analyzers/python_analyzer.py
  Size: 7.4 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - get_file_type (Lines: 7, Documented: Yes)
    - analyze (Lines: 134, Documented: Yes)
    - _read_file (Lines: 11, Documented: Yes)
    - _count_lines (Lines: 12, Documented: Yes)
  Classes:
    - PythonAnalyzer (Methods: 5, Documented: Yes)

codebase_analyzer/analyzers/generic_analyzer.py
  Size: 1.6 KB
  Functions:
    - __init__ (Lines: 2, Documented: No)
    - get_file_type (Lines: 8, Documented: Yes)
    - analyze (Lines: 29, Documented: Yes)
  Classes:
    - GenericAnalyzer (Methods: 3, Documented: Yes)

codebase_analyzer/features/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

codebase_analyzer/features/base.py
  Size: 0.9 KB
  Functions:
    - extract (Lines: 3, Documented: Yes)
    - get_feature_names (Lines: 3, Documented: Yes)
  Classes:
    - CodeFeatures (Methods: 0, Documented: Yes)
    - FeatureExtractor (Methods: 2, Documented: Yes)

codebase_analyzer/features/performance.py
  Size: 19.6 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - extract (Lines: 22, Documented: No)
    - get_feature_names (Lines: 15, Documented: No)
    - _analyze_complexity (Lines: 62, Documented: No)
    - _analyze_memory_usage (Lines: 48, Documented: No)
    - _analyze_io_operations (Lines: 48, Documented: No)
    - _analyze_caching (Lines: 40, Documented: No)
    - _analyze_bottlenecks (Lines: 53, Documented: No)
    - _analyze_async_patterns (Lines: 51, Documented: No)
    - _estimate_time_complexity (Lines: 9, Documented: No)
    - _estimate_space_complexity (Lines: 7, Documented: No)
    - _calculate_performance_score (Lines: 20, Documented: No)
    - _score_complexity (Lines: 20, Documented: No)
    - _score_memory (Lines: 6, Documented: No)
    - _score_io (Lines: 9, Documented: No)
    - _get_default_metrics (Lines: 49, Documented: No)
    - visit_For (Lines: 2, Documented: No)
    - visit_While (Lines: 2, Documented: No)
    - _handle_loop (Lines: 5, Documented: No)
    - visit_ListComp (Lines: 3, Documented: No)
    - visit_GeneratorExp (Lines: 3, Documented: No)
    - visit_FunctionDef (Lines: 4, Documented: No)
    - visit_List (Lines: 7, Documented: No)
    - visit_Dict (Lines: 7, Documented: No)
    - visit_Call (Lines: 4, Documented: No)
    - get_opportunities (Lines: 6, Documented: No)
    - visit (Lines: 18, Documented: No)
    - _get_recommendation (Lines: 8, Documented: No)
    - visit_AsyncFunctionDef (Lines: 6, Documented: No)
    - visit_Await (Lines: 5, Documented: No)
    - visit_AsyncWith (Lines: 5, Documented: No)
    - visit_AsyncFor (Lines: 5, Documented: No)
  Classes:
    - PerformanceIssue (Methods: 0, Documented: Yes)
    - PerformanceFeatureExtractor (Methods: 16, Documented: Yes)
    - ComplexityVisitor (Methods: 7, Documented: No)
    - MemoryVisitor (Methods: 5, Documented: No)
    - IOVisitor (Methods: 2, Documented: No)
    - CachingVisitor (Methods: 3, Documented: No)
    - BottleneckVisitor (Methods: 3, Documented: No)
    - AsyncVisitor (Methods: 5, Documented: No)
    - RecursionDetector (Methods: 2, Documented: No)

codebase_analyzer/features/security.py
  Size: 15.9 KB
  Functions:
    - __init__ (Lines: 4, Documented: No)
    - extract (Lines: 22, Documented: No)
    - get_feature_names (Lines: 16, Documented: No)
    - _analyze_vulnerabilities (Lines: 71, Documented: No)
    - _analyze_sensitive_data (Lines: 35, Documented: No)
    - _analyze_security_patterns (Lines: 45, Documented: No)
    - _analyze_input_validation (Lines: 28, Documented: No)
    - _analyze_authentication (Lines: 30, Documented: No)
    - _analyze_crypto_usage (Lines: 37, Documented: No)
    - _calculate_security_score (Lines: 20, Documented: No)
    - _get_default_metrics (Lines: 43, Documented: No)
    - visit_Call (Lines: 9, Documented: No)
    - _get_vulnerability_description (Lines: 9, Documented: No)
    - _get_recommendation (Lines: 9, Documented: No)
    - visit_Assign (Lines: 17, Documented: No)
  Classes:
    - SecurityIssue (Methods: 0, Documented: Yes)
    - SecurityFeatureExtractor (Methods: 11, Documented: Yes)
    - VulnerabilityVisitor (Methods: 4, Documented: No)
    - SensitiveDataVisitor (Methods: 2, Documented: No)
    - SecurityPatternVisitor (Methods: 2, Documented: No)
    - InputValidationVisitor (Methods: 2, Documented: No)
    - AuthenticationVisitor (Methods: 1, Documented: No)

codebase_analyzer/features/complexity.py
  Size: 6.1 KB
  Functions:
    - extract (Lines: 33, Documented: No)
    - get_feature_names (Lines: 15, Documented: No)
    - _calculate_mean_complexity (Lines: 4, Documented: No)
    - _calculate_max_complexity (Lines: 4, Documented: No)
    - _get_complexity_distribution (Lines: 14, Documented: No)
    - _calculate_cognitive_complexity (Lines: 33, Documented: No)
    - _calculate_halstead_metrics (Lines: 12, Documented: No)
    - _calculate_avg_function_length (Lines: 4, Documented: No)
    - _get_default_metrics (Lines: 23, Documented: No)
    - __init__ (Lines: 3, Documented: No)
    - visit_If (Lines: 5, Documented: No)
    - visit_While (Lines: 5, Documented: No)
    - visit_For (Lines: 5, Documented: No)
    - visit_Try (Lines: 5, Documented: No)
  Classes:
    - ComplexityFeatureExtractor (Methods: 9, Documented: Yes)
    - CognitiveComplexityVisitor (Methods: 5, Documented: No)

codebase_analyzer/features/manager.py
  Size: 21.4 KB
  Functions:
    - __init__ (Lines: 7, Documented: No)
    - extract_all (Lines: 33, Documented: Yes)
    - _extract_safely (Lines: 7, Documented: Yes)
    - _get_default_metrics (Lines: 6, Documented: Yes)
    - _create_analysis_report (Lines: 18, Documented: Yes)
    - _calculate_overall_score (Lines: 15, Documented: Yes)
    - _generate_summary (Lines: 24, Documented: Yes)
    - _get_complexity_highlights (Lines: 10, Documented: Yes)
    - _get_quality_highlights (Lines: 10, Documented: Yes)
    - _get_security_highlights (Lines: 12, Documented: Yes)
    - _get_performance_highlights (Lines: 12, Documented: Yes)
    - _generate_recommendations (Lines: 24, Documented: Yes)
    - _get_complexity_recommendations (Lines: 28, Documented: Yes)
    - _get_quality_recommendations (Lines: 30, Documented: Yes)
    - _get_security_recommendations (Lines: 28, Documented: Yes)
    - _get_performance_recommendations (Lines: 28, Documented: Yes)
    - export_results (Lines: 27, Documented: Yes)
    - _generate_html_report (Lines: 86, Documented: Yes)
    - _generate_score_section (Lines: 7, Documented: Yes)
    - _generate_metrics_section (Lines: 25, Documented: Yes)
    - _generate_recommendations_section (Lines: 20, Documented: Yes)
    - _generate_details_section (Lines: 24, Documented: Yes)
    - _generate_metadata_section (Lines: 14, Documented: Yes)
  Classes:
    - FeatureExtractorManager (Methods: 23, Documented: Yes)

codebase_analyzer/features/quality.py
  Size: 15.9 KB
  Functions:
    - extract (Lines: 13, Documented: No)
    - get_feature_names (Lines: 17, Documented: No)
    - _analyze_documentation (Lines: 54, Documented: No)
    - _analyze_naming (Lines: 78, Documented: No)
    - _analyze_structure (Lines: 48, Documented: No)
    - _analyze_type_hints (Lines: 45, Documented: No)
    - _analyze_test_coverage (Lines: 21, Documented: No)
    - _analyze_code_smells (Lines: 61, Documented: No)
    - _calculate_coverage (Lines: 2, Documented: No)
    - _safe_mean (Lines: 2, Documented: No)
    - _calculate_test_quality (Lines: 9, Documented: No)
    - _calculate_smell_severity (Lines: 12, Documented: No)
    - _get_default_metrics (Lines: 46, Documented: No)
    - __init__ (Lines: 3, Documented: No)
    - visit_FunctionDef (Lines: 20, Documented: No)
    - visit_ClassDef (Lines: 9, Documented: No)
    - _assess_docstring_quality (Lines: 10, Documented: No)
    - visit_Name (Lines: 7, Documented: No)
    - _check_naming_convention (Lines: 23, Documented: No)
    - get_consistency_score (Lines: 8, Documented: No)
    - _get_name_pattern (Lines: 8, Documented: No)
    - visit_If (Lines: 2, Documented: No)
    - visit_For (Lines: 2, Documented: No)
    - visit_While (Lines: 2, Documented: No)
    - _handle_nesting (Lines: 5, Documented: No)
  Classes:
    - QualityFeatureExtractor (Methods: 13, Documented: Yes)
    - DocVisitor (Methods: 4, Documented: No)
    - NamingVisitor (Methods: 7, Documented: No)
    - StructureVisitor (Methods: 7, Documented: No)
    - TypeHintVisitor (Methods: 2, Documented: No)
    - SmellVisitor (Methods: 3, Documented: No)

build/lib/tests/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/tests/conftest.py
  Size: 0.9 KB
  Functions:
    - sample_codebase (Lines: 16, Documented: Yes)
    - analyzer (Lines: 4, Documented: Yes)

build/lib/tests/helpers.py
  Size: 1.0 KB
  Functions:
    - create_temp_file (Lines: 6, Documented: Yes)
    - create_temp_project (Lines: 8, Documented: Yes)
    - cleanup_temp (Lines: 6, Documented: Yes)
  Classes:
    - TestHelper (Methods: 3, Documented: No)

build/lib/tests/unit/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/tests/unit/test_analyzers/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/tests/unit/test_analyzers/test_python_analyzer.py
  Size: 2.5 KB
  Functions:
    - setup_method (Lines: 4, Documented: No)
    - test_analyze_empty_file (Lines: 6, Documented: No)
    - test_analyze_simple_function (Lines: 13, Documented: No)
    - test_analyze_complex_function (Lines: 16, Documented: No)
    - test_analyze_dependencies (Lines: 14, Documented: No)
    - teardown_method (Lines: 3, Documented: No)
  Classes:
    - TestPythonAnalyzer (Methods: 6, Documented: No)

build/lib/tests/unit/test_analyzers/test_project_analyzer.py
  Size: 4.5 KB
  Functions:
    - setup_method (Lines: 2, Documented: No)
    - test_project_analyzer_empty_directory (Lines: 15, Documented: Yes)
    - test_project_analyzer_with_files (Lines: 34, Documented: Yes)
    - test_project_analyzer_with_complex_structure (Lines: 51, Documented: Yes)
    - test_project_analyzer_with_non_python_files (Lines: 29, Documented: Yes)
    - teardown_method (Lines: 3, Documented: Yes)
  Classes:
    - TestProjectAnalyzer (Methods: 6, Documented: No)

build/lib/tests/unit/test_analyzers/test_codebase_analyzer.py
  Size: 3.9 KB
  Functions:
    - setup_method (Lines: 3, Documented: No)
    - test_analyze_project_simple (Lines: 28, Documented: Yes)
    - test_analyze_project_with_complexity (Lines: 18, Documented: Yes)
    - test_analyze_project_with_vulnerabilities (Lines: 10, Documented: Yes)
    - test_analyze_project_empty (Lines: 8, Documented: Yes)
    - test_generate_summary_no_analysis (Lines: 5, Documented: Yes)
    - test_generate_summary_after_analysis (Lines: 15, Documented: Yes)
    - test_analyze_project_invalid_path (Lines: 8, Documented: Yes)
  Classes:
    - TestCodebaseAnalyzer (Methods: 8, Documented: No)

build/lib/tests/integration/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/tests/integration/test_integration.py
  Size: 1.2 KB
  Functions:
    - setup_method (Lines: 2, Documented: No)
    - test_full_analysis (Lines: 31, Documented: Yes)
  Classes:
    - TestIntegration (Methods: 2, Documented: No)

build/lib/codebase_analyzer/__init__.py
  Size: 0.1 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/main.py
  Size: 0.8 KB
  Functions:
    - main (Lines: 14, Documented: Yes)

build/lib/codebase_analyzer/__main__.py
  Size: 0.1 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/analyzer.py
  Size: 3.6 KB
  Functions:
    - __init__ (Lines: 12, Documented: Yes)
    - analyze_project (Lines: 31, Documented: Yes)
    - generate_summary (Lines: 13, Documented: Yes)
  Classes:
    - CodebaseAnalyzer (Methods: 3, Documented: No)

build/lib/codebase_analyzer/utils/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/utils/file_utils.py
  Size: 3.6 KB
  Functions:
    - should_analyze_file (Lines: 20, Documented: Yes)
    - get_file_type (Lines: 26, Documented: Yes)
    - safe_read_file (Lines: 26, Documented: Yes)
    - save_to_file (Lines: 16, Documented: Yes)
    - generate_tree_structure (Lines: 19, Documented: Yes)

build/lib/codebase_analyzer/models/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/models/data_classes.py
  Size: 4.7 KB
  Functions:
    - __post_init__ (Lines: 3, Documented: No)
    - calculate_overall_score (Lines: 29, Documented: Yes)
  Classes:
    - FunctionInfo (Methods: 1, Documented: Yes)
    - MethodInfo (Methods: 0, Documented: Yes)
    - ClassInfo (Methods: 1, Documented: Yes)
    - FileInfo (Methods: 1, Documented: Yes)
    - ProjectMetrics (Methods: 2, Documented: Yes)
    - Recommendation (Methods: 1, Documented: Yes)

build/lib/codebase_analyzer/formatters/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/formatters/comprehensive_formatter.py
  Size: 12.8 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - _setup_colors (Lines: 14, Documented: Yes)
    - format_analysis (Lines: 24, Documented: Yes)
    - _format_project_overview (Lines: 16, Documented: Yes)
    - _format_executive_summary (Lines: 21, Documented: Yes)
    - _format_complexity_analysis (Lines: 21, Documented: Yes)
    - _format_quality_analysis (Lines: 20, Documented: Yes)
    - _format_security_analysis (Lines: 23, Documented: Yes)
    - _format_performance_analysis (Lines: 20, Documented: Yes)
    - _format_dependency_analysis (Lines: 20, Documented: Yes)
    - _format_pattern_analysis (Lines: 19, Documented: Yes)
    - _format_recommendations (Lines: 17, Documented: Yes)
    - _format_score (Lines: 11, Documented: Yes)
    - _format_header (Lines: 8, Documented: Yes)
    - _get_critical_findings (Lines: 20, Documented: Yes)
    - _get_prioritized_recommendations (Lines: 24, Documented: Yes)
    - _group_by_severity (Lines: 10, Documented: Yes)
  Classes:
    - FormattingOptions (Methods: 0, Documented: Yes)
    - ComprehensiveFormatter (Methods: 17, Documented: Yes)

build/lib/codebase_analyzer/formatters/summary_formatter.py
  Size: 7.1 KB
  Functions:
    - __init__ (Lines: 28, Documented: Yes)
    - add_source_file (Lines: 45, Documented: Yes)
    - generate_summary (Lines: 63, Documented: Yes)
    - _format_file_structure (Lines: 17, Documented: Yes)
  Classes:
    - SummaryFormatter (Methods: 4, Documented: Yes)

build/lib/codebase_analyzer/metrics/__init__.py
  Size: 0.6 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/metrics/dependency_metrics.py
  Size: 4.1 KB
  Functions:
    - health_score (Lines: 6, Documented: Yes)
    - analyze_project (Lines: 74, Documented: Yes)
  Classes:
    - DependencyMetrics (Methods: 1, Documented: Yes)
    - DependencyAnalyzer (Methods: 1, Documented: Yes)

build/lib/codebase_analyzer/metrics/security_metrics.py
  Size: 8.4 KB
  Functions:
    - __init__ (Lines: 2, Documented: No)
    - analyze_project (Lines: 18, Documented: Yes)
    - _detect_vulnerabilities (Lines: 10, Documented: Yes)
    - _check_for_insecure_functions (Lines: 40, Documented: Yes)
    - _detect_security_patterns (Lines: 18, Documented: Yes)
    - _check_authentication_pattern (Lines: 38, Documented: Yes)
    - _check_input_validation (Lines: 37, Documented: Yes)
    - _calculate_security_score (Lines: 23, Documented: Yes)
    - visit_Call (Lines: 6, Documented: No)
    - visit_Import (Lines: 5, Documented: No)
    - visit_If (Lines: 4, Documented: No)
  Classes:
    - Vulnerability (Methods: 0, Documented: No)
    - SecurityPattern (Methods: 0, Documented: No)
    - SecurityMetrics (Methods: 0, Documented: No)
    - SecurityAnalyzer (Methods: 8, Documented: Yes)
    - InsecureFunctionVisitor (Methods: 2, Documented: No)
    - AuthVisitor (Methods: 3, Documented: No)
    - ValidationVisitor (Methods: 3, Documented: No)

build/lib/codebase_analyzer/metrics/quality_metrics.py
  Size: 9.9 KB
  Functions:
    - quality_score (Lines: 21, Documented: Yes)
    - analyze_project (Lines: 45, Documented: Yes)
    - analyze_node (Lines: 14, Documented: Yes)
    - _calculate_type_hint_coverage (Lines: 32, Documented: Yes)
    - _calculate_documentation_coverage (Lines: 32, Documented: Yes)
    - _calculate_code_comment_ratio (Lines: 17, Documented: Yes)
    - _calculate_lint_score (Lines: 28, Documented: Yes)
    - _estimate_test_coverage (Lines: 3, Documented: Yes)
    - _run_coverage (Lines: 46, Documented: Yes)
    - __init__ (Lines: 3, Documented: No)
    - visit_FunctionDef (Lines: 9, Documented: No)
    - visit_AnnAssign (Lines: 4, Documented: No)
    - visit_ClassDef (Lines: 5, Documented: No)
    - visit_Module (Lines: 5, Documented: No)
    - visit (Lines: 5, Documented: No)
    - visit_Try (Lines: 7, Documented: No)
  Classes:
    - QualityMetrics (Methods: 1, Documented: Yes)
    - QualityAnalyzer (Methods: 8, Documented: Yes)
    - TypeHintVisitor (Methods: 3, Documented: No)
    - DocVisitor (Methods: 4, Documented: No)
    - CommentVisitor (Methods: 1, Documented: No)
    - LintVisitor (Methods: 2, Documented: No)

build/lib/codebase_analyzer/metrics/pattern_metrics.py
  Size: 15.4 KB
  Functions:
    - __init__ (Lines: 4, Documented: No)
    - analyze_project (Lines: 15, Documented: Yes)
    - _detect_design_patterns (Lines: 19, Documented: Yes)
    - _detect_singleton_pattern (Lines: 36, Documented: Yes)
    - _detect_factory_pattern (Lines: 40, Documented: Yes)
    - _detect_strategy_pattern (Lines: 31, Documented: Yes)
    - _detect_observer_pattern (Lines: 31, Documented: Yes)
    - _detect_decorator_pattern (Lines: 31, Documented: Yes)
    - _detect_adapter_pattern (Lines: 33, Documented: Yes)
    - _analyze_architecture (Lines: 4, Documented: Yes)
    - _analyze_layered_architecture (Lines: 14, Documented: Yes)
    - _determine_architecture_style (Lines: 16, Documented: Yes)
    - _detect_api_patterns (Lines: 3, Documented: Yes)
    - _detect_database_patterns (Lines: 3, Documented: Yes)
    - _detect_anti_patterns (Lines: 3, Documented: Yes)
    - get_pattern_summary (Lines: 27, Documented: Yes)
    - visit_ClassDef (Lines: 12, Documented: No)
    - _find_return_types (Lines: 8, Documented: No)
  Classes:
    - DesignPattern (Methods: 0, Documented: No)
    - ArchitecturalStyle (Methods: 0, Documented: No)
    - PatternMetrics (Methods: 0, Documented: No)
    - PatternAnalyzer (Methods: 16, Documented: Yes)
    - SingletonVisitor (Methods: 2, Documented: No)
    - FactoryVisitor (Methods: 3, Documented: No)
    - StrategyVisitor (Methods: 2, Documented: No)
    - ObserverVisitor (Methods: 2, Documented: No)
    - DecoratorVisitor (Methods: 2, Documented: No)
    - AdapterVisitor (Methods: 2, Documented: No)

build/lib/codebase_analyzer/metrics/complexity_analyzer.py
  Size: 4.8 KB
  Functions:
    - analyze_project (Lines: 38, Documented: Yes)
    - _analyze_complexity (Lines: 65, Documented: Yes)
    - __init__ (Lines: 4, Documented: No)
    - visit_FunctionDef (Lines: 21, Documented: No)
    - visit_If (Lines: 3, Documented: No)
    - visit_For (Lines: 3, Documented: No)
    - visit_While (Lines: 3, Documented: No)
    - visit_Try (Lines: 3, Documented: No)
    - visit_With (Lines: 3, Documented: No)
    - visit_BoolOp (Lines: 3, Documented: No)
  Classes:
    - ComplexityMetrics (Methods: 0, Documented: Yes)
    - ComplexityAnalyzer (Methods: 2, Documented: Yes)
    - ComplexityVisitor (Methods: 8, Documented: No)

build/lib/codebase_analyzer/metrics/performance_metrics.py
  Size: 12.0 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - analyze_project (Lines: 22, Documented: Yes)
    - _identify_hotspots (Lines: 10, Documented: Yes)
    - _analyze_hotspots (Lines: 43, Documented: Yes)
    - _identify_optimization_opportunities (Lines: 10, Documented: Yes)
    - _analyze_optimizations (Lines: 47, Documented: Yes)
    - _detect_memory_intensive_operations (Lines: 10, Documented: Yes)
    - _analyze_memory_ops (Lines: 23, Documented: Yes)
    - _detect_io_operations (Lines: 10, Documented: Yes)
    - _analyze_io_ops (Lines: 21, Documented: Yes)
    - _calculate_performance_score (Lines: 16, Documented: Yes)
    - visit_For (Lines: 14, Documented: No)
    - visit_While (Lines: 10, Documented: No)
    - _calculate_complexity (Lines: 6, Documented: No)
    - visit_ListComp (Lines: 3, Documented: No)
    - visit_Call (Lines: 6, Documented: No)
  Classes:
    - PerformanceHotspot (Methods: 0, Documented: Yes)
    - LoopOptimization (Methods: 0, Documented: Yes)
    - PerformanceMetrics (Methods: 0, Documented: Yes)
    - PerformanceAnalyzer (Methods: 11, Documented: Yes)
    - HotspotVisitor (Methods: 4, Documented: No)
    - OptimizationVisitor (Methods: 4, Documented: No)
    - MemoryVisitor (Methods: 3, Documented: No)
    - IOVisitor (Methods: 2, Documented: No)

build/lib/codebase_analyzer/recommendations/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/recommendations/ml_engine.py
  Size: 8.4 KB
  Functions:
    - analyze (Lines: 15, Documented: Yes)
    - train (Lines: 3, Documented: Yes)
    - save (Lines: 7, Documented: Yes)
    - load (Lines: 6, Documented: Yes)
    - __init__ (Lines: 4, Documented: No)
    - _process_features (Lines: 6, Documented: Yes)
    - _initialize_feature_extractors (Lines: 8, Documented: Yes)
    - _extract_complexity_features (Lines: 7, Documented: Yes)
    - _call_llm_api (Lines: 8, Documented: Yes)
    - _load_prompt_templates (Lines: 5, Documented: Yes)
    - _initialize_models (Lines: 12, Documented: Yes)
    - add_model (Lines: 3, Documented: Yes)
    - remove_model (Lines: 3, Documented: Yes)
    - _aggregate_recommendations (Lines: 21, Documented: Yes)
    - _merge_recommendations (Lines: 14, Documented: Yes)
  Classes:
    - MLRecommendation (Methods: 0, Documented: Yes)
    - ModelInterface (Methods: 4, Documented: Yes)
    - LocalMLModel (Methods: 8, Documented: Yes)
    - LLMInterface (Methods: 3, Documented: Yes)
    - ClaudeInterface (Methods: 6, Documented: Yes)
    - MLRecommendationEngine (Methods: 7, Documented: Yes)

build/lib/codebase_analyzer/recommendations/prompt_manager.py
  Size: 4.1 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - _load_templates (Lines: 17, Documented: Yes)
    - _merge_templates (Lines: 10, Documented: Yes)
    - _initialize_variables (Lines: 8, Documented: Yes)
    - set_variable (Lines: 3, Documented: Yes)
    - get_prompt (Lines: 18, Documented: Yes)
    - _get_template (Lines: 10, Documented: Yes)
    - add_template (Lines: 9, Documented: Yes)
    - list_templates (Lines: 5, Documented: Yes)
    - _collect_templates (Lines: 9, Documented: Yes)
  Classes:
    - PromptManager (Methods: 10, Documented: Yes)

build/lib/codebase_analyzer/recommendations/recommendation_engine.py
  Size: 6.5 KB
  Functions:
    - __post_init__ (Lines: 2, Documented: No)
    - generate_recommendations (Lines: 19, Documented: Yes)
    - _analyze_complexity_metrics (Lines: 25, Documented: Yes)
    - _analyze_quality_metrics (Lines: 30, Documented: Yes)
    - _analyze_dependency_metrics (Lines: 9, Documented: Yes)
    - _analyze_pattern_metrics (Lines: 9, Documented: Yes)
    - _analyze_security_metrics (Lines: 16, Documented: Yes)
    - _analyze_performance_metrics (Lines: 16, Documented: Yes)
  Classes:
    - RecommendationEngine (Methods: 8, Documented: Yes)

build/lib/codebase_analyzer/analyzers/base_analyzer.py
  Size: 0.9 KB
  Functions:
    - __init__ (Lines: 7, Documented: Yes)
    - analyze (Lines: 7, Documented: Yes)
    - get_file_type (Lines: 7, Documented: Yes)
  Classes:
    - BaseAnalyzer (Methods: 3, Documented: Yes)

build/lib/codebase_analyzer/analyzers/project_analyzer.py
  Size: 8.9 KB
  Functions:
    - __init__ (Lines: 11, Documented: Yes)
    - _hash_requirements (Lines: 13, Documented: Yes)
    - _load_dependency_cache (Lines: 17, Documented: Yes)
    - _save_dependency_cache (Lines: 16, Documented: Yes)
    - _check_dependency_health (Lines: 69, Documented: Yes)
    - analyze (Lines: 48, Documented: Yes)
  Classes:
    - ProjectAnalyzer (Methods: 6, Documented: Yes)

build/lib/codebase_analyzer/analyzers/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/analyzers/python_analyzer.py
  Size: 7.8 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - get_file_type (Lines: 7, Documented: Yes)
    - analyze (Lines: 142, Documented: Yes)
    - _read_file (Lines: 11, Documented: Yes)
    - _count_lines (Lines: 12, Documented: Yes)
  Classes:
    - PythonAnalyzer (Methods: 5, Documented: Yes)

build/lib/codebase_analyzer/analyzers/generic_analyzer.py
  Size: 1.4 KB
  Functions:
    - __init__ (Lines: 2, Documented: No)
    - get_file_type (Lines: 8, Documented: Yes)
    - analyze (Lines: 18, Documented: Yes)
  Classes:
    - GenericAnalyzer (Methods: 3, Documented: Yes)

build/lib/codebase_analyzer/features/__init__.py
  Size: 0.0 KB
  (Empty or initialization file)

build/lib/codebase_analyzer/features/base.py
  Size: 0.9 KB
  Functions:
    - extract (Lines: 3, Documented: Yes)
    - get_feature_names (Lines: 3, Documented: Yes)
  Classes:
    - CodeFeatures (Methods: 0, Documented: Yes)
    - FeatureExtractor (Methods: 2, Documented: Yes)

build/lib/codebase_analyzer/features/performance.py
  Size: 19.6 KB
  Functions:
    - __init__ (Lines: 3, Documented: No)
    - extract (Lines: 22, Documented: No)
    - get_feature_names (Lines: 15, Documented: No)
    - _analyze_complexity (Lines: 62, Documented: No)
    - _analyze_memory_usage (Lines: 48, Documented: No)
    - _analyze_io_operations (Lines: 48, Documented: No)
    - _analyze_caching (Lines: 40, Documented: No)
    - _analyze_bottlenecks (Lines: 53, Documented: No)
    - _analyze_async_patterns (Lines: 51, Documented: No)
    - _estimate_time_complexity (Lines: 9, Documented: No)
    - _estimate_space_complexity (Lines: 7, Documented: No)
    - _calculate_performance_score (Lines: 20, Documented: No)
    - _score_complexity (Lines: 20, Documented: No)
    - _score_memory (Lines: 6, Documented: No)
    - _score_io (Lines: 9, Documented: No)
    - _get_default_metrics (Lines: 49, Documented: No)
    - visit_For (Lines: 2, Documented: No)
    - visit_While (Lines: 2, Documented: No)
    - _handle_loop (Lines: 5, Documented: No)
    - visit_ListComp (Lines: 3, Documented: No)
    - visit_GeneratorExp (Lines: 3, Documented: No)
    - visit_FunctionDef (Lines: 4, Documented: No)
    - visit_List (Lines: 7, Documented: No)
    - visit_Dict (Lines: 7, Documented: No)
    - visit_Call (Lines: 4, Documented: No)
    - get_opportunities (Lines: 6, Documented: No)
    - visit (Lines: 18, Documented: No)
    - _get_recommendation (Lines: 8, Documented: No)
    - visit_AsyncFunctionDef (Lines: 6, Documented: No)
    - visit_Await (Lines: 5, Documented: No)
    - visit_AsyncWith (Lines: 5, Documented: No)
    - visit_AsyncFor (Lines: 5, Documented: No)
  Classes:
    - PerformanceIssue (Methods: 0, Documented: Yes)
    - PerformanceFeatureExtractor (Methods: 16, Documented: Yes)
    - ComplexityVisitor (Methods: 7, Documented: No)
    - MemoryVisitor (Methods: 5, Documented: No)
    - IOVisitor (Methods: 2, Documented: No)
    - CachingVisitor (Methods: 3, Documented: No)
    - BottleneckVisitor (Methods: 3, Documented: No)
    - AsyncVisitor (Methods: 5, Documented: No)
    - RecursionDetector (Methods: 2, Documented: No)

build/lib/codebase_analyzer/features/security.py
  Size: 15.9 KB
  Functions:
    - __init__ (Lines: 4, Documented: No)
    - extract (Lines: 22, Documented: No)
    - get_feature_names (Lines: 16, Documented: No)
    - _analyze_vulnerabilities (Lines: 71, Documented: No)
    - _analyze_sensitive_data (Lines: 35, Documented: No)
    - _analyze_security_patterns (Lines: 45, Documented: No)
    - _analyze_input_validation (Lines: 28, Documented: No)
    - _analyze_authentication (Lines: 30, Documented: No)
    - _analyze_crypto_usage (Lines: 37, Documented: No)
    - _calculate_security_score (Lines: 20, Documented: No)
    - _get_default_metrics (Lines: 43, Documented: No)
    - visit_Call (Lines: 9, Documented: No)
    - _get_vulnerability_description (Lines: 9, Documented: No)
    - _get_recommendation (Lines: 9, Documented: No)
    - visit_Assign (Lines: 17, Documented: No)
  Classes:
    - SecurityIssue (Methods: 0, Documented: Yes)
    - SecurityFeatureExtractor (Methods: 11, Documented: Yes)
    - VulnerabilityVisitor (Methods: 4, Documented: No)
    - SensitiveDataVisitor (Methods: 2, Documented: No)
    - SecurityPatternVisitor (Methods: 2, Documented: No)
    - InputValidationVisitor (Methods: 2, Documented: No)
    - AuthenticationVisitor (Methods: 1, Documented: No)

build/lib/codebase_analyzer/features/complexity.py
  Size: 6.1 KB
  Functions:
    - extract (Lines: 33, Documented: No)
    - get_feature_names (Lines: 15, Documented: No)
    - _calculate_mean_complexity (Lines: 4, Documented: No)
    - _calculate_max_complexity (Lines: 4, Documented: No)
    - _get_complexity_distribution (Lines: 14, Documented: No)
    - _calculate_cognitive_complexity (Lines: 33, Documented: No)
    - _calculate_halstead_metrics (Lines: 12, Documented: No)
    - _calculate_avg_function_length (Lines: 4, Documented: No)
    - _get_default_metrics (Lines: 23, Documented: No)
    - __init__ (Lines: 3, Documented: No)
    - visit_If (Lines: 5, Documented: No)
    - visit_While (Lines: 5, Documented: No)
    - visit_For (Lines: 5, Documented: No)
    - visit_Try (Lines: 5, Documented: No)
  Classes:
    - ComplexityFeatureExtractor (Methods: 9, Documented: Yes)
    - CognitiveComplexityVisitor (Methods: 5, Documented: No)

build/lib/codebase_analyzer/features/manager.py
  Size: 21.4 KB
  Functions:
    - __init__ (Lines: 7, Documented: No)
    - extract_all (Lines: 33, Documented: Yes)
    - _extract_safely (Lines: 7, Documented: Yes)
    - _get_default_metrics (Lines: 6, Documented: Yes)
    - _create_analysis_report (Lines: 18, Documented: Yes)
    - _calculate_overall_score (Lines: 15, Documented: Yes)
    - _generate_summary (Lines: 24, Documented: Yes)
    - _get_complexity_highlights (Lines: 10, Documented: Yes)
    - _get_quality_highlights (Lines: 10, Documented: Yes)
    - _get_security_highlights (Lines: 12, Documented: Yes)
    - _get_performance_highlights (Lines: 12, Documented: Yes)
    - _generate_recommendations (Lines: 24, Documented: Yes)
    - _get_complexity_recommendations (Lines: 28, Documented: Yes)
    - _get_quality_recommendations (Lines: 30, Documented: Yes)
    - _get_security_recommendations (Lines: 28, Documented: Yes)
    - _get_performance_recommendations (Lines: 28, Documented: Yes)
    - export_results (Lines: 27, Documented: Yes)
    - _generate_html_report (Lines: 86, Documented: Yes)
    - _generate_score_section (Lines: 7, Documented: Yes)
    - _generate_metrics_section (Lines: 25, Documented: Yes)
    - _generate_recommendations_section (Lines: 20, Documented: Yes)
    - _generate_details_section (Lines: 24, Documented: Yes)
    - _generate_metadata_section (Lines: 14, Documented: Yes)
  Classes:
    - FeatureExtractorManager (Methods: 23, Documented: Yes)

build/lib/codebase_analyzer/features/quality.py
  Size: 15.9 KB
  Functions:
    - extract (Lines: 13, Documented: No)
    - get_feature_names (Lines: 17, Documented: No)
    - _analyze_documentation (Lines: 54, Documented: No)
    - _analyze_naming (Lines: 78, Documented: No)
    - _analyze_structure (Lines: 48, Documented: No)
    - _analyze_type_hints (Lines: 45, Documented: No)
    - _analyze_test_coverage (Lines: 21, Documented: No)
    - _analyze_code_smells (Lines: 61, Documented: No)
    - _calculate_coverage (Lines: 2, Documented: No)
    - _safe_mean (Lines: 2, Documented: No)
    - _calculate_test_quality (Lines: 9, Documented: No)
    - _calculate_smell_severity (Lines: 12, Documented: No)
    - _get_default_metrics (Lines: 46, Documented: No)
    - __init__ (Lines: 3, Documented: No)
    - visit_FunctionDef (Lines: 20, Documented: No)
    - visit_ClassDef (Lines: 9, Documented: No)
    - _assess_docstring_quality (Lines: 10, Documented: No)
    - visit_Name (Lines: 7, Documented: No)
    - _check_naming_convention (Lines: 23, Documented: No)
    - get_consistency_score (Lines: 8, Documented: No)
    - _get_name_pattern (Lines: 8, Documented: No)
    - visit_If (Lines: 2, Documented: No)
    - visit_For (Lines: 2, Documented: No)
    - visit_While (Lines: 2, Documented: No)
    - _handle_nesting (Lines: 5, Documented: No)
  Classes:
    - QualityFeatureExtractor (Methods: 13, Documented: Yes)
    - DocVisitor (Methods: 4, Documented: No)
    - NamingVisitor (Methods: 7, Documented: No)
    - StructureVisitor (Methods: 7, Documented: No)
    - TypeHintVisitor (Methods: 2, Documented: No)
    - SmellVisitor (Methods: 3, Documented: No)

Dependencies
------------

Required:
  - abc
  - analyzer
  - analyzers
  - argparse
  - ast
  - base
  - base_analyzer
  - click
  - codebase_analyzer
  - collections
  - complexity
  - complexity_analyzer
  - concurrent
  - dataclasses
  - datetime
  - dependency_metrics
  - formatters
  - generic_analyzer
  - hashlib
  - json
  - lizard
  - logging
  - main
  - matplotlib
  - metrics
  - mimetypes
  - models
  - networkx
  - numpy
  - os
  - pathlib
  - pattern_metrics
  - performance
  - performance_metrics
  - pickle
  - pytest
  - python_analyzer
  - quality
  - quality_metrics
  - radon
  - re
  - recommendations
  - seaborn
  - security
  - security_metrics
  - setuptools
  - shutil
  - sklearn
  - subprocess
  - sys
  - tempfile
  - tests
  - time
  - traceback
  - typing
  - unittest
  - utils

Development:
  - abc
  - analyzer
  - analyzers
  - argparse
  - ast
  - base
  - base_analyzer
  - click
  - codebase_analyzer
  - collections
  - complexity
  - complexity_analyzer
  - concurrent
  - dataclasses
  - datetime
  - dependency_metrics
  - formatters
  - generic_analyzer
  - hashlib
  - json
  - lizard
  - logging
  - main
  - matplotlib
  - metrics
  - mimetypes
  - models
  - networkx
  - numpy
  - os
  - pathlib
  - pattern_metrics
  - performance
  - performance_metrics
  - pickle
  - pytest
  - python_analyzer
  - quality
  - quality_metrics
  - radon
  - re
  - recommendations
  - seaborn
  - security
  - security_metrics
  - setuptools
  - shutil
  - sklearn
  - subprocess
  - sys
  - tempfile
  - tests
  - time
  - traceback
  - typing
  - unittest
  - utils

Dependency Health
----------------
Outdated Packages:
Package       Version Latest  Type
------------- ------- ------- -----
bandit        1.8.0   1.8.3   wheel
black         24.10.0 25.1.0  wheel
coverage      7.6.10  7.6.12  wheel
filelock      3.16.1  3.17.0  wheel
flake8        7.1.1   7.1.2   wheel
fonttools     4.55.3  4.56.0  wheel
Jinja2        3.1.5   3.1.6   wheel
lizard        1.17.13 1.17.20 wheel
mando         0.7.1   0.8.2   wheel
matplotlib    3.10.0  3.10.1  wheel
mypy          1.14.1  1.15.0  wheel
numpy         2.2.1   2.2.3   wheel
pbr           6.1.0   6.1.1   wheel
pip           24.3.1  25.0.1  wheel
psutil        6.1.1   7.0.0   wheel
pydantic      2.9.2   2.10.6  wheel
pydantic_core 2.23.4  2.31.1  wheel
pytest        8.3.4   8.3.5   wheel
pytz          2024.2  2025.1  wheel
scikit-learn  1.6.0   1.6.1   wheel
scipy         1.15.0  1.15.2  wheel
setuptools    75.6.0  75.9.1  wheel
stevedore     5.4.0   5.4.1   wheel
tzdata        2024.2  2025.1  wheel


Vulnerabilities:
Safety check failed