#!/usr/bin/env python3
"""
DeonAi CLI - Anthropic Claude Integration
"""

import sys
import json
import anthropic
from pathlib import Path

CONFIG_DIR = Path.home() / ".deonai"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

# DeonAi personality system prompt
DEONAI_SYSTEM = """You are DeonAi, a helpful and intelligent CLI assistant.

Core traits:
- Direct and concise - no fluff
- Technical but friendly
- Give code examples when relevant
- Admit when you don't know something
- Focus on practical solutions
"""


def setup_config():
    """First-time setup - ask for API key"""
    print("🌊 DeonAi Setup\n")
    
    api_key = input("Paste your Claude API key: ").strip()
    
    if not api_key.startswith("sk-ant-"):
        print("⚠️  Invalid API key format")
        sys.exit(1)
    
    # Test the API key
    try:
        client = anthropic.Anthropic(api_key=api_key)
        client.messages.create(
            model="claude-sonnet-4.5",
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}]
        )
        print("✓ API key verified!")
    except Exception as e:
        print(f"✗ API key test failed: {e}")
        sys.exit(1)
    
    CONFIG_DIR.mkdir(exist_ok=True)
    config = {"api_key": api_key, "model": "claude-sonnet-4.5"}
    
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
        
        # One-shot mode
        if len(sys.argv) > 1:
            prompt = " ".join(sys.argv[1:])
            client = anthropic.Anthropic(api_key=config["api_key"])
            
            response = client.messages.create(
                model=config["model"],
                max_tokens=4096,
                system=DEONAI_SYSTEM,
                messages=[{"role": "user", "content": prompt}]
            )
            
            print(response.content[0].text)
        else:
            print("Run 'deonai <question>' to ask something")
            print("Run 'deonai --setup' to reconfigure")


if __name__ == "__main__":
    main()
