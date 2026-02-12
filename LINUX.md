# DeonAi CLI - Linux Quick Start

## Installation

### One-Line Install
```bash
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
./install.sh
```

### Manual Install
```bash
# Install dependencies
pip3 install --user requests colorama

# Copy to local bin
mkdir -p ~/.local/bin
cp deonai.py ~/.local/bin/deonai
chmod +x ~/.local/bin/deonai

# Add to PATH (if needed)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Supported Distributions

✅ **Tested:**
- Ubuntu 20.04+
- Debian 11+
- Fedora 35+
- Arch Linux
- Linux Mint
- Pop!_OS

🔄 **Should work:**
- CentOS / RHEL 8+
- openSUSE
- Manjaro
- Any modern Linux with Python 3.7+

## Requirements

- Python 3.7 or higher
- pip3
- Terminal with color support
- Internet connection

## Quick Setup

```bash
# 1. Configure API key
deonai --setup

# 2. Start chatting
deonai

# 3. Get help
deonai /help
```

## Linux-Specific Features

### Terminal Colors
DeonAi automatically detects terminal capabilities:
- 256-color terminals: Full color scheme
- Basic terminals: Simplified colors
- Non-TTY: Colors disabled

### Shell Integration

**Bash:**
```bash
# Add to ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

**Zsh:**
```bash
# Add to ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

**Fish:**
```fish
# Add to ~/.config/fish/config.fish
set -gx PATH $HOME/.local/bin $PATH
```

### Desktop Integration

The installer can create a `.desktop` entry for easy access from application menus.

## Configuration

All config stored in: `~/.deonai/`
- `config.json` - API key and model
- `history.json` - Conversation history
- `system_prompt.txt` - Custom AI personality
- `profiles.json` - Saved profiles
- `models_cache.json` - Model list cache

## Troubleshooting

### Command not found
```bash
# Check if installed
ls -la ~/.local/bin/deonai

# Check PATH
echo $PATH | grep -o "$HOME/.local/bin"

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Python not found
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

### Permissions
```bash
# Make executable
chmod +x ~/.local/bin/deonai

# Check ownership
ls -la ~/.local/bin/deonai
```

### Missing dependencies
```bash
pip3 install --user requests colorama
```

## Update

```bash
cd deonai-cli
git pull origin main
./install.sh
```

Or use built-in updater:
```bash
deonai --upgrade
```

## Uninstall

```bash
cd deonai-cli
./uninstall.sh
```

Or manually:
```bash
rm ~/.local/bin/deonai
rm -rf ~/.deonai
```

## Performance Tips

### Fast Startup
- Keep history small (use `/clear` occasionally)
- Cache models list (auto-cached for 24h)

### Memory Usage
- Each conversation uses ~1-5MB
- Large code files increase memory usage
- Clear history to reduce memory

## System Integration

### Run from anywhere
```bash
deonai "quick question"
```

### Pipe output
```bash
deonai "list python packages" | grep pandas
```

### Use in scripts
```bash
#!/bin/bash
result=$(deonai "generate random password")
echo "$result"
```

## Privacy & Security

- API key stored in `~/.deonai/config.json` (mode 600)
- Conversations stored locally
- No telemetry or tracking
- All network calls go through OpenRouter only

## Advanced Usage

### Multiple Profiles
```bash
# Save current setup
deonai
You: /profile save work

# Switch profiles
You: /profile load personal
```

### Custom System Prompts
```bash
You: /system
[Choose: Set custom system prompt]
You are a Python expert...
END
```

### Code Execution
```bash
You: /run script.py
You: /init python my-project
```

## Getting Help

- GitHub Issues: https://github.com/4shil/deonai-cli/issues
- Documentation: README.md
- In-app: `deonai /help`

## License

MIT License - Free to use and modify
