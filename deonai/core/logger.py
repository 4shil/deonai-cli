"""
DeonAi Core - Logging System
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from ..utils import Colors, colored

# Create logs directory
LOGS_DIR = Path.home() / ".deonai" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Log file with date
LOG_FILE = LOGS_DIR / f"deonai_{datetime.now().strftime('%Y%m%d')}.log"


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    FORMATS = {
        logging.DEBUG: f"{Colors.DIM}%(levelname)s{Colors.RESET} - %(message)s",
        logging.INFO: f"{Colors.CYAN}%(levelname)s{Colors.RESET} - %(message)s",
        logging.WARNING: f"{Colors.YELLOW}%(levelname)s{Colors.RESET} - %(message)s",
        logging.ERROR: f"{Colors.RED}%(levelname)s{Colors.RESET} - %(message)s",
        logging.CRITICAL: f"{Colors.RED}{Colors.BOLD}%(levelname)s{Colors.RESET} - %(message)s",
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "%(levelname)s - %(message)s")
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger(name: str = "deonai", level: int = logging.INFO) -> logging.Logger:
    """Setup logger with file and console handlers"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (errors only)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_logger()
