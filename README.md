# deonai-cli

A personal AI assistant for the terminal. One command to query, one command to chat — powered by OpenRouter with access to 200+ models including Claude, GPT-4, Gemini, and Llama.

![terminal ai demo](https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif)

## Installation

**Linux / macOS**

```bash
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
./install.sh
deonai --setup
```

**Windows**

```batch
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
install-windows.bat
deonai --setup
```

Get your API key at [openrouter.ai/keys](https://openrouter.ai/keys) and paste it during `--setup`.

## Usage

```bash
# One-shot query
deonai "explain docker volumes"

# Interactive chat mode
deonai

# Use a specific model
deonai --model anthropic/claude-3.5-sonnet "refactor this function"

# Add a file as context
deonai --file main.py "what does this do?"

# Switch models mid-session
/model gpt-4o

# Export conversation
deonai --export markdown
```

## Features

- One-shot queries and persistent interactive chat
- Conversation memory within a session
- 200+ models via a single OpenRouter API key
- Streaming responses (token-by-token)
- File context — attach files for AI to analyze
- AI-driven file creation and code execution
- Conversation search and export (Markdown / JSON)
- Token usage tracking
- Multiple configuration profiles

## Project Structure

```
deonai-cli/
├── deonai/
│   ├── cli/            # Argument parsing, REPL loop
│   ├── core/           # Chat engine, streaming, memory
│   ├── integrations/   # OpenRouter API client
│   ├── plugins/        # File ops, code execution
│   └── utils/          # Formatting, syntax highlighting
├── deonai.py           # Entry point
├── install.sh
├── install-windows.bat
└── requirements.txt
```

## Requirements

- Python 3.9+
- OpenRouter API key

Dependencies are installed automatically by the install script. To install manually:

```bash
pip install -r requirements.txt
```

## Configuration

Running `deonai --setup` creates a config file at `~/.config/deonai/config.json`. You can edit it directly to set a default model, system prompt, or additional profiles.

## License

MIT
