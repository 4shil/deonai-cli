# DeonAi CLI

Your personal AI assistant in the terminal. Simple, fast, customized. **Powered by OpenRouter** - access 200+ AI models with one API key!

![DeonAi Demo](https://user-images.githubusercontent.com/placeholder/demo.gif)

## Features

- **One-shot queries**: `deonai "explain docker compose"`
- **Interactive chat**: `deonai` for conversation mode
- **Memory**: Remembers conversation context
- **200+ Models**: Claude, GPT-4, Gemini, Llama, and more via OpenRouter
- **Streaming**: Real-time token-by-token responses
- **Export**: Save conversations as Markdown or JSON
- **Search**: Find past messages in history
- **Token tracking**: Monitor API usage
- **Quick switch**: Change models on the fly
- **Customizable**: Easy to modify prompts and behavior
- **Cost-effective**: Choose from free or paid models

## Installation

### Linux / macOS

```bash
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
./install.sh
deonai --setup
```

### Windows

```batch
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
install-windows.bat
deonai --setup
```

Get your OpenRouter API key at: https://openrouter.ai/keys

## Usage

### Interactive Mode (Chat)
```bash
deonai
```

Available commands:
- `exit` - Quit the application
- `clear` - Reset conversation history
- `models` - List all available AI models
- `switch` - Quick switch to another model
- `search <query>` - Search conversation history
- `export` - Export conversation to file
- `status` - Show current configuration
- `help` - Show all commands

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

To quick switch: Run `deonai` then type `switch`

## Screenshots

### Chat Mode
```
╔══════════════════════════════════════╗
║         DeonAi CLI v2.0             ║
║  Your Personal Terminal Assistant   ║
║      Powered by OpenRouter          ║
╚══════════════════════════════════════╝

Chat mode - Model: anthropic/claude-sonnet-4
Type 'help' for commands

You: explain quantum computing

DeonAi: Quantum computing is a type of computing that uses quantum-mechanical
phenomena like superposition and entanglement to perform calculations...

[USAGE] 245 tokens
```

### Export Example
```bash
You: export
[SUCCESS] Conversation exported:
  Markdown: ~/.deonai/conversation_20260212_131500.md
  JSON: ~/.deonai/conversation_20260212_131500.json
```

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

## Advanced Usage

### Export and Share Conversations
```bash
# In chat mode
You: export
# Creates markdown and JSON files in ~/.deonai/
```

### Search History
```bash
You: search docker
[SEARCH] Found 3 matches for 'docker':
  [12] User: how do I use docker compose
  [14] Assistant: Docker Compose is a tool for defining...
  [28] User: docker networking explained
```

### Switch Models Mid-Conversation
```bash
You: switch
[INFO] Quick model switch
Popular models:
  1. anthropic/claude-sonnet-4
  2. anthropic/claude-opus-4
  3. google/gemini-2.0-flash-exp:free
  4. openai/gpt-4o
  5. meta-llama/llama-3.3-70b-instruct
  0. Enter custom model ID

Choice: 3
[SUCCESS] Switched to: google/gemini-2.0-flash-exp:free
```

## Uninstall

```bash
rm ~/.local/bin/deonai  # Linux/macOS
rm -rf ~/.deonai
```

## License

MIT - Modify and share freely

## Changelog

### v2.1 - Feature Enhancement Release
- Added streaming responses for real-time output
- Added conversation export (Markdown + JSON)
- Added token usage tracking
- Added quick model switching
- Added conversation search
- Added help and status commands
- Improved error handling
- Added Windows installer
- Removed emojis for professional appearance

### v2.0 - OpenRouter Integration
- Added support for 200+ models via OpenRouter
- Replaced Anthropic-only API with OpenRouter
- Added `models` command to list available models during chat
- Added support for free models (Gemini, Llama)
- Interactive model selection during setup

### v1.0 - Initial Release
- Basic CLI with Anthropic Claude
- One-shot and chat modes
- Configuration system

---

Made by 4shil | Powered by [OpenRouter](https://openrouter.ai)

**Star this repo if you find it useful!**
