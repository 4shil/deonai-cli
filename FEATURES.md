# DeonAi CLI - Advanced Features

## 🧠 Memory & Knowledge Management

### Persistent Notes
Save important context as notes that persist across sessions:
```bash
/note project-requirements   # Saves last 4 messages as a note
/notes                       # List all saved notes
```

### Long-term Memory
Add entries to your permanent memory file:
```bash
/memory User prefers Python 3.11 and FastAPI
/memory                      # View all memory entries
```

### Smart Recall
Search through all your notes and memory:
```bash
/recall fastapi              # Find all mentions of "fastapi"
```

**Storage**: `~/.deonai/memory.md` and `~/.deonai/notes/*.md`

---

## ⚙️ Customizable Settings

Configure AI behavior and performance:
```bash
/settings                    # View current settings
/set temperature 0.9         # More creative responses
/set max_tokens 8192         # Longer responses
/set streaming true          # Enable/disable streaming
/set context_limit 100       # How many messages to keep
```

**Default Settings**:
- `temperature`: 0.7 (balanced)
- `max_tokens`: 4096
- `streaming`: true
- `auto_save`: true
- `context_limit`: 50

**Storage**: `~/.deonai/settings.json`

---

## 💾 Session Management

Save and restore entire conversations:

```bash
# Save current session
/save project-work

# List all saved sessions
/sessions

# Load a previous session
/load project-work
```

Each session includes:
- Full conversation history
- Model used
- Timestamp
- Message count

**Storage**: `~/.deonai/sessions/*.json`

---

## 🔀 Conversation Branching

Explore different paths in your conversation:

```bash
# Fork from current point
/fork

# Fork from a specific message
/fork 5

# Original is auto-saved as "before_fork_TIMESTAMP"
```

Use cases:
- Try different approaches to the same problem
- Test different prompts
- Explore alternative solutions
- Experiment without losing progress

---

## 📊 Smart Context Management

DeonAi automatically manages conversation memory:

**Auto-trimming**:
- Keeps last 50 messages by default (configurable)
- Trims to 30 when limit reached
- Preserves conversation flow
- Saves tokens and reduces costs

**Manual control**:
```bash
/set context_limit 100       # Increase limit
/set auto_save false         # Disable auto-save
```

---

## 💰 Cost Tracking

Monitor your usage and expenses:

```bash
/status                      # View session costs
/stats                       # View all-time statistics
```

**Tracks**:
- Tokens used (session & total)
- Estimated cost per session
- Model-specific pricing
- Message count
- Sessions count

**Pricing** (per 1M tokens, estimated):
- Claude Sonnet: $3.00
- Claude Opus: $15.00
- GPT-4: $30.00
- Gemini: Free
- Llama: $0.20

---

## 📈 Usage Statistics

Track your AI assistant usage over time:

```bash
/stats
```

**Shows**:
- Total messages sent
- Total tokens used
- Sessions count
- Files created
- First use date
- Top 5 models used

**Storage**: `~/.deonai/stats.json`

---

## 🎨 Comparison with OpenClaw

| Feature | DeonAi CLI | OpenClaw |
|---------|-----------|----------|
| **Memory Notes** | ✅ Markdown files | ✅ Database |
| **Sessions** | ✅ JSON files | ✅ SQLite |
| **Branching** | ✅ /fork command | ✅ UI-based |
| **Settings** | ✅ JSON config | ✅ Web UI |
| **Cost Tracking** | ✅ Estimated | ✅ Exact |
| **Search** | ✅ /recall | ✅ Full-text |
| **Size** | 🎯 ~100KB | 📦 ~50MB+ |
| **Speed** | ⚡ Instant | 🐢 2-3s startup |
| **Dependencies** | 📦 Minimal | 📦 Heavy |

---

## 🚀 Lightweight Philosophy

DeonAi stays lightweight while adding power:

**Before enhancements**:
- 1 file (deonai.py)
- 2 dependencies (requests, colorama)
- ~50KB script

**After enhancements**:
- Still 1 file
- +1 dependency (pygments - optional)
- ~70KB script
- Memory: <50MB RAM
- Startup: <0.5s

**Why it matters**:
- Fast even on slow machines
- Works over SSH
- No heavy frameworks
- Pure Python
- Easy to audit
- Portable (single file)

---

## 🎯 Best Practices

### Memory Management
- Use `/memory` for facts and preferences
- Use `/note` for conversation contexts
- Review notes weekly: `/notes`
- Search when needed: `/recall`

### Session Organization
- Save important conversations: `/save <descriptive-name>`
- Fork before experiments: `/fork`
- Clean up old sessions periodically

### Cost Optimization
- Lower temperature (0.5-0.7) for factual work
- Use free models (Gemini) for simple tasks
- Reduce context_limit for simple conversations
- Check costs: `/status`

### Performance
- Enable streaming for faster responses
- Trim old messages with lower context_limit
- Use /fork instead of starting new conversations

---

## 📂 File Structure

```
~/.deonai/
├── config.json                    # API key & model
├── settings.json                  # User preferences
├── history.json                   # Current conversation
├── stats.json                     # Usage statistics
├── memory.md                      # Long-term memory
├── .deonai_readline_history       # Command history
├── notes/                         # Saved notes
│   ├── project-requirements.md
│   └── bug-fix-ideas.md
└── sessions/                      # Saved sessions
    ├── project-work.json
    └── before_fork_20260215_1430.json
```

---

## 🔧 Advanced Configuration

### Temperature Presets
```bash
/set temperature 0.3    # Deterministic, factual
/set temperature 0.7    # Balanced (default)
/set temperature 1.0    # Creative, diverse
```

### Context Strategies
```bash
# Long conversations
/set context_limit 100
/set max_tokens 8192

# Quick chats (save costs)
/set context_limit 20
/set max_tokens 2048

# Maximum context
/set context_limit 200
/set max_tokens 16384
```

### Memory Strategies
- Daily: Quick notes for tasks
- Weekly: Consolidate to long-term memory
- Monthly: Review and clean notes
- Yearly: Export statistics

---

## 🎓 Examples

### Example 1: Research Session with Notes
```bash
# Start research
deonai

# Ask questions
You: Research FastAPI performance vs Flask

# Save key findings
/note fastapi-performance

# Continue, then save session
/save fastapi-research

# Later, recall findings
/recall fastapi
```

### Example 2: Code Refactoring with Branching
```bash
# Working on refactor
You: How should I refactor this function?

# Try approach 1
DeonAi: Here's a clean approach...

# Not sure, fork and try approach 2
/fork
You: Can you show me an alternative?

# Compare both, load the best one
/sessions
/load refactor-approach-1
```

### Example 3: Cost-Conscious Development
```bash
# Start session
deonai

# Check cost settings
/settings

# Optimize for cost
/set temperature 0.5
/set max_tokens 2048
/set context_limit 30

# Monitor usage
/status

# After session
/stats
```

---

## 🤝 vs OpenClaw Feature Parity

**✅ Implemented (DeonAi)**:
- Memory system
- Session management
- Conversation branching
- Settings customization
- Cost tracking
- Context management

**🚧 Simplified (DeonAi)**:
- Text-based search (vs full semantic search)
- JSON storage (vs SQLite database)
- CLI interface (vs Web UI)

**🎯 DeonAi Advantages**:
- Faster startup
- Smaller footprint
- No browser required
- Works over SSH
- Single file
- Terminal-native

---

**DeonAi**: Power of OpenClaw, speed of CLI 🚀
