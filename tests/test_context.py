"""
Test Context Manager - Workspace Detection
"""

import pytest
from pathlib import Path
from deonai.core.context import ContextManager


def test_context_manager_init():
    """Test context manager initialization"""
    ctx = ContextManager()
    assert ctx.cwd is not None
    assert ctx.workspace is not None
    assert ctx.project_info is not None


def test_workspace_detection():
    """Test workspace detection"""
    ctx = ContextManager()
    workspace = ctx.detect_workspace()
    
    assert workspace is not None
    assert isinstance(workspace, Path)
    assert workspace.exists()


def test_project_info():
    """Test project info extraction"""
    ctx = ContextManager()
    info = ctx.get_project_info()
    
    assert "root" in info
    assert "type" in info
    assert "language" in info
    assert "features" in info


def test_is_in_workspace():
    """Test workspace membership check"""
    ctx = ContextManager()
    
    # Current dir should be in workspace
    assert ctx.is_in_workspace(ctx.cwd)
    
    # Root should not be (unless workspace is root)
    if ctx.workspace != Path("/"):
        assert not ctx.is_in_workspace(Path("/"))
