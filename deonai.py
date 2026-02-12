#!/usr/bin/env python3
"""
DeonAi CLI - Your personal AI assistant in the terminal
Simple, fast, customized for you.
"""

import sys
import json
import requests
from pathlib import Path

# DeonAi branding
DEONAI_BANNER = """
╔══════════════════════════════════════╗
║         🌊 DeonAi CLI v1.0          ║
║  Your Personal Terminal Assistant   ║
╚══════════════════════════════════════╝
"""

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
    print(DEONAI_BANNER)
    print("Welcome! Let's set up DeonAi.\n")
    
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
    
    # Choose model
    print("Choose your model:")
    print("1. claude-sonnet-4.5 (balanced - recommended)")
    print("2. claude-opus-4 (most capable)")
    print("3. claude-haiku-4 (fastest, cheapest)")
    
    choice = input("\nChoice [1]: ").strip() or "1"
    models = {
        "1": "claude-sonnet-4.5",
        "2": "claude-opus-4",
        "3": "claude-haiku-4"
    }
    model = models.get(choice, "claude-sonnet-4.5")
    
    # Save config
    CONFIG_DIR.mkdir(exist_ok=True)
    config = {"api_key": api_key, "model": model}
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    
    # Set restrictive permissions
    import os
    os.chmod(CONFIG_FILE, 0o600)
    
    print(f"\n✓ DeonAi configured with {model}")
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


def chat_mode(client, model):
    """Interactive chat mode"""
    print(DEONAI_BANNER)
    print("Chat mode - Type 'exit' to quit, 'clear' to reset conversation\n")
    
    history = load_history()
    if history:
        print(f"📝 Loaded {len(history)//2} previous messages\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == "clear":
                history = []
                save_history(history)
                print("🗑️  Conversation cleared\n")
                continue
            
            history.append({"role": "user", "content": user_input})
            
            print("\nDeonAi: ", end="", flush=True)
            
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                system=DEONAI_SYSTEM,
                messages=history
            )
            
            assistant_text = response.content[0].text
            print(assistant_text + "\n")
            
            history.append({"role": "assistant", "content": assistant_text})
            save_history(history)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_config()
    else:
        config = load_config()
        client = anthropic.Anthropic(api_key=config["api_key"])
        
        # One-shot mode or chat mode
        if len(sys.argv) > 1:
            prompt = " ".join(sys.argv[1:])
            
            response = client.messages.create(
                model=config["model"],
                max_tokens=4096,
                system=DEONAI_SYSTEM,
                messages=[{"role": "user", "content": prompt}]
            )
            
            print(response.content[0].text)
        else:
            # Interactive chat mode
            chat_mode(client, config["model"])


if __name__ == "__main__":
    main()
