#!/usr/bin/env python3
"""
DeonAi CLI - Configuration system
"""

import sys
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".deonai"
CONFIG_FILE = CONFIG_DIR / "config.json"


def setup_config():
    """First-time setup - ask for API key"""
    print("🌊 DeonAi Setup\n")
    
    api_key = input("Paste your Claude API key: ").strip()
    
    if not api_key.startswith("sk-ant-"):
        print("⚠️  Invalid API key format")
        sys.exit(1)
    
    CONFIG_DIR.mkdir(exist_ok=True)
    config = {"api_key": api_key}
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    
    print("✓ Configuration saved!")


def load_config():
    """Load existing config"""
    if not CONFIG_FILE.exists():
        print("Run 'deonai --setup' first")
        sys.exit(1)
    
    with open(CONFIG_FILE) as f:
        return json.load(f)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_config()
    else:
        config = load_config()
        print(f"✓ Config loaded: {config['api_key'][:10]}...")


if __name__ == "__main__":
    main()
