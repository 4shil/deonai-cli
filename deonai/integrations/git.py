"""
DeonAi Integrations - Git Helper
Feature 38: Git integration
"""

import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from ..core.base import BaseIntegration, IntegrationError
from ..core.logger import logger


@dataclass
class GitStatus:
    """Git repository status"""
    branch: str
    is_clean: bool
    staged: List[str]
    unstaged: List[str]
    untracked: List[str]
    ahead: int = 0
    behind: int = 0


class GitHelper(BaseIntegration):
    """Git repository integration"""
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
        self._is_repo = None
        self._git_root = None
    
    def is_available(self) -> bool:
        """Check if git is installed and available"""
        try:
            subprocess.run(
                ["git", "--version"],
                capture_output=True,
                timeout=2,
                check=True
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def initialize(self) -> bool:
        """Initialize git integration"""
        if not self.is_available():
            logger.warning("Git not available")
            return False
        
        if self.is_git_repo():
            self._git_root = self._find_git_root()
            logger.info(f"Git repository detected: {self._git_root}")
            return True
        
        return False
    
    def is_git_repo(self) -> bool:
        """Check if current directory is in a git repo"""
        if self._is_repo is not None:
            return self._is_repo
        
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=2
            )
            self._is_repo = result.returncode == 0
            return self._is_repo
        except (subprocess.SubprocessError, FileNotFoundError):
            self._is_repo = False
            return False
    
    def _find_git_root(self) -> Optional[Path]:
        """Find git repository root"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            return Path(result.stdout.strip())
        except (subprocess.SubprocessError, FileNotFoundError):
            return None
    
    def get_current_branch(self) -> Optional[str]:
        """Get current git branch name"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            return result.stdout.strip()
        except subprocess.SubprocessError:
            return None
    
    def get_status(self) -> GitStatus:
        """Get detailed git status"""
        try:
            # Get branch
            branch = self.get_current_branch() or "detached"
            
            # Get status
            result = subprocess.run(
                ["git", "status", "--porcelain", "--branch"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            
            lines = result.stdout.strip().split("\n")
            
            staged = []
            unstaged = []
            untracked = []
            ahead = 0
            behind = 0
            
            for line in lines:
                if line.startswith("##"):
                    # Branch info line
                    if "ahead" in line:
                        ahead = int(line.split("ahead ")[1].split("]")[0].split(",")[0])
                    if "behind" in line:
                        behind = int(line.split("behind ")[1].split("]")[0].split(",")[0])
                    continue
                
                if not line:
                    continue
                
                status_code = line[:2]
                filename = line[3:]
                
                # Staged changes
                if status_code[0] != " " and status_code[0] != "?":
                    staged.append(filename)
                
                # Unstaged changes
                if status_code[1] != " " and status_code[1] != "?":
                    unstaged.append(filename)
                
                # Untracked files
                if status_code == "??":
                    untracked.append(filename)
            
            is_clean = not (staged or unstaged or untracked)
            
            return GitStatus(
                branch=branch,
                is_clean=is_clean,
                staged=staged,
                unstaged=unstaged,
                untracked=untracked,
                ahead=ahead,
                behind=behind
            )
            
        except subprocess.SubprocessError as e:
            raise IntegrationError(f"Git status failed: {e}")
    
    def get_diff(self, staged: bool = False, file: Optional[str] = None) -> str:
        """
        Get git diff
        
        Args:
            staged: Show staged changes (--cached)
            file: Specific file to diff
        
        Returns:
            Diff output
        """
        try:
            cmd = ["git", "diff"]
            
            if staged:
                cmd.append("--cached")
            
            if file:
                cmd.append(file)
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
            
            return result.stdout
            
        except subprocess.SubprocessError as e:
            raise IntegrationError(f"Git diff failed: {e}")
    
    def stage_file(self, filepath: str) -> bool:
        """Stage a file for commit"""
        try:
            subprocess.run(
                ["git", "add", filepath],
                cwd=self.repo_path,
                capture_output=True,
                timeout=5,
                check=True
            )
            logger.info(f"Staged file: {filepath}")
            return True
        except subprocess.SubprocessError as e:
            logger.error(f"Failed to stage {filepath}: {e}")
            return False
    
    def unstage_file(self, filepath: str) -> bool:
        """Unstage a file"""
        try:
            subprocess.run(
                ["git", "reset", "HEAD", filepath],
                cwd=self.repo_path,
                capture_output=True,
                timeout=5,
                check=True
            )
            logger.info(f"Unstaged file: {filepath}")
            return True
        except subprocess.SubprocessError as e:
            logger.error(f"Failed to unstage {filepath}: {e}")
            return False
    
    def commit(self, message: str) -> Tuple[bool, str]:
        """
        Create a commit
        
        Returns:
            (success, commit_hash_or_error)
        """
        try:
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
            
            # Extract commit hash
            output = result.stdout
            if "nothing to commit" in output.lower():
                return False, "Nothing to commit"
            
            # Get last commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            commit_hash = hash_result.stdout.strip()[:7]
            
            logger.info(f"Created commit: {commit_hash}")
            return True, commit_hash
            
        except subprocess.SubprocessError as e:
            logger.error(f"Commit failed: {e}")
            return False, str(e)
    
    def get_recent_commits(self, count: int = 10) -> List[Dict[str, str]]:
        """Get recent commit history"""
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--pretty=format:%h|%an|%ar|%s"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            
            commits = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                
                parts = line.split("|", 3)
                if len(parts) == 4:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "time": parts[2],
                        "message": parts[3]
                    })
            
            return commits
            
        except subprocess.SubprocessError:
            return []
