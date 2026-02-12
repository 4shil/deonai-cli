#!/usr/bin/env python3
"""
DeonAi CLI - Your personal AI assistant in the terminal
Simple, fast, customized for you. Powered by OpenRouter.
"""

import sys
import json
import requests
import os
import re
from pathlib import Path

# Color codes for beautiful CLI
class Colors:
    # Main palette - Ocean/Cyan theme
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Reset
    RESET = '\033[0m'
    
    @staticmethod
    def disable():
        """Disable colors (for Windows compatibility)"""
        Colors.CYAN = ''
        Colors.BLUE = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.MAGENTA = ''
        Colors.BOLD = ''
        Colors.DIM = ''
        Colors.UNDERLINE = ''
        Colors.RESET = ''

# Enable colors on Windows
if sys.platform == 'win32':
    try:
        import colorama
        colorama.init()
    except ImportError:
        Colors.disable()

def colored(text, color='', style=''):
    """Apply color and style to text"""
    return f"{style}{color}{text}{Colors.RESET}"

# DeonAi branding with beautiful ASCII art
DEONAI_BANNER = f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ███████╗ ██████╗ ███╗   ██╗     █████╗ ██╗     ║
║   ██╔══██╗██╔════╝██╔═══██╗████╗  ██║    ██╔══██╗██║     ║
║   ██║  ██║█████╗  ██║   ██║██╔██╗ ██║    ███████║██║     ║
║   ██║  ██║██╔══╝  ██║   ██║██║╚██╗██║    ██╔══██║██║     ║
║   ██████╔╝███████╗╚██████╔╝██║ ╚████║    ██║  ██║██║     ║
║   ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝     ║
║                                                           ║
║        {Colors.MAGENTA}Your Personal AI Coding Assistant{Colors.CYAN}              ║
║                {Colors.DIM}v2.4 • Powered by OpenRouter{Colors.RESET}{Colors.CYAN}                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.RESET}
"""

CONFIG_DIR = Path.home() / ".deonai"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
PROFILES_FILE = CONFIG_DIR / "profiles.json"

# OpenRouter API settings
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
MODELS_CACHE_FILE = CONFIG_DIR / "models_cache.json"

# DeonAi personality system prompt
DEONAI_SYSTEM = """You are DeonAi, a helpful and intelligent CLI assistant with file operation capabilities.

Core traits:
- Direct and concise - no fluff
- Technical but friendly
- Give code examples when relevant
- Admit when you don't know something
- Focus on practical solutions

File operations:
When the user asks you to create, modify, or write files:
1. Generate the complete file content
2. Format it in a code block with the filename
3. Use this exact format:

WRITE_FILE: filename.ext
```language
file content here
```

Example:
WRITE_FILE: hello.py
```python
print("Hello, World!")
```

The system will detect this pattern and automatically save the file.
You can write multiple files in one response.
"""


def fetch_openrouter_models(api_key):
    """Fetch all available models from OpenRouter"""
    try:
        response = requests.get(
            f"{OPENROUTER_API_URL}/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/4shil/deonai-cli",
            },
            timeout=10
        )
        response.raise_for_status()
        
        models = response.json().get("data", [])
        
        # Cache the models
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(MODELS_CACHE_FILE, "w") as f:
            json.dump(models, f)
        
        return models
    except Exception as e:
        print(f"[WARNING] Could not fetch models: {e}")
        # Try to load from cache
        if MODELS_CACHE_FILE.exists():
            with open(MODELS_CACHE_FILE) as f:
                return json.load(f)
        return []


def setup_config():
    """First-time setup - ask for API key"""
    print(DEONAI_BANNER)
    print("Welcome! Let's set up DeonAi with OpenRouter.\n")
    
    api_key = input("Paste your OpenRouter API key: ").strip()
    
    if not api_key.startswith("sk-or-"):
        print("[ERROR] That doesn't look like a valid OpenRouter API key.")
        print("It should start with 'sk-or-'")
        print("Get one at: https://openrouter.ai/keys")
        sys.exit(1)
    
    # Fetch available models
    print("\n[INFO] Fetching available models from OpenRouter...")
    models = fetch_openrouter_models(api_key)
    
    if not models:
        print("[ERROR] Could not fetch models. Please check your API key.")
        sys.exit(1)
    
    print(f"[SUCCESS] Found {len(models)} models!\n")
    
    # Show popular models
    print("Choose your model:")
    popular_models = [
        ("anthropic/claude-sonnet-4", "Claude Sonnet 4 (recommended)"),
        ("anthropic/claude-opus-4", "Claude Opus 4 (most capable)"),
        ("google/gemini-2.0-flash-exp:free", "Gemini 2.0 Flash (free)"),
        ("meta-llama/llama-3.3-70b-instruct", "Llama 3.3 70B"),
        ("openai/gpt-4o", "GPT-4o"),
    ]
    
    for i, (model_id, desc) in enumerate(popular_models, 1):
        # Check if model is available
        if any(m.get("id") == model_id for m in models):
            print(f"{i}. {desc}")
    
    print(f"{len(popular_models)+1}. List all {len(models)} models")
    print(f"{len(popular_models)+2}. Enter model ID manually")
    
    choice = input(f"\nChoice [1]: ").strip() or "1"
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(popular_models):
            model = popular_models[choice_num - 1][0]
        elif choice_num == len(popular_models) + 1:
            # List all models
            print("\n[INFO] All available models:")
            for m in models[:50]:  # Show first 50
                print(f"  - {m.get('id')} ({m.get('name', 'Unknown')})")
            if len(models) > 50:
                print(f"  ... and {len(models) - 50} more")
            model = input("\nEnter model ID: ").strip()
        else:
            model = input("\nEnter model ID: ").strip()
    except ValueError:
        model = choice
    
    # Validate model exists
    if not any(m.get("id") == model for m in models):
        print(f"[WARNING] Model '{model}' not found, using default")
        model = "anthropic/claude-sonnet-4"
    
    # Save config
    CONFIG_DIR.mkdir(exist_ok=True)
    config = {"api_key": api_key, "model": model}
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    
    # Set restrictive permissions
    import os
    os.chmod(CONFIG_FILE, 0o600)
    
    print(f"\n[SUCCESS] DeonAi configured with {model}")
    print(f"Config saved to: {CONFIG_FILE}")
    print("\nRun 'deonai' again to start chatting!\n")


def load_config():
    """Load existing config"""
    if not CONFIG_FILE.exists():
        print("Run 'deonai --setup' first")
        sys.exit(1)
    
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_history(history):
    """Save conversation history"""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)


def load_history():
    """Load conversation history"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []


def save_profile(name, api_key, model):
    """Save a named profile"""
    profiles = {}
    if PROFILES_FILE.exists():
        with open(PROFILES_FILE) as f:
            profiles = json.load(f)
    
    profiles[name] = {
        "api_key": api_key,
        "model": model
    }
    
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=2)


def list_profiles():
    """List all saved profiles"""
    if not PROFILES_FILE.exists():
        return {}
    with open(PROFILES_FILE) as f:
        return json.load(f)


def load_profile(name):
    """Load a specific profile"""
    profiles = list_profiles()
    return profiles.get(name)


def read_file(filepath):
    """Read file content safely"""
    try:
        path = Path(filepath).expanduser()
        
        # Security check - prevent reading sensitive files
        forbidden = ['/etc/passwd', '/etc/shadow', '.env', '.ssh/id_rsa']
        if any(str(path).endswith(f) for f in forbidden):
            return None, colored("[ERROR]", Colors.RED, Colors.BOLD) + " Cannot read sensitive system files"
        
        if not path.exists():
            return None, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" File not found: {filepath}"
        
        if not path.is_file():
            return None, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" Not a file: {filepath}"
        
        # Check file size (max 1MB)
        if path.stat().st_size > 1_000_000:
            return None, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" File too large (max 1MB): {filepath}"
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return content, None
    except Exception as e:
        return None, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" Could not read file: {e}"


def write_file(filepath, content, mode='w'):
    """Write content to file safely"""
    try:
        path = Path(filepath).expanduser()
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Security check - prevent overwriting system files
        forbidden_dirs = ['/etc', '/sys', '/proc', '/dev']
        if any(str(path).startswith(d) for d in forbidden_dirs):
            return False, colored("[ERROR]", Colors.RED, Colors.BOLD) + " Cannot write to system directories"
        
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        
        return True, colored("[SUCCESS]", Colors.GREEN, Colors.BOLD) + f" Written to: {colored(filepath, Colors.CYAN)}"
    except Exception as e:
        return False, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" Could not write file: {e}"


def list_directory(dirpath='.'):
    """List directory contents"""
    try:
        path = Path(dirpath).expanduser()
        
        if not path.exists():
            return None, f"[ERROR] Directory not found: {dirpath}"
        
        if not path.is_dir():
            return None, f"[ERROR] Not a directory: {dirpath}"
        
        items = []
        for item in sorted(path.iterdir()):
            item_type = 'DIR' if item.is_dir() else 'FILE'
            size = item.stat().st_size if item.is_file() else 0
            items.append((item.name, item_type, size))
        
        return items, None
    except Exception as e:
        return None, f"[ERROR] Could not list directory: {e}"


def parse_and_save_files(response_text, current_dir='.'):
    """Parse AI response for WRITE_FILE commands and save them"""
    import re
    
    # Pattern: WRITE_FILE: filename.ext\n```language\ncontent\n```
    pattern = r'WRITE_FILE:\s*([^\n]+)\n```[^\n]*\n(.*?)```'
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    saved_files = []
    for filename, content in matches:
        filename = filename.strip()
        content = content.strip()
        
        # Resolve relative to current directory
        filepath = Path(current_dir) / filename
        
        success, message = write_file(str(filepath), content)
        if success:
            saved_files.append(filename)
            print(f"\n{message}")
        else:
            print(f"\n{message}")
    
    return saved_files


def run_code(filepath, language=None):
    """Execute code file safely"""
    import subprocess
    
    try:
        path = Path(filepath).expanduser()
        
        if not path.exists():
            return None, f"[ERROR] File not found: {filepath}"
        
        # Auto-detect language if not specified
        if not language:
            ext = path.suffix.lower()
            lang_map = {
                '.py': 'python',
                '.js': 'node',
                '.sh': 'bash',
                '.rb': 'ruby',
                '.go': 'go run',
                '.rs': 'rustc',
            }
            language = lang_map.get(ext)
        
        if not language:
            return None, f"[ERROR] Unsupported file type: {path.suffix}"
        
        # Build command
        if language == 'python':
            cmd = ['python3', str(path)]
        elif language == 'node':
            cmd = ['node', str(path)]
        elif language == 'bash':
            cmd = ['bash', str(path)]
        elif language == 'go run':
            cmd = ['go', 'run', str(path)]
        else:
            cmd = [language, str(path)]
        
        # Execute with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=path.parent
        )
        
        output = {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
        return output, None
        
    except subprocess.TimeoutExpired:
        return None, "[ERROR] Execution timed out (10s limit)"
    except FileNotFoundError:
        return None, f"[ERROR] Interpreter not found for {language}"
    except Exception as e:
        return None, f"[ERROR] Execution failed: {e}"


def create_project_structure(project_type, project_name):
    """Create a basic project structure"""
    try:
        base_path = Path(project_name)
        
        if base_path.exists():
            return False, f"[ERROR] Directory already exists: {project_name}"
        
        templates = {
            'python': {
                'dirs': ['src', 'tests', 'docs'],
                'files': {
                    'README.md': f"# {project_name}\n\nA Python project",
                    'requirements.txt': "# Add dependencies here\n",
                    '.gitignore': "__pycache__/\n*.pyc\n.env\nvenv/\n",
                    'src/__init__.py': "",
                    'src/main.py': 'def main():\n    print("Hello from {project_name}")\n\nif __name__ == "__main__":\n    main()\n',
                    'tests/__init__.py': "",
                    'tests/test_main.py': "import unittest\n\nclass TestMain(unittest.TestCase):\n    def test_example(self):\n        self.assertTrue(True)\n"
                }
            },
            'node': {
                'dirs': ['src', 'tests'],
                'files': {
                    'README.md': f"# {project_name}\n\nA Node.js project",
                    'package.json': '{\n  "name": "' + project_name + '",\n  "version": "1.0.0",\n  "main": "src/index.js"\n}',
                    '.gitignore': "node_modules/\n.env\n",
                    'src/index.js': 'console.log("Hello from ' + project_name + '");',
                    'tests/index.test.js': "// Add tests here\n"
                }
            },
            'web': {
                'dirs': ['css', 'js', 'images'],
                'files': {
                    'index.html': '<!DOCTYPE html>\n<html>\n<head>\n    <title>' + project_name + '</title>\n    <link rel="stylesheet" href="css/style.css">\n</head>\n<body>\n    <h1>' + project_name + '</h1>\n    <script src="js/main.js"></script>\n</body>\n</html>',
                    'css/style.css': 'body {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 20px;\n}\n',
                    'js/main.js': 'console.log("' + project_name + ' loaded");',
                    'README.md': f"# {project_name}\n\nA web project"
                }
            }
        }
        
        if project_type not in templates:
            return False, f"[ERROR] Unknown project type: {project_type}"
        
        template = templates[project_type]
        
        # Create base directory
        base_path.mkdir(parents=True)
        
        # Create subdirectories
        for dir_name in template['dirs']:
            (base_path / dir_name).mkdir(parents=True, exist_ok=True)
        
        # Create files
        for file_path, content in template['files'].items():
            full_path = base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
        
        return True, f"[SUCCESS] Created {project_type} project: {project_name}"
        
    except Exception as e:
        return False, f"[ERROR] Could not create project: {e}"


def chat_mode(api_key, model):
    """Interactive chat mode"""
    print(DEONAI_BANNER)
    print(f"{colored('Chat Mode', Colors.CYAN, Colors.BOLD)} - Model: {colored(model, Colors.MAGENTA)}")
    print(f"{Colors.DIM}Type 'help' for commands{Colors.RESET}\n")
    
    history = load_history()
    total_tokens = 0
    multiline_mode = False
    
    if history:
        print(f"{colored('[INFO]', Colors.BLUE)} Loaded {colored(str(len(history)//2), Colors.CYAN)} previous messages\n")
    
    while True:
        try:
            # Check for multiline input (triple quotes)
            if multiline_mode:
                user_input = input(f"{Colors.DIM}... {Colors.RESET}").strip()
                if user_input == '"""':
                    multiline_mode = False
                    user_input = multiline_buffer
                    multiline_buffer = ""
                else:
                    multiline_buffer += user_input + "\n"
                    continue
            else:
                user_input = input(f"{colored('You:', Colors.GREEN, Colors.BOLD)} ").strip()
                
                # Check if starting multiline mode
                if user_input == '"""':
                    multiline_mode = True
                    multiline_buffer = ""
                    print(colored('[INFO]', Colors.BLUE) + ' Multiline mode (type """ to end)')
                    continue
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print(f"\n{colored('Goodbye!', Colors.CYAN, Colors.BOLD)} 👋\n")
                break
            
            if user_input.lower() == "clear":
                history = []
                save_history(history)
                print("[INFO] Conversation cleared\n")
                continue
            
            if user_input.lower() == "models":
                print("\n[INFO] Fetching available models...")
                models = fetch_openrouter_models(api_key)
                if models:
                    print(f"\n[INFO] Available models ({len(models)} total):\n")
                    for m in models[:30]:  # Show first 30
                        name = m.get('name', m.get('id'))
                        model_id = m.get('id')
                        print(f"  - {model_id}")
                        print(f"    {name}")
                    if len(models) > 30:
                        print(f"\n  ... and {len(models) - 30} more models")
                    print("\nTo switch model, run 'deonai --setup' again\n")
                else:
                    print("[ERROR] Could not fetch models\n")
                continue
            
            if user_input.lower() == "help":
                print("\n[HELP] DeonAi Commands:")
                print("  exit      - Quit the application")
                print("  clear     - Reset conversation history")
                print("  undo      - Remove last message pair from history")
                print("  models    - List all available AI models")
                print("  switch    - Quick switch to another model")
                print("  search    - Search conversation history")
                print("  profile   - Manage profiles (save/load/list)")
                print("  retry     - Retry the last message with a different model")
                print("  system    - Change system prompt")
                print('  """       - Start multiline input (end with """)')
                print("  read      - Read file and show content")
                print("  ls        - List directory contents")
                print("  run       - Execute a code file")
                print("  init      - Create a new project (python/node/web)")
                print("  help      - Show this help message")
                print("  status    - Show current configuration")
                print("  export    - Export conversation to file\n")
                continue
            
            if user_input.lower().startswith("init "):
                parts = user_input[5:].split()
                if len(parts) < 2:
                    print("[ERROR] Usage: init <type> <name>")
                    print("Types: python, node, web\n")
                    continue
                
                project_type = parts[0]
                project_name = parts[1]
                
                success, message = create_project_structure(project_type, project_name)
                print(f"\n{message}\n")
                
                if success:
                    items, _ = list_directory(project_name)
                    if items:
                        print(f"[INFO] Project structure:")
                        for name, item_type, size in items:
                            print(f"  {name}{'/' if item_type == 'DIR' else ''}")
                        print()
                continue
            
            if user_input.lower().startswith("run "):
                filepath = user_input[4:].strip()
                
                print(f"\n[INFO] Executing: {filepath}")
                output, error = run_code(filepath)
                
                if error:
                    print(f"{error}\n")
                else:
                    if output['returncode'] == 0:
                        print("[SUCCESS] Execution completed\n")
                    else:
                        print(f"[WARNING] Exit code: {output['returncode']}\n")
                    
                    if output['stdout']:
                        print("--- Output ---")
                        print(output['stdout'])
                    
                    if output['stderr']:
                        print("--- Errors ---")
                        print(output['stderr'])
                    
                    print("--- End ---\n")
                    
                    # Add execution result to context
                    add_ctx = input("Add execution result to context? (y/N): ").strip().lower()
                    if add_ctx == 'y':
                        result_msg = f"[Execution of {filepath}]\nExit code: {output['returncode']}\nOutput:\n{output['stdout']}\nErrors:\n{output['stderr']}"
                        history.append({"role": "user", "content": result_msg})
                        save_history(history)
                        print("[INFO] Result added to context\n")
                continue
            
            if user_input.lower().startswith("read "):
                filepath = user_input[5:].strip()
                content, error = read_file(filepath)
                
                if error:
                    print(f"\n{error}\n")
                else:
                    print(f"\n[INFO] File: {filepath}")
                    print(f"[INFO] Size: {len(content)} bytes\n")
                    print("--- Content ---")
                    print(content)
                    print("--- End ---\n")
                    
                    # Ask if they want to add it to context
                    add_ctx = input("Add to conversation context? (y/N): ").strip().lower()
                    if add_ctx == 'y':
                        context_msg = f"[File: {filepath}]\n```\n{content}\n```"
                        history.append({"role": "user", "content": context_msg})
                        save_history(history)
                        print("[INFO] File added to context. Ask questions about it!\n")
                continue
            
            if user_input.lower().startswith("ls"):
                parts = user_input.split(maxsplit=1)
                dirpath = parts[1] if len(parts) > 1 else '.'
                
                items, error = list_directory(dirpath)
                
                if error:
                    print(f"\n{error}\n")
                else:
                    print(f"\n[INFO] Directory: {dirpath}\n")
                    for name, item_type, size in items:
                        if item_type == 'DIR':
                            print(f"  [DIR]  {name}/")
                        else:
                            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                            print(f"  [FILE] {name} ({size_str})")
                    print()
                continue
            
            if user_input.lower() == "undo":
                if len(history) >= 2:
                    # Remove last user and assistant message
                    history.pop()  # Remove assistant
                    removed = history.pop()  # Remove user
                    save_history(history)
                    print(f"[INFO] Removed last message pair\n")
                elif len(history) == 1:
                    removed = history.pop()
                    save_history(history)
                    print(f"[INFO] Removed last message\n")
                else:
                    print("[ERROR] No messages to undo\n")
                continue
            
            if user_input.lower().startswith("system"):
                parts = user_input.split(maxsplit=1)
                
                if len(parts) == 1:
                    print("\n[INFO] Current system prompt:")
                    print(DEONAI_SYSTEM)
                    print()
                    
                    change = input("Change system prompt? (y/N): ").strip().lower()
                    if change == "y":
                        print("\nEnter new system prompt (end with empty line):")
                        lines = []
                        while True:
                            line = input()
                            if not line:
                                break
                            lines.append(line)
                        
                        if lines:
                            new_prompt = "\n".join(lines)
                            # Save to a temporary variable for this session
                            globals()['DEONAI_SYSTEM'] = new_prompt
                            print("[SUCCESS] System prompt updated for this session\n")
                        else:
                            print("[INFO] No changes made\n")
                else:
                    # Quick system prompt change
                    new_prompt = parts[1]
                    globals()['DEONAI_SYSTEM'] = new_prompt
                    print("[SUCCESS] System prompt updated\n")
                
                continue
            
            if user_input.lower() == "retry":
                if len(history) < 2:
                    print("[ERROR] No previous message to retry\n")
                    continue
                
                # Remove last assistant response
                if history[-1]["role"] == "assistant":
                    history.pop()
                
                # Get the last user message
                if history and history[-1]["role"] == "user":
                    last_user_msg = history[-1]["content"]
                    print(f"\n[INFO] Retrying: {last_user_msg[:50]}...")
                    
                    # Optionally switch model for retry
                    retry_choice = input("Switch model for retry? (y/N): ").strip().lower()
                    if retry_choice == "y":
                        print("\nQuick models:")
                        quick_models = [
                            "anthropic/claude-sonnet-4",
                            "google/gemini-2.0-flash-exp:free",
                            "openai/gpt-4o",
                        ]
                        for i, m in enumerate(quick_models, 1):
                            print(f"  {i}. {m}")
                        
                        choice = input("Choice (or Enter to keep current): ").strip()
                        if choice.isdigit() and 1 <= int(choice) <= len(quick_models):
                            model = quick_models[int(choice) - 1]
                            print(f"[INFO] Switched to {model}")
                    
                    # Re-send the message
                    print("\nDeonAi: ", end="", flush=True)
                    user_input = last_user_msg
                    # Fall through to normal message processing
                else:
                    print("[ERROR] Could not find last user message\n")
                    continue
            
            if user_input.lower().startswith("profile"):
                parts = user_input.split()
                
                if len(parts) == 1 or parts[1] == "list":
                    profiles = list_profiles()
                    if profiles:
                        print("\n[INFO] Saved profiles:")
                        for name, data in profiles.items():
                            print(f"  - {name}: {data['model']}")
                        print()
                    else:
                        print("[INFO] No saved profiles\n")
                
                elif parts[1] == "save":
                    if len(parts) < 3:
                        profile_name = input("Profile name: ").strip()
                    else:
                        profile_name = parts[2]
                    
                    save_profile(profile_name, api_key, model)
                    print(f"[SUCCESS] Profile '{profile_name}' saved\n")
                
                elif parts[1] == "load":
                    if len(parts) < 3:
                        profile_name = input("Profile name: ").strip()
                    else:
                        profile_name = parts[2]
                    
                    profile = load_profile(profile_name)
                    if profile:
                        api_key = profile["api_key"]
                        model = profile["model"]
                        
                        # Update active config
                        config = {"api_key": api_key, "model": model}
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(config, f)
                        
                        print(f"[SUCCESS] Loaded profile '{profile_name}': {model}\n")
                    else:
                        print(f"[ERROR] Profile '{profile_name}' not found\n")
                
                else:
                    print("[ERROR] Usage: profile [list|save|load] [name]\n")
                
                continue
            
            if user_input.lower().startswith("search"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    query = input("Enter search query: ").strip()
                else:
                    query = parts[1]
                
                if not query:
                    print("[ERROR] No search query provided\n")
                    continue
                
                query_lower = query.lower()
                matches = []
                
                for i, msg in enumerate(history):
                    if query_lower in msg["content"].lower():
                        matches.append((i, msg))
                
                if matches:
                    print(f"\n[SEARCH] Found {len(matches)} matches for '{query}':\n")
                    for idx, msg in matches[:10]:  # Show first 10
                        role = msg["role"].capitalize()
                        content = msg["content"][:100]  # First 100 chars
                        if len(msg["content"]) > 100:
                            content += "..."
                        print(f"  [{idx}] {role}: {content}")
                    if len(matches) > 10:
                        print(f"\n  ... and {len(matches) - 10} more matches")
                    print()
                else:
                    print(f"[INFO] No matches found for '{query}'\n")
                continue
            
            if user_input.lower() == "switch":
                print("\n[INFO] Quick model switch")
                print("Popular models:")
                quick_models = [
                    "anthropic/claude-sonnet-4",
                    "anthropic/claude-opus-4",
                    "google/gemini-2.0-flash-exp:free",
                    "openai/gpt-4o",
                    "meta-llama/llama-3.3-70b-instruct"
                ]
                for i, m in enumerate(quick_models, 1):
                    print(f"  {i}. {m}")
                print("  0. Enter custom model ID")
                
                choice = input("\nChoice: ").strip()
                try:
                    idx = int(choice)
                    if 1 <= idx <= len(quick_models):
                        new_model = quick_models[idx - 1]
                    elif idx == 0:
                        new_model = input("Enter model ID: ").strip()
                    else:
                        print("[ERROR] Invalid choice\n")
                        continue
                except ValueError:
                    new_model = choice
                
                # Update config
                config = load_config()
                config["model"] = new_model
                with open(CONFIG_FILE, "w") as f:
                    json.dump(config, f)
                
                model = new_model
                print(f"[SUCCESS] Switched to: {model}\n")
                continue
            
            if user_input.lower() == "export":
                if not history:
                    print("[WARNING] No conversation history to export\n")
                    continue
                
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Export to markdown
                export_file = CONFIG_DIR / f"conversation_{timestamp}.md"
                with open(export_file, "w") as f:
                    f.write(f"# DeonAi Conversation Export\n")
                    f.write(f"**Model:** {model}\n")
                    f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("---\n\n")
                    
                    for msg in history:
                        role = msg["role"].capitalize()
                        content = msg["content"]
                        f.write(f"## {role}\n\n{content}\n\n")
                
                # Also export as JSON
                json_file = CONFIG_DIR / f"conversation_{timestamp}.json"
                with open(json_file, "w") as f:
                    json.dump({
                        "model": model,
                        "timestamp": timestamp,
                        "messages": history
                    }, f, indent=2)
                
                print(f"[SUCCESS] Conversation exported:")
                print(f"  Markdown: {export_file}")
                print(f"  JSON: {json_file}\n")
                continue
            
            if user_input.lower() == "status":
                print(f"\n[STATUS] Current Configuration:")
                print(f"  Model: {model}")
                print(f"  Messages in history: {len(history)}")
                print(f"  Total tokens used: {total_tokens}")
                print(f"  Config: {CONFIG_FILE}")
                print(f"  History: {HISTORY_FILE}")
                
                # Check file sizes
                import os
                if HISTORY_FILE.exists():
                    size = os.path.getsize(HISTORY_FILE) / 1024
                    print(f"  History size: {size:.2f} KB")
                
                # Show last conversation date
                if history:
                    print(f"  Messages: {len(history)} total")
                
                # Profile info
                profiles = list_profiles()
                if profiles:
                    print(f"  Saved profiles: {len(profiles)}")
                
                print()
                continue
            
            history.append({"role": "user", "content": user_input})
            
            print(f"\n{colored('DeonAi:', Colors.MAGENTA, Colors.BOLD)} ", end="", flush=True)
            
            # Call OpenRouter API
            try:
                # Check if streaming is supported
                use_streaming = True
                
                response = requests.post(
                    f"{OPENROUTER_API_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "HTTP-Referer": "https://github.com/4shil/deonai-cli",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": DEONAI_SYSTEM}
                        ] + history,
                        "stream": use_streaming
                    },
                    timeout=60,
                    stream=use_streaming
                )
                response.raise_for_status()
                
                if use_streaming:
                    # Stream the response
                    assistant_text = ""
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith("data: "):
                                line = line[6:]
                                if line.strip() == "[DONE]":
                                    break
                                try:
                                    chunk = json.loads(line)
                                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        print(content, end="", flush=True)
                                        assistant_text += content
                                except json.JSONDecodeError:
                                    continue
                    print("\n")
                    
                    # Check for file write commands
                    saved_files = parse_and_save_files(assistant_text)
                    if saved_files:
                        print(f"[INFO] Created {len(saved_files)} file(s): {', '.join(saved_files)}\n")
                    
                    usage = {}
                    tokens_used = 0
                else:
                    result = response.json()
                    assistant_text = result["choices"][0]["message"]["content"]
                    
                    print(assistant_text)
                    
                    # Check for file write commands
                    saved_files = parse_and_save_files(assistant_text)
                    if saved_files:
                        print(f"\n[INFO] Created {len(saved_files)} file(s): {', '.join(saved_files)}\n")
                    
                    # Track token usage
                    usage = result.get("usage", {})
                    tokens_used = usage.get("total_tokens", 0)
                    total_tokens += tokens_used
                    
                    if tokens_used > 0:
                        print(f"\n[USAGE] {tokens_used} tokens\n")
                    else:
                        print()
                
                history.append({"role": "assistant", "content": assistant_text})
                save_history(history)
            except requests.exceptions.Timeout:
                print("[ERROR] Request timed out. Try again.\n")
                history.pop()  # Remove user message since it failed
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] API Error: {e}\n")
                history.pop()  # Remove user message since it failed
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}\n")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_config()
    elif len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("DeonAi CLI v2.1")
        print("Powered by OpenRouter")
        print("https://github.com/4shil/deonai-cli")
    elif len(sys.argv) > 1 and sys.argv[1] == "--models":
        # Quick model list without entering chat
        config = load_config()
        models = fetch_openrouter_models(config["api_key"])
        if models:
            print(f"\n[INFO] {len(models)} models available:\n")
            for m in models[:50]:
                print(f"  {m.get('id')}")
            if len(models) > 50:
                print(f"\n  ... and {len(models) - 50} more")
        else:
            print("[ERROR] Could not fetch models")
    else:
        config = load_config()
        api_key = config["api_key"]
        model = config["model"]
        
        # One-shot mode or chat mode
        if len(sys.argv) > 1:
            prompt = " ".join(sys.argv[1:])
            
            try:
                response = requests.post(
                    f"{OPENROUTER_API_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "HTTP-Referer": "https://github.com/4shil/deonai-cli",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": DEONAI_SYSTEM},
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=60
                )
                response.raise_for_status()
                
                print(response.json()["choices"][0]["message"]["content"])
            except Exception as e:
                print(f"[ERROR] {e}")
        else:
            # Interactive chat mode
            chat_mode(api_key, model)


if __name__ == "__main__":
    main()
