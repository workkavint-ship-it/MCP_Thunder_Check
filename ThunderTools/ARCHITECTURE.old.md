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
