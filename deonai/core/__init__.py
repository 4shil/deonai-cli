"""
DeonAi Core Package
"""

from .config import (
    CONFIG_DIR,
    CONFIG_FILE,
    HISTORY_FILE,
    PROFILES_FILE,
    SYSTEM_PROMPT_FILE,
    MODELS_CACHE_FILE,
    OPENROUTER_API_URL,
    DEONAI_SYSTEM,
    load_config,
    save_config,
    load_history,
    save_history
)

__all__ = [
    'CONFIG_DIR',
    'CONFIG_FILE',
    'HISTORY_FILE',
    'PROFILES_FILE',
    'SYSTEM_PROMPT_FILE',
    'MODELS_CACHE_FILE',
    'OPENROUTER_API_URL',
    'DEONAI_SYSTEM',
    'load_config',
    'save_config',
    'load_history',
    'save_history'
]
