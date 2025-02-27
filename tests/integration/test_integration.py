from pathlib import Path
from codebase_analyzer.analyzer import CodebaseAnalyzer
import pytest

class TestIntegration:
    def setup_method(self):
        self.analyzer = CodebaseAnalyzer()

    def test_full_analysis(self, tmp_path):
        """Test full analysis on a sample project."""
        # Create a sample project structure
        project_dir = tmp_path / "sample_project"
        project_dir.mkdir()
        (project_dir / "main.py").write_text("""
def main():
    if True:
        print('Hello, world!')
    return None
""")
        (project_dir / "utils.py").write_text("""
import os

def helper():
    os.system('echo test')
""")
        (project_dir / "README.md").write_text("# Sample Project")

        # Run analysis
        result = self.analyzer.analyze_project(project_dir)
        summary = self.analyzer.generate_summary()

        # Assertions
        assert result.total_files == 2  # Only .py files counted
        assert result.total_lines > 0
        assert "Codebase Analysis Summary" in summary
        assert "Total Files: 2" in summary
        assert len(result.security.vulnerabilities) > 0  # os.system call
        assert result.complexity.cyclomatic_complexity >= 2  # if + base
        assert 0 <= result.calculate_overall_score() <= 100