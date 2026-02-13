# Quick Implementation Guide
## Getting to World-Class: Features 36-39 (Core)

This is the **fast-track guide** to implementing the 4 critical features that will make DeonAi world-class.

---

## 📋 Pre-Implementation Checklist

### 1. Refactor to Modular Structure
**Effort:** 1 day  
**Current:** Single 1559-line file  
**Target:** Modular architecture

```bash
# Create structure
mkdir -p deonai/{core,integrations,utils}
touch deonai/__init__.py
touch deonai/core/{__init__.py,cli.py,chat.py,context.py,tools.py}
touch deonai/integrations/{__init__.py,git.py}
touch deonai/utils/{__init__.py,diff.py,colors.py}

# Entry point becomes a thin wrapper
mv deonai.py deonai/__main__.py
ln -s deonai/__main__.py deonai-cli
```

**Benefits:**
- Easier testing
- Parallel development
- Community contributions
- Plugin system ready

---

## 🎯 Feature 36: Context Manager (3-4 days)

### Overview
Make DeonAi aware of your project structure and automatically include relevant files.

### Implementation Steps

#### Step 1: Workspace Detection (Day 1, AM)
```python
# deonai/core/context.py

import os
from pathlib import Path
from typing import Optional, List
import subprocess

class ContextManager:
    def __init__(self, cwd: Path = None):
        self.cwd = cwd or Path.cwd()
        self.workspace = self.detect_workspace()
        
    def detect_workspace(self) -> Path:
        """Find git root or project root"""
        current = self.cwd
        
        # Try git root first
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=current,
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return Path(result.stdout.strip())
        except:
            pass
        
        # Look for project markers
        markers = [
            "package.json", "pyproject.toml", "Cargo.toml",
            "go.mod", "pom.xml", "Makefile", ".git"
        ]
        
        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    return current
            current = current.parent
        
        return self.cwd
    
    def get_project_info(self) -> dict:
        """Extract project metadata"""
        info = {
            "root": str(self.workspace),
            "type": "unknown",
            "files": [],
            "language": None
        }
        
        # Detect project type
        if (self.workspace / "package.json").exists():
            info["type"] = "nodejs"
            info["language"] = "javascript"
        elif (self.workspace / "pyproject.toml").exists() or \
             (self.workspace / "setup.py").exists():
            info["type"] = "python"
            info["language"] = "python"
        elif (self.workspace / "Cargo.toml").exists():
            info["type"] = "rust"
            info["language"] = "rust"
        elif (self.workspace / "go.mod").exists():
            info["type"] = "go"
            info["language"] = "go"
        
        return info
```

**Test:**
```python
# test_context.py
def test_workspace_detection():
    ctx = ContextManager()
    assert ctx.workspace.exists()
    info = ctx.get_project_info()
    print(f"Detected: {info}")
```

---

#### Step 2: Smart File Discovery (Day 1, PM + Day 2)
```python
# deonai/core/context.py (continued)

class ContextManager:
    # ... previous code ...
    
    def find_relevant_files(
        self, 
        query: str,
        max_files: int = 10,
        include_patterns: List[str] = None
    ) -> List[Path]:
        """Find files relevant to query"""
        
        # Default patterns by language
        if not include_patterns:
            info = self.get_project_info()
            include_patterns = self._get_default_patterns(info["language"])
        
        files = []
        
        # Search for files matching patterns
        for pattern in include_patterns:
            files.extend(self.workspace.rglob(pattern))
        
        # Filter out common excludes
        exclude_dirs = {
            "node_modules", ".git", "__pycache__", "venv",
            "build", "dist", ".next", "target"
        }
        
        files = [
            f for f in files
            if not any(ex in f.parts for ex in exclude_dirs)
        ]
        
        # Rank by relevance (simple: filename matching)
        scored = []
        query_lower = query.lower()
        
        for file in files:
            score = 0
            name_lower = file.name.lower()
            
            # Exact match
            if query_lower in name_lower:
                score += 10
            
            # Partial match
            for word in query_lower.split():
                if word in name_lower:
                    score += 5
            
            # Prefer shorter paths (likely more relevant)
            score -= len(file.parts)
            
            scored.append((score, file))
        
        # Sort by score and limit
        scored.sort(reverse=True)
        return [f for _, f in scored[:max_files]]
    
    def _get_default_patterns(self, language: str) -> List[str]:
        """Get file patterns for language"""
        patterns = {
            "python": ["*.py"],
            "javascript": ["*.js", "*.jsx", "*.ts", "*.tsx"],
            "rust": ["*.rs"],
            "go": ["*.go"],
            "java": ["*.java"],
        }
        return patterns.get(language, ["*.py", "*.js", "*.go", "*.rs"])
    
    def analyze_imports(self, file: Path) -> List[Path]:
        """Find files imported by this file"""
        if not file.exists():
            return []
        
        content = file.read_text()
        imports = []
        
        # Python imports
        if file.suffix == ".py":
            import re
            # Match: from X import Y, import X
            pattern = r'(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)'
            matches = re.findall(pattern, content)
            
            for match in matches:
                # Convert module.name to module/name.py
                parts = match.split('.')
                possible_file = self.workspace / '/'.join(parts)
                
                if possible_file.with_suffix('.py').exists():
                    imports.append(possible_file.with_suffix('.py'))
        
        # JavaScript imports
        elif file.suffix in [".js", ".jsx", ".ts", ".tsx"]:
            import re
            # Match: import X from 'Y', require('Y')
            pattern = r'(?:import.*from|require)\s+[\'"]([^\'"]+)[\'"]'
            matches = re.findall(pattern, content)
            
            for match in matches:
                # Relative imports
                if match.startswith('.'):
                    possible_file = file.parent / match
                    for ext in ['', '.js', '.jsx', '.ts', '.tsx']:
                        test_file = possible_file.with_suffix(ext)
                        if test_file.exists():
                            imports.append(test_file)
                            break
        
        return imports
```

---

#### Step 3: Context Building (Day 3)
```python
# deonai/core/context.py (continued)

class ContextManager:
    # ... previous code ...
    
    def build_context(
        self,
        query: str,
        current_file: Path = None,
        max_tokens: int = 8000
    ) -> str:
        """Build comprehensive context string"""
        
        context_parts = []
        token_count = 0
        
        # 1. Project info
        info = self.get_project_info()
        project_context = f"""
Project: {info['root']}
Type: {info['type']}
Language: {info['language']}
"""
        context_parts.append(project_context)
        token_count += len(project_context) // 4  # Rough token estimate
        
        # 2. Current file (if specified)
        if current_file and current_file.exists():
            content = current_file.read_text()
            file_context = f"""
--- Current File: {current_file.name} ---
{content}
--- End {current_file.name} ---
"""
            if token_count + len(content) // 4 < max_tokens:
                context_parts.append(file_context)
                token_count += len(content) // 4
                
                # 3. Imports from current file
                imports = self.analyze_imports(current_file)
                for imp in imports[:3]:  # Limit imports
                    if token_count >= max_tokens * 0.8:
                        break
                    try:
                        imp_content = imp.read_text()
                        imp_context = f"""
--- Imported File: {imp.name} ---
{imp_content[:1000]}  # Truncate large files
... (truncated)
"""
                        context_parts.append(imp_context)
                        token_count += len(imp_context) // 4
                    except:
                        pass
        
        # 4. Relevant files from query
        relevant = self.find_relevant_files(query, max_files=5)
        for file in relevant:
            if token_count >= max_tokens * 0.9:
                break
            if current_file and file == current_file:
                continue  # Already included
            
            try:
                content = file.read_text()
                file_context = f"""
--- Relevant File: {file.relative_to(self.workspace)} ---
{content[:2000]}  # Show first 2000 chars
... (truncated if longer)
"""
                if token_count + len(file_context) // 4 < max_tokens:
                    context_parts.append(file_context)
                    token_count += len(file_context) // 4
            except:
                pass
        
        return "\n".join(context_parts)
```

---

#### Step 4: Integration (Day 4)
```python
# deonai/core/chat.py (modified)

from .context import ContextManager

class ChatSession:
    def __init__(self, api_key: str, model: str):
        self.context_mgr = ContextManager()
        self.api_key = api_key
        self.model = model
        self.history = []
    
    def send_message(self, user_input: str, files: List[Path] = None):
        """Send with automatic context"""
        
        # Build context
        context = self.context_mgr.build_context(
            query=user_input,
            current_file=files[0] if files else None
        )
        
        # Prepend context to first message
        if not self.history:
            system_msg = f"""You are an AI coding assistant with project context.

{context}

Answer questions about this project and help with coding tasks."""
            self.history.append({"role": "system", "content": system_msg})
        
        # Send user message
        self.history.append({"role": "user", "content": user_input})
        
        # Call API...
        response = self.call_api(self.history)
        
        return response
```

**Test:**
```bash
# In a Python project
deonai

You: explain the main.py file
# Should automatically include main.py content + imports
```

---

## 🔧 Feature 37: Agentic Tool System (4-5 days)

### Overview
Let AI use tools (read files, run commands, search code) autonomously.

### Implementation Steps

#### Step 1: Tool Registry (Day 1)
```python
# deonai/core/tools.py

from typing import Callable, Dict, Any, List
import json
from dataclasses import dataclass
import inspect

@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    function: Callable
    
class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(
        self,
        name: str,
        description: str,
        parameters: dict = None
    ):
        """Decorator to register a tool"""
        def decorator(func: Callable):
            # Auto-generate parameters from function signature
            if parameters is None:
                sig = inspect.signature(func)
                auto_params = {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
                for param_name, param in sig.parameters.items():
                    auto_params["properties"][param_name] = {
                        "type": "string",  # Default to string
                        "description": f"Parameter {param_name}"
                    }
                    if param.default == inspect.Parameter.empty:
                        auto_params["required"].append(param_name)
                params = auto_params
            else:
                params = parameters
            
            tool = Tool(
                name=name,
                description=description,
                parameters=params,
                function=func
            )
            self.tools[name] = tool
            return func
        return decorator
    
    def get_openai_tools(self) -> List[dict]:
        """Convert to OpenAI function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]
    
    def execute(self, name: str, arguments: dict) -> str:
        """Execute a tool by name"""
        if name not in self.tools:
            return f"Error: Tool '{name}' not found"
        
        try:
            result = self.tools[name].function(**arguments)
            return str(result)
        except Exception as e:
            return f"Error executing {name}: {e}"

# Global registry
registry = ToolRegistry()
```

---

#### Step 2: Built-in Tools (Day 2)
```python
# deonai/core/tools.py (continued)

from pathlib import Path
import subprocess

@registry.register(
    name="read_file",
    description="Read the contents of a file",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to read"
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
        
        content = file_path.read_text()
        return f"Contents of {path}:\n{content}"
    except Exception as e:
        return f"Error reading {path}: {e}"

@registry.register(
    name="write_file",
    description="Write content to a file",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to write to"
            },
            "content": {
                "type": "string",
                "description": "Content to write"
            }
        },
        "required": ["path", "content"]
    }
)
def write_file(path: str, content: str) -> str:
    """Write file contents"""
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"

@registry.register(
    name="run_command",
    description="Execute a shell command (use cautiously)",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Shell command to execute"
            }
        },
        "required": ["command"]
    }
)
def run_command(command: str) -> str:
    """Execute shell command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout or result.stderr
        return f"Command: {command}\nOutput:\n{output}"
    except Exception as e:
        return f"Error running command: {e}"

@registry.register(
    name="list_files",
    description="List files in a directory",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Directory path (default: current)"
            },
            "pattern": {
                "type": "string",
                "description": "Glob pattern (e.g., '*.py')"
            }
        }
    }
)
def list_files(path: str = ".", pattern: str = "*") -> str:
    """List files"""
    try:
        dir_path = Path(path)
        files = list(dir_path.glob(pattern))
        if not files:
            return f"No files found matching {pattern} in {path}"
        
        file_list = "\n".join(f"  {f.relative_to(dir_path)}" for f in files[:50])
        return f"Files in {path} matching {pattern}:\n{file_list}"
    except Exception as e:
        return f"Error listing files: {e}"
```

---

#### Step 3: Tool Calling Loop (Day 3-4)
```python
# deonai/core/chat.py (add tool support)

class ChatSession:
    # ... existing code ...
    
    def send_with_tools(self, user_input: str):
        """Send message with tool support"""
        
        # Add user message
        self.history.append({"role": "user", "content": user_input})
        
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call API with tools
            response = requests.post(
                f"{OPENROUTER_API_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": self.history,
                    "tools": registry.get_openai_tools(),
                    "tool_choice": "auto"
                }
            )
            
            result = response.json()
            message = result["choices"][0]["message"]
            
            # Check if AI wants to use tools
            if message.get("tool_calls"):
                print(f"🔧 AI is using tools...")
                
                # Add assistant message
                self.history.append(message)
                
                # Execute each tool
                for tool_call in message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])
                    
                    print(f"  → {tool_name}({tool_args})")
                    
                    # Execute tool
                    result = registry.execute(tool_name, tool_args)
                    
                    print(f"  ✓ Result: {result[:100]}...")
                    
                    # Add tool result to history
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result
                    })
                
                # Continue loop (AI will process tool results)
                continue
            
            else:
                # No tool calls, return final response
                assistant_text = message["content"]
                self.history.append({
                    "role": "assistant",
                    "content": assistant_text
                })
                return assistant_text
        
        return "Max iterations reached"
```

**Example Usage:**
```bash
deonai

You: check if main.py exists and show me its first 10 lines

🔧 AI is using tools...
  → read_file({'path': 'main.py'})
  ✓ Result: Contents of main.py: ...

DeonAi: Yes, main.py exists! Here are the first 10 lines:
[Shows content]
```

---

## 🔗 Feature 38: Git Integration (2-3 days)

### Quick Implementation
```python
# deonai/integrations/git.py

import subprocess
from pathlib import Path
from typing import Optional

class GitHelper:
    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path.cwd()
    
    def is_git_repo(self) -> bool:
        """Check if current dir is a git repo"""
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            return True
        except:
            return False
    
    def get_status(self) -> str:
        """Get git status"""
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout
    
    def get_diff(self, staged: bool = False) -> str:
        """Get git diff"""
        cmd = ["git", "diff"]
        if staged:
            cmd.append("--staged")
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout
    
    def generate_commit_message(self, diff: str) -> str:
        """AI-generated commit message"""
        # Call AI with diff
        prompt = f"""Generate a concise git commit message for these changes:

{diff}

Format: <type>: <description>
Types: feat, fix, docs, style, refactor, test, chore"""
        
        # Use DeonAi API to generate
        # ... (integrate with main chat system)
        pass

# Add as tool
@registry.register(
    name="git_status",
    description="Show git repository status"
)
def git_status() -> str:
    git = GitHelper()
    if not git.is_git_repo():
        return "Not a git repository"
    return git.get_status()

@registry.register(
    name="git_diff",
    description="Show uncommitted changes"
)
def git_diff() -> str:
    git = GitHelper()
    if not git.is_git_repo():
        return "Not a git repository"
    return git.get_diff()
```

---

## 📝 Feature 39: Diff/Patch System (3-4 days)

### Quick Implementation
```python
# deonai/utils/diff.py

import difflib
from pathlib import Path
from typing import List, Tuple

class DiffEngine:
    def generate_diff(
        self,
        original: str,
        modified: str,
        filename: str = "file"
    ) -> str:
        """Generate unified diff"""
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            modified.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm=""
        )
        return "".join(diff)
    
    def apply_patch(self, file_path: Path, patch: str) -> bool:
        """Apply patch to file"""
        # Backup first
        backup = file_path.with_suffix(file_path.suffix + ".bak")
        backup.write_text(file_path.read_text())
        
        try:
            # Use patch command
            import subprocess
            subprocess.run(
                ["patch", str(file_path)],
                input=patch.encode(),
                check=True
            )
            return True
        except:
            # Restore backup
            file_path.write_text(backup.read_text())
            return False
    
    def preview_diff(self, diff: str):
        """Show colored diff"""
        for line in diff.split("\n"):
            if line.startswith("+"):
                print(f"\033[32m{line}\033[0m")  # Green
            elif line.startswith("-"):
                print(f"\033[31m{line}\033[0m")  # Red
            elif line.startswith("@@"):
                print(f"\033[36m{line}\033[0m")  # Cyan
            else:
                print(line)
```

---

## 📦 Testing & Release

### Test Suite
```python
# tests/test_context.py
def test_workspace_detection(): ...
def test_file_discovery(): ...
def test_import_analysis(): ...

# tests/test_tools.py
def test_tool_registration(): ...
def test_tool_execution(): ...
def test_read_file_tool(): ...

# tests/test_git.py
def test_git_detection(): ...
def test_git_diff(): ...
```

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Example videos/GIFs
- [ ] Changelog updated
- [ ] Git tag v3.0

---

## 🎯 Success Criteria

After implementing Features 36-39:

✅ DeonAi can work on real projects  
✅ Understands project context automatically  
✅ Can use tools autonomously  
✅ Git-aware and developer-friendly  
✅ Safe code modifications with diffs  

**Result:** World-class coding assistant! 🚀

---

*Implementation Guide v1.0*  
*Estimated Total Time: 12-15 days*
