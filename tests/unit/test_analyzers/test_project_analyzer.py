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
    
        assert isinstance(result, str)
        assert "CODEBASE SUMMARY" in result
        assert str(project_dir) in result
        assert "Project Overview" in result
    
        assert "main.py" in result
        assert "utils/helper.py" in result
        assert "tests/test_main.py" in result
    
        assert "Total Files: 3" in result  # Updated for precision
        assert "Python Files: 3" in result

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
    
        assert isinstance(result, str)
        assert "CODEBASE SUMMARY" in result
    
        assert "src/main.py" in result
        assert "src/utils/helper.py" in result
        assert "tests/test_main.py" in result
    
        assert "main" in result
        assert "helper_function" in result
        assert "HelperClass" in result
        assert "Total Files: 3" in result

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
    
        assert isinstance(result, str)
        assert "CODEBASE SUMMARY" in result
    
        assert "Python Files: 1" in result
        assert "Documentation Files: 1" in result
        assert "Configuration Files: 1" in result
        assert "Text Files: 1" in result
        assert "Total Files: 4" in result

    def test_analyze_empty_project(self):
        """Test analyzing an empty project directory with detailed metrics."""
        temp_dir = self.helper.create_temp_project({})
        analyzer = ProjectAnalyzer(Path(temp_dir))
        result = analyzer.analyze()
        assert isinstance(result, str)
        assert "Total Files: 0" in result
        assert "Classes: 0" in result
        assert "Functions: 0" in result
        assert "Dependency Health" in result  # Check new feature

    def test_analyze_simple_project(self):
        """Test analyzing a project with a simple Python file."""
        project_files = {
            "test.py": 'def foo():\n    """Simple function."""\n    return "bar"'
        }
        temp_dir = self.helper.create_temp_project(project_files)
        analyzer = ProjectAnalyzer(Path(temp_dir))
        result = analyzer.analyze()
        assert "Total Files: 1" in result
        assert "Functions: 1" in result
        assert "Documented: 1" in result
        assert "test.py" in result
        assert "foo" in result
        assert "Dependency Health" in result  # Check new feature