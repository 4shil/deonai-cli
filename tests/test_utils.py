"""
Tests for DeonAi Utils
"""

from deonai.utils import Colors, colored, LoadingAnimation, TypingAnimation


def test_colors():
    """Test color codes"""
    assert Colors.CYAN != ''
    assert Colors.RED != ''
    assert Colors.GREEN != ''
    assert Colors.RESET != ''


def test_colored():
    """Test colored text function"""
    text = colored("Hello", Colors.CYAN, Colors.BOLD)
    assert "Hello" in text
    assert Colors.RESET in text


def test_loading_animation():
    """Test loading animation creation"""
    anim = LoadingAnimation("Testing")
    assert anim.message == "Testing"
    assert not anim.running
    
    # Test start/stop doesn't crash
    anim.start()
    anim.stop()


def test_typing_animation():
    """Test typing animation creation"""
    anim = TypingAnimation()
    assert not anim.running
    
    # Test start/stop doesn't crash
    anim.start()
    anim.stop()
