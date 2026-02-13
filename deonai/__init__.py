"""
DeonAi CLI Package
Version 3.0.0-dev
"""

__version__ = "3.0.0-dev"
__author__ = "4shil"
__description__ = "Your AI coding assistant in the terminal"

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
