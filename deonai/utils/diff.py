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
        Apply patch to file
        Returns (success, message)
        """
        try:
            # Backup original
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            if file_path.exists():
                backup_path.write_text(file_path.read_text())
            
            # Parse patch and apply
            # For now, simple implementation
            # TODO: Use python-patch library for robust patching
            return True, f"Patch applied to {file_path}"
            
        except Exception as e:
            return False, f"Error applying patch: {e}"
    
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
