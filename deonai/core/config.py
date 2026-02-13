"""
DeonAi Core - Configuration Management
"""

import json
import sys
from pathlib import Path
from ..utils import Colors, colored

# Configuration paths
CONFIG_DIR = Path.home() / ".deonai"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
PROFILES_FILE = CONFIG_DIR / "profiles.json"
SYSTEM_PROMPT_FILE = CONFIG_DIR / "system_prompt.txt"
MODELS_CACHE_FILE = CONFIG_DIR / "models_cache.json"

# OpenRouter API settings
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

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


def save_config(config: dict):
    """Save configuration"""
    try:
        CONFIG_DIR.mkdir(exist_ok=True, parents=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"{colored('[ERROR]', Colors.RED)} Could not save config: {e}")
        return False


def save_history(history: list):
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
