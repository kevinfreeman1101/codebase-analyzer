CODEBASE SUMMARY
===============

Root: /mnt/Egg/code/python/apps/codebase-analyzer

Project Overview
--------------
Name: codebase-analyzer

Summary Statistics
------------------
Directories: 19
Total Files: 53
Total Size: 291.2 KB
Classes: 97
Functions: 770
Documented: 398 (52% of functions)

File Distribution:
- markdown: 2 files
- python: 41 files
- text: 6 files
- requirements: 1 files
- ini: 1 files
- json: 2 files

Directory Structure
------------------
├─ README.md
├─ codebase_analyzer
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ analyzer.py
│  ├─ analyzers
│  │  ├─ __init__.py
│  │  ├─ base_analyzer.py
│  │  ├─ generic_analyzer.py
│  │  ├─ project_analyzer.py
│  │  └─ python_analyzer.py
│  ├─ examples
│  │  ├─ ci_integration.py
│  │  ├─ feature_extractor_examples.py
│  │  ├─ prompt_example.py
│  │  ├─ prompts
│  │  │  └─ templates.json
│  │  └─ recommendations_example.py
│  ├─ features
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ complexity.py
│  │  ├─ manager.py
│  │  ├─ performance.py
│  │  ├─ quality.py
│  │  └─ security.py
│  ├─ formatters
│  │  ├─ comprehensive_formatter.py
│  │  └─ summary_formatter.py
│  ├─ main.py
│  ├─ metrics
│  │  ├─ __init__.py
│  │  ├─ complexity_analyzer.py
│  │  ├─ dependency_metrics.py
│  │  ├─ pattern_metrics.py
│  │  ├─ performance_metrics.py
│  │  ├─ quality_metrics.py
│  │  └─ security_metrics.py
│  ├─ models
│  │  ├─ __init__.py
│  │  └─ data_classes.py
│  ├─ recommendations
│  │  ├─ ml_engine.py
│  │  ├─ prompt_manager.py
│  │  └─ recommendation_engine.py
│  ├─ utils
│  │  ├─ __init__.py
│  │  └─ file_utils.py
│  └─ visualizations
│     ├─ examples.py
│     └─ metric_visualizer.py
├─ codebase_analyzer.egg-info
│  ├─ PKG-INFO
│  ├─ SOURCES.txt
│  ├─ dependency_links.txt
│  ├─ entry_points.txt
│  ├─ requires.txt
│  └─ top_level.txt
├─ example_usage.py
├─ requirements-dev.txt
├─ requirements.txt
├─ setup.py
├─ setup_test_structure.sh
├─ summaries
│  └─ _summary.markdown
└─ tests
   ├─ __init__.py
   ├─ conftest.py
   ├─ helpers.py
   ├─ integration
   │  └─ __init__.py
   ├─ pytest.ini
   └─ unit
      ├─ __init__.py
      ├─ test_analyzers
      │  ├─ __init__.py
      │  ├─ test_analyzers
      │  ├─ test_project_analyzer.py
      │  └─ test_python_analyzer.py
      └─ test_features
         └─ test_complexity_features.py

Source Files
------------

Ini Files:

/mnt/Egg/code/python/apps/codebase-analyzer/tests/pytest.ini
  Size: 237.0 B


Json Files:

/mnt/Egg/code/python/apps/codebase-analyzer/.vscode/settings.json
  Size: 47.0 B

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/prompts/templates.json
  Size: 3.8 KB


Markdown Files:

/mnt/Egg/code/python/apps/codebase-analyzer/.pytest_cache/README.md
  Size: 302.0 B

/mnt/Egg/code/python/apps/codebase-analyzer/README.md


Python Files:

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/__init__.py
  Size: 102.0 B
  (Empty or initialization file)

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/__main__.py
  Size: 743.0 B
  Public Functions:
    - main

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/analyzer.py
  Size: 11.9 KB
  Class: CodebaseAnalyzer
    Main analyzer that coordinates all metric analyzers.
    Methods:
      Public:
        - analyze_project
          Perform comprehensive analysis of the project.
        - generate_summary
          Generate a comprehensive analysis summary.
      Private:
        - _add_critical_findings
          Add critical findings from all analyzers.
        - _add_recommendations
          Add prioritized recommendations based on all metrics.
        - _format_complexity_summary
          Format complexity metrics summary.
        - _format_dependency_summary
          Format dependency analysis summary.
        - _format_pattern_summary
          Format code pattern analysis summary.
        - _format_performance_summary
          Format performance analysis summary.
        - _format_quality_summary
          Format code quality metrics summary.
        - _format_security_summary
          Format security analysis summary.
  Class: ProjectMetrics
    Comprehensive project metrics combining all analyzers.
    Attributes:
      - complexity: ComplexityMetrics
      - dependencies: DependencyMetrics
      - patterns: PatternMetrics
      - performance: PerformanceMetrics
      - project_path: Path
      - quality: QualityMetrics
      - security: SecurityMetrics
      - timestamp: datetime.datetime
      - total_files: int
      - total_lines: int
    Methods:
      Public:
        - calculate_overall_score
          Calculate weighted overall project score.
  Public Functions:
    - analyze_project
      Perform comprehensive analysis of the project.
    - calculate_overall_score
      Calculate weighted overall project score.
    - generate_summary
      Generate a comprehensive analysis summary.

  Private Functions:
    - _add_critical_findings
      Add critical findings from all analyzers.
    - _add_recommendations
      Add prioritized recommendations based on all metrics.
    - _format_complexity_summary
      Format complexity metrics summary.
    - _format_dependency_summary
      Format dependency analysis summary.
    - _format_pattern_summary
      Format code pattern analysis summary.
    - _format_performance_summary
      Format performance analysis summary.
    - _format_quality_summary
      Format code quality metrics summary.
    - _format_security_summary
      Format security analysis summary.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/analyzers/base_analyzer.py
  Size: 742.0 B
  Class: BaseAnalyzer
    Base class for file analyzers.
    Methods:
      Public:
        - analyze
          Analyze the file and return FileInfo object.

Returns:
    FileInfo object or None if analysis fails
        - get_file_type
          Get the type of file this analyzer handles.

Returns:
    String representing the file type
  Public Functions:
    - analyze
      Analyze the file and return FileInfo object.
      Returns:
      FileInfo object or None if analysis fails
    - get_file_type
      Get the type of file this analyzer handles.
      Returns:
      String representing the file type

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/analyzers/generic_analyzer.py
  Size: 1.0 KB
  Class: GenericAnalyzer
    Analyzer for non-Python files.
    Methods:
      Public:
        - analyze
        - get_file_type
  Public Functions:
    - analyze
    - get_file_type

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/analyzers/project_analyzer.py
  Size: 11.1 KB
  Class: ProjectAnalyzer
    Analyzes an entire project directory and generates a summary.
    Methods:
      Public:
        - analyze
          Analyze the project and return a formatted summary.
      Private:
        - _analyze_file
          Analyze a single file and return its information.

Args:
    file_path: Path to the file to analyze

Returns:
    Dictionary containing file information or None if analysis fails
        - _clean_dependencies
          Clean up and categorize dependencies.
        - _extract_project_metadata
          Extract project metadata from setup.py and __init__.py files.
        - _extract_setup_info
          Extract information from setup.py.
        - _get_file_type
          Determine the file type based on extension.
        - _get_project_files
          Get all project files recursively.

Returns:
    List of Path objects for all files in the project
  Public Functions:
    - analyze
      Analyze the project and return a formatted summary.

  Private Functions:
    - _analyze_file
      Analyze a single file and return its information.
      Args:
      file_path: Path to the file to analyze
      Returns:
      Dictionary containing file information or None if analysis fails
    - _clean_dependencies
      Clean up and categorize dependencies.
    - _extract_project_metadata
      Extract project metadata from setup.py and __init__.py files.
    - _extract_setup_info
      Extract information from setup.py.
    - _get_file_type
      Determine the file type based on extension.
    - _get_project_files
      Get all project files recursively.
      Returns:
      List of Path objects for all files in the project

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/analyzers/python_analyzer.py
  Size: 8.0 KB
  Class: PythonAnalyzer
    Methods:
      Public:
        - analyze
          Analyze the Python file and return FileInfo.
        - get_external_dependencies
          Extract external dependencies (excluding standard library).
        - get_file_type
      Private:
        - _analyze_ast
          Analyze the AST and collect information about the code.
        - _calculate_complexity
          Calculate cyclomatic complexity of a node.
        - _get_code_snippet
          Extract the actual code for a node.
        - _get_dependencies
          Extract dependencies from a node.
        - _get_return_type
          Extract return type annotation if present.
        - _process_class
          Process a class definition node.
        - _process_class_attributes
          Extract class attributes from class body.
        - _process_function
          Process a function definition node.
        - _process_import
          Process import statements.
        - _process_import_from
          Process from ... import statements.
  Public Functions:
    - analyze
      Analyze the Python file and return FileInfo.
    - get_external_dependencies
      Extract external dependencies (excluding standard library).
    - get_file_type

  Private Functions:
    - _analyze_ast
      Analyze the AST and collect information about the code.
    - _calculate_complexity
      Calculate cyclomatic complexity of a node.
    - _get_code_snippet
      Extract the actual code for a node.
    - _get_dependencies
      Extract dependencies from a node.
    - _get_return_type
      Extract return type annotation if present.
    - _process_class
      Process a class definition node.
    - _process_class_attributes
      Extract class attributes from class body.
    - _process_function
      Process a function definition node.
    - _process_import
      Process import statements.
    - _process_import_from
      Process from ... import statements.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/ci_integration.py
  Size: 3.2 KB
  Public Functions:
    - analyze_project_for_ci
      Analyzes a project directory and generates reports for CI/CD pipeline.
      Returns True if all quality checks pass, False otherwise.
    - check_analysis_results
      Checks if analysis results meet quality thresholds.
      Returns True if all checks pass, False otherwise.
    - main
      Example usage in CI pipeline.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/feature_extractor_examples.py
  Size: 5.0 KB
  Public Functions:
    - analyze_project_file
      Example of analyzing a real project file.
    - analyze_with_custom_output
      Example of analyzing code and customizing the output.
    - basic_analysis_example
      Basic example of analyzing a simple code snippet.
    - generate_summary_report
    - main
      Run all examples.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/prompt_example.py
  Size: 661.0 B
  (Empty or initialization file)

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/recommendations_example.py
  Size: 906.0 B
  Class: CustomModel

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/base.py
  Size: 952.0 B
  Class: CodeFeatures
    Container for extracted code features.
    Attributes:
      - complexity_metrics: Dict[str, float]
      - dependency_metrics: Dict[str, Any]
      - documentation_metrics: Dict[str, float]
      - pattern_metrics: Dict[str, Any]
      - performance_metrics: Dict[str, float]
      - quality_metrics: Dict[str, float]
      - security_metrics: Dict[str, float]
      - test_metrics: Dict[str, float]
  Class: FeatureExtractor
    Base class for all feature extractors.
    Methods:
      Public:
        - extract
          Extract features from code.
        - get_feature_names
          Get list of features this extractor provides.
  Public Functions:
    - extract
      Extract features from code.
    - get_feature_names
      Get list of features this extractor provides.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/complexity.py
  Size: 5.6 KB
  Class: CognitiveComplexityVisitor
    Methods:
      Public:
        - visit_For
        - visit_If
        - visit_Try
        - visit_While
  Class: ComplexityFeatureExtractor
    Extracts complexity-related features.
    Methods:
      Public:
        - extract
        - get_feature_names
      Private:
        - _calculate_avg_function_length
        - _calculate_cognitive_complexity
        - _calculate_halstead_metrics
        - _calculate_max_complexity
        - _calculate_mean_complexity
        - _get_complexity_distribution
        - _get_default_metrics
  Public Functions:
    - extract
    - get_feature_names
    - visit_For
    - visit_If
    - visit_Try
    - visit_While

  Private Functions:
    - _calculate_avg_function_length
    - _calculate_cognitive_complexity
    - _calculate_halstead_metrics
    - _calculate_max_complexity
    - _calculate_mean_complexity
    - _get_complexity_distribution
    - _get_default_metrics

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/manager.py
  Size: 21.4 KB
  Class: FeatureExtractorManager
    Coordinates multiple feature extractors and aggregates their results.
    Methods:
      Public:
        - export_results
          Exports analysis results in the specified format.

Args:
    results: Analysis results to export
    format: Output format ('json' or 'html')
    output_path: Optional path to save the output
    
Returns:
    Exported content as string if no output_path is provided
        - extract_all
          Extracts all features from the given code using all registered extractors.

Args:
    code: The source code to analyze
    file_path: Optional path to the source file
    
Returns:
    Dictionary containing all extracted features and metadata
      Private:
        - _calculate_overall_score
          Calculates the overall code quality score from all metrics.
        - _create_analysis_report
          Creates a comprehensive analysis report with all results and metadata.
        - _extract_safely
          Safely extracts features using the given extractor with error handling.
        - _generate_details_section
          Generates the detailed results section of the HTML report.
        - _generate_html_report
          Generates an HTML report from analysis results.
        - _generate_metadata_section
          Generates the metadata section of the HTML report.
        - _generate_metrics_section
          Generates the metrics section of the HTML report.
        - _generate_recommendations
          Generates prioritized recommendations based on analysis results.
        - _generate_recommendations_section
          Generates the recommendations section of the HTML report.
        - _generate_score_section
          Generates the overall score section of the HTML report.
        - _generate_summary
          Generates a high-level summary of the analysis results.
        - _get_complexity_highlights
          Extracts key complexity insights from results.
        - _get_complexity_recommendations
          Generates recommendations for complexity issues.
        - _get_default_metrics
          Returns default metrics for a given extractor when analysis fails.
        - _get_performance_highlights
          Extracts key performance insights from results.
        - _get_performance_recommendations
          Generates recommendations for performance issues.
        - _get_quality_highlights
          Extracts key quality insights from results.
        - _get_quality_recommendations
          Generates recommendations for code quality issues.
        - _get_security_highlights
          Extracts key security insights from results.
        - _get_security_recommendations
          Generates recommendations for security issues.
  Public Functions:
    - export_results
      Exports analysis results in the specified format.
      Args:
      results: Analysis results to export
      format: Output format ('json' or 'html')
      output_path: Optional path to save the output
      Returns:
      Exported content as string if no output_path is provided
    - extract_all
      Extracts all features from the given code using all registered extractors.
      Args:
      code: The source code to analyze
      file_path: Optional path to the source file
      Returns:
      Dictionary containing all extracted features and metadata

  Private Functions:
    - _calculate_overall_score
      Calculates the overall code quality score from all metrics.
    - _create_analysis_report
      Creates a comprehensive analysis report with all results and metadata.
    - _extract_safely
      Safely extracts features using the given extractor with error handling.
    - _generate_details_section
      Generates the detailed results section of the HTML report.
    - _generate_html_report
      Generates an HTML report from analysis results.
    - _generate_metadata_section
      Generates the metadata section of the HTML report.
    - _generate_metrics_section
      Generates the metrics section of the HTML report.
    - _generate_recommendations
      Generates prioritized recommendations based on analysis results.
    - _generate_recommendations_section
      Generates the recommendations section of the HTML report.
    - _generate_score_section
      Generates the overall score section of the HTML report.
    - _generate_summary
      Generates a high-level summary of the analysis results.
    - _get_complexity_highlights
      Extracts key complexity insights from results.
    - _get_complexity_recommendations
      Generates recommendations for complexity issues.
    - _get_default_metrics
      Returns default metrics for a given extractor when analysis fails.
    - _get_performance_highlights
      Extracts key performance insights from results.
    - _get_performance_recommendations
      Generates recommendations for performance issues.
    - _get_quality_highlights
      Extracts key quality insights from results.
    - _get_quality_recommendations
      Generates recommendations for code quality issues.
    - _get_security_highlights
      Extracts key security insights from results.
    - _get_security_recommendations
      Generates recommendations for security issues.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/performance.py
  Size: 19.5 KB
  Class: AsyncVisitor
    Methods:
      Public:
        - visit_AsyncFor
        - visit_AsyncFunctionDef
        - visit_AsyncWith
        - visit_Await
  Class: BottleneckVisitor
    Methods:
      Public:
        - visit
      Private:
        - _get_recommendation
  Class: CachingVisitor
    Methods:
      Public:
        - get_opportunities
        - visit_Call
  Class: ComplexityVisitor
    Methods:
      Public:
        - visit_For
        - visit_FunctionDef
        - visit_GeneratorExp
        - visit_ListComp
        - visit_While
      Private:
        - _handle_loop
  Class: IOVisitor
    Methods:
      Public:
        - visit_Call
  Class: MemoryVisitor
    Methods:
      Public:
        - visit_Call
        - visit_Dict
        - visit_FunctionDef
        - visit_List
  Class: PerformanceFeatureExtractor
    Extracts performance-related features and identifies potential bottlenecks.
    Methods:
      Public:
        - extract
        - get_feature_names
      Private:
        - _analyze_async_patterns
        - _analyze_bottlenecks
        - _analyze_caching
        - _analyze_complexity
        - _analyze_io_operations
        - _analyze_memory_usage
        - _calculate_performance_score
        - _estimate_space_complexity
        - _estimate_time_complexity
        - _get_default_metrics
        - _score_complexity
        - _score_io
        - _score_memory
  Class: PerformanceIssue
    Container for performance issues found in code.
    Attributes:
      - description: str
      - estimated_impact: Optional[str]
      - line_number: int
      - recommendation: Optional[str]
      - severity: str
      - snippet: str
      - type: str
  Class: RecursionDetector
    Methods:
      Public:
        - visit_Call
  Public Functions:
    - extract
    - get_feature_names
    - get_opportunities
    - visit
    - visit_AsyncFor
    - visit_AsyncFunctionDef
    - visit_AsyncWith
    - visit_Await
    - visit_Call
    - visit_Dict
    - visit_For
    - visit_FunctionDef
    - visit_GeneratorExp
    - visit_List
    - visit_ListComp
    - visit_While

  Private Functions:
    - _analyze_async_patterns
    - _analyze_bottlenecks
    - _analyze_caching
    - _analyze_complexity
    - _analyze_io_operations
    - _analyze_memory_usage
    - _calculate_performance_score
    - _estimate_space_complexity
    - _estimate_time_complexity
    - _get_default_metrics
    - _get_recommendation
    - _handle_loop
    - _score_complexity
    - _score_io
    - _score_memory

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/quality.py
  Size: 15.9 KB
  Class: DocVisitor
    Methods:
      Public:
        - visit_ClassDef
        - visit_FunctionDef
      Private:
        - _assess_docstring_quality
  Class: NamingVisitor
    Methods:
      Public:
        - get_consistency_score
        - visit_ClassDef
        - visit_FunctionDef
        - visit_Name
      Private:
        - _check_naming_convention
        - _get_name_pattern
  Class: QualityFeatureExtractor
    Extracts code quality features including documentation, naming conventions,
code structure, type hints, and test coverage metrics.
    Methods:
      Public:
        - extract
        - get_feature_names
      Private:
        - _analyze_code_smells
        - _analyze_documentation
        - _analyze_naming
        - _analyze_structure
        - _analyze_test_coverage
        - _analyze_type_hints
        - _calculate_coverage
        - _calculate_smell_severity
        - _calculate_test_quality
        - _get_default_metrics
        - _safe_mean
  Class: SmellVisitor
    Methods:
      Public:
        - visit_ClassDef
        - visit_FunctionDef
  Class: StructureVisitor
    Methods:
      Public:
        - visit_ClassDef
        - visit_For
        - visit_FunctionDef
        - visit_If
        - visit_While
      Private:
        - _handle_nesting
  Class: TypeHintVisitor
    Methods:
      Public:
        - visit_FunctionDef
  Public Functions:
    - extract
    - get_consistency_score
    - get_feature_names
    - visit_ClassDef
    - visit_For
    - visit_FunctionDef
    - visit_If
    - visit_Name
    - visit_While

  Private Functions:
    - _analyze_code_smells
    - _analyze_documentation
    - _analyze_naming
    - _analyze_structure
    - _analyze_test_coverage
    - _analyze_type_hints
    - _assess_docstring_quality
    - _calculate_coverage
    - _calculate_smell_severity
    - _calculate_test_quality
    - _check_naming_convention
    - _get_default_metrics
    - _get_name_pattern
    - _handle_nesting
    - _safe_mean

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/security.py
  Size: 15.9 KB
  Class: AuthenticationVisitor
    Methods:
      Public:
        - visit_Call
  Class: InputValidationVisitor
    Methods:
      Public:
        - visit_Call
  Class: SecurityFeatureExtractor
    Extracts security-related features and identifies potential vulnerabilities.
    Methods:
      Public:
        - extract
        - get_feature_names
      Private:
        - _analyze_authentication
        - _analyze_crypto_usage
        - _analyze_input_validation
        - _analyze_security_patterns
        - _analyze_sensitive_data
        - _analyze_vulnerabilities
        - _calculate_security_score
        - _get_default_metrics
  Class: SecurityIssue
    Container for security issues found in code.
    Attributes:
      - cwe_id: Optional[str]
      - description: str
      - line_number: int
      - recommendation: Optional[str]
      - severity: str
      - snippet: str
      - type: str
  Class: SecurityPatternVisitor
    Methods:
      Public:
        - visit_Call
  Class: SensitiveDataVisitor
    Methods:
      Public:
        - visit_Assign
  Class: VulnerabilityVisitor
    Methods:
      Public:
        - visit_Call
      Private:
        - _get_recommendation
        - _get_vulnerability_description
  Public Functions:
    - extract
    - get_feature_names
    - visit_Assign
    - visit_Call

  Private Functions:
    - _analyze_authentication
    - _analyze_crypto_usage
    - _analyze_input_validation
    - _analyze_security_patterns
    - _analyze_sensitive_data
    - _analyze_vulnerabilities
    - _calculate_security_score
    - _get_default_metrics
    - _get_recommendation
    - _get_vulnerability_description

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/formatters/comprehensive_formatter.py
  Size: 12.8 KB
  Class: ComprehensiveFormatter
    Formats analysis results into various output formats with customizable detail levels.
    Methods:
      Public:
        - format_analysis
          Format complete analysis results.
      Private:
        - _format_complexity_analysis
          Format complexity analysis section.
        - _format_dependency_analysis
          Format dependency analysis section.
        - _format_executive_summary
          Format executive summary with key findings.
        - _format_header
          Format section headers.
        - _format_pattern_analysis
          Format code pattern analysis section.
        - _format_performance_analysis
          Format performance analysis section.
        - _format_project_overview
          Format project overview section.
        - _format_quality_analysis
          Format code quality analysis section.
        - _format_recommendations
          Format recommendations section.
        - _format_score
          Format a score with color coding.
        - _format_security_analysis
          Format security analysis section.
        - _get_critical_findings
          Extract critical findings from all metrics.
        - _get_prioritized_recommendations
          Generate prioritized recommendations based on all metrics.
        - _group_by_severity
          Group items by severity level.
        - _setup_colors
          Setup ANSI color codes for terminal output.
  Class: FormattingOptions
    Configuration options for output formatting.
    Attributes:
      - color_output: bool
      - detail_level: str - medium
      - format_type: str - text
      - include_code_snippets: bool
      - include_timestamps: bool
      - max_items_per_section: int
  Public Functions:
    - format_analysis
      Format complete analysis results.

  Private Functions:
    - _format_complexity_analysis
      Format complexity analysis section.
    - _format_dependency_analysis
      Format dependency analysis section.
    - _format_executive_summary
      Format executive summary with key findings.
    - _format_header
      Format section headers.
    - _format_pattern_analysis
      Format code pattern analysis section.
    - _format_performance_analysis
      Format performance analysis section.
    - _format_project_overview
      Format project overview section.
    - _format_quality_analysis
      Format code quality analysis section.
    - _format_recommendations
      Format recommendations section.
    - _format_score
      Format a score with color coding.
    - _format_security_analysis
      Format security analysis section.
    - _get_critical_findings
      Extract critical findings from all metrics.
    - _get_prioritized_recommendations
      Generate prioritized recommendations based on all metrics.
    - _group_by_severity
      Group items by severity level.
    - _setup_colors
      Setup ANSI color codes for terminal output.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/formatters/summary_formatter.py
  Size: 14.2 KB
  Class: SummaryFormatter
    Formats codebase analysis results into a readable summary.
    Methods:
      Public:
        - add_build_artifact
          Add a build artifact file.
        - add_dependency
          Add a project dependency to the specified category.
        - add_source_file
          Add information about a source file.
        - format_summary
          Generate the complete codebase summary.
        - set_project_overview
          Set the project overview description.
        - set_python_version
          Set the minimum Python version requirement.
        - update_project_overview
          Update project overview information.
      Private:
        - _format_function_groups
          Format grouped functions with proper indentation and documentation.
        - _format_tree
          Generate hierarchical tree structure.
        - _get_file_type_counts
          Count files by type.
        - _get_percentage
          Calculate percentage, handling division by zero.
        - _get_project_metrics
          Generate project metrics summary.
        - _get_size_str
          Convert bytes to human readable string.
        - _group_functions
          Group functions by visibility (public/private).
  Public Functions:
    - add_build_artifact
      Add a build artifact file.
    - add_dependency
      Add a project dependency to the specified category.
    - add_source_file
      Add information about a source file.
    - format_summary
      Generate the complete codebase summary.
    - set_project_overview
      Set the project overview description.
    - set_python_version
      Set the minimum Python version requirement.
    - update_project_overview
      Update project overview information.

  Private Functions:
    - _format_function_groups
      Format grouped functions with proper indentation and documentation.
    - _format_tree
      Generate hierarchical tree structure.
    - _get_file_type_counts
      Count files by type.
    - _get_percentage
      Calculate percentage, handling division by zero.
    - _get_project_metrics
      Generate project metrics summary.
    - _get_size_str
      Convert bytes to human readable string.
    - _group_functions
      Group functions by visibility (public/private).

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/main.py
  Size: 6.8 KB
  Class: CodebaseAnalyzer
    Methods:
      Public:
        - analyze
          Analyze the codebase and return file info.
        - generate_summary
          Generate a summary of the codebase.
        - save_summary
          Save the summary to a file.
      Private:
        - _analyze_file
          Analyze a single file.
  Public Functions:
    - analyze
      Analyze the codebase and return file info.
    - generate_summary
      Generate a summary of the codebase.
    - main
      Analyze a Python codebase and generate a summary for LLMs.
    - save_summary
      Save the summary to a file.

  Private Functions:
    - _analyze_file
      Analyze a single file.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/__init__.py
  Size: 495.0 B
  (Empty or initialization file)

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/complexity_analyzer.py
  Size: 5.7 KB
  Class: CognitiveVisitor
    Methods:
      Public:
        - visit_For
        - visit_If
        - visit_Try
        - visit_While
  Class: ComplexityAnalyzer
    Analyzes code complexity metrics.
    Methods:
      Public:
        - analyze_node
          Analyze complexity metrics for an AST node.
        - reset_metrics
      Private:
        - _calculate_cognitive_complexity
          Calculate cognitive complexity based on nesting and structures.
        - _calculate_cyclomatic_complexity
          Calculate cyclomatic complexity (McCabe complexity).
        - _calculate_halstead_metrics
          Calculate Halstead complexity metrics.
        - _calculate_maintainability_index
          Calculate maintainability index.
        - _count_lines_of_code
          Count logical lines of code.
  Class: ComplexityMetrics
    Attributes:
      - cognitive_complexity: int
      - cyclomatic_complexity: int
      - halstead_metrics: Dict[str, float]
      - lines_of_code: int
      - maintainability_index: float
      - nesting_depth: int
  Class: HalsteadVisitor
    Methods:
      Public:
        - visit_BinOp
        - visit_Name
        - visit_Num
  Public Functions:
    - analyze_node
      Analyze complexity metrics for an AST node.
    - reset_metrics
    - visit_BinOp
    - visit_For
    - visit_If
    - visit_Name
    - visit_Num
    - visit_Try
    - visit_While

  Private Functions:
    - _calculate_cognitive_complexity
      Calculate cognitive complexity based on nesting and structures.
    - _calculate_cyclomatic_complexity
      Calculate cyclomatic complexity (McCabe complexity).
    - _calculate_halstead_metrics
      Calculate Halstead complexity metrics.
    - _calculate_maintainability_index
      Calculate maintainability index.
    - _count_lines_of_code
      Count logical lines of code.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/dependency_metrics.py
  Size: 7.8 KB
  Class: DependencyAnalyzer
    Analyzes project dependencies and their relationships.
    Methods:
      Public:
        - analyze_project
          Analyze all dependencies in the project.
        - get_dependency_summary
          Generate a human-readable dependency summary.
      Private:
        - _analyze_imports
          Analyze all imports in Python files.
        - _analyze_requirements
          Analyze requirements.txt and similar files.
        - _check_security_advisories
          Check for known security vulnerabilities.
        - _detect_circular_dependencies
          Detect circular dependencies in the project.
        - _find_unused_imports
          Find imports that are declared but not used.
        - _parse_requirement
          Parse a single requirement line.
  Class: DependencyInfo
    Attributes:
      - is_direct: bool
      - license: Optional[str]
      - name: str
      - security_advisories: List[str]
      - usage_count: int
      - version_installed: Optional[str]
      - version_required: str
  Class: DependencyMetrics
    Attributes:
      - circular_dependencies: List[List[str]]
      - dependency_graph: Dict[str, Set[str]]
      - direct_dependencies: Dict[str, DependencyInfo]
      - indirect_dependencies: Dict[str, DependencyInfo]
      - internal_dependencies: Dict[str, List[str]]
      - unused_imports: List[str]
  Class: ImportVisitor
    Methods:
      Public:
        - visit_Import
        - visit_ImportFrom
  Public Functions:
    - analyze_project
      Analyze all dependencies in the project.
    - dfs
    - find_cycles
    - get_dependency_summary
      Generate a human-readable dependency summary.
    - visit_Import
    - visit_ImportFrom

  Private Functions:
    - _analyze_imports
      Analyze all imports in Python files.
    - _analyze_requirements
      Analyze requirements.txt and similar files.
    - _check_security_advisories
      Check for known security vulnerabilities.
    - _detect_circular_dependencies
      Detect circular dependencies in the project.
    - _find_unused_imports
      Find imports that are declared but not used.
    - _parse_requirement
      Parse a single requirement line.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/pattern_metrics.py
  Size: 10.8 KB
  Class: ArchitecturalStyle
    Attributes:
      - confidence: float
      - evidence: List[str]
      - name: str
      - suggestions: List[str]
  Class: DesignPattern
    Attributes:
      - confidence: float
      - description: str
      - implementation_notes: Optional[str]
      - locations: List[str]
      - name: str
  Class: FactoryVisitor
    Methods:
      Public:
        - visit_ClassDef
      Private:
        - _find_return_types
  Class: PatternAnalyzer
    Analyzes code patterns and architectural styles.
    Methods:
      Public:
        - analyze_project
          Analyze all patterns in the project.
        - get_pattern_summary
          Generate a human-readable pattern summary.
      Private:
        - _analyze_architecture
          Analyze the overall architectural style of the project.
        - _detect_design_patterns
          Detect common design patterns in the codebase.
        - _detect_factory_pattern
          Detect Factory pattern implementation.
        - _detect_singleton_pattern
          Detect Singleton pattern implementation.
        - _detect_strategy_pattern
          Detect Strategy pattern implementation.
        - _determine_architecture_style
          Determine the predominant architectural style.
  Class: PatternMetrics
    Attributes:
      - anti_patterns: List[Dict[str, str]]
      - api_patterns: Dict[str, float]
      - architectural_style: ArchitecturalStyle
      - database_patterns: Dict[str, float]
      - design_patterns: List[DesignPattern]
  Class: SingletonVisitor
    Methods:
      Public:
        - visit_ClassDef
  Class: StrategyVisitor
    Methods:
      Public:
        - visit_ClassDef
  Public Functions:
    - analyze_project
      Analyze all patterns in the project.
    - get_pattern_summary
      Generate a human-readable pattern summary.
    - visit_ClassDef

  Private Functions:
    - _analyze_architecture
      Analyze the overall architectural style of the project.
    - _detect_design_patterns
      Detect common design patterns in the codebase.
    - _detect_factory_pattern
      Detect Factory pattern implementation.
    - _detect_singleton_pattern
      Detect Singleton pattern implementation.
    - _detect_strategy_pattern
      Detect Strategy pattern implementation.
    - _determine_architecture_style
      Determine the predominant architectural style.
    - _find_return_types

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/performance_metrics.py
  Size: 19.1 KB
  Class: AsyncPatternVisitor
    Methods:
      Public:
        - visit_AsyncFunctionDef
        - visit_Await
        - visit_Call
  Class: CachingVisitor
    Methods:
      Public:
        - visit_FunctionDef
      Private:
        - _is_expensive_operation
  Class: HotspotVisitor
    Methods:
      Public:
        - visit_Call
        - visit_For
        - visit_ListComp
      Private:
        - _check_append_in_loop
        - _check_inefficient_operations
  Class: OptimizationOpportunity
    Attributes:
      - code_example: Optional[str]
      - current_pattern: str
      - estimated_impact: str
      - implementation_difficulty: str
      - location: str
      - suggested_pattern: str
  Class: OptimizationVisitor
    Methods:
      Public:
        - visit_BinOp
        - visit_For
  Class: PerformanceAnalyzer
    Analyzes code for performance patterns and optimization opportunities.
    Methods:
      Public:
        - analyze_project
          Perform comprehensive performance analysis of the project.
        - get_performance_summary
          Generate a human-readable performance summary.
      Private:
        - _analyze_async_patterns
          Analyze async/await usage and opportunities.
        - _analyze_complexity_hotspots
          Analyze code for performance hotspots.
        - _analyze_resource_usage
          Analyze resource usage patterns.
        - _calculate_performance_score
          Calculate overall performance score.
        - _identify_caching_opportunities
          Identify opportunities for caching.
        - _identify_optimization_opportunities
          Identify potential optimization opportunities.
  Class: PerformanceHotspot
    Attributes:
      - description: str
      - estimated_improvement: str
      - impact: str
      - location: str
      - recommendation: str
      - severity: str
      - type: str
  Class: PerformanceMetrics
    Attributes:
      - async_patterns: Dict[str, List[str]]
      - caching_opportunities: List[Dict[str, str]]
      - hotspots: List[PerformanceHotspot]
      - optimization_opportunities: List[OptimizationOpportunity]
      - performance_score: float
      - resource_usage: ResourceUsage
  Class: ResourceUsage
    Attributes:
      - cpu_patterns: Dict[str, List[str]]
      - io_patterns: Dict[str, List[str]]
      - memory_patterns: Dict[str, List[str]]
      - network_patterns: Dict[str, List[str]]
  Class: ResourceVisitor
    Methods:
      Public:
        - visit_Call
      Private:
        - _check_cpu_patterns
        - _check_io_patterns
        - _check_memory_patterns
        - _check_network_patterns
  Public Functions:
    - analyze_project
      Perform comprehensive performance analysis of the project.
    - get_performance_summary
      Generate a human-readable performance summary.
    - visit_AsyncFunctionDef
    - visit_Await
    - visit_BinOp
    - visit_Call
    - visit_For
    - visit_FunctionDef
    - visit_ListComp

  Private Functions:
    - _analyze_async_patterns
      Analyze async/await usage and opportunities.
    - _analyze_complexity_hotspots
      Analyze code for performance hotspots.
    - _analyze_resource_usage
      Analyze resource usage patterns.
    - _calculate_performance_score
      Calculate overall performance score.
    - _check_append_in_loop
    - _check_cpu_patterns
    - _check_inefficient_operations
    - _check_io_patterns
    - _check_memory_patterns
    - _check_network_patterns
    - _identify_caching_opportunities
      Identify opportunities for caching.
    - _identify_optimization_opportunities
      Identify potential optimization opportunities.
    - _is_expensive_operation

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/quality_metrics.py
  Size: 5.0 KB
  Class: CommentVisitor
    Methods:
      Public:
        - visit
  Class: DocVisitor
    Methods:
      Public:
        - visit_ClassDef
        - visit_FunctionDef
        - visit_Module
  Class: LintVisitor
    Methods:
      Public:
        - visit_FunctionDef
        - visit_Try
  Class: QualityAnalyzer
    Analyzes code quality metrics.
    Methods:
      Public:
        - analyze_node
          Analyze quality metrics for an AST node.
      Private:
        - _calculate_code_comment_ratio
          Calculate ratio of comments to code.
        - _calculate_documentation_coverage
          Calculate documentation coverage percentage.
        - _calculate_lint_score
          Calculate a lint score based on common code style issues.
        - _calculate_type_hint_coverage
          Calculate percentage of type-hinted functions and variables.
        - _estimate_test_coverage
          Estimate test coverage based on test file analysis.
  Class: QualityMetrics
    Attributes:
      - code_to_comment_ratio: float
      - documentation_coverage: float
      - lint_score: float
      - test_coverage: float
      - type_hint_coverage: float
  Class: TypeHintVisitor
    Methods:
      Public:
        - visit_AnnAssign
        - visit_FunctionDef
  Public Functions:
    - analyze_node
      Analyze quality metrics for an AST node.
    - visit
    - visit_AnnAssign
    - visit_ClassDef
    - visit_FunctionDef
    - visit_Module
    - visit_Try

  Private Functions:
    - _calculate_code_comment_ratio
      Calculate ratio of comments to code.
    - _calculate_documentation_coverage
      Calculate documentation coverage percentage.
    - _calculate_lint_score
      Calculate a lint score based on common code style issues.
    - _calculate_type_hint_coverage
      Calculate percentage of type-hinted functions and variables.
    - _estimate_test_coverage
      Estimate test coverage based on test file analysis.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/security_metrics.py
  Size: 12.6 KB
  Class: SecurityAnalyzer
    Analyzes code for security vulnerabilities and patterns.
    Methods:
      Public:
        - analyze_project
          Perform comprehensive security analysis of the project.
        - get_security_summary
          Generate a human-readable security summary.
      Private:
        - _calculate_security_score
          Calculate overall security score.
        - _check_authentication_pattern
          Check for proper authentication implementation.
        - _detect_security_patterns
          Detect implementation of security patterns.
        - _scan_for_sensitive_data
          Scan for potential sensitive data exposure.
        - _scan_for_vulnerabilities
          Scan for common security vulnerabilities.
  Class: SecurityMetrics
    Attributes:
      - compliance_issues: Dict[str, List[str]]
      - outdated_dependencies: List[Dict[str, str]]
      - security_patterns: List[SecurityPattern]
      - security_score: float
      - sensitive_data_exposure: List[Dict[str, str]]
      - vulnerabilities: List[SecurityVulnerability]
  Class: SecurityPattern
    Attributes:
      - implementation: str
      - name: str
      - strength: float
      - suggestions: List[str]
  Class: SecurityVulnerability
    Attributes:
      - cwe_id: Optional[str]
      - description: str
      - location: str
      - recommendation: str
      - severity: str
      - type: str
  Class: VulnerabilityVisitor
    Methods:
      Public:
        - visit_Call
      Private:
        - _check_command_injection
        - _check_sql_injection
        - _check_unsafe_deserialization
        - _check_weak_crypto
  Public Functions:
    - analyze_project
      Perform comprehensive security analysis of the project.
    - get_security_summary
      Generate a human-readable security summary.
    - visit_Call

  Private Functions:
    - _calculate_security_score
      Calculate overall security score.
    - _check_authentication_pattern
      Check for proper authentication implementation.
    - _check_command_injection
    - _check_sql_injection
    - _check_unsafe_deserialization
    - _check_weak_crypto
    - _detect_security_patterns
      Detect implementation of security patterns.
    - _scan_for_sensitive_data
      Scan for potential sensitive data exposure.
    - _scan_for_vulnerabilities
      Scan for common security vulnerabilities.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/models/data_classes.py
  Size: 1007.0 B
  Class: ClassInfo
    Attributes:
      - attributes: List[Dict[str, Any]]
      - base_classes: List[str]
      - code: CodeSnippet
      - complexity: Optional[int]
      - docstring: str
      - file_path: str
      - methods: List[FunctionInfo]
      - name: str
  Class: CodeSnippet
    Attributes:
      - content: str
      - end_line: int
      - start_line: int
  Class: FileInfo
    Attributes:
      - classes: Dict[str, ClassInfo]
      - content: str
      - dependencies: Set[str]
      - functions: Dict[str, FunctionInfo]
      - path: str
      - size: int
      - type: str
  Class: FunctionInfo
    Attributes:
      - code: CodeSnippet
      - complexity: Optional[int]
      - dependencies: Set[str]
      - docstring: str
      - file_path: str
      - loc: int
      - name: str
      - params: List[str]
      - returns: str

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/recommendations/ml_engine.py
  Size: 8.4 KB
  Class: ClaudeInterface
    Claude-specific implementation.
    Methods:
      Public:
        - analyze
        - load
          Load configuration and prompts.
        - save
          Save configuration and prompts.
        - train
          Claude doesn't require traditional training.
      Private:
        - _call_llm_api
          Make API call to Claude.
  Class: LLMInterface
    Base class for LLM-based analysis.
    Methods:
      Private:
        - _call_llm_api
          Make API call to LLM service.
        - _load_prompt_templates
          Load prompt templates from configuration.
  Class: LocalMLModel
    Local machine learning model implementation.
    Methods:
      Public:
        - analyze
        - load
        - save
        - train
      Private:
        - _extract_complexity_features
          Extract complexity-related features.
        - _initialize_feature_extractors
          Initialize feature extraction functions.
        - _process_features
          Process raw features into model-ready format.
  Class: MLRecommendation
    Machine learning based recommendation with confidence score.
    Attributes:
      - alternative_solutions: List[str]
      - category: str
      - code_snippets: List[str]
      - confidence: float
      - features_used: List[str]
      - model_name: str
      - reasoning: str
      - suggestion: str
  Class: MLRecommendationEngine
    Coordinates different ML models for code analysis.
    Methods:
      Public:
        - add_model
          Add a new model to the engine.
        - analyze
          Get recommendations from specified or all models.
        - remove_model
          Remove a model from the engine.
      Private:
        - _aggregate_recommendations
          Aggregate and deduplicate recommendations from multiple models.
        - _initialize_models
          Initialize configured models.
        - _merge_recommendations
          Merge similar recommendations from different models.
  Class: ModelInterface
    Abstract base class for all ML models.
    Methods:
      Public:
        - analyze
          Analyze code features and return recommendations.
        - load
          Load the model from disk.
        - save
          Save the model to disk.
        - train
          Train the model with provided data.
  Public Functions:
    - add_model
      Add a new model to the engine.
    - analyze
      Get recommendations from specified or all models.
    - load
      Load configuration and prompts.
    - remove_model
      Remove a model from the engine.
    - save
      Save configuration and prompts.
    - train
      Claude doesn't require traditional training.

  Private Functions:
    - _aggregate_recommendations
      Aggregate and deduplicate recommendations from multiple models.
    - _call_llm_api
      Make API call to Claude.
    - _extract_complexity_features
      Extract complexity-related features.
    - _initialize_feature_extractors
      Initialize feature extraction functions.
    - _initialize_models
      Initialize configured models.
    - _load_prompt_templates
      Load prompt templates from configuration.
    - _merge_recommendations
      Merge similar recommendations from different models.
    - _process_features
      Process raw features into model-ready format.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/recommendations/prompt_manager.py
  Size: 4.1 KB
  Class: PromptManager
    Manages prompt templates and their rendering.
    Methods:
      Public:
        - add_template
          Add a new template or override existing one.
        - get_prompt
          Get a rendered prompt template.
        - list_templates
          List all available templates.
        - set_variable
          Set a template variable value.
      Private:
        - _collect_templates
          Recursively collect template names.
        - _get_template
          Get a template by name, supporting dot notation.
        - _initialize_variables
          Initialize default template variables.
        - _load_templates
          Load built-in and custom prompt templates.
        - _merge_templates
          Merge custom templates with base templates.
  Public Functions:
    - add_template
      Add a new template or override existing one.
    - get_prompt
      Get a rendered prompt template.
    - list_templates
      List all available templates.
    - set_variable
      Set a template variable value.

  Private Functions:
    - _collect_templates
      Recursively collect template names.
    - _get_template
      Get a template by name, supporting dot notation.
    - _initialize_variables
      Initialize default template variables.
    - _load_templates
      Load built-in and custom prompt templates.
    - _merge_templates
      Merge custom templates with base templates.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/recommendations/recommendation_engine.py
  Size: 20.7 KB
  Class: CategoryType
    Attributes:
      - ARCHITECTURE
      - COMPLEXITY
      - DEPENDENCIES
      - DOCUMENTATION
      - PERFORMANCE
      - QUALITY
      - SECURITY
      - TESTING
  Class: PriorityLevel
    Attributes:
      - CRITICAL
      - HIGH
      - INFO
      - LOW
      - MEDIUM
  Class: Recommendation
    Structured recommendation with actionable insights.
    Attributes:
      - affected_files: List[str]
      - category: CategoryType
      - created_at: datetime.datetime
      - description: str
      - effort: str
      - impact: str
      - metrics_impact: Dict[str, float]
      - priority: PriorityLevel
      - references: List[str]
      - suggested_actions: List[str]
      - title: str
  Class: RecommendationEngine
    Generates prioritized recommendations based on codebase analysis.
    Methods:
      Public:
        - export_recommendations
          Export recommendations in the specified format.
        - generate_recommendations
          Generate comprehensive recommendations based on all metrics.
      Private:
        - _analyze_complexity_metrics
          Analyze code complexity metrics and generate recommendations.
        - _analyze_dependency_metrics
          Analyze dependency metrics and generate recommendations.
        - _analyze_pattern_metrics
          Analyze code pattern metrics and generate recommendations.
        - _analyze_performance_metrics
          Analyze performance metrics and generate recommendations.
        - _analyze_quality_metrics
          Analyze code quality metrics and generate recommendations.
        - _analyze_security_metrics
          Analyze security metrics and generate recommendations.
        - _export_html
          Export recommendations as HTML with styling and interactive elements.
        - _export_markdown
          Export recommendations as markdown.
        - _load_best_practices
          Load best practices and guidelines.
        - _load_threshold_configs
          Load configuration thresholds for metrics.
  Public Functions:
    - export_recommendations
      Export recommendations in the specified format.
    - generate_recommendations
      Generate comprehensive recommendations based on all metrics.

  Private Functions:
    - _analyze_complexity_metrics
      Analyze code complexity metrics and generate recommendations.
    - _analyze_dependency_metrics
      Analyze dependency metrics and generate recommendations.
    - _analyze_pattern_metrics
      Analyze code pattern metrics and generate recommendations.
    - _analyze_performance_metrics
      Analyze performance metrics and generate recommendations.
    - _analyze_quality_metrics
      Analyze code quality metrics and generate recommendations.
    - _analyze_security_metrics
      Analyze security metrics and generate recommendations.
    - _export_html
      Export recommendations as HTML with styling and interactive elements.
    - _export_markdown
      Export recommendations as markdown.
    - _load_best_practices
      Load best practices and guidelines.
    - _load_threshold_configs
      Load configuration thresholds for metrics.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/utils/file_utils.py
  Size: 4.2 KB
  Public Functions:
    - generate_tree_structure
      Generate a tree-like structure of the project.
      Args:
      root_dir: Root directory of the project
      files: List of file paths
      Returns:
      List of strings representing the tree structure
    - get_file_type
      Determine the type of file based on extension and mime type.
      Args:
      file_path: Path to the file
      Returns:
      String representing the file type
    - safe_read_file
      Safely read a file with multiple encoding fallbacks.
      Args:
      file_path: Path to the file to read
      Returns:
      The file contents as a string
      Raises:
      IOError: If the file cannot be read with any encoding
    - save_to_file
      Save content to a file with proper encoding.
      Args:
      content: String content to save
      file_path: Path where to save the file
      Returns:
      Boolean indicating success or failure
    - should_analyze_file
      Determine if a file should be analyzed based on its extension.
      Args:
      file_path: Path to the file to check
      Returns:
      bool: True if the file should be analyzed, False otherwise

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/visualizations/examples.py
  Size: 2.9 KB
  Class: CodebaseAnalyzer
    Methods:
      Public:
        - analyze_project
          Analyze project and optionally generate visualizations.

Args:
    project_path: Path to the project to analyze
    generate_visuals: Whether to generate visualization reports

Returns:
    Dictionary containing analysis results and paths to generated files
  Public Functions:
    - analyze_project
      Analyze project and optionally generate visualizations.
      Args:
      project_path: Path to the project to analyze
      generate_visuals: Whether to generate visualization reports
      Returns:
      Dictionary containing analysis results and paths to generated files
    - generate_visualization_report
      Example usage of the MetricVisualizer class.
      Args:
      metrics: Dictionary containing all analysis metrics
      output_dir: Directory to store visualization outputs
      Returns:
      Path to the generated HTML report
    - main
      Command-line interface for running analysis with visualizations.

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/visualizations/metric_visualizer.py
  Size: 13.6 KB
  Class: MetricVisualizer
    Generates visual representations of codebase metrics.
    Methods:
      Public:
        - generate_html_report
          Generate an HTML report containing all visualizations.
        - generate_visualizations
          Generate all visualizations for the metrics.
      Private:
        - _generate_complexity_heatmap
          Generate a heatmap of code complexity across the codebase.
        - _generate_dependency_graph
          Generate a network graph of project dependencies.
        - _generate_pattern_distribution
          Generate a treemap of detected code patterns.
        - _generate_performance_timeline
          Generate a timeline of performance metrics.
        - _generate_quality_metrics_sunburst
          Generate a sunburst chart of code quality metrics.
        - _generate_score_dashboard
          Generate a dashboard of key metric scores.
        - _generate_security_radar
          Generate a radar chart of security metrics.
  Public Functions:
    - generate_html_report
      Generate an HTML report containing all visualizations.
    - generate_visualizations
      Generate all visualizations for the metrics.
    - plot_sunburst

  Private Functions:
    - _generate_complexity_heatmap
      Generate a heatmap of code complexity across the codebase.
    - _generate_dependency_graph
      Generate a network graph of project dependencies.
    - _generate_pattern_distribution
      Generate a treemap of detected code patterns.
    - _generate_performance_timeline
      Generate a timeline of performance metrics.
    - _generate_quality_metrics_sunburst
      Generate a sunburst chart of code quality metrics.
    - _generate_score_dashboard
      Generate a dashboard of key metric scores.
    - _generate_security_radar
      Generate a radar chart of security metrics.

/mnt/Egg/code/python/apps/codebase-analyzer/example_usage.py
  Size: 944.0 B
  (Empty or initialization file)

/mnt/Egg/code/python/apps/codebase-analyzer/setup.py
  Size: 310.0 B
  (Empty or initialization file)

/mnt/Egg/code/python/apps/codebase-analyzer/tests/conftest.py
  Size: 887.0 B
  Public Functions:
    - analyzer
      Creates a CodebaseAnalyzer instance.
    - sample_codebase
      Creates a temporary sample codebase for testing.

/mnt/Egg/code/python/apps/codebase-analyzer/tests/helpers.py
  Size: 1.0 KB
  Class: TestHelper
    Methods:
      Public:
        - cleanup_temp
          Clean up temporary files/directories.
        - create_temp_file
          Create a temporary file with given content.
        - create_temp_project
          Create a temporary project directory with specified files.
  Public Functions:
    - cleanup_temp
      Clean up temporary files/directories.
    - create_temp_file
      Create a temporary file with given content.
    - create_temp_project
      Create a temporary project directory with specified files.

/mnt/Egg/code/python/apps/codebase-analyzer/tests/unit/test_analyzers/test_project_analyzer.py
  Size: 4.5 KB
  Class: TestProjectAnalyzer
    Methods:
      Public:
        - setup_method
        - teardown_method
          Clean up any remaining temporary files.
        - test_project_analyzer_empty_directory
          Test analyzing an empty directory.
        - test_project_analyzer_with_complex_structure
          Test analyzing a project with a more complex structure.
        - test_project_analyzer_with_files
          Test analyzing a directory with Python files.
        - test_project_analyzer_with_non_python_files
          Test analyzing a project with mixed file types.
  Public Functions:
    - setup_method
    - teardown_method
      Clean up any remaining temporary files.
    - test_project_analyzer_empty_directory
      Test analyzing an empty directory.
    - test_project_analyzer_with_complex_structure
      Test analyzing a project with a more complex structure.
    - test_project_analyzer_with_files
      Test analyzing a directory with Python files.
    - test_project_analyzer_with_non_python_files
      Test analyzing a project with mixed file types.

/mnt/Egg/code/python/apps/codebase-analyzer/tests/unit/test_analyzers/test_python_analyzer.py
  Size: 2.7 KB
  Class: FileInfo
    Attributes:
      - classes: Dict[str, dict]
      - content: str
      - dependencies: Set[str]
      - functions: Dict[str, dict]
      - path: Path
      - size: int
      - type: str
  Class: TestPythonAnalyzer
    Methods:
      Public:
        - setup_method
        - teardown_method
        - test_analyze_complex_function
        - test_analyze_dependencies
        - test_analyze_empty_file
        - test_analyze_simple_function
  Public Functions:
    - setup_method
    - teardown_method
    - test_analyze_complex_function
    - test_analyze_dependencies
    - test_analyze_empty_file
    - test_analyze_simple_function

/mnt/Egg/code/python/apps/codebase-analyzer/tests/unit/test_features/test_complexity_features.py
  Size: 1.8 KB
  Class: ComplexityFeatures
    Attributes:
      - code_metrics: dict
      - cognitive_complexity: int
      - cyclomatic_complexity: dict
      - halstead_metrics: dict
      - maintenance_index: float
  Class: TestComplexityFeatures
    Methods:
      Public:
        - setup_method
        - test_complexity_basic_function
        - test_complexity_nested_structures
        - test_maintainability_index
  Public Functions:
    - setup_method
    - test_complexity_basic_function
    - test_complexity_nested_structures
    - test_maintainability_index


Requirements Files:

/mnt/Egg/code/python/apps/codebase-analyzer/requirements.txt
  Size: 172.0 B


Text Files:

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/SOURCES.txt
  Size: 1.6 KB

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/dependency_links.txt
  Size: 1.0 B

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/entry_points.txt
  Size: 66.0 B

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/requires.txt
  Size: 13.0 B

/mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/top_level.txt
  Size: 24.0 B

/mnt/Egg/code/python/apps/codebase-analyzer/requirements-dev.txt
  Size: 181.0 B

Dependencies
------------

Required:
- abc.ABC
- abc.abstractmethod
- analyzers.generic_analyzer.GenericAnalyzer
- analyzers.project_analyzer.ProjectAnalyzer
- analyzers.python_analyzer.PythonAnalyzer
- argparse
- ast
- bandit
- base.FeatureExtractor
- base_analyzer.BaseAnalyzer
- chardet
- click
- codebase_analyzer.CodebaseAnalyzer
- codebase_analyzer.analyzer.CodebaseAnalyzer
- codebase_analyzer.analyzers.project_analyzer.ProjectAnalyzer
- codebase_analyzer.analyzers.python_analyzer.PythonAnalyzer
- codebase_analyzer.features.complexity.ComplexityFeatureExtractor
- codebase_analyzer.features.manager.FeatureExtractorManager
- collections.defaultdict
- complexity.ComplexityFeatureExtractor
- complexity_metrics.ComplexityAnalyzer
- concurrent.futures
- dataclasses.dataclass
- dataclasses.field
- datetime
- datetime.datetime
- dependency_metrics.DependencyAnalyzer
- dis
- enum.Enum
- formatters.summary_formatter.SummaryFormatter
- generic_analyzer.GenericAnalyzer
- importlib.metadata
- json
- lizard
- logging
- main.CodebaseAnalyzer
- main.main
- matplotlib.pyplot
- metrics.ComplexityMetrics
- metrics.DependencyMetrics
- metrics.PatternMetrics
- metrics.PerformanceMetrics
- metrics.QualityMetrics
- metrics.SecurityMetrics
- metrics.complexity_metrics.ComplexityAnalyzer
- metrics.complexity_metrics.ComplexityMetrics
- metrics.dependency_metrics.DependencyAnalyzer
- metrics.dependency_metrics.DependencyMetrics
- metrics.pattern_metrics.PatternAnalyzer
- metrics.pattern_metrics.PatternMetrics
- metrics.performance_metrics.PerformanceAnalyzer
- metrics.performance_metrics.PerformanceMetrics
- metrics.quality_metrics.QualityAnalyzer
- metrics.quality_metrics.QualityMetrics
- metrics.security_metrics.SecurityAnalyzer
- metrics.security_metrics.SecurityMetrics
- mimetypes
- models.data_classes.ClassInfo
- models.data_classes.CodeSnippet
- models.data_classes.FileInfo
- models.data_classes.FunctionInfo
- networkx
- numpy
- os
- packaging.version
- pathlib.Path
- pattern_metrics.PatternAnalyzer
- performance.PerformanceFeatureExtractor
- performance_metrics.PerformanceAnalyzer
- pickle
- pkg_resources
- pytest
- python_analyzer.PythonAnalyzer
- quality.QualityFeatureExtractor
- quality_metrics.QualityAnalyzer
- radon.complexity
- radon.metrics
- radon.visitors.ComplexityVisitor
- re
- recommendations.recommendation_engine.RecommendationEngine
- seaborn
- security.SecurityFeatureExtractor
- security_metrics.SecurityAnalyzer
- setuptools.find_packages
- setuptools.setup
- shutil
- sklearn.base.BaseEstimator
- sys
- tempfile
- tests.helpers.TestHelper
- typing.Any
- typing.Dict
- typing.List
- typing.Optional
- typing.Set
- typing.Tuple
- typing.Type
- typing.Union
- utils.file_utils.generate_tree_structure
- utils.file_utils.get_file_type
- utils.file_utils.safe_read_file
- utils.file_utils.save_to_file
- utils.file_utils.should_analyze_file

# Code Analysis Recommendations


## HIGH Priority

### Insufficient Test Coverage

**Category:** testing

**Impact:** Reduced reliability and increased regression risks

**Effort:** High - requires significant testing effort

**Suggested Actions:**
- Identify uncovered code paths
- Add unit tests for critical components
- Implement integration tests
- Set up CI/CD test automation

**Affected Files:**

**References:**
- Test Coverage Best Practices
- Testing Pyramid Guide

---

### Reduce Code Complexity

**Category:** complexity

**Impact:** Improved maintainability and reduced bug risk

**Effort:** High - requires refactoring

**Suggested Actions:**
- Refactor format_summary (complexity: 33) at /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/formatters/summary_formatter.py
- Refactor get_performance_summary (complexity: 16) at /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/performance_metrics.py

**Affected Files:**
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/formatters/summary_formatter.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/performance_metrics.py

**References:**
- Code Complexity Guidelines
- Refactoring Techniques

---


## MEDIUM Priority

### Improve Code Documentation

**Category:** documentation

**Impact:** Better maintainability and onboarding experience

**Effort:** Medium - can be done incrementally

**Suggested Actions:**
- Add docstrings to public APIs
- Document complex algorithms
- Update README files
- Generate API documentation

**Affected Files:**
- /mnt/Egg/code/python/apps/codebase-analyzer/README.md
- /mnt/Egg/code/python/apps/codebase-analyzer/setup.py
- /mnt/Egg/code/python/apps/codebase-analyzer/requirements-dev.txt
- /mnt/Egg/code/python/apps/codebase-analyzer/example_usage.py
- /mnt/Egg/code/python/apps/codebase-analyzer/requirements.txt
- /mnt/Egg/code/python/apps/codebase-analyzer/tests/pytest.ini
- /mnt/Egg/code/python/apps/codebase-analyzer/tests/unit/test_features/test_complexity_features.py
- /mnt/Egg/code/python/apps/codebase-analyzer/tests/unit/test_analyzers/test_python_analyzer.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/entry_points.txt
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/SOURCES.txt
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/requires.txt
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/top_level.txt
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer.egg-info/dependency_links.txt
- /mnt/Egg/code/python/apps/codebase-analyzer/.vscode/settings.json
- /mnt/Egg/code/python/apps/codebase-analyzer/.pytest_cache/README.md
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/__init__.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/__main__.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/models/data_classes.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/recommendations_example.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/prompt_example.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/examples/prompts/templates.json
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/metrics/__init__.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/analyzers/generic_analyzer.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/performance.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/security.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/complexity.py
- /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/features/quality.py

**References:**
- Documentation Best Practices
- API Documentation Guide

---
