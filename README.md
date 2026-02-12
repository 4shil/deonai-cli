# DeonAi CLI

Your personal AI assistant in the terminal with **full coding capabilities**. Simple, fast, customized. **Powered by OpenRouter** - access 200+ AI models with one API key!

![DeonAi Demo](https://user-images.githubusercontent.com/placeholder/demo.gif)

## Features

### AI Capabilities
- **One-shot queries**: `deonai "explain docker compose"`
- **Interactive chat**: `deonai` for conversation mode
- **Memory**: Remembers conversation context
- **200+ Models**: Claude, GPT-4, Gemini, Llama, and more via OpenRouter
- **Streaming**: Real-time token-by-token responses

### Coding Features NEW
- **File operations**: Read, write, and manage files
- **AI file creation**: Ask AI to create files, it writes them automatically
- **Code execution**: Run Python, Node.js, Bash, Go, Ruby files
- **Project scaffolding**: Generate complete project structures
- **Context-aware**: Add files to conversation for AI analysis

### Power User Features
- **Export**: Save conversations as Markdown or JSON
- **Search**: Find past messages in history
- **Token tracking**: Monitor API usage
- **Quick switch**: Change models on the fly
- **Profiles**: Save multiple API configurations
- **Multiline input**: Paste code easily
- **Retry**: Regenerate responses with different models
- **Undo**: Remove last messages
- **Custom prompts**: Change AI personality mid-conversation

## Installation

### Linux / macOS

```bash
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
./install.sh
deonai --setup
```

### Windows

```batch
git clone https://github.com/4shil/deonai-cli.git
cd deonai-cli
install-windows.bat
deonai --setup
```

Get your OpenRouter API key at: https://openrouter.ai/keys

## Usage

### Interactive Mode (Chat)
```bash
deonai
```

### Coding Commands

```bash
# Read a file
read mycode.py

# List directory
ls src/

# Execute code
run mycode.py

# Create a new project
init python my-project
init node my-app
init web my-website
```

### AI-Powered File Creation

Just ask the AI to create files:

```
You: create a flask web server with user authentication

DeonAi: I'll create a Flask app for you.

WRITE_FILE: app.py
```python
from flask import Flask, request, session
import hashlib

app = Flask(__name__)
app.secret_key = "change-this-secret"

users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    users[username] = password
    return "Registered successfully"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    
    if users.get(username) == password:
        session['user'] = username
        return "Logged in"
    return "Invalid credentials"

if __name__ == '__main__':
    app.run(debug=True)
```

[SUCCESS] Written to: app.py
[INFO] Created 1 file(s): app.py

You: run app.py
[INFO] Executing: app.py
[SUCCESS] Execution completed
--- Output ---
 * Running on http://127.0.0.1:5000
--- End ---
```

### All Commands

```
Chat Commands:
  exit      - Quit the application
  clear     - Reset conversation history
  undo      - Remove last message pair
  models    - List all available AI models
  switch    - Quick switch to another model
  search    - Search conversation history
  profile   - Manage profiles (save/load/list)
  retry     - Retry last message with different model
  system    - Change system prompt
  """       - Start multiline input
  read      - Read file and show content
  ls        - List directory contents
  run       - Execute a code file
  init      - Create new project (python/node/web)
  help      - Show this help
  status    - Show current configuration
  export    - Export conversation to file
```

### CLI Flags

```bash
deonai --version          # Show version
deonai --models           # List all models
deonai --setup            # Reconfigure
deonai "quick question"   # One-shot mode
```

## Coding Workflow Examples

### Example 1: Create and Run a Script

```bash
deonai
You: create a python script that downloads a website
DeonAi: [creates download.py automatically]
You: run download.py https://example.com
[shows output]
```

### Example 2: Debug Code

```bash
You: read buggy_code.py
[file content added to context]
You: this code has a bug on line 15, can you fix it?
DeonAi: [explains bug and creates fixed version]
You: run buggy_code.py
[verify it works]
```

### Example 3: Start a New Project

```bash
You: init python ml-project
[SUCCESS] Created python project: ml-project
You: ls ml-project
[shows project structure]
You: create a machine learning training script in ml-project/src/
DeonAi: [creates train.py with ML code]
```

## Available Models

OpenRouter gives you access to 200+ models:

### Popular Models
- **Claude**: `anthropic/claude-sonnet-4`, `anthropic/claude-opus-4`
- **GPT**: `openai/gpt-4o`, `openai/gpt-4-turbo`
- **Gemini**: `google/gemini-2.0-flash-exp:free` (FREE!)
- **Llama**: `meta-llama/llama-3.3-70b-instruct`
- **DeepSeek**: `deepseek/deepseek-r1`

Run `deonai --models` to see all available models.

## Security

File operations include safety measures:
- Cannot read sensitive system files (passwd, shadow, ssh keys)
- Cannot write to system directories (/etc, /sys, /proc)
- Code execution has 10-second timeout
- File size limits (1MB max for reading)

## Requirements

- Python 3.7+
- `requests` package (installed automatically)
- OpenRouter API key (from https://openrouter.ai/keys)

For code execution, you'll need the relevant interpreters:
- Python 3 (for .py files)
- Node.js (for .js files)
- Bash (for .sh files)
- Go (for .go files)

## Advanced Usage

### Profiles for Different Projects

```bash
# Save work config
You: profile save work

# Switch to personal
You: profile save personal

# List profiles
You: profile list

# Load work profile
You: profile load work
```

### Multiline Code Input

```bash
You: """
def complex_function():
    # Multiple lines
    pass
"""
```

### Custom System Prompts

```bash
You: system You are a Python expert. Always include type hints and docstrings.
[SUCCESS] System prompt updated

You: create a calculator module
DeonAi: [creates code with type hints and docs]
```

## Why OpenRouter?

- **One API key** for 200+ models
- **No vendor lock-in** - switch models anytime
- **Cost optimization** - choose the best model for your budget
- **Unified interface** - same code works with all models
- **Free models available** - Gemini, Llama, and more

## Changelog

### v2.3 - Coding Features Release
- Added file reading, writing, and directory listing
- Added AI-powered file creation (WRITE_FILE syntax)
- Added code execution for Python, Node, Bash, Go, Ruby
- Added project scaffolding (init command)
- Added read, ls, run, init commands
- Enhanced AI system prompt for coding tasks

### v2.2 - Advanced Features
- Added --version and --models CLI flags
- Added profile system for multiple configs
- Added retry command
- Added system prompt changer
- Added multiline input mode
- Added undo command
- Enhanced status display

### v2.1 - Feature Enhancement Release
- Added streaming responses
- Added conversation export
- Added token usage tracking
- Added quick model switching
- Added conversation search
- Added Windows installer
- Removed emojis for professional appearance

### v2.0 - OpenRouter Integration
- Added support for 200+ models via OpenRouter
- Interactive model selection
- Free model support

### v1.0 - Initial Release
- Basic CLI with Anthropic Claude
- One-shot and chat modes
- Configuration system

---

Made by 4shil | Powered by [OpenRouter](https://openrouter.ai)

**Star this repo if you find it useful!**

## Contributing

Issues and PRs welcome! This is a hobby project that became surprisingly useful.

## License

MIT - Modify and share freely
