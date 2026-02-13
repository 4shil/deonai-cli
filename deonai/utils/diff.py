"""
DeonAi Utils - Diff Engine
"""

import difflib
from typing import Tuple, List
from pathlib import Path
from .colors import Colors, colored


class DiffEngine:
    """Generate and apply diffs for file modifications"""
    
    def generate_diff(
        self,
        original: str,
        modified: str,
        filename: str = "file"
    ) -> str:
        """Generate unified diff"""
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            modified.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm=""
        )
        return "".join(diff)
    
    def preview_diff(self, diff: str, colored_output: bool = True) -> str:
        """Preview diff with colors"""
        if not colored_output:
            return diff
        
        lines = []
        for line in diff.split("\n"):
            if line.startswith("+") and not line.startswith("+++"):
                lines.append(colored(line, Colors.GREEN))
            elif line.startswith("-") and not line.startswith("---"):
                lines.append(colored(line, Colors.RED))
            elif line.startswith("@@"):
                lines.append(colored(line, Colors.CYAN))
            elif line.startswith("+++") or line.startswith("---"):
                lines.append(colored(line, Colors.BLUE, Colors.BOLD))
            else:
                lines.append(line)
        
        return "\n".join(lines)
    
    def apply_patch(self, file_path: Path, patch: str) -> Tuple[bool, str]:
        """
        Apply patch to file using patch command
        Returns (success, message)
        """
        import tempfile
        
        try:
            # Create backup first
            backup = self.create_backup(file_path)
            
            # Write patch to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as f:
                f.write(patch)
                patch_file = f.name
            
            # Apply patch using command
            import subprocess
            result = subprocess.run(
                ["patch", str(file_path), patch_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Clean up temp file
            Path(patch_file).unlink()
            
            if result.returncode == 0:
                return True, f"Patch applied successfully to {file_path.name}"
            else:
                # Restore backup on failure
                self.restore_backup(file_path)
                return False, f"Patch failed: {result.stderr}"
                
        except FileNotFoundError:
            # patch command not available, try manual application
            return self._apply_patch_manual(file_path, patch)
        except Exception as e:
            # Restore backup on any error
            if backup.exists():
                self.restore_backup(file_path)
            return False, f"Error applying patch: {e}"
    
    def _apply_patch_manual(self, file_path: Path, patch: str) -> Tuple[bool, str]:
        """
        Manually apply patch when patch command unavailable
        Simple implementation for basic patches
        """
        try:
            import difflib
            
            # Parse patch
            lines = patch.split('\n')
            
            # Extract file content from patch (simplified)
            # This is a basic implementation - production code would need
            # a proper patch parser like python-patch
            
            original_lines = file_path.read_text().splitlines(keepends=True)
            
            # For now, return not supported
            return False, "Manual patch application not fully implemented. Install 'patch' command."
            
        except Exception as e:
            return False, f"Manual patch failed: {e}"
    
    def create_backup(self, file_path: Path) -> Path:
        """Create backup of file"""
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        if file_path.exists():
            backup_path.write_text(file_path.read_text())
        return backup_path
    
    def restore_backup(self, file_path: Path) -> bool:
        """Restore from backup"""
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        if backup_path.exists():
            file_path.write_text(backup_path.read_text())
            backup_path.unlink()
            return True
        return False
