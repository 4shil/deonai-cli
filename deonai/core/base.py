"""
DeonAi Core - Base Classes
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path


class BaseContext(ABC):
    """Base class for context management"""
    
    @abstractmethod
    def detect_workspace(self) -> Path:
        """Detect project workspace root"""
        pass
    
    @abstractmethod
    def get_relevant_files(self, query: str) -> List[Path]:
        """Find files relevant to query"""
        pass
    
    @abstractmethod
    def build_context(self, query: str, max_tokens: int) -> str:
        """Build context string for AI"""
        pass


class BaseTool(ABC):
    """Base class for agentic tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_parameters(self) -> dict:
        """Return OpenAI function parameters schema"""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters"""
        pass
    
    def to_openai_format(self) -> dict:
        """Convert to OpenAI function calling format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters()
            }
        }


class BaseIntegration(ABC):
    """Base class for integrations (Git, Editor, etc.)"""
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if integration is available"""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the integration"""
        pass


class DeonAiError(Exception):
    """Base exception for DeonAi errors"""
    pass


class ConfigError(DeonAiError):
    """Configuration related errors"""
    pass


class ContextError(DeonAiError):
    """Context management errors"""
    pass


class ToolError(DeonAiError):
    """Tool execution errors"""
    pass


class IntegrationError(DeonAiError):
    """Integration errors"""
    pass
