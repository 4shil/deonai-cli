"""
DeonAi Utils - Colors and styling
"""

import sys

class Colors:
    """Terminal color codes"""
    # Enhanced color palette - Modern theme
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    
    # Additional colors
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_MAGENTA = '\033[95m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    
    # Reset
    RESET = '\033[0m'
    
    @staticmethod
    def disable():
        """Disable colors (for Windows compatibility)"""
        Colors.CYAN = ''
        Colors.BLUE = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.MAGENTA = ''
        Colors.WHITE = ''
        Colors.BRIGHT_CYAN = ''
        Colors.BRIGHT_GREEN = ''
        Colors.BRIGHT_YELLOW = ''
        Colors.BRIGHT_MAGENTA = ''
        Colors.BOLD = ''
        Colors.DIM = ''
        Colors.UNDERLINE = ''
        Colors.BLINK = ''
        Colors.RESET = ''

# Enable colors on Windows
if sys.platform == 'win32':
    try:
        import colorama
        colorama.init()
    except ImportError:
        Colors.disable()


def colored(text, color='', style=''):
    """Apply color and style to text"""
    return f"{style}{color}{text}{Colors.RESET}"


# DeonAi branding with beautiful ASCII art
DEONAI_BANNER = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     ██████╗ ███████╗ ██████╗ ███╗   ██╗ █████╗ ██╗          ║
    ║     ██╔══██╗██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║          ║
    ║     ██║  ██║█████╗  ██║   ██║██╔██╗ ██║███████║██║          ║
    ║     ██║  ██║██╔══╝  ██║   ██║██║╚██╗██║██╔══██║██║          ║
    ║     ██████╔╝███████╗╚██████╔╝██║ ╚████║██║  ██║██║          ║
    ║     ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝          ║
    ║                                                               ║
    ║           {Colors.BRIGHT_MAGENTA}✨ Your AI Coding Assistant ✨{Colors.CYAN}                  ║
    ║                  {Colors.DIM}v3.0-dev • Powered by OpenRouter{Colors.RESET}{Colors.CYAN}             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
    {Colors.DIM}💡 Tip: Use {Colors.GREEN}/help{Colors.DIM} for commands • Start chatting naturally!{Colors.RESET}
"""
