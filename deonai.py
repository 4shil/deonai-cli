#!/usr/bin/env python3
"""
DeonAi CLI - Your personal AI assistant in the terminal
Simple, fast, customized for you. Powered by OpenRouter.
"""

import sys
import json
import requests
from pathlib import Path

# DeonAi branding
DEONAI_BANNER = """
╔══════════════════════════════════════╗
║         🌊 DeonAi CLI v2.0          ║
║  Your Personal Terminal Assistant   ║
║      Powered by OpenRouter 🌐       ║
╚══════════════════════════════════════╝
"""

CONFIG_DIR = Path.home() / ".deonai"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

# OpenRouter API settings
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
MODELS_CACHE_FILE = CONFIG_DIR / "models_cache.json"

# DeonAi personality system prompt
DEONAI_SYSTEM = """You are DeonAi, a helpful and intelligent CLI assistant.

Core traits:
- Direct and concise - no fluff
- Technical but friendly
- Give code examples when relevant
- Admit when you don't know something
- Focus on practical solutions
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
        print(f"⚠️  Could not fetch models: {e}")
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
        print("⚠️  That doesn't look like a valid OpenRouter API key.")
        print("It should start with 'sk-or-'")
        print("Get one at: https://openrouter.ai/keys")
        sys.exit(1)
    
    # Fetch available models
    print("\n🔍 Fetching available models from OpenRouter...")
    models = fetch_openrouter_models(api_key)
    
    if not models:
        print("❌ Could not fetch models. Please check your API key.")
        sys.exit(1)
    
    print(f"✓ Found {len(models)} models!\n")
    
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
            print("\n📋 All available models:")
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
        print(f"⚠️  Model '{model}' not found, using default")
        model = "anthropic/claude-sonnet-4"
    
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


def chat_mode(api_key, model):
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
            
            # Call OpenRouter API
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
                    ] + history
                },
                timeout=60
            )
            response.raise_for_status()
            
            assistant_text = response.json()["choices"][0]["message"]["content"]
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
                print(f"❌ Error: {e}")
        else:
            # Interactive chat mode
            chat_mode(api_key, model)


if __name__ == "__main__":
    main()
