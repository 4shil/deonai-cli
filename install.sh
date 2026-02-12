#!/bin/bash
# DeonAi CLI Installer for Linux
# Supports: Ubuntu, Debian, Fedora, Arch, and other distributions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║              DeonAi CLI - Linux Installer                ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        OS_VERSION=$VERSION_ID
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$DISTRIB_ID
        OS_VERSION=$DISTRIB_RELEASE
    else
        OS=$(uname -s)
    fi
    
    print_info "Detected OS: $OS"
}

# Check Python
check_python() {
    print_info "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
        return 0
    else
        print_error "Python 3 not found"
        echo ""
        echo "Install Python 3 with:"
        case $OS in
            ubuntu|debian)
                echo "  sudo apt update && sudo apt install python3 python3-pip"
                ;;
            fedora|rhel|centos)
                echo "  sudo dnf install python3 python3-pip"
                ;;
            arch)
                echo "  sudo pacman -S python python-pip"
                ;;
            *)
                echo "  Please install Python 3 for your distribution"
                ;;
        esac
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."
    
    # Try pip3 first, then pip
    if command -v pip3 &> /dev/null; then
        pip3 install --user requests colorama 2>&1 | grep -v "already satisfied" || true
    elif command -v pip &> /dev/null; then
        pip install --user requests colorama 2>&1 | grep -v "already satisfied" || true
    else
        print_error "pip not found. Install it first:"
        echo "  curl https://bootstrap.pypa.io/get-pip.py | python3"
        exit 1
    fi
    
    print_success "Dependencies installed"
}

# Install DeonAi
install_deonai() {
    print_info "Installing DeonAi CLI..."
    
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    
    # Copy and make executable
    cp deonai.py "$INSTALL_DIR/deonai"
    chmod +x "$INSTALL_DIR/deonai"
    
    # Create symlink if needed
    if [ ! -f "$INSTALL_DIR/deonai" ]; then
        print_error "Installation failed"
        exit 1
    fi
    
    print_success "DeonAi installed to $INSTALL_DIR/deonai"
}

# Check PATH
check_path() {
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        print_warning "~/.local/bin is not in your PATH"
        echo ""
        echo "Add this line to your shell config:"
        
        # Detect shell
        if [ -n "$BASH_VERSION" ]; then
            SHELL_CONFIG="~/.bashrc"
        elif [ -n "$ZSH_VERSION" ]; then
            SHELL_CONFIG="~/.zshrc"
        else
            SHELL_CONFIG="~/.profile"
        fi
        
        echo -e "${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
        echo ""
        echo "Add to: $SHELL_CONFIG"
        echo ""
        
        read -p "Add to PATH automatically? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/${SHELL_CONFIG#~/}"
            print_success "Added to $SHELL_CONFIG"
            print_info "Restart your terminal or run: source $SHELL_CONFIG"
        fi
    else
        print_success "PATH is configured correctly"
    fi
}

# Create desktop entry (optional)
create_desktop_entry() {
    if [ -d "$HOME/.local/share/applications" ]; then
        read -p "Create desktop shortcut? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cat > "$HOME/.local/share/applications/deonai.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=DeonAi CLI
Comment=AI Coding Assistant in Terminal
Exec=x-terminal-emulator -e deonai
Icon=utilities-terminal
Terminal=true
Categories=Development;Utility;
Keywords=ai;assistant;terminal;
EOF
            print_success "Desktop entry created"
        fi
    fi
}

# Main installation
main() {
    print_banner
    
    detect_os
    check_python
    install_dependencies
    install_deonai
    check_path
    create_desktop_entry
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                Installation Complete! ✓                  ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo "  1. Run: ${GREEN}deonai --setup${NC}  (configure API key)"
    echo "  2. Run: ${GREEN}deonai${NC}  (start chatting)"
    echo ""
    echo "Get your API key: ${CYAN}https://openrouter.ai/keys${NC}"
    echo ""
    echo "Documentation: ${CYAN}https://github.com/4shil/deonai-cli${NC}"
    echo ""
}

# Run installer
main
