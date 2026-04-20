# Thunder Tools Architecture

Clean, layered architecture: **Core Engines → CLI/MCP → User**

## Quick Overview

```
┌──────────────────────────────────────────────────────┐
│              User Interfaces                          │
├─────────────────────────┬────────────────────────────┤
│    CLI (Terminal)       │      MCP (VS Code)         │
│  core/thunder.py generate│ @workspace generate       │
│  core/thunder.py review │  @workspace review         │
└──────────┬──────────────┴──────────┬─────────────────┘
           │                         │
           └──────────┬──────────────┘
                     │
     ┌───────────────▼───────────────┐
     │        Core Engines           │
     ├───────────────────────────────┤
     │  • ReviewEngine               │
     │  • SkeletonGenerator          │
     └───────────────────────────────┘
```

## Directory Structure

```
ThunderTools/
├── core/                    # ⚙️  Core Engines (Business Logic)
│   ├── review_engine.py
│   └── skeleton_generator.py
│
├── cli/                     # 💻 CLI Interface
│   ├── thunder_cli.py
│   └── commands/
│       ├── generate.py
│       └── review.py
│
├── tools/                   # 🔧 MCP Tools (VS Code)
│   ├── generate_skeleton.py
│   ├── review_plugin.py
│   └── review_directory.py
│
└── server.py               # 🌐 MCP Server

ThunderTools/core/thunder.py  # 🚀 CLI Entry Point
```

## How It Works

### Same Engine, Different Interfaces

```python
# CLI uses core engine
from ThunderTools.core import ReviewEngine
engine = ReviewEngine(rules_file)
result = engine.review_file("Plugin.cpp")

# MCP uses SAME engine
from ThunderTools.core import ReviewEngine
engine = ReviewEngine(rules_file)
result = engine.review_file("Plugin.cpp")
```

### Why This Architecture?

1. **Reusability** - Write logic once, use everywhere
2. **Testability** - Test engines independently
3. **Extensibility** - Easy to add new interfaces (Web, IDE plugins, etc.)
4. **Maintainability** - Clear separation of concerns

## Usage

### CLI

```bash
# Generate plugin
python ThunderTools/core/thunder.py generate --plugin-name MyPlugin

# Review plugin  
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin
```

### MCP (VS Code Copilot)

```
User: Generate a Thunder plugin named MyPlugin
User: Review the MyPlugin directory
```

## Main documentation

- [CLI_USAGE.md](CLI_USAGE.md) - Complete CLI documentation
- [MCP_SETUP.md](MCP_SETUP.md) - MCP server setup
- [TOOLS_README.md](TOOLS_README.md) - Tool descriptions

## Design Principles

✅ **Single core logic** - Business rules live in `core/`  
✅ **Thin wrappers** - CLI and MCP just format I/O  
✅ **Same results** - CLI and MCP produce identical output  
✅ **Easy testing** - Mock at layer boundaries  
✅ **Future-proof** - Add web UI, IDE plugins, etc. without touching core  
# Thunder Tools - Modular Architecture

Clean, maintainable MCP server following Anthropic best practices.

## 📁 New Structure

```
ThunderTools/
├── server.py                    # Main MCP server (entry point)
├── tools/                       # Individual tool modules
│   ├── __init__.py
│   ├── review_plugin.py         # Review specific files
│   ├── review_directory.py      # Review entire directories
│   └── generate_skeleton.py     # Generate plugin skeletons
├── PluginReviewer/              # Review engine
│   ├── review_plugin.py
│   └── review_rules.yml
└── PluginSkeletonGenerator/     # Generator engine
    └── PluginSkeletonGenerator.py
```

## ✨ Benefits

### 1. **Modularity**
Each tool is in its own file:
- Easy to find and modify
- Clear separation of concerns
- Can test tools independently

### 2. **Maintainability**
- Add new tools by creating new files in `tools/`
- No need to edit a monolithic server file
- Tools auto-register when imported

### 3. **Following Anthropic Patterns**
- One class per tool
- `get_definition()` returns MCP schema
- `execute()` handles the logic
- Clean, predictable structure

## 🛠️ Adding a New Tool

Create `tools/my_new_tool.py`:

```python
class MyNewTool:
    def __init__(self, base_path):
        self.base_path = base_path
    
    def get_definition(self):
        return {
            "name": "my_new_tool",
            "description": "What it does",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                }
            }
        }
    
    def execute(self, arguments):
        # Your logic here
        return {
            "content": [{
                "type": "text",
                "text": "Result"
            }]
        }
```

Then import in `server.py`:
```python
from tools.my_new_tool import MyNewTool

# In __init__:
self.tools["my_new_tool"] = MyNewTool(self.base_path)
```

Done! The server auto-registers it.

## 🎯 How It Works

### Server (`server.py`)
- Lightweight coordinator
- Imports tool classes
- Handles MCP protocol (stdio)
- Routes requests to tools

### Tools (`tools/*.py`)
- Self-contained modules
- Each exports one tool class
- Implements `get_definition()` and `execute()`
- No dependencies between tools

### Engines (PluginReviewer, PluginSkeletonGenerator)
- Heavy lifting logic
- Tools are thin wrappers around engines
- Engines can be used standalone (CLI)

## 📖 See Also

- [MCP_SETUP.md](MCP_SETUP.md) - Setup guide
- [TOOLS_README.md](TOOLS_README.md) - Complete documentation
- [Anthropic MCP Docs](https://modelcontextprotocol.io/)

