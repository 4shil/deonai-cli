"""
DeonAi Core - Agentic Execution
Autonomous tool calling loop
"""

from typing import List, Dict, Any, Optional, Callable
import json
from .tools import registry, ToolCall
from .logger import logger
from ..utils import Colors, colored


class AgenticExecutor:
    """Manages autonomous tool execution loops"""
    
    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations
        self.current_iteration = 0
    
    def execute_loop(
        self,
        messages: List[Dict],
        api_call_fn: Callable,
        on_tool_start: Optional[Callable] = None,
        on_tool_complete: Optional[Callable] = None
    ) -> tuple[str, List[Dict]]:
        """
        Execute agentic loop with tool calling
        
        Args:
            messages: Conversation history
            api_call_fn: Function to call API (takes messages, returns response)
            on_tool_start: Callback when tool execution starts
            on_tool_complete: Callback when tool completes
        
        Returns:
            (final_response, updated_messages)
        """
        self.current_iteration = 0
        
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            
            logger.info(f"Agentic iteration {self.current_iteration}/{self.max_iterations}")
            
            # Call API with tools
            try:
                response = api_call_fn(messages)
            except Exception as e:
                logger.error(f"API call failed: {e}")
                return f"Error: API call failed: {e}", messages
            
            # Check if response has tool calls
            message = response.get("choices", [{}])[0].get("message", {})
            
            if not message.get("tool_calls"):
                # No tool calls - return final response
                content = message.get("content", "")
                messages.append({"role": "assistant", "content": content})
                return content, messages
            
            # Has tool calls - execute them
            if on_tool_start:
                on_tool_start(len(message["tool_calls"]))
            
            # Add assistant message with tool calls
            messages.append(message)
            
            # Parse and execute tools
            tool_calls = registry.parse_tool_calls(message)
            
            for call in tool_calls:
                logger.info(f"Executing tool: {call.name}")
                
                try:
                    # Execute tool
                    result = registry.execute(call.name, call.arguments)
                    
                    if on_tool_complete:
                        on_tool_complete(call.name, call.arguments, result)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result
                    })
                    
                except Exception as e:
                    error_msg = f"Error: {e}"
                    logger.error(f"Tool {call.name} failed: {e}")
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": error_msg
                    })
            
            # Continue loop to process tool results
        
        # Max iterations reached
        logger.warning(f"Max iterations ({self.max_iterations}) reached")
        return "Max iterations reached. Task may be incomplete.", messages
    
    def execute_single_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> str:
        """
        Execute a single tool directly (non-agentic)
        
        Args:
            tool_name: Name of tool to execute
            arguments: Tool arguments
        
        Returns:
            Tool result
        """
        try:
            logger.info(f"Direct tool execution: {tool_name}")
            result = registry.execute(tool_name, arguments)
            return result
        except Exception as e:
            logger.error(f"Direct tool execution failed: {e}")
            return f"Error: {e}"


class ToolCallFormatter:
    """Format tool calls for display"""
    
    @staticmethod
    def format_tool_start(tool_calls: List[ToolCall]) -> str:
        """Format tool execution start message"""
        if len(tool_calls) == 1:
            call = tool_calls[0]
            args_str = json.dumps(call.arguments, indent=2)
            return f"{colored('🔧 Using tool:', Colors.CYAN)} {colored(call.name, Colors.YELLOW, Colors.BOLD)}\n{colored('Arguments:', Colors.DIM)}\n{args_str}"
        else:
            output = f"{colored('🔧 Using', Colors.CYAN)} {colored(str(len(tool_calls)), Colors.YELLOW, Colors.BOLD)} {colored('tools:', Colors.CYAN)}\n"
            for i, call in enumerate(tool_calls, 1):
                output += f"  {i}. {colored(call.name, Colors.YELLOW)}\n"
            return output
    
    @staticmethod
    def format_tool_result(tool_name: str, result: str, max_length: int = 200) -> str:
        """Format tool result for display"""
        # Truncate long results
        if len(result) > max_length:
            result_preview = result[:max_length] + "..."
        else:
            result_preview = result
        
        return f"{colored('✓', Colors.GREEN)} {colored(tool_name, Colors.YELLOW)}: {result_preview}"


# Global executor instance
executor = AgenticExecutor()
formatter = ToolCallFormatter()
