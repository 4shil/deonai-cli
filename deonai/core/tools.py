"""
DeonAi Core - Tool System
Feature 37: Agentic tool execution
"""

from typing import Callable, Dict, List, Any, Optional
import inspect
import json
from dataclasses import dataclass
from .base import BaseTool, ToolError
from .logger import logger


@dataclass
class ToolCall:
    """Represents a tool call from AI"""
    id: str
    name: str
    arguments: dict


class Tool(BaseTool):
    """Concrete tool implementation"""
    
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[dict] = None
    ):
        super().__init__(name, description)
        self.function = function
        self._parameters = parameters or self._auto_generate_parameters()
    
    def _auto_generate_parameters(self) -> dict:
        """Auto-generate parameter schema from function signature"""
        sig = inspect.signature(self.function)
        
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in sig.parameters.items():
            # Skip self/cls
            if param_name in ['self', 'cls']:
                continue
            
            # Get type hint if available
            param_type = "string"  # Default
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == list:
                    param_type = "array"
            
            schema["properties"][param_name] = {
                "type": param_type,
                "description": f"Parameter: {param_name}"
            }
            
            # Required if no default
            if param.default == inspect.Parameter.empty:
                schema["required"].append(param_name)
        
        return schema
    
    def get_parameters(self) -> dict:
        """Return OpenAI function parameters schema"""
        return self._parameters
    
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters"""
        try:
            result = self.function(**kwargs)
            return str(result)
        except Exception as e:
            raise ToolError(f"Tool '{self.name}' failed: {e}")


class ToolRegistry:
    """Registry for managing agentic tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        logger.info("Tool registry initialized")
    
    def register(
        self,
        name: str,
        description: str,
        parameters: Optional[dict] = None
    ):
        """
        Decorator to register a tool
        
        Usage:
            @registry.register("tool_name", "Description")
            def my_tool(arg1: str, arg2: int):
                return result
        """
        def decorator(func: Callable) -> Callable:
            tool = Tool(
                name=name,
                description=description,
                function=func,
                parameters=parameters
            )
            self.tools[name] = tool
            logger.info(f"Registered tool: {name}")
            return func
        
        return decorator
    
    def register_tool(self, tool: BaseTool):
        """Register a tool object directly"""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def unregister(self, name: str) -> bool:
        """Unregister a tool"""
        if name in self.tools:
            del self.tools[name]
            logger.info(f"Unregistered tool: {name}")
            return True
        return False
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self.tools.keys())
    
    def get_openai_tools(self) -> List[dict]:
        """
        Convert all tools to OpenAI function calling format
        Returns list of tool definitions
        """
        return [tool.to_openai_format() for tool in self.tools.values()]
    
    def execute(self, name: str, arguments: dict) -> str:
        """
        Execute a tool by name with arguments
        
        Args:
            name: Tool name
            arguments: Tool arguments as dict
        
        Returns:
            Tool result as string
        
        Raises:
            ToolError: If tool not found or execution fails
        """
        tool = self.get_tool(name)
        if not tool:
            raise ToolError(f"Tool not found: {name}")
        
        try:
            logger.info(f"Executing tool: {name} with args: {arguments}")
            result = tool.execute(**arguments)
            logger.info(f"Tool {name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool {name} failed: {e}")
            raise ToolError(f"Tool '{name}' execution failed: {e}")
    
    def execute_multiple(self, tool_calls: List[ToolCall]) -> List[tuple[str, str]]:
        """
        Execute multiple tool calls
        
        Returns:
            List of (tool_call_id, result) tuples
        """
        results = []
        
        for call in tool_calls:
            try:
                result = self.execute(call.name, call.arguments)
                results.append((call.id, result))
            except ToolError as e:
                results.append((call.id, f"Error: {e}"))
        
        return results
    
    def parse_tool_calls(self, response: dict) -> List[ToolCall]:
        """
        Parse tool calls from OpenAI response
        
        Args:
            response: OpenAI API response message dict
        
        Returns:
            List of ToolCall objects
        """
        tool_calls = []
        
        raw_calls = response.get("tool_calls", [])
        for call in raw_calls:
            try:
                tool_calls.append(ToolCall(
                    id=call["id"],
                    name=call["function"]["name"],
                    arguments=json.loads(call["function"]["arguments"])
                ))
            except (KeyError, json.JSONDecodeError) as e:
                logger.error(f"Failed to parse tool call: {e}")
        
        return tool_calls


# Global registry instance
registry = ToolRegistry()
