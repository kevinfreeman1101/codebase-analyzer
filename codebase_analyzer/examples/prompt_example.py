# Initialize prompt manager
prompt_manager = PromptManager()

# Set project-specific variables
prompt_manager.set_variable('project_type', 'web_application')
prompt_manager.set_variable('language', 'python')
prompt_manager.set_variable('framework', 'django')

# Get a specific prompt
analysis_prompt = prompt_manager.get_prompt('code_analysis.analysis_prompt', {
    'metrics_json': json.dumps(code_metrics),
    'current_issues': ['performance bottlenecks', 'security vulnerabilities']
})

# Add a custom template
prompt_manager.add_template('custom.performance', """
Analyze performance metrics for specific framework: {framework}
Metrics: {metrics_json}
""")