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
import threading
import time
import shutil
from pathlib import Path

# Color codes for beautiful CLI
class Colors:
    # Enhanced color palette - Modern theme
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    
    # Additional colors
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_MAGENTA = '\033[95m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    
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
        Colors.WHITE = ''
        Colors.BRIGHT_CYAN = ''
        Colors.BRIGHT_GREEN = ''
        Colors.BRIGHT_YELLOW = ''
        Colors.BRIGHT_MAGENTA = ''
        Colors.BOLD = ''
        Colors.DIM = ''
        Colors.UNDERLINE = ''
        Colors.BLINK = ''
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


def get_terminal_width():
    """Get current terminal width, fallback to 80"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def center_text(text, width=None):
    """Center text within terminal width"""
    if width is None:
        width = get_terminal_width()
    return text.center(width)


def wrap_text(text, width=None, indent=0):
    """Wrap text to terminal width with optional indent"""
    if width is None:
        width = get_terminal_width()
    
    words = text.split()
    lines = []
    current_line = ' ' * indent
    
    for word in words:
        if len(current_line) + len(word) + 1 <= width:
            if current_line.strip():
                current_line += ' ' + word
            else:
                current_line = ' ' * indent + word
        else:
            if current_line.strip():
                lines.append(current_line)
            current_line = ' ' * indent + word
    
    if current_line.strip():
        lines.append(current_line)
    
    return '\n'.join(lines)


class LoadingAnimation:
    """Animated loading spinner with multiple styles"""
    
    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['|', '/', '-', '\\'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'bounce': ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈'],
        'dots2': ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
        'circle': ['◐', '◓', '◑', '◒'],
        'square': ['◰', '◳', '◲', '◱'],
        'toggle': ['⊶', '⊷'],
    }
    
    def __init__(self, message="Processing", style='dots'):
        self.message = message
        self.running = False
        self.thread = None
        self.frames = self.SPINNERS.get(style, self.SPINNERS['dots'])
        self.current_frame = 0
    
    def _animate(self):
        """Animation loop"""
        while self.running:
            frame = self.frames[self.current_frame % len(self.frames)]
            sys.stdout.write(f'\r{colored(frame, Colors.CYAN, Colors.BOLD)} {colored(self.message, Colors.DIM)}...')
            sys.stdout.flush()
            self.current_frame += 1
            time.sleep(0.08)
    
    def start(self):
        """Start the animation"""
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the animation"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 20) + '\r')
        sys.stdout.flush()


class TypingAnimation:
    """Animated typing indicator for AI responses"""
    def __init__(self):
        self.running = False
        self.thread = None
        self.dots = 0
    
    def _animate(self):
        """Animation loop"""
        while self.running:
            dots = '.' * (self.dots % 4)
            sys.stdout.write(f'\r{colored("DeonAi:", Colors.MAGENTA, Colors.BOLD)} {colored("thinking", Colors.DIM)}{dots}   ')
            sys.stdout.flush()
            self.dots += 1
            time.sleep(0.3)
    
    def start(self):
        """Start the animation"""
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the animation"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)  # Add timeout to prevent hanging
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()


class ProgressBar:
    """ASCII progress bar with percentage"""
    def __init__(self, total, width=40, char='█', empty_char='░'):
        self.total = total
        self.current = 0
        self.width = width
        self.char = char
        self.empty_char = empty_char
    
    def update(self, current):
        """Update progress"""
        self.current = min(current, self.total)
        self.render()
    
    def render(self):
        """Render the progress bar"""
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        filled = int((self.current / self.total) * self.width) if self.total > 0 else 0
        bar = self.char * filled + self.empty_char * (self.width - filled)
        
        sys.stdout.write(f'\r{colored("[", Colors.CYAN)}{colored(bar, Colors.GREEN)}{colored("]", Colors.CYAN)} {colored(f"{percent:.1f}%", Colors.YELLOW)}')
        sys.stdout.flush()
    
    def complete(self):
        """Mark as complete and move to next line"""
        self.current = self.total
        self.render()
        print()


# Box drawing utilities
class BoxChars:
    """Unicode box-drawing characters for better UI"""
    # Double line box
    TOP_LEFT = '╔'
    TOP_RIGHT = '╗'
    BOTTOM_LEFT = '╚'
    BOTTOM_RIGHT = '╝'
    HORIZONTAL = '═'
    VERTICAL = '║'
    
    # Single line box
    S_TOP_LEFT = '┌'
    S_TOP_RIGHT = '┐'
    S_BOTTOM_LEFT = '└'
    S_BOTTOM_RIGHT = '┘'
    S_HORIZONTAL = '─'
    S_VERTICAL = '│'
    
    # Heavy line box
    H_TOP_LEFT = '┏'
    H_TOP_RIGHT = '┓'
    H_BOTTOM_LEFT = '┗'
    H_BOTTOM_RIGHT = '┛'
    H_HORIZONTAL = '━'
    H_VERTICAL = '┃'
    
    # Rounded box
    R_TOP_LEFT = '╭'
    R_TOP_RIGHT = '╮'
    R_BOTTOM_LEFT = '╰'
    R_BOTTOM_RIGHT = '╯'


def draw_box(text, width=60, style='double', color=Colors.CYAN):
    """Draw a box around text with specified style"""
    if style == 'double':
        tl, tr, bl, br = BoxChars.TOP_LEFT, BoxChars.TOP_RIGHT, BoxChars.BOTTOM_LEFT, BoxChars.BOTTOM_RIGHT
        h, v = BoxChars.HORIZONTAL, BoxChars.VERTICAL
    elif style == 'single':
        tl, tr, bl, br = BoxChars.S_TOP_LEFT, BoxChars.S_TOP_RIGHT, BoxChars.S_BOTTOM_LEFT, BoxChars.S_BOTTOM_RIGHT
        h, v = BoxChars.S_HORIZONTAL, BoxChars.S_VERTICAL
    elif style == 'heavy':
        tl, tr, bl, br = BoxChars.H_TOP_LEFT, BoxChars.H_TOP_RIGHT, BoxChars.H_BOTTOM_LEFT, BoxChars.H_BOTTOM_RIGHT
        h, v = BoxChars.H_HORIZONTAL, BoxChars.H_VERTICAL
    elif style == 'rounded':
        tl, tr, bl, br = BoxChars.R_TOP_LEFT, BoxChars.R_TOP_RIGHT, BoxChars.R_BOTTOM_LEFT, BoxChars.R_BOTTOM_RIGHT
        h, v = BoxChars.S_HORIZONTAL, BoxChars.S_VERTICAL
    else:
        tl, tr, bl, br = '+', '+', '+', '+'
        h, v = '-', '|'
    
    lines = text.split('\n')
    result = []
    result.append(f"{color}{tl}{h * (width - 2)}{tr}{Colors.RESET}")
    
    for line in lines:
        padding = width - len(line) - 4
        result.append(f"{color}{v}{Colors.RESET} {line}{' ' * padding} {color}{v}{Colors.RESET}")
    
    result.append(f"{color}{bl}{h * (width - 2)}{br}{Colors.RESET}")
    return '\n'.join(result)


# DeonAi branding with beautiful ASCII art
DEONAI_BANNER = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     ██████╗ ███████╗ ██████╗ ███╗   ██╗ █████╗ ██╗          ║
    ║     ██╔══██╗██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║          ║
    ║     ██║  ██║█████╗  ██║   ██║██╔██╗ ██║███████║██║          ║
    ║     ██║  ██║██╔══╝  ██║   ██║██║╚██╗██║██╔══██║██║          ║
    ║     ██████╔╝███████╗╚██████╔╝██║ ╚████║██║  ██║██║          ║
    ║     ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝          ║
    ║                                                               ║
    ║           {Colors.BRIGHT_MAGENTA}✨ Your AI Coding Assistant ✨{Colors.CYAN}                  ║
    ║                  {Colors.DIM}v2.7 • Powered by OpenRouter{Colors.RESET}{Colors.CYAN}                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
    {Colors.DIM}💡 Tip: Use {Colors.GREEN}/help{Colors.DIM} for commands • Start chatting naturally!{Colors.RESET}
"""

CONFIG_DIR = Path.home() / ".deonai"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
PROFILES_FILE = CONFIG_DIR / "profiles.json"
SYSTEM_PROMPT_FILE = CONFIG_DIR / "system_prompt.txt"

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


def load_system_prompt():
    """Load custom system prompt if exists, otherwise return default"""
    try:
        if SYSTEM_PROMPT_FILE.exists():
            with open(SYSTEM_PROMPT_FILE, 'r', encoding='utf-8') as f:
                custom = f.read().strip()
                if custom:
                    return custom
    except Exception:
        pass
    return DEONAI_SYSTEM


def save_system_prompt(prompt):
    """Save custom system prompt"""
    try:
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(SYSTEM_PROMPT_FILE, 'w', encoding='utf-8') as f:
            f.write(prompt)
        return True
    except Exception as e:
        print(f"{colored('[ERROR]', Colors.RED, Colors.BOLD)} Could not save system prompt: {e}")
        return False


def reset_system_prompt():
    """Reset to default system prompt"""
    try:
        if SYSTEM_PROMPT_FILE.exists():
            SYSTEM_PROMPT_FILE.unlink()
        return True
    except Exception:
        return False


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
    print(f"{colored('Welcome to DeonAi Setup!', Colors.CYAN, Colors.BOLD)}\n")
    print(f"{Colors.DIM}Get your free API key at: {colored('https://openrouter.ai/keys', Colors.BLUE, Colors.UNDERLINE)}{Colors.RESET}\n")
    
    api_key = input(f"{colored('Paste your OpenRouter API key:', Colors.YELLOW)} ").strip()
    
    if not api_key.startswith("sk-or-"):
        print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} Invalid API key format")
        print(f"{Colors.DIM}Keys should start with 'sk-or-'{Colors.RESET}")
        print(f"{Colors.DIM}Get one at: https://openrouter.ai/keys{Colors.RESET}\n")
        sys.exit(1)
    
    # Fetch available models
    loader = LoadingAnimation("Fetching available models")
    loader.start()
    models = fetch_openrouter_models(api_key)
    loader.stop()
    
    if not models:
        print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} Could not fetch models. Check your API key.\n")
        sys.exit(1)
    
    print(f"\n{colored('[SUCCESS]', Colors.GREEN, Colors.BOLD)} Found {colored(str(len(models)), Colors.CYAN)} models!\n")
    
    # Show popular models
    print(f"{colored('Choose your model:', Colors.CYAN, Colors.BOLD)}\n")
    popular_models = [
        ("anthropic/claude-sonnet-4", "Claude Sonnet 4", "💎 Recommended"),
        ("anthropic/claude-opus-4", "Claude Opus 4", "🚀 Most capable"),
        ("google/gemini-2.0-flash-exp:free", "Gemini 2.0 Flash", "✨ FREE"),
        ("meta-llama/llama-3.3-70b-instruct", "Llama 3.3 70B", "🦙 Open source"),
        ("openai/gpt-4o", "GPT-4o", "🤖 OpenAI"),
    ]
    
    for i, (model_id, name, badge) in enumerate(popular_models, 1):
        # Check if model is available
        if any(m.get("id") == model_id for m in models):
            print(f"  {colored(str(i), Colors.GREEN)}. {colored(name, Colors.CYAN)} {colored(badge, Colors.DIM)}")
    
    print(f"\n  {colored(str(len(popular_models)+1), Colors.GREEN)}. List all {len(models)} models")
    print(f"  {colored(str(len(popular_models)+2), Colors.GREEN)}. Enter model ID manually\n")
    
    choice = input(f"{colored('Choice [1]:', Colors.YELLOW)} ").strip() or "1"
    
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
        print(f"{colored('[ERROR]', Colors.RED)} Run 'deonai --setup' first")
        sys.exit(1)
    
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{colored('[ERROR]', Colors.RED)} Config file is corrupted")
        print(f"{Colors.DIM}Run 'deonai --setup' to fix{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{colored('[ERROR]', Colors.RED)} Could not load config: {e}")
        sys.exit(1)


def save_history(history):
    """Save conversation history"""
    try:
        CONFIG_DIR.mkdir(exist_ok=True, parents=True)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)
    except Exception as e:
        print(f"{colored('[WARNING]', Colors.YELLOW)} Could not save history: {e}")


def load_history():
    """Load conversation history"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"{colored('[WARNING]', Colors.YELLOW)} History file corrupted, starting fresh")
            return []
        except Exception:
            return []
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
            return False, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" Directory already exists: {project_name}"
        
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
            return False, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" Unknown project type: {project_type}"
        
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
        
        return True, colored("[SUCCESS]", Colors.GREEN, Colors.BOLD) + f" Created {colored(project_type, Colors.CYAN)} project: {colored(project_name, Colors.CYAN)}"
        
    except Exception as e:
        return False, colored("[ERROR]", Colors.RED, Colors.BOLD) + f" Could not create project: {e}"


def update_from_github():
    """Update DeonAi CLI from GitHub repository"""
    import subprocess
    
    print(f"\n{colored('═' * 60, Colors.CYAN)}")
    print(f"{colored('DeonAi Auto-Update', Colors.CYAN, Colors.BOLD)}")
    print(f"{colored('═' * 60, Colors.CYAN)}\n")
    
    repo_url = "https://github.com/4shil/deonai-cli.git"
    
    try:
        # Get current script location
        script_path = Path(__file__).resolve()
        repo_dir = script_path.parent
        
        print(f"{colored('[INFO]', Colors.BLUE)} Checking for updates...")
        print(f"{colored('[INFO]', Colors.BLUE)} Repository: {colored(repo_url, Colors.CYAN)}\n")
        
        # Check if we're in a git repo
        is_git_repo = (repo_dir / '.git').exists()
        
        if is_git_repo:
            # Pull latest changes
            print(f"{colored('[INFO]', Colors.BLUE)} Pulling latest changes...\n")
            
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if "Already up to date" in result.stdout:
                    print(f"{colored('[SUCCESS]', Colors.GREEN, Colors.BOLD)} You are already on the latest version!\n")
                else:
                    print(f"{colored('[SUCCESS]', Colors.GREEN, Colors.BOLD)} Updated successfully!")
                    print(f"\n{Colors.DIM}{result.stdout}{Colors.RESET}\n")
                    print(f"{colored('[INFO]', Colors.BLUE)} Please restart DeonAi to use the new version.\n")
            else:
                print(f"{colored('[ERROR]', Colors.RED, Colors.BOLD)} Update failed:\n")
                print(f"{Colors.DIM}{result.stderr}{Colors.RESET}\n")
                return False
        else:
            # Not a git repo, download fresh copy
            print(f"{colored('[INFO]', Colors.BLUE)} Not installed via git. Downloading fresh copy...\n")
            print(f"{colored('[INFO]', Colors.YELLOW)} Manual update required:")
            print(f"  1. cd ~")
            print(f"  2. rm -rf deonai-cli")
            print(f"  3. git clone {repo_url}")
            print(f"  4. cd deonai-cli")
            print(f"  5. ./install.sh\n")
            return False
        
        return True
        
    except FileNotFoundError:
        print(f"{colored('[ERROR]', Colors.RED, Colors.BOLD)} Git not installed")
        print(f"{colored('[INFO]', Colors.YELLOW)} Install git to use auto-update\n")
        return False
    except subprocess.TimeoutExpired:
        print(f"{colored('[ERROR]', Colors.RED, Colors.BOLD)} Update timed out\n")
        return False
    except Exception as e:
        print(f"{colored('[ERROR]', Colors.RED, Colors.BOLD)} Update failed: {e}\n")
        return False


def chat_mode(api_key, model):
    """Interactive chat mode"""
    print(DEONAI_BANNER)
    print(f"{colored('Chat Mode', Colors.CYAN, Colors.BOLD)} - Model: {colored(model, Colors.MAGENTA)}")
    print(f"{Colors.DIM}Type '/help' for commands or just chat naturally{Colors.RESET}\n")
    
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
            
            # Check if this is a slash command
            if user_input.startswith('/'):
                command = user_input[1:].lower()
                
                if command == "exit":
                    print(f"\n{colored('Goodbye!', Colors.CYAN, Colors.BOLD)} 👋\n")
                    break
                
                elif command == "clear":
                    history = []
                    save_history(history)
                    print(f"{colored('[INFO]', Colors.BLUE)} Conversation cleared\n")
                    continue
                
                elif command == "models":
                    loader = LoadingAnimation("Fetching models")
                    loader.start()
                    models = fetch_openrouter_models(api_key)
                    loader.stop()
                    
                    if models:
                        print(f"\n{colored('═' * 60, Colors.CYAN)}")
                        print(f"{colored('Available Models', Colors.CYAN, Colors.BOLD)} {colored(f'({len(models)} total)', Colors.DIM)}")
                        print(f"{colored('═' * 60, Colors.CYAN)}\n")
                        
                        for i, m in enumerate(models[:30], 1):
                            name = m.get('name', m.get('id'))
                            model_id = m.get('id')
                            print(f"  {colored(f'{i:2d}.', Colors.DIM)} {colored(model_id, Colors.CYAN)}")
                            print(f"      {Colors.DIM}{name}{Colors.RESET}")
                        
                        if len(models) > 30:
                            print(f"\n  {Colors.DIM}... and {colored(str(len(models) - 30), Colors.CYAN)} more models{Colors.RESET}")
                        
                        print(f"\n{colored('═' * 60, Colors.CYAN)}")
                        print(f"{Colors.DIM}Use {colored('/switch', Colors.GREEN)} to change models{Colors.RESET}\n")
                    else:
                        print(f"{colored('[ERROR]', Colors.RED, Colors.BOLD)} Could not fetch models\n")
                    continue
                
                elif command == "help":
                    print(f"\n{colored('═' * 60, Colors.CYAN)}")
                    print(f"{colored('DeonAi Commands', Colors.CYAN, Colors.BOLD)}")
                    print(f"{colored('═' * 60, Colors.CYAN)}\n")
                    
                    print(f"{colored('Basic:', Colors.YELLOW, Colors.BOLD)}")
                    print(f"  {colored('/exit', Colors.GREEN)}      - Quit the application")
                    print(f"  {colored('/clear', Colors.GREEN)}     - Reset conversation history")
                    print(f"  {colored('/undo', Colors.GREEN)}      - Remove last message pair")
                    print(f"  {colored('/help', Colors.GREEN)}      - Show this help message")
                    print(f"  {colored('/status', Colors.GREEN)}    - Show current configuration\n")
                    
                    print(f"{colored('AI Control:', Colors.YELLOW, Colors.BOLD)}")
                    print(f"  {colored('/models', Colors.GREEN)}    - List all available AI models")
                    print(f"  {colored('/switch', Colors.GREEN)}    - Quick switch to another model")
                    print(f"  {colored('/retry', Colors.GREEN)}     - Retry last message with different model")
                    print(f"  {colored('/system', Colors.GREEN)}    - Change system prompt")
                    triple_quotes = '"""'
                    print(f'  {colored(triple_quotes, Colors.GREEN)}       - Start multiline input (end with {triple_quotes})\n')
                    
                    print(f"{colored('File Operations:', Colors.YELLOW, Colors.BOLD)}")
                    print(f"  {colored('/read', Colors.GREEN)} <file>    - Read file and show content")
                    print(f"  {colored('/ls', Colors.GREEN)} [dir]       - List directory contents")
                    print(f"  {colored('/run', Colors.GREEN)} <file>     - Execute a code file")
                    print(f"  {colored('/init', Colors.GREEN)} <type> <name> - Create new project\n")
                    
                    print(f"{colored('Utilities:', Colors.YELLOW, Colors.BOLD)}")
                    print(f"  {colored('/search', Colors.GREEN)} <query> - Search conversation history")
                    print(f"  {colored('/profile', Colors.GREEN)}  - Manage profiles (save/load/list)")
                    print(f"  {colored('/export', Colors.GREEN)}   - Export conversation to file\n")
                    
                    print(f"{colored('Note:', Colors.YELLOW)} {Colors.DIM}Commands start with / to distinguish from AI chat{Colors.RESET}")
                    print(f"{colored('═' * 60, Colors.CYAN)}\n")
                    continue
                
                elif command == "switch":
                    print(f"\n{colored('Quick Model Switch', Colors.CYAN, Colors.BOLD)}")
                    print(f"\n{colored('Popular models:', Colors.YELLOW)}")
                    quick_models = [
                        "anthropic/claude-sonnet-4",
                        "anthropic/claude-opus-4",
                        "google/gemini-2.0-flash-exp:free",
                        "openai/gpt-4o",
                        "meta-llama/llama-3.3-70b-instruct"
                    ]
                    for i, m in enumerate(quick_models, 1):
                        print(f"  {colored(str(i), Colors.GREEN)}. {colored(m, Colors.CYAN)}")
                    print(f"  {colored('0', Colors.GREEN)}. Enter custom model ID\n")
                    
                    choice = input(f"{colored('Choice:', Colors.YELLOW)} ").strip()
                    try:
                        idx = int(choice)
                        if 1 <= idx <= len(quick_models):
                            new_model = quick_models[idx - 1]
                        elif idx == 0:
                            new_model = input(f"{colored('Enter model ID:', Colors.YELLOW)} ").strip()
                        else:
                            print(f"{colored('[ERROR]', Colors.RED)} Invalid choice\n")
                            continue
                    except ValueError:
                        new_model = choice
                    
                    if new_model:
                        # Update config
                        config = load_config()
                        config["model"] = new_model
                        model = new_model
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(config, f)
                        print(f"\n{colored('[SUCCESS]', Colors.GREEN, Colors.BOLD)} Switched to: {colored(model, Colors.CYAN)}\n")
                    continue
                
                elif command == "undo":
                    if len(history) >= 2:
                        history.pop()  # Remove assistant
                        history.pop()  # Remove user
                        save_history(history)
                        print(f"{colored('[INFO]', Colors.BLUE)} Removed last message pair\n")
                    elif len(history) == 1:
                        history.pop()
                        save_history(history)
                        print(f"{colored('[INFO]', Colors.BLUE)} Removed last message\n")
                    else:
                        print(f"{colored('[ERROR]', Colors.RED)} No messages to undo\n")
                    continue
                
                elif command == "status":
                    print(f"\n{colored('═' * 60, Colors.CYAN)}")
                    print(f"{colored('DeonAi Status', Colors.CYAN, Colors.BOLD)}")
                    print(f"{colored('═' * 60, Colors.CYAN)}\n")
                    print(f"{colored('Model:', Colors.YELLOW)} {colored(model, Colors.CYAN)}")
                    print(f"{colored('Messages:', Colors.YELLOW)} {colored(str(len(history)), Colors.CYAN)}")
                    print(f"{colored('Tokens used:', Colors.YELLOW)} {colored(str(total_tokens), Colors.CYAN)}")
                    custom_prompt = SYSTEM_PROMPT_FILE.exists()
                    print(f"{colored('System prompt:', Colors.YELLOW)} {colored('Custom' if custom_prompt else 'Default', Colors.CYAN)}")
                    print(f"\n{colored('═' * 60, Colors.CYAN)}\n")
                    continue
                
                # For file and other commands starting with /, strip slash and continue to old handlers
                elif command.startswith(('read', 'ls', 'run', 'init', 'search', 'profile', 'export', 'retry', 'system')):
                    user_input = user_input[1:]  # Strip the slash
                    # Will be processed by old handlers below
                
                else:
                    # Unknown slash command
                    print(f"{colored('[ERROR]', Colors.RED)} Unknown command: /{command}")
                    print(f"{colored('[INFO]', Colors.BLUE)} Type {colored('/help', Colors.GREEN)} to see available commands\n")
                    continue
            
            # Old command handling (without slash) for backward compatibility
            if user_input.lower() == "exit":
                print(f"\n{colored('Goodbye!', Colors.CYAN, Colors.BOLD)} 👋\n")
                break
            
            if user_input.lower() == "clear":
                history = []
                save_history(history)
                print(f"{colored('[INFO]', Colors.BLUE)} Conversation cleared\n")
                continue
            
            if user_input.lower() == "models":
                loader = LoadingAnimation("Fetching models")
                loader.start()
                models = fetch_openrouter_models(api_key)
                loader.stop()
                
                if models:
                    print(f"\n{colored('═' * 60, Colors.CYAN)}")
                    print(f"{colored('Available Models', Colors.CYAN, Colors.BOLD)} {colored(f'({len(models)} total)', Colors.DIM)}")
                    print(f"{colored('═' * 60, Colors.CYAN)}\n")
                    
                    for i, m in enumerate(models[:30], 1):
                        name = m.get('name', m.get('id'))
                        model_id = m.get('id')
                        print(f"  {colored(f'{i:2d}.', Colors.DIM)} {colored(model_id, Colors.CYAN)}")
                        print(f"      {Colors.DIM}{name}{Colors.RESET}")
                    
                    if len(models) > 30:
                        print(f"\n  {Colors.DIM}... and {colored(str(len(models) - 30), Colors.CYAN)} more models{Colors.RESET}")
                    
                    print(f"\n{colored('═' * 60, Colors.CYAN)}")
                    print(f"{Colors.DIM}Use {colored('/switch', Colors.GREEN)} to change models{Colors.RESET}\n")
                else:
                    print(f"{colored('[ERROR]', Colors.RED, Colors.BOLD)} Could not fetch models\n")
                continue
            
            if user_input.lower() == "help":
                print(f"\n{colored('═' * 60, Colors.CYAN)}")
                print(f"{colored('DeonAi Commands', Colors.CYAN, Colors.BOLD)}")
                print(f"{colored('═' * 60, Colors.CYAN)}\n")
                
                print(f"{colored('Basic:', Colors.YELLOW, Colors.BOLD)}")
                print(f"  {colored('exit', Colors.GREEN)}      - Quit the application")
                print(f"  {colored('clear', Colors.GREEN)}     - Reset conversation history")
                print(f"  {colored('undo', Colors.GREEN)}      - Remove last message pair")
                print(f"  {colored('help', Colors.GREEN)}      - Show this help message")
                print(f"  {colored('status', Colors.GREEN)}    - Show current configuration\n")
                
                print(f"{colored('AI Control:', Colors.YELLOW, Colors.BOLD)}")
                print(f"  {colored('models', Colors.GREEN)}    - List all available AI models")
                print(f"  {colored('switch', Colors.GREEN)}    - Quick switch to another model")
                print(f"  {colored('retry', Colors.GREEN)}     - Retry last message with different model")
                print(f"  {colored('system', Colors.GREEN)}    - Change system prompt")
                triple_quotes = '"""'
                print(f'  {colored(triple_quotes, Colors.GREEN)}       - Start multiline input (end with {triple_quotes})\n')
                
                print(f"{colored('File Operations:', Colors.YELLOW, Colors.BOLD)}")
                print(f"  {colored('read', Colors.GREEN)}      - Read file and show content")
                print(f"  {colored('ls', Colors.GREEN)}        - List directory contents")
                print(f"  {colored('run', Colors.GREEN)}       - Execute a code file")
                print(f"  {colored('init', Colors.GREEN)}      - Create new project (python/node/web)\n")
                
                print(f"{colored('Utilities:', Colors.YELLOW, Colors.BOLD)}")
                print(f"  {colored('search', Colors.GREEN)}    - Search conversation history")
                print(f"  {colored('profile', Colors.GREEN)}   - Manage profiles (save/load/list)")
                print(f"  {colored('export', Colors.GREEN)}    - Export conversation to file\n")
                
                print(f"{colored('═' * 60, Colors.CYAN)}\n")
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
                    current_prompt = load_system_prompt()
                    is_custom = SYSTEM_PROMPT_FILE.exists()
                    
                    print(f"\n{colored('═' * 60, Colors.CYAN)}")
                    print(f"{colored('System Prompt', Colors.CYAN, Colors.BOLD)} {colored('(Custom)' if is_custom else '(Default)', Colors.YELLOW)}")
                    print(f"{colored('═' * 60, Colors.CYAN)}\n")
                    print(f"{Colors.DIM}{current_prompt}{Colors.RESET}\n")
                    print(f"{colored('═' * 60, Colors.CYAN)}\n")
                    
                    print(f"{colored('Options:', Colors.YELLOW, Colors.BOLD)}")
                    print(f"  {colored('1', Colors.GREEN)} - Set custom system prompt")
                    print(f"  {colored('2', Colors.GREEN)} - Reset to default")
                    print(f"  {colored('3', Colors.GREEN)} - Cancel\n")
                    
                    choice = input(f"{colored('Choose:', Colors.CYAN)} ").strip()
                    
                    if choice == "1":
                        print(f"\n{colored('[INFO]', Colors.BLUE)} Enter new system prompt (type END on a new line to finish):\n")
                        lines = []
                        while True:
                            line = input()
                            if line.strip().upper() == "END":
                                break
                            lines.append(line)
                        
                        if lines:
                            new_prompt = "\n".join(lines).strip()
                            if save_system_prompt(new_prompt):
                                print(f"\n{colored('[SUCCESS]', Colors.GREEN, Colors.BOLD)} System prompt saved! Will apply to new conversations.\n")
                        else:
                            print(f"\n{colored('[INFO]', Colors.BLUE)} No changes made\n")
                    
                    elif choice == "2":
                        if reset_system_prompt():
                            print(f"\n{colored('[SUCCESS]', Colors.GREEN, Colors.BOLD)} Reset to default system prompt\n")
                        else:
                            print(f"\n{colored('[INFO]', Colors.BLUE)} Already using default prompt\n")
                    
                else:
                    # Quick system prompt change
                    new_prompt = parts[1]
                    if save_system_prompt(new_prompt):
                        print(f"{colored('[SUCCESS]', Colors.GREEN, Colors.BOLD)} System prompt updated\n")
                
                continue
            
            if user_input.lower() == "retry":
                if len(history) < 2:
                    print(f"{colored('[ERROR]', Colors.RED)} No previous message to retry\n")
                    continue
                
                # Remove last assistant response if exists
                if history and history[-1]["role"] == "assistant":
                    history.pop()
                
                # Get the last user message - verify it exists and is user role
                if history and history[-1]["role"] == "user":
                    last_user_msg = history[-1]["content"]
                    print(f"\n{colored('[INFO]', Colors.BLUE)} Retrying: {colored(last_user_msg[:50], Colors.DIM)}...")
                    save_history(history)  # Save after removing assistant message
                    
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
            
            # Show typing animation
            typing = TypingAnimation()
            typing.start()
            
            # Call OpenRouter API
            try:
                # Try streaming first
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
                            {"role": "system", "content": load_system_prompt()}
                        ] + history,
                        "stream": use_streaming
                    },
                    timeout=60,
                    stream=use_streaming
                )
                response.raise_for_status()
                
                # Stop typing animation and show AI label
                typing.stop()
                print(f"\n{colored('DeonAi:', Colors.MAGENTA, Colors.BOLD)} ", end="", flush=True)
                
                if use_streaming:
                    # Stream the response
                    assistant_text = ""
                    has_content = False
                    
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
                                        has_content = True
                                        print(content, end="", flush=True)
                                        assistant_text += content
                                except json.JSONDecodeError:
                                    continue
                    
                    # If no content was streamed, it might be an error
                    if not has_content and not assistant_text:
                        print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} No response received from model")
                        print(f"{colored('[INFO]', Colors.BLUE)} This model might not support streaming or have issues")
                        print(f"{Colors.DIM}Try switching to a different model with {colored('/switch', Colors.GREEN)}{Colors.RESET}\n")
                        if history:  # Safety check
                            history.pop()  # Remove user message
                        continue
                    
                    print("\n")
                    
                    # Check for file write commands
                    saved_files = parse_and_save_files(assistant_text)
                    if saved_files:
                        print(f"{colored('[INFO]', Colors.BLUE)} Created {len(saved_files)} file(s): {', '.join(saved_files)}\n")
                    
                    usage = {}
                    tokens_used = 0
                else:
                    result = response.json()
                    
                    # Check if we got a valid response
                    if "choices" not in result or not result["choices"]:
                        print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} Invalid response from API")
                        print(f"{colored('[INFO]', Colors.BLUE)} Try a different model with {colored('/switch', Colors.GREEN)}\n")
                        if history:  # Safety check
                            history.pop()
                        continue
                    
                    assistant_text = result["choices"][0]["message"]["content"]
                    
                    if not assistant_text:
                        print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} Empty response from model")
                        print(f"{Colors.DIM}Try switching models or rephrasing your question{Colors.RESET}\n")
                        if history:  # Safety check
                            history.pop()
                        continue
                    
                    print(assistant_text)
                    
                    # Check for file write commands
                    saved_files = parse_and_save_files(assistant_text)
                    if saved_files:
                        print(f"\n{colored('[INFO]', Colors.BLUE)} Created {len(saved_files)} file(s): {', '.join(saved_files)}\n")
                    
                    # Track token usage
                    usage = result.get("usage", {})
                    tokens_used = usage.get("total_tokens", 0)
                    total_tokens += tokens_used
                    
                    if tokens_used > 0:
                        print(f"\n{colored('[USAGE]', Colors.DIM)} {tokens_used} tokens\n")
                    else:
                        print()
                
                history.append({"role": "assistant", "content": assistant_text})
                save_history(history)
                
            except requests.exceptions.Timeout:
                typing.stop()
                print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} Request timed out. Try again.\n")
                if history:  # Safety check
                    history.pop()  # Remove user message since it failed
            except requests.exceptions.RequestException as e:
                typing.stop()
                print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} API Error: {e}\n")
                if history:  # Safety check
                    history.pop()  # Remove user message since it failed
            except Exception as e:
                typing.stop()
                print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} Unexpected error: {e}\n")
                if history:  # Safety check
                    history.pop()
            
        except KeyboardInterrupt:
            # Stop typing animation if running
            if 'typing' in locals():
                typing.stop()
            print(f"\n\n{colored('Goodbye!', Colors.CYAN, Colors.BOLD)} 👋\n")
            break
        except Exception as e:
            # Stop typing animation if running
            if 'typing' in locals():
                typing.stop()
            print(f"\n{colored('[ERROR]', Colors.RED, Colors.BOLD)} {e}\n")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_config()
    elif len(sys.argv) > 1 and sys.argv[1] == "--version":
        print(DEONAI_BANNER)
        print(f"{colored('Version:', Colors.CYAN, Colors.BOLD)} 2.7")
        print(f"{colored('Repository:', Colors.CYAN, Colors.BOLD)} https://github.com/4shil/deonai-cli")
        print(f"{colored('Powered by:', Colors.CYAN, Colors.BOLD)} OpenRouter\n")
    elif len(sys.argv) > 1 and sys.argv[1] == "--upgrade":
        update_from_github()
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
                            {"role": "system", "content": load_system_prompt()},
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
