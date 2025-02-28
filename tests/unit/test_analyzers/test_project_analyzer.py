import pytest
from pathlib import Path
from tests.helpers import TestHelper
from codebase_analyzer.analyzers.project_analyzer import ProjectAnalyzer

class TestProjectAnalyzer:
    def setup_method(self):
        self.helper = TestHelper()

    def teardown_method(self):
        self.helper.cleanup_temp()

    def test_project_analyzer_empty_directory(self):
        """Test analyzing an empty directory."""
        project_dir = self.helper.create_temp_project({})
        analyzer = ProjectAnalyzer(root_path=project_dir)
        result = analyzer.analyze()
        
        assert isinstance(result, str)
        assert "CODEBASE SUMMARY" in result
        assert "Total Files: 0" in result

    def test_project_analyzer_with_files(self):
        """Test analyzing a directory with Python files."""
        files = {
            "main.py": "print('hello')",
            "utils/helper.py": "def help(): pass",
            "tests/test_main.py": "def test_main(): pass"
        }
        project_dir = self.helper.create_temp_project(files)
    
        analyzer = ProjectAnalyzer(root_path=project_dir)
        result = analyzer.analyze()
    
        # Basic type assertion
        assert isinstance(result, str)
    
        # Content assertions
        assert "CODEBASE SUMMARY" in result
        assert str(project_dir) in result
        assert "Project Overview" in result
    
        # File-specific assertions
        assert "main.py" in result
        assert "utils/helper.py" in result
        assert "tests/test_main.py" in result
    
        # Statistics assertions
        assert "Total Files:" in result
        assert "Python Files:" in result  # Should now match with fix

    def test_project_analyzer_with_complex_structure(self):
        """Test analyzing a project with a more complex structure."""
        files = {
            "src/main.py": """
def main():
    print('hello')
if __name__ == '__main__':
    main()
""",
            "src/utils/helper.py": """
def helper_function(x):
    return x * 2
class HelperClass:
    def method(self):
        pass
""",
            "tests/test_main.py": """
def test_main():
    assert True
def test_helper():
    assert True
"""
        }
        project_dir = self.helper.create_temp_project(files)
    
        analyzer = ProjectAnalyzer(root_path=project_dir)
        result = analyzer.analyze()
    
        # Basic assertions
        assert isinstance(result, str)
        assert "CODEBASE SUMMARY" in result
    
        # Structure assertions
        assert "src/main.py" in result
        assert "src/utils/helper.py" in result
        assert "tests/test_main.py" in result
    
        # Content assertions
        assert "main" in result  # Function from main.py
        assert "helper_function" in result  # Function from helper.py

    def test_project_analyzer_with_non_python_files(self):
        """Test analyzing a project with mixed file types."""
        files = {
            "src/main.py": "print('hello')",
            "README.md": """# Project
Description""",
            "config.json": """{"key": "value"}""",
            "requirements.txt": "pytest>=6.0.0"
        }
        project_dir = self.helper.create_temp_project(files)
    
        analyzer = ProjectAnalyzer(root_path=project_dir)
        result = analyzer.analyze()
    
        # Basic assertions
        assert isinstance(result, str)
        assert "CODEBASE SUMMARY" in result
    
        # File type assertions
        assert "Python Files:" in result  # Should now match with fix
        assert "Documentation Files:" in result
        assert "Configuration Files:" in result
        assert "Text Files:" in result