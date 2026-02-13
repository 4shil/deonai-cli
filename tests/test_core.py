"""
Tests for DeonAi Core - Configuration
"""

import pytest
import json
from pathlib import Path
from deonai.core import load_config, save_config, CONFIG_FILE


def test_imports():
    """Test that core modules import correctly"""
    from deonai.core import (
        BaseContext,
        BaseTool,
        logger,
        DeonAiError
    )
    assert BaseContext is not None
    assert BaseTool is not None
    assert logger is not None
    assert DeonAiError is not None


def test_exceptions():
    """Test custom exceptions"""
    from deonai.core import ConfigError, ToolError, ContextError
    
    with pytest.raises(ConfigError):
        raise ConfigError("Test config error")
    
    with pytest.raises(ToolError):
        raise ToolError("Test tool error")
    
    with pytest.raises(ContextError):
        raise ContextError("Test context error")


def test_logger():
    """Test logging setup"""
    from deonai.core import logger
    
    assert logger is not None
    assert logger.name == "deonai"
    
    # Test logging doesn't crash
    logger.info("Test info message")
    logger.debug("Test debug message")
