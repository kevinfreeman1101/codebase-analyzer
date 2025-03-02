"""Formatter for generating concise project summaries."""

from typing import Dict, Optional, Set, List
from pathlib import Path
from ..models.data_classes import FileInfo, FunctionInfo, ClassInfo

class SummaryFormatter:
    """Generates a concise summary of the project analysis."""

    def __init__(self, root_path: Path):
        """Initialize the SummaryFormatter with project root.

        Args:
            root_path: Path to the project root directory.
        """
        self.root_path = root_path
        self.source_files: Dict[str, FileInfo] = {}
        self.file_structure: Dict[str, Dict] = {}  # Nested dicts until leaf sets
        self.file_counts: Dict[str, int] = {}
        self.total_files: int = 0
        self.total_size: float = 0
        self.function_count: int = 0
        self.class_count: int = 0
        self.documented_count: int = 0
        self.dependencies: Dict[str, Set[str]] = {
            'required': set(),
            'standard': set(),
            'development': set()
        }
        self.dependency_health: Dict[str, str] = {'outdated': '', 'vulnerabilities': ''}  # Track dependency health
        self.project_overview: Dict[str, str] = {
            'name': self.root_path.name,
            'description': '',
            'python_version': '',
            'author': '',
            'version': ''
        }

    def add_source_file(self, relative_path: str, file_info: FileInfo) -> None:
        """Add source file information to the formatter.

        Args:
            relative_path: Path relative to the root.
            file_info: FileInfo object containing analysis results.
        """
        self.source_files[relative_path] = file_info
        self.total_files += 1
        self.total_size += file_info.size

        parts = relative_path.split('/')
        current_level = self.file_structure
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        if '_files' not in current_level:
            current_level['_files'] = set()
        current_level['_files'].add(parts[-1])

        file_type = file_info.type
        self.file_counts[file_type] = self.file_counts.get(file_type, 0) + 1

        self.function_count += len(file_info.functions)
        self.class_count += len(file_info.classes)

        for func_info in file_info.functions.values():
            if func_info.docstring:
                self.documented_count += 1

        for class_info in file_info.classes.values():
            if class_info.docstring:
                self.documented_count += 1
            self.documented_count += sum(1 for m in class_info.methods.values() if m.docstring)

        if 'test' in relative_path.lower():
            self.dependencies['development'].update(file_info.dependencies)
        else:
            self.dependencies['required'].update(file_info.dependencies - self.dependencies['standard'])

    def generate_summary(self) -> str:
        """Generate a formatted summary of the project analysis.

        Returns:
            str: A concise summary string including function and class details.
        """
        summary = []
        summary.append("CODEBASE SUMMARY")
        summary.append("===============")
        summary.append(f"\nRoot: {self.root_path}")

        summary.append("\nProject Overview")
        summary.append("--------------")
        summary.append(f"Name: {self.project_overview['name']}")

        summary.append("\nSummary Statistics")
        summary.append("------------------")
        summary.append(f"Directories: {len(self.file_structure)}")
        summary.append(f"Total Files: {self.total_files}")
        summary.append(f"Total Size: {self.total_size / 1024:.1f} KB")
        summary.append(f"Classes: {self.class_count}")
        summary.append(f"Functions: {self.function_count}")
        summary.append(f"Documented: {self.documented_count} ({self.documented_count / (self.function_count + self.class_count) * 100:.0f}% of functions)" if (self.function_count + self.class_count) > 0 else "Documented: 0 (0% of functions)")

        summary.append("\nFile Distribution:")
        for file_type, count in self.file_counts.items():
            summary.append(f"- {file_type.capitalize()} Files: {count} files")

        summary.append("\nDirectory Structure")
        summary.append("------------------")
        self._format_file_structure(summary, self.file_structure)

        summary.append("\nSource Files")
        summary.append("------------")
        for path, file_info in self.source_files.items():
            summary.append(f"\n{path}")
            summary.append(f"  Size: {file_info.size / 1024:.1f} KB")
            if file_info.functions:
                summary.append("  Functions:")
                for fname, finfo in file_info.functions.items():
                    summary.append(f"    - {fname} (Lines: {finfo.loc}, Documented: {'Yes' if finfo.docstring else 'No'})")
            if file_info.classes:
                summary.append("  Classes:")
                for cname, cinfo in file_info.classes.items():
                    summary.append(f"    - {cname} (Methods: {len(cinfo.methods)}, Documented: {'Yes' if cinfo.docstring else 'No'})")
            if not file_info.functions and not file_info.classes:
                summary.append("  (Empty or initialization file)")

        summary.append("\nDependencies")
        summary.append("------------")
        for dep_type, deps in self.dependencies.items():
            if deps:
                summary.append(f"\n{dep_type.capitalize()}:")
                summary.extend(f"  - {dep}" for dep in sorted(deps))

        summary.append("\nDependency Health")
        summary.append("----------------")
        summary.append("Outdated Packages:")
        summary.append(self.dependency_health['outdated'] or "None detected")
        summary.append("\nVulnerabilities:")
        summary.append(self.dependency_health['vulnerabilities'] or "None detected")

        return "\n".join(summary)

    def _format_file_structure(self, summary: List[str], structure: Dict[str, dict], prefix: str = "├─ ") -> None:
        """Recursively format the file structure.

        Args:
            summary: List to append formatted lines to.
            structure: Dictionary representing the file structure.
            prefix: String prefix for tree visualization.
        """
        items = sorted([k for k in structure.keys() if k != '_files'])
        files = structure.get('_files', set())
        all_items = items + sorted(files)
        for i, item in enumerate(all_items):
            is_last = i == len(all_items) - 1
            summary.append(f"{prefix}{item}")
            if item in structure and isinstance(structure[item], dict):
                new_prefix = "│  " if not is_last else "   "
                self._format_file_structure(summary, structure[item], new_prefix + "├─ ")