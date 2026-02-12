#!/bin/bash
# DeonAi CLI Installer

echo "🌊 Installing DeonAi CLI..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install it first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install --user requests

# Copy script to user bin
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

cp deonai.py "$INSTALL_DIR/deonai"
chmod +x "$INSTALL_DIR/deonai"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  Add this to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo "✅ DeonAi installed!"
echo ""
echo "Run 'deonai --setup' to configure your OpenRouter API key"
echo "Then run 'deonai' to start chatting"
echo ""
echo "Get your API key at: https://openrouter.ai/keys"

