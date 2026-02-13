"""
DeonAi Core - Context Manager
Feature 36: Project-aware context system
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, List
from .base import BaseContext, ContextError
from .logger import logger


class ContextManager(BaseContext):
    """Manages project context and workspace detection"""
    
    # Project markers for detection
    PROJECT_MARKERS = [
        # Version control
        ".git",
        ".hg",
        ".svn",
        # Python
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "requirements.txt",
        "Pipfile",
        "poetry.lock",
        # JavaScript/Node
        "package.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        # Go
        "go.mod",
        "go.sum",
        # Rust
        "Cargo.toml",
        "Cargo.lock",
        # Java
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        # Ruby
        "Gemfile",
        "Rakefile",
        # PHP
        "composer.json",
        # General
        "Makefile",
        "CMakeLists.txt",
        ".editorconfig",
    ]
    
    def __init__(self, cwd: Optional[Path] = None):
        self.cwd = cwd or Path.cwd()
        self.workspace = None
        self.project_info = None
        
        # Auto-detect on init
        try:
            self.workspace = self.detect_workspace()
            self.project_info = self.get_project_info()
            logger.info(f"Detected workspace: {self.workspace}")
            logger.info(f"Project type: {self.project_info.get('type')}")
        except Exception as e:
            logger.warning(f"Could not detect workspace: {e}")
            self.workspace = self.cwd
            self.project_info = {"type": "unknown", "language": None}
    
    def detect_workspace(self) -> Path:
        """
        Detect project workspace root
        Priority: 1) Git root 2) Project markers 3) CWD
        """
        # Try git root first (most reliable)
        git_root = self._find_git_root()
        if git_root:
            return git_root
        
        # Look for project markers
        marker_root = self._find_marker_root()
        if marker_root:
            return marker_root
        
        # Default to current directory
        return self.cwd
    
    def _find_git_root(self) -> Optional[Path]:
        """Find git repository root"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                git_root = Path(result.stdout.strip())
                if git_root.exists():
                    logger.debug(f"Found git root: {git_root}")
                    return git_root
                    
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            logger.debug(f"Git not available: {e}")
        
        return None
    
    def _find_marker_root(self) -> Optional[Path]:
        """Find project root by looking for markers"""
        current = self.cwd
        
        # Walk up directory tree
        while current != current.parent:
            # Check for any project marker
            for marker in self.PROJECT_MARKERS:
                marker_path = current / marker
                if marker_path.exists():
                    logger.debug(f"Found project marker: {marker} in {current}")
                    return current
            
            current = current.parent
        
        return None
    
    def get_project_info(self) -> Dict:
        """
        Extract project metadata
        Returns dict with type, language, files, etc.
        """
        if not self.workspace:
            return {"type": "unknown", "language": None, "root": str(self.cwd)}
        
        info = {
            "root": str(self.workspace),
            "type": "unknown",
            "language": None,
            "features": []
        }
        
        # Detect project type and language
        detections = [
            # Python
            (["pyproject.toml", "setup.py"], "python", "python"),
            (["requirements.txt", "Pipfile"], "python", "python"),
            # JavaScript/TypeScript
            (["package.json"], "nodejs", "javascript"),
            (["tsconfig.json"], "nodejs", "typescript"),
            # Go
            (["go.mod"], "go", "go"),
            # Rust
            (["Cargo.toml"], "rust", "rust"),
            # Java
            (["pom.xml"], "java-maven", "java"),
            (["build.gradle"], "java-gradle", "java"),
            # Ruby
            (["Gemfile"], "ruby", "ruby"),
            # PHP
            (["composer.json"], "php", "php"),
            # C/C++
            (["CMakeLists.txt"], "cmake", "cpp"),
            (["Makefile"], "make", "c"),
        ]
        
        for markers, proj_type, language in detections:
            for marker in markers:
                if (self.workspace / marker).exists():
                    info["type"] = proj_type
                    info["language"] = language
                    info["features"].append(marker)
                    break
            
            if info["type"] != "unknown":
                break
        
        # Check for git
        if (self.workspace / ".git").exists():
            info["features"].append("git")
        
        return info
    
    def get_relevant_files(self, query: str) -> List[Path]:
        """Find files relevant to query (stub - implemented in Step 6)"""
        return []
    
    def build_context(self, query: str, max_tokens: int = 8000) -> str:
        """Build context string (stub - implemented in Step 8)"""
        return f"Project: {self.workspace}\nType: {self.project_info['type']}\n"
    
    def is_in_workspace(self, path: Path) -> bool:
        """Check if path is within workspace"""
        try:
            path.resolve().relative_to(self.workspace.resolve())
            return True
        except ValueError:
            return False
