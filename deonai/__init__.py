"""
DeonAi CLI Package
Version 3.0.0
"""

__version__ = "3.0.0"
__author__ = "4shil"
__description__ = "Your AI coding assistant in the terminal - Now with project awareness and autonomous capabilities"

from .core import *
from .utils import *

__all__ = [
    '__version__',
    'Colors',
    'colored',
    'DEONAI_BANNER',
    'load_config',
    'save_config',
    'load_history',
    'save_history'
]
