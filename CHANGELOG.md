# Changelog

All notable changes to DeonAi CLI will be documented in this file.

## [3.0.0] - 2026-02-13

### 🎉 Major Release - World-Class Features

This is a transformative release that elevates DeonAi from a simple chat CLI to a production-grade AI coding assistant with project awareness, autonomous capabilities, and professional-grade tools.

### Added

#### Feature 36: Context Manager 🧠
- **Workspace Detection**: Automatically detects project root (Git, markers)
- **Smart File Discovery**: Intelligent relevance scoring algorithm
- **Import Analysis**: Follows Python and JavaScript imports
- **Context Building**: Token-aware context assembly (8K default)
- Supports: Python, JavaScript, TypeScript, Go, Rust, Java, Ruby, PHP

#### Feature 37: Agentic Tool System 🤖
- **Autonomous Execution**: AI can use tools independently
- **Tool Registry**: Decorator-based tool registration
- **14 Built-in Tools**: read, write, list, run, search, git, patch
- **Multi-step Loops**: Up to 5 iterations per task
- **Callbacks**: UI hooks for tool execution events

#### Feature 38: Git Integration 🔗
- **GitHelper**: Comprehensive Git operations wrapper
- **Status**: Branch, staged, unstaged, untracked files
- **Diff**: View changes (staged/unstaged, per-file)
- **Commit**: Create commits with messages
- **Log**: Recent commit history
- **Commands**: /git status, /git diff, /git log

#### Feature 39: Diff/Patch System 📝
- **DiffEngine**: Generate unified diffs
- **Colored Preview**: Syntax-highlighted diffs
- **Safe Application**: Auto-backup before changes
- **Restore**: Easy undo via backups
- **Preview Tool**: Review changes before applying

### Tools (14 total)

**Core Tools (5):**
- `read_file`: Read file contents (100KB limit)
- `write_file`: Write/create files
- `list_files`: Directory listing with patterns
- `run_command`: Execute shell commands (30s timeout)
- `search_code`: Grep-like code search

**Git Tools (5):**
- `git_status`: Repository status
- `git_diff`: Show changes
- `git_add`: Stage files
- `git_commit`: Create commits
- `git_log`: Commit history

**Patch Tools (4):**
- `apply_patch`: Apply unified diffs safely
- `preview_changes`: Show diff before applying
- `create_backup`: Manual backup
- `restore_backup`: Restore from backup

### Changed

- **Architecture**: Refactored from monolithic to modular (15+ modules)
- **Version**: Bumped to 3.0.0-dev
- **Commands**: Enhanced /help with tool listings
- **Logging**: Comprehensive logging system with daily logs
- **Error Handling**: Custom exception hierarchy

### Infrastructure

- **Modular Structure**: deonai/{core,integrations,utils,cli,plugins}
- **Base Classes**: BaseContext, BaseTool, BaseIntegration
- **Testing**: pytest framework with test coverage
- **Type Hints**: Throughout codebase
- **Documentation**: ARCHITECTURE.md, PROGRESS.md

### Performance

- Token budget management (4 chars = 1 token)
- File size limits (100KB reads, 1MB search)
- Timeouts on all external operations
- Workspace detection caching

### Security

- Automatic backups before file modifications
- Working directory validation
- Command timeout protection
- No remote Git operations

---

## [2.8.0] - 2026-02-12

### Added
- Comprehensive Linux support
- Enhanced installer with OS detection
- Uninstaller script
- LINUX.md documentation

### Fixed
- Missing SYSTEM_PROMPT_FILE constant
- Animation thread hanging
- Corrupted JSON handling
- history.pop() safety checks

---

## [2.7.0] - 2026-02-12

### Added
- Beautiful animations (loading, typing)
- Ocean/cyan color theme
- Slash commands
- Bug fixes (12 bugs fixed)

---

## [2.6.0] - 2026-02-11

### Added
- Custom system prompts
- Persistent AI personality
- System prompt management commands

---

## [2.5.0] - 2026-02-10

### Added
- Slash command prefix (/)
- Cleaner command separation

---

## [2.4.0] - Earlier

### Added
- Colors and ASCII banner
- Auto-update (--upgrade)
- Organized help menu

---

## [2.3.0] - Earlier

### Added
- File operations (read, write, list)
- AI-powered file creation
- Code execution (Python, Node, Bash, Go, Ruby)
- Project scaffolding

---

[3.0.0]: https://github.com/4shil/deonai-cli/compare/v2.8...v3.0.0
[2.8.0]: https://github.com/4shil/deonai-cli/compare/v2.7...v2.8
[2.7.0]: https://github.com/4shil/deonai-cli/compare/v2.6...v2.7
