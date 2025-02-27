# Example configuration
model_config = {
    'claude': {
        'type': 'claude',
        'api_key': 'your_api_key',
        'model_version': 'claude-3',
        'temperature': 0.7
    },
    'local_ml': {
        'type': 'local',
        'model_path': 'models/code_analysis_model.pkl',
        'feature_config': {
            'use_complexity': True,
            'use_quality': True,
            'use_security': True
        }
    }
}

# Initialize the ML recommendation engine
ml_engine = MLRecommendationEngine(model_config)

# Analyze code with specific model
claude_recommendations = ml_engine.analyze(code_features, model_name='claude')

# Analyze code with all models
all_recommendations = ml_engine.analyze(code_features)

# Add custom model
class CustomModel(ModelInterface):
    # Implement required methods
    pass

custom_model = CustomModel()
ml_engine.add_model('custom_model', custom_model)