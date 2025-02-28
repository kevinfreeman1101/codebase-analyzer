import mimetypes
from pathlib import Path
from typing import List

def should_analyze_file(file_path: str) -> bool:
    """Determine if a file should be analyzed based on its extension.

    Args:
        file_path: Path to the file to check

    Returns:
        bool: True if the file should be analyzed, False otherwise
    """
    ignored_extensions = ['.pyc', '.pyo', '.pyd', '.egg', '.egg-info']
    ignored_dirs = ['__pycache__', 'node_modules', 'venv', '.venv', '.git']

    path = Path(file_path)
    if any(part in ignored_dirs for part in path.parts):
        return False
    if path.suffix in ignored_extensions:
        return False
    # For testing, allow files without extensions or with known text types
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is None or mime_type.startswith('text') or path.suffix in ['.py', '.md', '.json', '.txt']

def get_file_type(file_path: str) -> str:
    """Determine the type of file based on extension and mime type.

    Args:
        file_path: Path to the file

    Returns:
        String representing the file type
    """
    path = Path(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    extension_map = {
        '.py': 'python',
        '.md': 'md',
        '.json': 'json',
        '.txt': 'txt',
        '.ini': 'ini',
        '.conf': 'conf',
        '.yml': 'yml',
        '.yaml': 'yml'
    }
    # Return extension-based type if known, else infer from mime or default to 'text'
    ext = path.suffix.lower()
    if ext in extension_map:
        return extension_map[ext]
    return 'python' if mime_type == 'text/x-python' else 'text' if mime_type and mime_type.startswith('text') else ext[1:] if ext else 'text'

def safe_read_file(file_path: str) -> str:
    """Safely read a file with multiple encoding fallbacks.

    Args:
        file_path: Path to the file to read

    Returns:
        The file contents as a string

    Raises:
        IOError: If the file cannot be read with any encoding
    """
    if not should_analyze_file(file_path):
        raise IOError(f"File type not supported for analysis: {file_path}")
    
    encodings = ['utf-8', 'latin-1', 'ascii']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except IOError as e:
            raise IOError(f"Cannot read file {file_path}: {str(e)}")
    raise IOError(f"Cannot decode file {file_path} with available encodings")

def save_to_file(content: str, file_path: str) -> bool:
    """Save content to a file with proper encoding.

    Args:
        content: String content to save
        file_path: Path where to save the file

    Returns:
        Boolean indicating success or failure
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError:
        return False

def generate_tree_structure(root_dir: str, files: List[str]) -> List[str]:
    """Generate a tree-like structure of the project.

    Args:
        root_dir: Root directory of the project
        files: List of file paths

    Returns:
        List of strings representing the tree structure
    """
    root_path = Path(root_dir)
    tree = []
    for file in sorted(files):
        rel_path = Path(file).relative_to(root_path)
        parts = rel_path.parts
        indent = "  " * (len(parts) - 1)
        prefix = "└─ " if len(parts) == 1 else "├─ "
        tree.append(f"{indent}{prefix}{parts[-1]}")
    return tree