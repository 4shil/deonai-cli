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
║         DeonAi CLI v2.0             ║
║  Your Personal Terminal Assistant   ║
║      Powered by OpenRouter          ║
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


def chat_mode(api_key, model):
    """Interactive chat mode"""
    print(DEONAI_BANNER)
    print(f"Chat mode - Model: {model}")
    print("Type 'help' for commands\n")
    
    history = load_history()
    total_tokens = 0
    
    if history:
        print(f"[INFO] Loaded {len(history)//2} previous messages\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("\nGoodbye!")
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
                print("  models    - List all available AI models")
                print("  switch    - Quick switch to another model")
                print("  search    - Search conversation history")
                print("  help      - Show this help message")
                print("  status    - Show current configuration")
                print("  export    - Export conversation to file\n")
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
                print(f"  Config: {CONFIG_FILE}\n")
                continue
            
            history.append({"role": "user", "content": user_input})
            
            print("\nDeonAi: ", end="", flush=True)
            
            # Call OpenRouter API
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
                            {"role": "system", "content": DEONAI_SYSTEM}
                        ] + history
                    },
                    timeout=60
                )
                response.raise_for_status()
                
                result = response.json()
                assistant_text = result["choices"][0]["message"]["content"]
                
                # Track token usage
                usage = result.get("usage", {})
                tokens_used = usage.get("total_tokens", 0)
                total_tokens += tokens_used
                
                print(assistant_text)
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
