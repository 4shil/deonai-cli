"""
Tests for Diff Engine
"""

from pathlib import Path
import tempfile
from deonai.utils import DiffEngine


def test_diff_engine_init():
    """Test diff engine creation"""
    engine = DiffEngine()
    assert engine is not None


def test_generate_diff():
    """Test diff generation"""
    engine = DiffEngine()
    
    original = "line 1\nline 2\nline 3\n"
    modified = "line 1\nline 2 modified\nline 3\nline 4\n"
    
    diff = engine.generate_diff(original, modified, "test.txt")
    
    assert diff
    assert "-line 2" in diff or "line 2" in diff
    assert "+line 2 modified" in diff or "modified" in diff


def test_preview_diff():
    """Test colored diff preview"""
    engine = DiffEngine()
    
    diff = """--- a/test.txt
+++ b/test.txt
@@ -1,3 +1,4 @@
 line 1
-line 2
+line 2 modified
 line 3
+line 4
"""
    
    preview = engine.preview_diff(diff, colored_output=False)
    assert preview == diff
    
    # Test colored output
    colored_preview = engine.preview_diff(diff, colored_output=True)
    assert colored_preview  # Just check it doesn't crash


def test_backup_restore():
    """Test file backup and restore"""
    engine = DiffEngine()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("original content")
        test_file = Path(f.name)
    
    try:
        # Create backup
        backup = engine.create_backup(test_file)
        assert backup.exists()
        assert backup.read_text() == "original content"
        
        # Modify file
        test_file.write_text("modified content")
        
        # Restore
        success = engine.restore_backup(test_file)
        assert success
        assert test_file.read_text() == "original content"
        assert not backup.exists()  # Backup should be deleted after restore
        
    finally:
        test_file.unlink()
        if backup.exists():
            backup.unlink()
