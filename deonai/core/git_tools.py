"""
DeonAi Core - Git Tools
Register Git operations as agentic tools
"""

from ..integrations import GitHelper
from .tools import registry
from .logger import logger


# Initialize Git helper
git_helper = GitHelper()


@registry.register(
    name="git_status",
    description="Show git repository status - branch, staged/unstaged changes, untracked files. Use this to check what has changed.",
    parameters={"type": "object", "properties": {}}
)
def git_status() -> str:
    """Get git status"""
    try:
        if not git_helper.is_git_repo():
            return "Not a git repository"
        
        git_helper.initialize()
        status = git_helper.get_status()
        
        output = f"Branch: {status.branch}\n"
        
        if status.ahead:
            output += f"↑ Ahead by {status.ahead} commit(s)\n"
        if status.behind:
            output += f"↓ Behind by {status.behind} commit(s)\n"
        
        output += "\n"
        
        if status.is_clean:
            output += "✓ Working directory clean"
        else:
            if status.staged:
                output += f"Staged files ({len(status.staged)}):\n"
                for f in status.staged[:10]:
                    output += f"  + {f}\n"
                if len(status.staged) > 10:
                    output += f"  ... and {len(status.staged) - 10} more\n"
                output += "\n"
            
            if status.unstaged:
                output += f"Unstaged changes ({len(status.unstaged)}):\n"
                for f in status.unstaged[:10]:
                    output += f"  M {f}\n"
                if len(status.unstaged) > 10:
                    output += f"  ... and {len(status.unstaged) - 10} more\n"
                output += "\n"
            
            if status.untracked:
                output += f"Untracked files ({len(status.untracked)}):\n"
                for f in status.untracked[:10]:
                    output += f"  ? {f}\n"
                if len(status.untracked) > 10:
                    output += f"  ... and {len(status.untracked) - 10} more\n"
        
        return output
        
    except Exception as e:
        logger.error(f"git_status error: {e}")
        return f"Error: {e}"


@registry.register(
    name="git_diff",
    description="Show git diff of changes. Use 'staged=true' to see staged changes, 'staged=false' for unstaged. Specify 'file' to diff a specific file.",
    parameters={
        "type": "object",
        "properties": {
            "staged": {
                "type": "boolean",
                "description": "Show staged changes (true) or unstaged (false)"
            },
            "file": {
                "type": "string",
                "description": "Specific file to diff (optional)"
            }
        }
    }
)
def git_diff(staged: bool = False, file: str = None) -> str:
    """Get git diff"""
    try:
        if not git_helper.is_git_repo():
            return "Not a git repository"
        
        diff = git_helper.get_diff(staged=staged, file=file)
        
        if not diff:
            if staged:
                return "No staged changes"
            else:
                return "No unstaged changes"
        
        # Limit diff size
        if len(diff) > 5000:
            diff = diff[:5000] + "\n\n... (diff truncated, too large)"
        
        return diff
        
    except Exception as e:
        logger.error(f"git_diff error: {e}")
        return f"Error: {e}"


@registry.register(
    name="git_add",
    description="Stage a file for commit. Use this before committing changes.",
    parameters={
        "type": "object",
        "properties": {
            "file": {
                "type": "string",
                "description": "File path to stage"
            }
        },
        "required": ["file"]
    }
)
def git_add(file: str) -> str:
    """Stage a file"""
    try:
        if not git_helper.is_git_repo():
            return "Not a git repository"
        
        success = git_helper.stage_file(file)
        if success:
            return f"Staged: {file}"
        else:
            return f"Failed to stage: {file}"
        
    except Exception as e:
        logger.error(f"git_add error: {e}")
        return f"Error: {e}"


@registry.register(
    name="git_commit",
    description="Create a git commit with staged changes. Provide a clear, descriptive commit message.",
    parameters={
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Commit message describing the changes"
            }
        },
        "required": ["message"]
    }
)
def git_commit(message: str) -> str:
    """Create a commit"""
    try:
        if not git_helper.is_git_repo():
            return "Not a git repository"
        
        success, result = git_helper.commit(message)
        
        if success:
            return f"Committed: {result}\nMessage: {message}"
        else:
            return f"Commit failed: {result}"
        
    except Exception as e:
        logger.error(f"git_commit error: {e}")
        return f"Error: {e}"


@registry.register(
    name="git_log",
    description="Show recent commit history. Use this to see what has been committed recently.",
    parameters={
        "type": "object",
        "properties": {
            "count": {
                "type": "integer",
                "description": "Number of commits to show (default: 10)"
            }
        }
    }
)
def git_log(count: int = 10) -> str:
    """Show commit history"""
    try:
        if not git_helper.is_git_repo():
            return "Not a git repository"
        
        commits = git_helper.get_recent_commits(count)
        
        if not commits:
            return "No commits found"
        
        output = f"Recent commits ({len(commits)}):\n\n"
        
        for commit in commits:
            output += f"{commit['hash']} - {commit['message']}\n"
            output += f"  by {commit['author']}, {commit['time']}\n\n"
        
        return output
        
    except Exception as e:
        logger.error(f"git_log error: {e}")
        return f"Error: {e}"


logger.info(f"Loaded {5} Git tools")
