"""
DeonAi Utils - File Operations Helpers
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional
from .colors import Colors, colored


def parse_and_save_files(response_text: str, current_dir: str = '.') -> List[str]:
    """
    Parse AI response for WRITE_FILE directives and save files
    Returns list of saved filenames
    """
    pattern = r'WRITE_FILE:\s*([^\n]+)\n```(?:\w+)?\n(.*?)```'
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    saved_files = []
    for filename, content in matches:
        filename = filename.strip()
        filepath = Path(current_dir) / filename
        
        try:
            # Create parent directories if needed
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            filepath.write_text(content)
            saved_files.append(filename)
            
        except Exception as e:
            print(f"{colored('[ERROR]', Colors.RED)} Could not write {filename}: {e}")
    
    return saved_files


def read_file(filepath: str) -> Tuple[bool, str]:
    """
    Read file contents
    Returns (success, content_or_error)
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return False, f"File not found: {filepath}"
        
        if not path.is_file():
            return False, f"Not a file: {filepath}"
        
        # Check file size
        size = path.stat().st_size
        if size > 1024 * 1024:  # 1MB limit
            return False, f"File too large: {size} bytes (max 1MB)"
        
        content = path.read_text(encoding='utf-8', errors='ignore')
        return True, content
        
    except Exception as e:
        return False, f"Error reading file: {e}"


def write_file(filepath: str, content: str, mode: str = 'w') -> Tuple[bool, str]:
    """
    Write content to file
    Returns (success, message)
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        
        return True, f"Written to {filepath}"
        
    except Exception as e:
        return False, f"Error writing file: {e}"


def list_directory(dirpath: str = '.', pattern: str = '*') -> Tuple[bool, List[str]]:
    """
    List files in directory
    Returns (success, list_of_files_or_error)
    """
    try:
        path = Path(dirpath)
        if not path.exists():
            return False, [f"Directory not found: {dirpath}"]
        
        if not path.is_dir():
            return False, [f"Not a directory: {dirpath}"]
        
        files = []
        for item in path.glob(pattern):
            if item.is_file():
                files.append(str(item.relative_to(path)))
            elif item.is_dir():
                files.append(str(item.relative_to(path)) + "/")
        
        return True, sorted(files)
        
    except Exception as e:
        return False, [f"Error listing directory: {e}"]


def detect_language(filepath: str) -> Optional[str]:
    """Detect programming language from file extension"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'zsh',
        '.fish': 'fish',
    }
    
    ext = Path(filepath).suffix.lower()
    return ext_map.get(ext)


def validate_syntax(filepath: str, language: str = None) -> Tuple[bool, str]:
    """
    Validate file syntax (basic check)
    Returns (valid, message)
    """
    if not language:
        language = detect_language(filepath)
    
    if not language:
        return True, "Unknown language, skipping validation"
    
    try:
        path = Path(filepath)
        content = path.read_text()
        
        # Basic validation
        if language == 'python':
            compile(content, filepath, 'exec')
            return True, "Syntax OK"
        
        # For other languages, just check it's not empty
        if not content.strip():
            return False, "File is empty"
        
        return True, "Basic checks passed"
        
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"
