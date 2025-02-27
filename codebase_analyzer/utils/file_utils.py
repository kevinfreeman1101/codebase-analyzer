# /mnt/Egg/code/python/apps/codebase-analyzer/codebase_analyzer/utils/file_utils.py
import os
import chardet
import mimetypes
from pathlib import Path
from typing import Optional, List, Set
import logging

logger = logging.getLogger(__name__)

ANALYZABLE_EXTENSIONS: Set[str] = {
    '.py', '.pyw', '.pyi', '.pyx', '.pxd', '.pxi',  # Python files
    '.txt', '.md', '.rst', '.json', '.yaml', '.yml', # Text files
    '.html', '.htm', '.css', '.js', '.ts',          # Web files
    '.xml', '.csv', '.ini', '.conf', '.cfg',        # Config files (added .cfg)
}

BINARY_EXTENSIONS: Set[str] = {
    '.pyc', '.pyo', '.so', '.dll', '.exe',
    '.whl', '.egg', '.zip', '.tar', '.gz',
    '.jpg', '.png', '.gif', '.wav', '.mp3',
    '.pdf', '.doc', '.docx', '.class'
}

def safe_read_file(file_path: str) -> str:
    """
    Safely read a file with multiple encoding fallbacks.

    Args:
        file_path: Path to the file to read

    Returns:
        The file contents as a string

    Raises:
        IOError: If the file cannot be read with any encoding
    """
    if not should_analyze_file(file_path):
        raise IOError(f"File type not supported for analysis: {file_path}")

    # First try chardet for automatic detection
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        detected = chardet.detect(raw_data)
        if detected['encoding'] and detected['confidence'] > 0.7:
            try:
                return raw_data.decode(detected['encoding'])
            except UnicodeDecodeError:
                pass
    except Exception:
        pass

    # Try our fallback encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise IOError(f"Error reading {file_path}: {str(e)}")

    # Last resort: try with utf-8 and replace errors
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Failed to read {file_path} with all encodings: {str(e)}")

def should_analyze_file(file_path: str) -> bool:
    """
    Determine if a file should be analyzed based on its extension.

    Args:
        file_path: Path to the file to check

    Returns:
        bool: True if the file should be analyzed, False otherwise
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    return (ext in ANALYZABLE_EXTENSIONS and
            ext not in BINARY_EXTENSIONS and
            not path.name.startswith('.'))

def get_file_type(file_path: str) -> str:
    """
    Determine the type of file based on extension and mime type.

    Args:
        file_path: Path to the file

    Returns:
        String representing the file type
    """
    ext = os.path.splitext(file_path)[1].lower()
    if not ext:
        mime_type = mimetypes.guess_type(file_path)[0]
        return f"no_extension_{mime_type or 'unknown'}"
    return ext[1:]  # Remove the leading dot

def generate_tree_structure(root_dir: str, files: list) -> List[str]:
    """
    Generate a tree-like structure of the project.

    Args:
        root_dir: Root directory of the project
        files: List of file paths

    Returns:
        List of strings representing the tree structure
    """
    tree = []
    for file_path in sorted(files):
        rel_path = os.path.relpath(file_path, root_dir)
        parts = rel_path.split(os.sep)
        indent = "  " * (len(parts) - 1)
        tree.append(f"{indent}└─ {parts[-1]}")
    return tree

def save_to_file(content: str, file_path: str) -> bool:
    """
    Save content to a file with proper encoding.

    Args:
        content: String content to save
        file_path: Path where to save the file

    Returns:
        Boolean indicating success or failure
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error saving file {file_path}: {str(e)}")
        return False