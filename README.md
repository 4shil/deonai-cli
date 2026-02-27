# deonai-cli

A personal AI assistant for the terminal. Talks to 200+ models through OpenRouter, reads and writes files directly, tracks git context, and keeps conversation history — all from the command line.

![demo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm9jcG43bHo4NzJhYXRrZ2h2cGZobnE4bmhsMWx4cW1ra3V6ZzY0YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT9IgzoKnwFNmISR8I/giphy.gif)

---

## What it does

- Chat with any LLM model available on OpenRouter directly from your terminal
- Ask it to create or modify files — it writes them automatically using a `WRITE_FILE:` pattern it detects in responses
- Git-aware: reads your current repo context and includes it in conversations
- Persistent history stored at `~/.deonai/`
- Multiple profiles for different configurations and system prompts

---

## Stack

- Python 3.10+
- requests (HTTP to OpenRouter)
- colorama + pygments (terminal UI)
- No framework — pure CLI

---

## Install

**Linux/macOS**

```bash
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
chmod +x install.sh
./install.sh
```

**Windows**

```cmd
install-windows.bat
```

The installer sets up a virtual environment, installs dependencies, and adds `deonai` to your PATH.

---

## Setup

On first run, set your OpenRouter API key:

```bash
deonai config set api_key YOUR_OPENROUTER_KEY
```

Get a free key at [openrouter.ai](https://openrouter.ai).

---

## Usage

```bash
# Start a conversation
deonai chat

# Ask a one-off question
deonai ask "how do I reverse a list in Python"

# List available models
deonai models

# Switch model
deonai config set model anthropic/claude-3-haiku

# View history
deonai history

# Run tests
pytest
```

---

## File operations

Ask it to write files during a conversation:

```
You: create a FastAPI hello world app in main.py
DeonAi: WRITE_FILE: main.py
        ```python
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/")
        def root():
            return {"message": "Hello, World!"}
        ```
```

The CLI detects the `WRITE_FILE:` pattern and saves the file automatically.

---

## Project structure

```
deonai-cli/
├── deonai/
│   ├── cli/
│   │   └── commands.py        # CLI entry points
│   ├── core/
│   │   ├── agent.py           # Conversation loop + model calls
│   │   ├── base.py            # Base classes
│   │   ├── config.py          # Config management (~/.deonai/)
│   │   ├── context.py         # Project context gathering
│   │   ├── tools.py           # Tool definitions
│   │   ├── patch_tools.py     # File write/patch tools
│   │   ├── builtin_tools.py   # Built-in tool implementations
│   │   ├── git_tools.py       # Git integration
│   │   └── logger.py
│   ├── integrations/
│   │   └── git.py             # Git repo context
│   ├── utils/
│   │   ├── colors.py          # Terminal colors
│   │   ├── animations.py      # Typing indicators
│   │   ├── diff.py            # File diff display
│   │   └── fileops.py         # File read/write helpers
│   └── plugins/               # Plugin system (extensible)
├── tests/
├── install.sh
├── install-windows.bat
├── uninstall.sh
└── requirements.txt
```

---

## Config

Config is stored at `~/.deonai/config.json`. Keys:

```json
{
  "api_key": "your-openrouter-key",
  "model": "openai/gpt-4o",
  "system_prompt": "optional custom instructions"
}
```

History lives at `~/.deonai/history.json`. Profiles at `~/.deonai/profiles.json`.

---

## Uninstall

```bash
./uninstall.sh
```

---

## License

MIT
