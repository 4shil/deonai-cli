# DeonAi CLI - Linux Installation & Troubleshooting

## 🐧 Supported Distributions

DeonAi CLI is tested and works on:
- **Ubuntu** 20.04, 22.04, 24.04
- **Debian** 11, 12
- **Arch Linux** (and Manjaro)
- **Fedora** 38+
- **openSUSE**
- Most other Linux distributions with Python 3.8+

---

## 📦 Installation

### Quick Install (All Distributions)

```bash
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
./install.sh
```

The installer will:
1. Detect your distribution
2. Check Python version
3. Install dependencies
4. Set up the `deonai` command
5. Configure your PATH

---

## 🔧 Manual Installation

### Arch Linux / Manjaro

```bash
# Install dependencies via pacman (recommended)
sudo pacman -S python python-pip python-requests python-pygments

# Or install everything via pip
pip install --user -r requirements.txt

# Make executable and add to PATH
chmod +x deonai.py
mkdir -p ~/.local/bin
cp deonai.py ~/.local/bin/deonai

# Add to PATH (add this to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

### Ubuntu / Debian

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip
pip3 install --user -r requirements.txt

# Install
chmod +x deonai.py
mkdir -p ~/.local/bin
cp deonai.py ~/.local/bin/deonai
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Fedora / RHEL

```bash
# Install dependencies
sudo dnf install python3 python3-pip
pip3 install --user -r requirements.txt

# Install
chmod +x deonai.py
mkdir -p ~/.local/bin
cp deonai.py ~/.local/bin/deonai
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## ⚙️ Configuration

### First Run Setup

```bash
deonai --setup
```

This will:
1. Ask for your OpenRouter API key (get one at https://openrouter.ai/keys)
2. Let you choose a model
3. Save config to `~/.deonai/config.json`

### Config Location

All DeonAi files are stored in `~/.deonai/`:
```
~/.deonai/
├── config.json              # API key & model
├── history.json             # Conversation history
├── stats.json               # Usage statistics
├── system_prompt.txt        # Custom system prompt (optional)
└── .deonai_readline_history # Command history
```

---

## 🐛 Troubleshooting

### "deonai: command not found"

**Solution 1: Check PATH**
```bash
echo $PATH | grep ".local/bin"
```
If not found, add to your shell config:
```bash
# For bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For fish
set -Ua fish_user_paths ~/.local/bin
```

**Solution 2: Run directly**
```bash
python3 ~/path/to/deonai.py
```

### "readline not available" Warning

This is **not critical** - the CLI will work, but command history (↑/↓ arrows) won't work.

**Fix:**
```bash
# Most distributions already have readline
pip3 install --user gnureadline  # Alternative implementation
```

### "pygments not found" - No Syntax Highlighting

**Arch Linux:**
```bash
sudo pacman -S python-pygments
```

**Other distros:**
```bash
pip3 install --user pygments
```

### Permission Errors with Config Directory

```bash
# Fix permissions
mkdir -p ~/.deonai
chmod 755 ~/.deonai
```

### "Cannot connect to OpenRouter API"

1. Check internet connection
2. Verify API key: `deonai --setup`
3. Test with curl:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://openrouter.ai/api/v1/models
```

### Colors Not Working

Some terminals don't support ANSI colors. DeonAi detects this automatically, but you can force:

```bash
# Force colors
export TERM=xterm-256color

# Disable colors
export TERM=dumb
```

### Python Version Issues

DeonAi requires Python 3.8+. Check version:
```bash
python3 --version
```

If too old, install newer Python:
```bash
# Ubuntu/Debian
sudo apt install python3.11

# Arch
sudo pacman -S python

# Fedora
sudo dnf install python3.11
```

---

## 🚀 Arch Linux Specific Tips

### Using AUR (Future)

If you want to create an AUR package:
```bash
# Create PKGBUILD
pkgname=deonai-cli
pkgver=3.0
pkgrel=1
pkgdesc="AI coding assistant for terminal"
arch=('any')
url="https://github.com/4shil/deonai-cli"
license=('MIT')
depends=('python' 'python-requests' 'python-pygments')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
```

### Pacman vs Pip

For Arch users, it's recommended to use pacman for system packages:
```bash
sudo pacman -S python-requests python-pygments
```
This ensures packages are managed by the package manager.

---

## 🔄 Updating

```bash
cd ~/deonai-cli
git pull origin main
./install.sh  # Or just run: deonai (it will use the new version)
```

---

## 📊 Performance on Linux

DeonAi runs fast on Linux:
- Startup time: < 0.5s
- Memory usage: ~30-50 MB
- CPU usage: Minimal (unless streaming)

---

## 🔐 Security

- API keys stored in `~/.deonai/config.json` (mode 0600)
- No data sent to third parties (except OpenRouter API)
- History stored locally only
- Open source - audit the code yourself!

---

## 🆘 Getting Help

1. Check this guide first
2. GitHub Issues: https://github.com/4shil/deonai-cli/issues
3. Run with debug mode: `python3 -v deonai.py` for detailed errors

---

## 📝 Example Commands

```bash
# Setup
deonai --setup

# Start chatting
deonai

# View statistics
deonai  # then type: /stats

# Switch model
deonai  # then type: /switch

# Update
cd ~/deonai-cli && git pull
```

---

**Made with ❤️ for Linux users**
