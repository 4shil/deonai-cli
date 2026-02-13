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

from .base import (
    BaseContext,
    BaseTool,
    BaseIntegration,
    DeonAiError,
    ConfigError,
    ContextError,
    ToolError,
    IntegrationError
)

from .logger import logger, setup_logger

from .context import ContextManager

from .tools import Tool, ToolRegistry, ToolCall, registry

from .agent import AgenticExecutor, ToolCallFormatter, executor, formatter

# Import to register built-in tools
from . import builtin_tools
from . import git_tools
from . import patch_tools

__all__ = [
    # Config
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
    'save_history',
    # Base classes
    'BaseContext',
    'BaseTool',
    'BaseIntegration',
    # Exceptions
    'DeonAiError',
    'ConfigError',
    'ContextError',
    'ToolError',
    'IntegrationError',
    # Logging
    'logger',
    'setup_logger',
    # Context
    'ContextManager',
    # Tools
    'Tool',
    'ToolRegistry',
    'ToolCall',
    'registry',
    # Agent
    'AgenticExecutor',
    'ToolCallFormatter',
    'executor',
    'formatter'
]
