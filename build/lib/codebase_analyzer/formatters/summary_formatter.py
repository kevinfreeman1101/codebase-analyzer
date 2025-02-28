from pathlib import Path
from typing import Dict, List, Optional, Set
import os
from ..models.data_classes import FileInfo

class SummaryFormatter:
    """Formats codebase analysis results into a readable summary."""

    def __init__(self, root_path: Path):
        """Initialize the SummaryFormatter.

        Args:
            root_path: Path to the project root directory
        """
        self.root_path = root_path
        self.source_files = {}
        self.file_structure = {}
        self.file_counts = {}
        self.total_files = 0
        self.total_size = 0
        self.function_count = 0
        self.class_count = 0
        self.documented_count = 0
        self.dependencies = {
            'required': set(),
            'standard': set(),
            'development': set()
        }
        self.project_overview = {
            'name': self.root_path.name,
            'description': '',
            'python_version': '',
            'author': '',
            'version': ''
        }
        self.build_artifacts = set()

        # File type display names
        self.file_type_names = {
            'python': 'Python Files',
            'md': 'Documentation Files',
            'json': 'Configuration Files',
            'txt': 'Text Files',
            'documentation': 'Documentation Files',
            'configuration': 'Configuration Files',
            'text': 'Text Files'
        }

    def _get_size_str(self, size_in_bytes: int) -> str:
        """Convert bytes to human readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.1f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.1f} TB"

    def _get_percentage(self, part: int, total: int) -> int:
        """Calculate percentage, handling division by zero."""
        return round((part / total) * 100) if total > 0 else 0

    def _get_file_type_counts(self) -> Dict[str, int]:
        """Count files by type."""
        type_counts = {}
        for info in self.source_files.values():
            file_type = info.type
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
        return type_counts

    def _format_project_overview(self) -> List[str]:
        """Format the project overview section."""
        sections = [
            "Project Overview",
            "--------------",
            f"Name: {self.project_overview['name']}"
        ]
        if self.project_overview['description']:
            sections.append(f"Description: {self.project_overview['description']}")
        if self.project_overview['version']:
            sections.append(f"Version: {self.project_overview['version']}")
        if self.project_overview['author']:
            sections.append(f"Author: {self.project_overview['author']}")
        if self.project_overview['python_version']:
            sections.append(f"Python Version: {self.project_overview['python_version']}")
        return sections

    def _format_summary_statistics(self) -> List[str]:
        """Format the summary statistics section."""
        dir_count = sum(1 for path in self.root_path.rglob("*") 
                       if path.is_dir() 
                       and not any(part.startswith(('.', '__pycache__', '*.egg-info')) 
                                  for part in path.parts))
        metrics = [
            "Summary Statistics",
            "------------------",
            f"Directories: {dir_count}",
            f"Total Files: {self.total_files}",
            f"Total Size: {self._get_size_str(self.total_size)}",
            f"Classes: {self.class_count}",
            f"Functions: {self.function_count}",
            f"Documented: {self.documented_count} ({self._get_percentage(self.documented_count, self.function_count)}% of functions)",
            "",
            "File Distribution:"
        ]
        for file_type, count in self._get_file_type_counts().items():
            display_name = self.file_type_names.get(file_type, file_type.capitalize())
            metrics.append(f"- {display_name}: {count} files")
        return metrics

    def _format_tree(self, path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
        """Generate hierarchical tree structure."""
        lines = []
        if any(part.startswith('.') for part in path.parts) or \
           any(part.startswith('__pycache__') for part in path.parts):
            return lines

        if path != self.root_path:
            connector = "└─ " if is_last else "├─ "
            lines.append(f"{prefix}{connector}{path.name}")
            prefix += "   " if is_last else "│  "

        if path.is_dir():
            children = sorted(list(path.iterdir()))
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                lines.extend(self._format_tree(child, prefix, is_last_child))
        return lines

    def _format_function_groups(self, grouped_funcs: Dict[str, List[tuple]], indent: str = "") -> List[str]:
        """Format grouped functions with proper indentation and documentation."""
        lines = []
        if grouped_funcs['public']:
            lines.append(f"{indent}Public Functions:")
            for func_name, func_info in grouped_funcs['public']:
                lines.append(f"{indent}  - {func_name}")
                if func_info.docstring:
                    doc_lines = func_info.docstring.split('\n')
                    for line in doc_lines:
                        if line.strip():
                            if any(marker in line for marker in ['Args:', 'Returns:', 'Raises:']):
                                lines.append(f"{indent}    {line}")
                            else:
                                lines.append(f"{indent}    {line.strip()}")

        if grouped_funcs['private']:
            if grouped_funcs['public']:
                lines.append("")
            lines.append(f"{indent}Private Functions:")
            for func_name, func_info in grouped_funcs['private']:
                lines.append(f"{indent}  - {func_name}")
                if func_info.docstring:
                    doc_lines = func_info.docstring.split('\n')
                    for line in doc_lines:
                        if line.strip():
                            if any(marker in line for marker in ['Args:', 'Returns:', 'Raises:']):
                                lines.append(f"{indent}    {line}")
                            else:
                                lines.append(f"{indent}    {line.strip()}")
        return lines

    def _group_functions(self, functions: Dict[str, 'FunctionInfo']) -> Dict[str, List[tuple]]:
        """Group functions by visibility (public/private)."""
        grouped = {'public': [], 'private': []}
        for func_name, func_info in sorted(functions.items()):
            if func_name == '__init__':
                continue
            if func_name.startswith('_'):
                grouped['private'].append((func_name, func_info))
            else:
                grouped['public'].append((func_name, func_info))
        return grouped

    def _format_source_files(self) -> List[str]:
        """Format the source files section."""
        sections = ["Source Files", "------------"]
        by_type: Dict[str, List[tuple]] = {}
        for file_path, info in self.source_files.items():
            file_type = info.type
            if file_type not in by_type:
                by_type[file_type] = []
            by_type[file_type].append((file_path, info))

        for file_type, files in sorted(by_type.items()):
            display_name = self.file_type_names.get(file_type, file_type.capitalize())
            sections.append(f"\n{display_name}:\n")
            for file_path, info in sorted(files):
                sections.append(f"{file_path}")
                sections.append(f"  Size: {self._get_size_str(info.size)}")

                # Always include functions and classes if present
                if info.functions:
                    grouped_funcs = self._group_functions(info.functions)
                    sections.extend(self._format_function_groups(grouped_funcs, indent="  "))
                if info.classes:
                    for class_name, class_info in sorted(info.classes.items()):
                        sections.append(f"  Class: {class_name}")
                        if class_info.docstring:
                            sections.append(f"    {class_info.docstring}")
                        if class_info.attributes:
                            sections.append("    Attributes:")
                            for attr_info in sorted(class_info.attributes, key=lambda x: x.get('name', '')):
                                attr_name = attr_info.get('name', '')
                                attr_type = f": {attr_info.get('type_annotation', '')}" if attr_info.get('type_annotation') else ""
                                attr_doc = f" - {attr_info.get('docstring', '')}" if attr_info.get('docstring') else ""
                                sections.append(f"      - {attr_name}{attr_type}{attr_doc}")
                        if class_info.methods:
                            sections.append("    Methods:")
                            public_methods = [(m.name, m.docstring) for m in class_info.methods if not m.name.startswith('_') and m.name != '__init__']
                            private_methods = [(m.name, m.docstring) for m in class_info.methods if m.name.startswith('_') and m.name != '__init__']
                            if public_methods:
                                sections.append("      Public:")
                                for method_name, method_doc in sorted(public_methods):
                                    method_str = f"        - {method_name}"
                                    if method_doc:
                                        method_str += f"\n          {method_doc}"
                                    sections.append(method_str)
                            if private_methods:
                                sections.append("      Private:")
                                for method_name, method_doc in sorted(private_methods):
                                    method_str = f"        - {method_name}"
                                    if method_doc:
                                        method_str += f"\n          {method_doc}"
                                    sections.append(method_str)

                if not info.functions and not info.classes and file_type.lower() == 'python':
                    if info.content and info.content.strip().startswith('"""'):
                        sections.append(f"  {info.content.strip().splitlines()[0]}")
                    else:
                        sections.append("  (Empty or initialization file)")
                sections.append("")
        return sections

    def _format_dependencies(self) -> List[str]:
        """Format the dependencies section."""
        sections = ["Dependencies", "------------"]
        if self.dependencies['required']:
            sections.extend(["\nRequired:", *[f"- {dep}" for dep in sorted(self.dependencies['required'])]])
        if self.dependencies['development']:
            sections.extend(["\nDevelopment:", *[f"- {dep}" for dep in sorted(self.dependencies['development'])]])
        return sections if any(deps for deps in self.dependencies.values()) else []

    def _format_build_artifacts(self) -> List[str]:
        """Format the build artifacts section."""
        return ["Build Artifacts", "--------------", *[f"- {artifact}" for artifact in sorted(self.build_artifacts)]] if self.build_artifacts else []

    def update_project_overview(self, info: Dict) -> None:
        """Update project overview information."""
        if info:
            self.project_overview.update({
                k: v for k, v in info.items() 
                if k in self.project_overview and v
            })

    def set_python_version(self, version: str) -> None:
        """Set the minimum Python version requirement."""
        self.project_overview['python_version'] = version

    def set_project_overview(self, overview: str) -> None:
        """Set the project overview description."""
        self.project_overview['description'] = overview

    def add_build_artifact(self, file_path: str) -> None:
        """Add a build artifact file."""
        self.build_artifacts.add(file_path)
        self.total_files += 1
        full_path = self.root_path / file_path
        if full_path.exists():
            self.total_size += os.path.getsize(full_path)

    def add_dependency(self, category: str, dependencies: Set[str]) -> None:
        """Add project dependencies to the specified category."""
        if category in self.dependencies:
            self.dependencies[category].update(dependencies)

    def add_source_file(self, file_path: str, info: FileInfo) -> None:
        """Add information about a source file."""
        self.source_files[file_path] = info
        self.total_files += 1

        full_path = self.root_path / Path(file_path)
        if full_path.exists():
            size = os.path.getsize(full_path)
            self.total_size += size
        else:
            size = info.size

        file_type = info.type
        self.file_counts[file_type] = self.file_counts.get(file_type, 0) + 1

        if file_type == 'python':
            self.function_count += len(info.functions)
            self.documented_count += sum(1 for f in info.functions.values() if f.docstring)
            if info.classes:
                self.class_count += len(info.classes)
                for class_info in info.classes.values():
                    self.function_count += len(class_info.methods)
                    self.documented_count += sum(1 for m in class_info.methods if m.docstring)

        path_parts = file_path.split('/')
        current_dict = self.file_structure
        for part in path_parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        current_dict[path_parts[-1]] = {
            'type': file_type,
            'size': size,
            'functions': len(info.functions),
            'classes': len(info.classes)
        }

        if info.dependencies:
            self.add_dependency('required', info.dependencies)

    def format_summary(self) -> str:
        """Generate the complete codebase summary."""
        sections = [
            "CODEBASE SUMMARY",
            "===============",
            f"\nRoot: {self.root_path.absolute()}"
        ]
        sections.extend(self._format_project_overview())
        sections.extend([""])
        sections.extend(self._format_summary_statistics())
        sections.extend(["", "Directory Structure", "------------------"])
        sections.extend(self._format_tree(self.root_path))
        sections.extend([""])
        sections.extend(self._format_source_files())
        sections.extend(self._format_dependencies())
        if self.build_artifacts:
            sections.extend([""])
            sections.extend(self._format_build_artifacts())
        return "\n".join(sections)