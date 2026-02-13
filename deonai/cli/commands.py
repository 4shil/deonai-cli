"""
DeonAi CLI - Chat Commands
Slash commands for chat interface
"""

from typing import Optional, Tuple
from ..core import registry
from ..integrations import GitHelper
from ..utils import Colors, colored


class CommandHandler:
    """Handle slash commands in chat"""
    
    def __init__(self):
        self.git = GitHelper()
        self.commands = {
            "help": self.cmd_help,
            "clear": self.cmd_clear,
            "models": self.cmd_models,
            "switch": self.cmd_switch,
            "profile": self.cmd_profile,
            "system": self.cmd_system,
            "export": self.cmd_export,
            "undo": self.cmd_undo,
            "retry": self.cmd_retry,
            "tools": self.cmd_tools,
            "git": self.cmd_git,
        }
    
    def is_command(self, text: str) -> bool:
        """Check if text is a command"""
        return text.strip().startswith("/")
    
    def parse_command(self, text: str) -> Tuple[str, list]:
        """Parse command and arguments"""
        text = text.strip()[1:]  # Remove /
        parts = text.split(maxsplit=1)
        
        if len(parts) == 1:
            return parts[0].lower(), []
        else:
            cmd = parts[0].lower()
            args = parts[1].split()
            return cmd, args
    
    def execute(self, text: str) -> Optional[str]:
        """
        Execute a command
        Returns response text or None if command not found
        """
        if not self.is_command(text):
            return None
        
        cmd, args = self.parse_command(text)
        
        handler = self.commands.get(cmd)
        if handler:
            return handler(args)
        else:
            return f"{colored('[ERROR]', Colors.RED)} Unknown command: /{cmd}\nType /help for available commands"
    
    def cmd_help(self, args: list) -> str:
        """Show help"""
        help_text = f"""
{colored('DeonAi Commands', Colors.CYAN, Colors.BOLD)}

{colored('Chat:', Colors.YELLOW)}
  /help              Show this help
  /clear             Clear conversation history
  /undo              Remove last message pair
  /retry             Retry last message with same/different model
  
{colored('Models:', Colors.YELLOW)}
  /models            List available models
  /switch [model]    Switch to different model
  
{colored('Tools:', Colors.YELLOW)}
  /tools             List available agentic tools
  
{colored('Git:', Colors.YELLOW)}
  /git status        Show git repository status
  /git diff          Show unstaged changes
  /git diff staged   Show staged changes
  /git log           Show recent commits
  
{colored('Profile:', Colors.YELLOW)}
  /profile save [name]   Save current config as profile
  /profile load [name]   Load a saved profile
  /profile list          List all profiles
  
{colored('System:', Colors.YELLOW)}
  /system            Manage AI system prompt
  /export [format]   Export conversation (md/json)

{colored('Tip:', Colors.DIM)} Most commands work without arguments for interactive mode
"""
        return help_text
    
    def cmd_clear(self, args: list) -> str:
        """Clear history"""
        return "COMMAND:CLEAR"  # Special marker for CLI to handle
    
    def cmd_undo(self, args: list) -> str:
        """Undo last message"""
        return "COMMAND:UNDO"
    
    def cmd_retry(self, args: list) -> str:
        """Retry last message"""
        return "COMMAND:RETRY"
    
    def cmd_models(self, args: list) -> str:
        """List models"""
        return "COMMAND:MODELS"
    
    def cmd_switch(self, args: list) -> str:
        """Switch model"""
        if args:
            return f"COMMAND:SWITCH:{args[0]}"
        return "COMMAND:SWITCH"
    
    def cmd_profile(self, args: list) -> str:
        """Profile management"""
        if not args:
            return f"{colored('[ERROR]', Colors.RED)} Usage: /profile <save|load|list> [name]"
        
        action = args[0].lower()
        if action in ["save", "load"]:
            if len(args) < 2:
                return f"{colored('[ERROR]', Colors.RED)} Profile name required"
            return f"COMMAND:PROFILE:{action}:{args[1]}"
        elif action == "list":
            return "COMMAND:PROFILE:list"
        else:
            return f"{colored('[ERROR]', Colors.RED)} Unknown profile action: {action}"
    
    def cmd_system(self, args: list) -> str:
        """System prompt"""
        return "COMMAND:SYSTEM"
    
    def cmd_export(self, args: list) -> str:
        """Export conversation"""
        format_type = args[0] if args else "md"
        return f"COMMAND:EXPORT:{format_type}"
    
    def cmd_tools(self, args: list) -> str:
        """List available tools"""
        tools = registry.list_tools()
        
        output = f"\n{colored('Available Tools', Colors.CYAN, Colors.BOLD)} ({len(tools)} total)\n\n"
        
        # Categorize tools
        core_tools = [t for t in tools if t in ["read_file", "write_file", "list_files", "run_command", "search_code"]]
        git_tools = [t for t in tools if t.startswith("git_")]
        other_tools = [t for t in tools if t not in core_tools and t not in git_tools]
        
        if core_tools:
            output += f"{colored('Core Tools:', Colors.YELLOW)}\n"
            for tool_name in core_tools:
                tool = registry.get_tool(tool_name)
                output += f"  • {colored(tool_name, Colors.GREEN)}: {tool.description[:60]}...\n"
            output += "\n"
        
        if git_tools:
            output += f"{colored('Git Tools:', Colors.YELLOW)}\n"
            for tool_name in git_tools:
                tool = registry.get_tool(tool_name)
                output += f"  • {colored(tool_name, Colors.GREEN)}: {tool.description[:60]}...\n"
            output += "\n"
        
        if other_tools:
            output += f"{colored('Other Tools:', Colors.YELLOW)}\n"
            for tool_name in other_tools:
                tool = registry.get_tool(tool_name)
                output += f"  • {colored(tool_name, Colors.GREEN)}: {tool.description[:60]}...\n"
        
        output += f"\n{colored('Usage:', Colors.DIM)} Just ask naturally! AI will use tools autonomously.\n"
        output += f"{colored('Example:', Colors.DIM)} 'Check git status and list Python files'\n"
        
        return output
    
    def cmd_git(self, args: list) -> str:
        """Git commands"""
        if not args:
            return self._git_help()
        
        subcmd = args[0].lower()
        
        if subcmd == "status":
            result = registry.execute("git_status", {})
            return f"\n{colored('Git Status:', Colors.CYAN, Colors.BOLD)}\n\n{result}"
        
        elif subcmd == "diff":
            staged = "staged" in args
            result = registry.execute("git_diff", {"staged": staged})
            return f"\n{colored('Git Diff:', Colors.CYAN, Colors.BOLD)} {'(staged)' if staged else '(unstaged)'}\n\n{result}"
        
        elif subcmd == "log":
            count = 10
            if len(args) > 1:
                try:
                    count = int(args[1])
                except ValueError:
                    pass
            
            result = registry.execute("git_log", {"count": count})
            return f"\n{colored('Git Log:', Colors.CYAN, Colors.BOLD)}\n\n{result}"
        
        else:
            return self._git_help()
    
    def _git_help(self) -> str:
        """Git command help"""
        return f"""
{colored('Git Commands:', Colors.CYAN, Colors.BOLD)}

  /git status        Show repository status
  /git diff          Show unstaged changes
  /git diff staged   Show staged changes  
  /git log [count]   Show recent commits (default: 10)

{colored('Note:', Colors.DIM)} You can also ask AI to use Git naturally:
  'What is the current git status?'
  'Show me the diff of my changes'
  'Commit these changes with message X'
"""


# Global command handler
handler = CommandHandler()
