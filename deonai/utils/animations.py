"""
DeonAi Utils - Animations
"""

import sys
import threading
import time
from .colors import Colors, colored


class LoadingAnimation:
    """Animated loading spinner"""
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None
        # Cool spinner frames
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current_frame = 0
    
    def _animate(self):
        """Animation loop"""
        while self.running:
            frame = self.frames[self.current_frame % len(self.frames)]
            sys.stdout.write(f'\r{colored(frame, Colors.CYAN)} {colored(self.message, Colors.DIM)}...')
            sys.stdout.flush()
            self.current_frame += 1
            time.sleep(0.08)
    
    def start(self):
        """Start the animation"""
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the animation"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 20) + '\r')
        sys.stdout.flush()


class TypingAnimation:
    """Animated typing indicator for AI responses"""
    def __init__(self):
        self.running = False
        self.thread = None
        self.dots = 0
    
    def _animate(self):
        """Animation loop"""
        while self.running:
            dots = '.' * (self.dots % 4)
            sys.stdout.write(f'\r{colored("DeonAi:", Colors.MAGENTA, Colors.BOLD)} {colored("thinking", Colors.DIM)}{dots}   ')
            sys.stdout.flush()
            self.dots += 1
            time.sleep(0.3)
    
    def start(self):
        """Start the animation"""
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the animation"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()
