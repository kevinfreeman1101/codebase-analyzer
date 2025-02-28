# codebase_analyzer/recommendations/ml_engine.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type
import json
from pathlib import Path
import pickle
from dataclasses import dataclass
import numpy as np
from sklearn.base import BaseEstimator
import logging

@dataclass
class MLRecommendation:
    """Machine learning based recommendation with confidence score."""
    category: str
    suggestion: str
    reasoning: str
    confidence: float
    code_snippets: List[str]
    alternative_solutions: List[str]
    model_name: str
    features_used: List[str]

class ModelInterface(ABC):
    """Abstract base class for all ML models."""

    @abstractmethod
    def analyze(self, code_features: Dict[str, Any]) -> List[MLRecommendation]:
        """Analyze code features and return recommendations."""
        pass

    @abstractmethod
    def train(self, training_data: Dict[str, Any]) -> None:
        """Train the model with provided data."""
        pass

    @abstractmethod
    def save(self, path: Path) -> None:
        """Save the model to disk."""
        pass

    @abstractmethod
    def load(self, path: Path) -> None:
        """Load the model from disk."""
        pass

class LocalMLModel(ModelInterface):
    """Local machine learning model implementation."""

    def __init__(self, model: Optional[BaseEstimator] = None):
        self.model = model
        self.feature_extractors = self._initialize_feature_extractors()

    def analyze(self, code_features: Dict[str, Any]) -> List[MLRecommendation]:
        processed_features = self._process_features(code_features)
        predictions = self.model.predict_proba(processed_features)
        return self._convert_predictions_to_recommendations(predictions, code_features)

    def train(self, training_data: Dict[str, Any]) -> None:
        X = self._process_features(training_data['features'])
        y = training_data['labels']
        self.model.fit(X, y)

    def save(self, path: Path) -> None:
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, path: Path) -> None:
        with open(path, 'rb') as f:
            self.model = pickle.load(f)

    def _process_features(self, features: Dict[str, Any]) -> np.ndarray:
        """Process raw features into model-ready format."""
        processed = {}
        for extractor in self.feature_extractors:
            processed.update(extractor(features))
        return np.array(list(processed.values())).reshape(1, -1)

    def _initialize_feature_extractors(self):
        """Initialize feature extraction functions."""
        return [
            self._extract_complexity_features,
            self._extract_quality_features,
            self._extract_security_features,
            self._extract_performance_features
        ]

    def _extract_complexity_features(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Extract complexity-related features."""
        return {
            'avg_complexity': features.get('complexity', {}).get('average', 0.0),
            'max_complexity': features.get('complexity', {}).get('max', 0.0),
            'complexity_trend': features.get('complexity', {}).get('trend', 0.0)
        }

    # Additional feature extractors...

class LLMInterface(ModelInterface):
    """Base class for LLM-based analysis."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.prompt_templates = self._load_prompt_templates()

    @abstractmethod
    def _call_llm_api(self, prompt: str) -> str:
        """Make API call to LLM service."""
        pass

    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates from configuration."""
        template_path = Path(__file__).parent / 'prompts' / 'templates.json'
        with open(template_path) as f:
            return json.load(f)

class ClaudeInterface(LLMInterface):
    """Claude-specific implementation."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = self._initialize_client()

    def analyze(self, code_features: Dict[str, Any]) -> List[MLRecommendation]:
        prompt = self._prepare_analysis_prompt(code_features)
        response = self._call_llm_api(prompt)
        return self._parse_recommendations(response)

    def train(self, training_data: Dict[str, Any]) -> None:
        """Claude doesn't require traditional training."""
        pass

    def save(self, path: Path) -> None:
        """Save configuration and prompts."""
        with open(path, 'w') as f:
            json.dump({
                'config': self.config,
                'prompts': self.prompt_templates
            }, f)

    def load(self, path: Path) -> None:
        """Load configuration and prompts."""
        with open(path) as f:
            data = json.load(f)
            self.config = data['config']
            self.prompt_templates = data['prompts']

    def _call_llm_api(self, prompt: str) -> str:
        """Make API call to Claude."""
        try:
            response = self.client.complete(prompt)
            return response.completion
        except Exception as e:
            logging.error(f"Claude API error: {e}")
            return ""

class MLRecommendationEngine:
    """Coordinates different ML models for code analysis."""

    def __init__(self, model_config: Dict[str, Any]):
        self.model_config = model_config
        self.models: Dict[str, ModelInterface] = {}
        self._initialize_models()

    def _initialize_models(self) -> None:
        """Initialize configured models."""
        model_mapping = {
            'claude': ClaudeInterface,
            'local': LocalMLModel,
            # Add more model types here
        }

        for model_name, config in self.model_config.items():
            model_type = config['type']
            if model_type in model_mapping:
                self.models[model_name] = model_mapping[model_type](config)

    def add_model(self, name: str, model: ModelInterface) -> None:
        """Add a new model to the engine."""
        self.models[name] = model

    def remove_model(self, name: str) -> None:
        """Remove a model from the engine."""
        self.models.pop(name, None)

    def analyze(self, code_features: Dict[str, Any], 
                model_name: Optional[str] = None) -> List[MLRecommendation]:
        """Get recommendations from specified or all models."""
        recommendations = []

        if model_name and model_name in self.models:
            return self.models[model_name].analyze(code_features)

        for model in self.models.values():
            try:
                recommendations.extend(model.analyze(code_features))
            except Exception as e:
                logging.error(f"Model analysis error: {e}")

        return self._aggregate_recommendations(recommendations)

    def _aggregate_recommendations(self, 
                                 recommendations: List[MLRecommendation]
                                 ) -> List[MLRecommendation]:
        """Aggregate and deduplicate recommendations from multiple models."""
        # Group similar recommendations
        grouped = {}
        for rec in recommendations:
            key = (rec.category, rec.suggestion)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(rec)

        # Merge similar recommendations
        merged = []
        for recs in grouped.values():
            if len(recs) == 1:
                merged.append(recs[0])
            else:
                merged.append(self._merge_recommendations(recs))

        return sorted(merged, key=lambda x: x.confidence, reverse=True)

    def _merge_recommendations(self, 
                             recommendations: List[MLRecommendation]
                             ) -> MLRecommendation:
        """Merge similar recommendations from different models."""
        return MLRecommendation(
            category=recommendations[0].category,
            suggestion=recommendations[0].suggestion,
            reasoning="\n".join(set(r.reasoning for r in recommendations)),
            confidence=np.mean([r.confidence for r in recommendations]),
            code_snippets=list(set(sum((r.code_snippets for r in recommendations), []))),
            alternative_solutions=list(set(sum((r.alternative_solutions for r in recommendations), []))),
            model_name="ensemble",
            features_used=list(set(sum((r.features_used for r in recommendations), [])))
        )