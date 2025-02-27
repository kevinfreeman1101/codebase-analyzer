# codebase_analyzer/recommendations/prompt_manager.py
from pathlib import Path
import json
from typing import Dict, Any, Optional
import logging

class PromptManager:
    """Manages prompt templates and their rendering."""

    def __init__(self, custom_templates_path: Optional[Path] = None):
        self.templates = self._load_templates(custom_templates_path)
        self.template_variables = self._initialize_variables()

    def _load_templates(self, custom_path: Optional[Path] = None) -> Dict[str, Any]:
        """Load built-in and custom prompt templates."""
        # Load built-in templates
        base_path = Path(__file__).parent / 'prompts' / 'templates.json'
        with open(base_path) as f:
            templates = json.load(f)

        # Load and merge custom templates if provided
        if custom_path and custom_path.exists():
            try:
                with open(custom_path) as f:
                    custom_templates = json.load(f)
                templates = self._merge_templates(templates, custom_templates)
            except Exception as e:
                logging.error(f"Error loading custom templates: {e}")

        return templates

    def _merge_templates(self, base: Dict[str, Any], 
                        custom: Dict[str, Any]) -> Dict[str, Any]:
        """Merge custom templates with base templates."""
        merged = base.copy()
        for category, templates in custom.items():
            if category in merged:
                merged[category].update(templates)
            else:
                merged[category] = templates
        return merged

    def _initialize_variables(self) -> Dict[str, Any]:
        """Initialize default template variables."""
        return {
            'project_type': 'unknown',
            'language': 'unknown',
            'framework': 'unknown',
            'current_issues': []
        }

    def set_variable(self, name: str, value: Any) -> None:
        """Set a template variable value."""
        self.template_variables[name] = value

    def get_prompt(self, template_name: str, 
                   variables: Optional[Dict[str, Any]] = None) -> str:
        """Get a rendered prompt template."""
        # Find the template
        template = self._get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")

        # Merge default and provided variables
        render_vars = self.template_variables.copy()
        if variables:
            render_vars.update(variables)

        # Render the template
        try:
            return template.format(**render_vars)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {e}")

    def _get_template(self, template_name: str) -> Optional[str]:
        """Get a template by name, supporting dot notation."""
        parts = template_name.split('.')
        current = self.templates
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current if isinstance(current, str) else None

    def add_template(self, name: str, template: str) -> None:
        """Add a new template or override existing one."""
        parts = name.split('.')
        current = self.templates
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = template

    def list_templates(self) -> Dict[str, str]:
        """List all available templates."""
        templates = {}
        self._collect_templates(self.templates, '', templates)
        return templates

    def _collect_templates(self, current: Dict[str, Any], 
                          prefix: str, result: Dict[str, str]) -> None:
        """Recursively collect template names."""
        for key, value in current.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, str):
                result[full_key] = value
            elif isinstance(value, dict):
                self._collect_templates(value, full_key, result)