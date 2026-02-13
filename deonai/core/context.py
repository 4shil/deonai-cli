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
    
    def get_relevant_files(
        self,
        query: str,
        max_files: int = 10,
        include_patterns: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Find files relevant to query using intelligent scoring
        
        Args:
            query: Search query
            max_files: Maximum files to return
            include_patterns: File patterns to include (e.g. ['*.py'])
        
        Returns:
            List of relevant file paths, sorted by relevance
        """
        # Default patterns based on project language
        if not include_patterns:
            include_patterns = self._get_default_patterns()
        
        # Collect all matching files
        all_files = []
        for pattern in include_patterns:
            all_files.extend(self.workspace.rglob(pattern))
        
        # Filter out excluded directories
        filtered_files = self._filter_excluded(all_files)
        
        # Score and sort by relevance
        scored_files = self._score_files(filtered_files, query)
        
        # Return top N
        return [path for _, path in scored_files[:max_files]]
    
    def _get_default_patterns(self) -> List[str]:
        """Get file patterns based on project language"""
        language = self.project_info.get("language")
        
        patterns_map = {
            "python": ["*.py"],
            "javascript": ["*.js", "*.jsx", "*.mjs"],
            "typescript": ["*.ts", "*.tsx"],
            "go": ["*.go"],
            "rust": ["*.rs"],
            "java": ["*.java"],
            "ruby": ["*.rb"],
            "php": ["*.php"],
            "c": ["*.c", "*.h"],
            "cpp": ["*.cpp", "*.cc", "*.cxx", "*.hpp", "*.hxx"],
        }
        
        # Get patterns for detected language
        patterns = patterns_map.get(language, [])
        
        # Add common config files
        patterns.extend(["*.md", "*.txt", "*.json", "*.yaml", "*.yml"])
        
        return patterns if patterns else ["*.*"]
    
    def _filter_excluded(self, files: List[Path]) -> List[Path]:
        """Filter out files in excluded directories"""
        excluded_dirs = {
            "node_modules",
            "__pycache__",
            ".git",
            ".hg",
            ".svn",
            "venv",
            "env",
            ".venv",
            ".env",
            "build",
            "dist",
            "target",
            ".next",
            ".nuxt",
            "vendor",
            ".idea",
            ".vscode",
            "__pypackages__",
            ".pytest_cache",
            ".mypy_cache",
            ".tox",
            "coverage",
            ".coverage",
        }
        
        filtered = []
        for file in files:
            # Check if any part of path is in excluded
            if not any(excluded in file.parts for excluded in excluded_dirs):
                filtered.append(file)
        
        return filtered
    
    def _score_files(self, files: List[Path], query: str) -> List[tuple]:
        """
        Score files by relevance to query
        Returns list of (score, path) tuples sorted by score desc
        """
        query_lower = query.lower()
        query_words = query_lower.split()
        
        scored = []
        
        for file in files:
            if not file.is_file():
                continue
            
            score = 0
            name_lower = file.name.lower()
            path_str = str(file).lower()
            
            # Exact filename match
            if query_lower == name_lower:
                score += 100
            
            # Filename contains query
            if query_lower in name_lower:
                score += 50
            
            # Path contains query
            if query_lower in path_str:
                score += 20
            
            # Word matches in filename
            for word in query_words:
                if word in name_lower:
                    score += 10
            
            # Prefer shorter paths (closer to root)
            relative_path = file.relative_to(self.workspace)
            depth_penalty = len(relative_path.parts) * 2
            score -= depth_penalty
            
            # Prefer recently modified (if accessible)
            try:
                mtime = file.stat().st_mtime
                # Normalize to 0-10 range (rough heuristic)
                import time
                age_days = (time.time() - mtime) / 86400
                if age_days < 7:
                    score += 5
                elif age_days < 30:
                    score += 2
            except:
                pass
            
            # Only include files with positive score
            if score > 0:
                scored.append((score, file))
        
        # Sort by score descending
        scored.sort(reverse=True, key=lambda x: x[0])
        
        return scored
    
    def analyze_imports(self, file: Path) -> List[Path]:
        """
        Analyze file imports and find related files
        Supports Python and JavaScript/TypeScript
        """
        if not file.exists() or not file.is_file():
            return []
        
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            language = self._detect_file_language(file)
            
            if language == 'python':
                return self._analyze_python_imports(file, content)
            elif language in ['javascript', 'typescript']:
                return self._analyze_js_imports(file, content)
            
            return []
            
        except Exception as e:
            logger.debug(f"Error analyzing imports in {file}: {e}")
            return []
    
    def _detect_file_language(self, file: Path) -> Optional[str]:
        """Detect language from file extension"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.mjs': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
        }
        return ext_map.get(file.suffix.lower())
    
    def build_context(self, query: str, max_tokens: int = 8000) -> str:
        """Build context string (stub - implemented in Step 8)"""
        return f"Project: {self.workspace}\nType: {self.project_info['type']}\n"
    
    def _analyze_python_imports(self, file: Path, content: str) -> List[Path]:
        """Analyze Python imports"""
        import re
        
        imports = []
        
        # Match: import x, from x import y, from .x import y
        patterns = [
            r'^import\s+([a-zA-Z_][a-zA-Z0-9_\.]*)',
            r'^from\s+([a-zA-Z_\.][a-zA-Z0-9_\.]*)\s+import',
        ]
        
        for line in content.split('\n'):
            line = line.strip()
            
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    module = match.group(1)
                    
                    # Convert module.name to path
                    if module.startswith('.'):
                        # Relative import
                        parts = module.lstrip('.').split('.')
                        import_path = file.parent
                        for part in parts:
                            if part:
                                import_path = import_path / part
                    else:
                        # Absolute import (relative to workspace)
                        parts = module.split('.')
                        import_path = self.workspace / '/'.join(parts)
                    
                    # Try common extensions
                    for ext in ['.py', '/__init__.py']:
                        test_path = Path(str(import_path) + ext)
                        if test_path.exists() and self.is_in_workspace(test_path):
                            imports.append(test_path)
                            break
        
        return imports
    
    def _analyze_js_imports(self, file: Path, content: str) -> List[Path]:
        """Analyze JavaScript/TypeScript imports"""
        import re
        
        imports = []
        
        # Match: import x from 'y', import 'y', require('y')
        patterns = [
            r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)',
        ]
        
        for line in content.split('\n'):
            line = line.strip()
            
            for pattern in patterns:
                matches = re.findall(pattern, line)
                for module in matches:
                    # Only process relative imports
                    if module.startswith('.'):
                        import_path = file.parent / module
                        
                        # Normalize path
                        try:
                            import_path = import_path.resolve()
                        except:
                            continue
                        
                        # Try common extensions
                        for ext in ['', '.js', '.jsx', '.ts', '.tsx', '/index.js', '/index.ts']:
                            test_path = Path(str(import_path) + ext)
                            if test_path.exists() and self.is_in_workspace(test_path):
                                imports.append(test_path)
                                break
        
        return imports
    
    def is_in_workspace(self, path: Path) -> bool:
        """Check if path is within workspace"""
        try:
            path.resolve().relative_to(self.workspace.resolve())
            return True
        except ValueError:
            return False
