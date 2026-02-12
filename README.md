# 🌊 DeonAi CLI

Your personal AI assistant in the terminal. Simple, fast, customized.

## Features

- 🚀 **One-shot queries**: `deonai "explain docker compose"`
- 💬 **Interactive chat**: `deonai` for conversation mode
- 🧠 **Memory**: Remembers conversation context
- 🎨 **Branded**: Custom DeonAi personality
- 🔧 **Customizable**: Easy to modify prompts and behavior

## Installation

```bash
# Clone this repo
git clone https://github.com/yourusername/deonai-cli.git
cd deonai-cli

# Run installer
./install.sh

# Setup (paste your Claude API key)
deonai --setup
```

## Usage

### Interactive Mode (Chat)
```bash
deonai
```

Starts a conversation. Type messages, get responses. Commands:
- `exit` - quit
- `clear` - reset conversation

### One-Shot Mode
```bash
deonai "write a bash script to backup my files"
deonai "explain async/await in JavaScript"
deonai "what's the weather API for Python?"
```

Perfect for quick questions or piping into other commands.

## Configuration

Config stored in `~/.deonai/config.json`:
```json
{
  "api_key": "sk-ant-...",
  "model": "claude-sonnet-4.5"
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

Run `deonai --setup` again, or manually edit `~/.deonai/config.json`

Available models:
- `claude-sonnet-4.5` - Balanced (recommended)
- `claude-opus-4` - Most capable
- `claude-haiku-4` - Fastest, cheapest

## Requirements

- Python 3.7+
- `anthropic` package (installed automatically)
- Claude API key (from console.anthropic.com)

## License

MIT - Modify and share freely

---

Made with 🌊 by DeonAi
