# 🌊 DeonAi CLI

Your personal AI assistant in the terminal. Simple, fast, customized. **Now powered by OpenRouter** - access 200+ AI models with one API key!

## Features

- 🚀 **One-shot queries**: `deonai "explain docker compose"`
- 💬 **Interactive chat**: `deonai` for conversation mode
- 🧠 **Memory**: Remembers conversation context
- 🌐 **200+ Models**: Claude, GPT-4, Gemini, Llama, and more via OpenRouter
- 🎨 **Branded**: Custom DeonAi personality
- 🔧 **Customizable**: Easy to modify prompts and behavior
- 💰 **Cost-effective**: Choose from free or paid models

## Installation

```bash
# Clone this repo
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli

# Run installer
./install.sh

# Setup (paste your OpenRouter API key)
deonai --setup
```

Get your OpenRouter API key at: https://openrouter.ai/keys

## Usage

### Interactive Mode (Chat)
```bash
deonai
```

Starts a conversation. Type messages, get responses. Commands:
- `exit` - quit
- `clear` - reset conversation
- `models` - list all available models

### One-Shot Mode
```bash
deonai "write a bash script to backup my files"
deonai "explain async/await in JavaScript"
deonai "what's the weather API for Python?"
```

Perfect for quick questions or piping into other commands.

## Available Models

OpenRouter gives you access to 200+ models from multiple providers:

### Popular Models
- **Claude**: `anthropic/claude-sonnet-4`, `anthropic/claude-opus-4`
- **GPT**: `openai/gpt-4o`, `openai/gpt-4-turbo`
- **Gemini**: `google/gemini-2.0-flash-exp:free` (FREE!)
- **Llama**: `meta-llama/llama-3.3-70b-instruct`
- **DeepSeek**: `deepseek/deepseek-r1` (reasoning model)

Run `deonai --setup` to see all available models and switch between them.

## Configuration

Config stored in `~/.deonai/config.json`:
```json
{
  "api_key": "sk-or-...",
  "model": "anthropic/claude-sonnet-4"
}
```

To reconfigure: `deonai --setup`

## Customization

### Change Personality

Edit the `DEONAI_SYSTEM` prompt in `deonai.py`:

```python
DEONAI_SYSTEM = """You are DeonAi, a [YOUR CUSTOM TRAITS HERE]

Core traits:
- [Add your own]
- [Make it unique]
"""
```

### Change Model

Run `deonai --setup` again to choose from 200+ models, or manually edit `~/.deonai/config.json`

### Free Models

Several models are completely free:
- `google/gemini-2.0-flash-exp:free`
- `google/gemini-flash-1.5`
- `meta-llama/llama-3.2-3b-instruct:free`

## Why OpenRouter?

- **One API key** for 200+ models
- **No vendor lock-in** - switch models anytime
- **Cost optimization** - choose the best model for your budget
- **Unified interface** - same code works with all models
- **Automatic fallbacks** - if one provider is down, try another

## Requirements

- Python 3.7+
- `requests` package (installed automatically)
- OpenRouter API key (from https://openrouter.ai/keys)

## Examples

```bash
# Quick coding help
deonai "regex to match email addresses"

# Compare models (try different ones)
deonai --setup  # switch to gemini-2.0-flash-exp:free
deonai "explain quantum computing"

# Use in scripts
ANSWER=$(deonai "short answer: capital of France")
echo $ANSWER

# Interactive learning
deonai  # then type "teach me python generators"
```

## Uninstall

```bash
rm ~/.local/bin/deonai
rm -rf ~/.deonai
```

## License

MIT - Modify and share freely

## Changelog

### v2.0 - OpenRouter Integration
- ✨ Added support for 200+ models via OpenRouter
- 🔄 Replaced Anthropic-only API with OpenRouter
- 📋 Added `models` command to list available models during chat
- 🆓 Added support for free models (Gemini, Llama)
- 🎯 Interactive model selection during setup

### v1.0 - Initial Release
- Basic CLI with Anthropic Claude
- One-shot and chat modes
- Configuration system

---

Made with 🌊 by DeonAi | Powered by [OpenRouter](https://openrouter.ai)
