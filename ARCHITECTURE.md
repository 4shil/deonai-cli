# DeonAi v3.0 Architecture

## Package Structure

```
deonai/
├── __init__.py                 # Main package exports
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── base.py                 # Base classes & exceptions
│   ├── config.py               # Configuration management
│   ├── logger.py               # Logging system
│   ├── context.py              # Context manager (Feature 36)
│   ├── tools.py                # Tool registry
│   ├── agent.py                # Agentic executor (Feature 37)
│   ├── builtin_tools.py        # Core tools (5)
│   ├── git_tools.py            # Git tools (5)
│   └── patch_tools.py          # Patch/diff tools (4)
├── integrations/               # External integrations
│   ├── __init__.py
│   └── git.py                  # Git helper (Feature 38)
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── colors.py               # Terminal colors
│   ├── animations.py           # Loading animations
│   ├── diff.py                 # Diff engine (Feature 39)
│   └── fileops.py              # File operations
├── cli/                        # CLI interface
│   ├── __init__.py
│   └── commands.py             # Command handler
└── plugins/                    # Plugin system (future)
    └── __init__.py
```

## Component Interactions

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface                        │
│                  (commands.py)                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Core System                            │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────┐  │
│  │  Context   │  │   Tools    │  │   Agent Loop    │  │
│  │  Manager   │◄─┤  Registry  │◄─┤   (Executor)    │  │
│  └────────────┘  └────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Tool Layer                             │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────────┐  │
│  │  Core    │ │   Git    │ │    Patch/Diff         │  │
│  │  Tools   │ │  Tools   │ │     Tools             │  │
│  │  (5)     │ │  (5)     │ │     (4)               │  │
│  └──────────┘ └──────────┘ └───────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Integrations & Utils                       │
│  ┌────────────────┐  ┌────────────────────────────┐    │
│  │  Git Helper    │  │  Diff Engine, File Ops     │    │
│  └────────────────┘  └────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Query → AI Response
```
User Input
    ↓
Command Handler (check for /commands)
    ↓
Context Manager (build context)
    ↓
API Call (with tools + context)
    ↓
Agentic Executor (process tool calls)
    ↓
Tool Registry (execute tools)
    ↓
Response to User
```

### 2. Tool Execution Flow
```
AI wants to use tool
    ↓
Agentic Executor detects tool_calls
    ↓
Parse tool calls → ToolCall objects
    ↓
Registry.execute(tool_name, arguments)
    ↓
Tool.execute(**kwargs)
    ↓
Return result to AI
    ↓
AI processes result → next action or final answer
```

### 3. Context Building Flow
```
User query received
    ↓
ContextManager.build_context()
    ↓
1. Detect workspace (git root/markers)
    ↓
2. Get project info (type, language)
    ↓
3. Find relevant files (scoring algorithm)
    ↓
4. Analyze imports (if current file)
    ↓
5. Assemble context (token budget management)
    ↓
Return context string → prepend to conversation
```

## Key Design Patterns

### 1. Decorator Pattern (Tool Registration)
```python
@registry.register("tool_name", "Description")
def my_tool(arg1: str) -> str:
    return "result"
```

### 2. Strategy Pattern (Context Building)
- Different strategies for different languages
- Pluggable file discovery algorithms
- Extensible scoring system

### 3. Template Method (Agentic Loop)
- Base loop structure
- Customizable callbacks
- Extensible tool execution

### 4. Factory Pattern (Tool Creation)
- Tool instances created from decorators
- Parameter schema auto-generation
- Unified tool interface

## Error Handling Strategy

```
User Action
    ↓
Try: Execute operation
    ↓
Catch specific exceptions:
    - ToolError → Tool execution failed
    - ContextError → Context building failed
    - IntegrationError → Git/external failed
    - ConfigError → Configuration invalid
    ↓
Log error (with context)
    ↓
Return user-friendly message
    ↓
Continue operation (don't crash)
```

## Performance Considerations

1. **Context Building:**
   - Token budget management
   - File size limits
   - Lazy loading of imports

2. **Tool Execution:**
   - Timeouts on all external calls
   - Result size limits
   - Concurrent execution (future)

3. **Caching:**
   - Workspace detection cached
   - Project info cached
   - Model list cached (24h)

## Extension Points

1. **New Tools:**
   - Register with decorator
   - Auto-integrated into agentic loop

2. **New Integrations:**
   - Inherit from BaseIntegration
   - Implement is_available() and initialize()

3. **New Commands:**
   - Add to CommandHandler.commands dict
   - Return COMMAND: prefix for special handling

4. **Plugins:**
   - Plugin system structure ready
   - Future: Load external plugins

## Security Considerations

1. **Tool Execution:**
   - run_command has 30s timeout
   - File size limits (100KB reads)
   - Working directory validation

2. **File Operations:**
   - Workspace boundary checks
   - Backup before modifications
   - Restore on failures

3. **Git Operations:**
   - Read-only by default
   - Explicit confirmation for commits
   - No remote operations (push/pull)

## Testing Strategy

1. **Unit Tests:**
   - Core components isolated
   - Mock external dependencies
   - Fast execution

2. **Integration Tests:**
   - Component interactions
   - Real file operations (temp dirs)
   - Git operations (test repos)

3. **Manual Testing:**
   - End-to-end workflows
   - UX validation
   - Error scenarios

---

**Architecture Version:** 3.0  
**Last Updated:** Step 17/18  
**Status:** Production-ready
