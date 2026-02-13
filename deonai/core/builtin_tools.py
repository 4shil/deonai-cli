"""
DeonAi Core - Built-in Tools
Agentic tools for file operations, shell, search
"""

from pathlib import Path
import subprocess
from .tools import registry
from .logger import logger


@registry.register(
    name="read_file",
    description="Read the contents of a file. Use this to examine code, configs, or any text file.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to read (relative to project root)"
            }
        },
        "required": ["path"]
    }
)
def read_file(path: str) -> str:
    """Read file contents"""
    try:
        file_path = Path(path)
        
        if not file_path.exists():
            return f"Error: File not found: {path}"
        
        if not file_path.is_file():
            return f"Error: Not a file: {path}"
        
        # Size limit: 100KB
        size = file_path.stat().st_size
        if size > 100 * 1024:
            return f"Error: File too large ({size} bytes). Maximum: 100KB"
        
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        return f"Contents of {path}:\n\n{content}"
        
    except Exception as e:
        logger.error(f"read_file error: {e}")
        return f"Error reading file: {e}"


@registry.register(
    name="write_file",
    description="Write content to a file. Creates parent directories if needed. Use this to create or modify files.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to write to (relative to project root)"
            },
            "content": {
                "type": "string",
                "description": "Content to write to the file"
            }
        },
        "required": ["path", "content"]
    }
)
def write_file(path: str, content: str) -> str:
    """Write content to file"""
    try:
        file_path = Path(path)
        
        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        file_path.write_text(content, encoding='utf-8')
        
        return f"Successfully wrote {len(content)} characters to {path}"
        
    except Exception as e:
        logger.error(f"write_file error: {e}")
        return f"Error writing file: {e}"


@registry.register(
    name="list_files",
    description="List files in a directory. Use this to explore project structure.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Directory path to list (default: current directory)"
            },
            "pattern": {
                "type": "string",
                "description": "Glob pattern to filter files (e.g., '*.py', '*.js')"
            }
        }
    }
)
def list_files(path: str = ".", pattern: str = "*") -> str:
    """List files in directory"""
    try:
        dir_path = Path(path)
        
        if not dir_path.exists():
            return f"Error: Directory not found: {path}"
        
        if not dir_path.is_dir():
            return f"Error: Not a directory: {path}"
        
        # List files
        files = []
        dirs = []
        
        for item in sorted(dir_path.glob(pattern)):
            if item.is_file():
                files.append(item.name)
            elif item.is_dir():
                dirs.append(item.name + "/")
        
        output = f"Contents of {path}:\n\n"
        
        if dirs:
            output += "Directories:\n"
            output += "\n".join(f"  📁 {d}" for d in dirs[:20])
            if len(dirs) > 20:
                output += f"\n  ... and {len(dirs) - 20} more directories"
            output += "\n\n"
        
        if files:
            output += "Files:\n"
            output += "\n".join(f"  📄 {f}" for f in files[:30])
            if len(files) > 30:
                output += f"\n  ... and {len(files) - 30} more files"
        
        if not files and not dirs:
            output += "  (empty or no matches)"
        
        return output
        
    except Exception as e:
        logger.error(f"list_files error: {e}")
        return f"Error listing files: {e}"


@registry.register(
    name="run_command",
    description="Execute a shell command. Use with caution. Timeout: 30 seconds.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Shell command to execute"
            },
            "cwd": {
                "type": "string",
                "description": "Working directory (optional)"
            }
        },
        "required": ["command"]
    }
)
def run_command(command: str, cwd: str = ".") -> str:
    """Execute shell command"""
    try:
        logger.info(f"Running command: {command}")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=cwd
        )
        
        output = f"Command: {command}\n"
        output += f"Exit code: {result.returncode}\n\n"
        
        if result.stdout:
            output += "STDOUT:\n" + result.stdout + "\n"
        
        if result.stderr:
            output += "STDERR:\n" + result.stderr
        
        return output
        
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after 30 seconds"
    except Exception as e:
        logger.error(f"run_command error: {e}")
        return f"Error running command: {e}"


@registry.register(
    name="search_code",
    description="Search for text in files using grep. Use this to find code patterns, functions, or strings.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Text to search for"
            },
            "path": {
                "type": "string",
                "description": "Path to search in (default: current directory)"
            },
            "file_pattern": {
                "type": "string",
                "description": "File pattern to search (e.g., '*.py', '*.js')"
            }
        },
        "required": ["query"]
    }
)
def search_code(query: str, path: str = ".", file_pattern: str = "*") -> str:
    """Search for text in files"""
    try:
        search_path = Path(path)
        
        if not search_path.exists():
            return f"Error: Path not found: {path}"
        
        results = []
        
        # Search files
        for file in search_path.rglob(file_pattern):
            if not file.is_file():
                continue
            
            # Skip binary and large files
            try:
                if file.stat().st_size > 1024 * 1024:  # 1MB
                    continue
                
                content = file.read_text(encoding='utf-8', errors='ignore')
                
                # Find matches
                for i, line in enumerate(content.split('\n'), 1):
                    if query.lower() in line.lower():
                        results.append(f"{file}:{i}:{line.strip()}")
                        
                        if len(results) >= 50:  # Limit results
                            break
            except:
                continue
            
            if len(results) >= 50:
                break
        
        if results:
            output = f"Found {len(results)} matches for '{query}':\n\n"
            output += "\n".join(results)
            if len(results) >= 50:
                output += "\n\n... (limited to 50 results)"
            return output
        else:
            return f"No matches found for '{query}' in {path}"
        
    except Exception as e:
        logger.error(f"search_code error: {e}")
        return f"Error searching: {e}"


# Log loaded tools
logger.info(f"Loaded {len(registry.list_tools())} built-in tools")
