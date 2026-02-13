"""
DeonAi Utils Package
"""

from .colors import Colors, colored, DEONAI_BANNER
from .animations import LoadingAnimation, TypingAnimation
from .diff import DiffEngine
from .fileops import (
    parse_and_save_files,
    read_file,
    write_file,
    list_directory,
    detect_language,
    validate_syntax
)

__all__ = [
    'Colors',
    'colored',
    'DEONAI_BANNER',
    'LoadingAnimation',
    'TypingAnimation',
    'DiffEngine',
    'parse_and_save_files',
    'read_file',
    'write_file',
    'list_directory',
    'detect_language',
    'validate_syntax'
]
