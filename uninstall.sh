#!/bin/bash
# DeonAi CLI Uninstaller for Linux

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║            DeonAi CLI - Uninstaller                      ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_banner

echo ""
echo -e "${YELLOW}This will remove:${NC}"
echo "  • DeonAi executable (~/.local/bin/deonai)"
echo "  • Configuration files (~/.deonai/)"
echo "  • Desktop entry (if exists)"
echo ""

read -p "Continue with uninstallation? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled"
    exit 0
fi

# Remove executable
if [ -f "$HOME/.local/bin/deonai" ]; then
    rm "$HOME/.local/bin/deonai"
    print_success "Removed executable"
fi

# Ask about config
echo ""
read -p "Remove configuration and history? (y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "$HOME/.deonai" ]; then
        rm -rf "$HOME/.deonai"
        print_success "Removed configuration"
    fi
fi

# Remove desktop entry
if [ -f "$HOME/.local/share/applications/deonai.desktop" ]; then
    rm "$HOME/.local/share/applications/deonai.desktop"
    print_success "Removed desktop entry"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Uninstall Complete! ✓                       ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Python packages (requests, colorama) were NOT removed"
echo "You can remove them with: pip3 uninstall requests colorama"
echo ""
