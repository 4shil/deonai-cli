"""
DeonAi Core - Patch Tool
Safe file modification via diffs
"""

from pathlib import Path
from ..utils import DiffEngine
from .tools import registry
from .logger import logger


# Initialize diff engine
diff_engine = DiffEngine()


@registry.register(
    name="apply_patch",
    description="Apply a patch/diff to a file safely. The patch should be in unified diff format. File is automatically backed up.",
    parameters={
        "type": "object",
        "properties": {
            "file": {
                "type": "string",
                "description": "Path to file to patch"
            },
            "patch": {
                "type": "string",
                "description": "Unified diff patch to apply"
            }
        },
        "required": ["file", "patch"]
    }
)
def apply_patch(file: str, patch: str) -> str:
    """Apply patch to file"""
    try:
        file_path = Path(file)
        
        if not file_path.exists():
            return f"Error: File not found: {file}"
        
        # Apply patch
        success, message = diff_engine.apply_patch(file_path, patch)
        
        if success:
            logger.info(f"Patch applied to {file}")
            return f"✓ {message}"
        else:
            logger.error(f"Patch failed for {file}: {message}")
            return f"✗ {message}"
            
    except Exception as e:
        logger.error(f"apply_patch error: {e}")
        return f"Error: {e}"


@registry.register(
    name="preview_changes",
    description="Generate a diff showing proposed changes between original and modified content. Use this before applying changes to review them.",
    parameters={
        "type": "object",
        "properties": {
            "file": {
                "type": "string",
                "description": "File path (for labeling)"
            },
            "original": {
                "type": "string",
                "description": "Original file content"
            },
            "modified": {
                "type": "string",
                "description": "Modified/proposed content"
            }
        },
        "required": ["file", "original", "modified"]
    }
)
def preview_changes(file: str, original: str, modified: str) -> str:
    """Preview changes as a diff"""
    try:
        # Generate diff
        diff = diff_engine.generate_diff(original, modified, file)
        
        if not diff:
            return "No changes detected"
        
        # Return colored preview
        preview = diff_engine.preview_diff(diff, colored_output=False)
        
        output = f"Proposed changes to {file}:\n\n{preview}"
        output += f"\n\nTo apply: Confirm or use apply_patch tool"
        
        return output
        
    except Exception as e:
        logger.error(f"preview_changes error: {e}")
        return f"Error: {e}"


@registry.register(
    name="create_backup",
    description="Create a backup of a file before modifying it. Returns backup file path.",
    parameters={
        "type": "object",
        "properties": {
            "file": {
                "type": "string",
                "description": "File to backup"
            }
        },
        "required": ["file"]
    }
)
def create_backup_tool(file: str) -> str:
    """Create file backup"""
    try:
        file_path = Path(file)
        
        if not file_path.exists():
            return f"Error: File not found: {file}"
        
        backup_path = diff_engine.create_backup(file_path)
        logger.info(f"Created backup: {backup_path}")
        
        return f"Backup created: {backup_path.name}"
        
    except Exception as e:
        logger.error(f"create_backup error: {e}")
        return f"Error: {e}"


@registry.register(
    name="restore_backup",
    description="Restore a file from its backup (.bak file). Use this to undo changes.",
    parameters={
        "type": "object",
        "properties": {
            "file": {
                "type": "string",
                "description": "File to restore (backup must exist)"
            }
        },
        "required": ["file"]
    }
)
def restore_backup_tool(file: str) -> str:
    """Restore from backup"""
    try:
        file_path = Path(file)
        
        success = diff_engine.restore_backup(file_path)
        
        if success:
            logger.info(f"Restored backup for {file}")
            return f"✓ Restored {file} from backup"
        else:
            return f"✗ No backup found for {file}"
            
    except Exception as e:
        logger.error(f"restore_backup error: {e}")
        return f"Error: {e}"


logger.info("Loaded 4 patch/diff tools")
