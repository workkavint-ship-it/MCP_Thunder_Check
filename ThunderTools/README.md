# Thunder Tools - Universal MCP Server

**AI-powered Thunder plugin development tools** for any MCP-compatible client.

✅ Works with: Claude Desktop, VS Code, Cursor, and other MCP clients  
✅ **Modular architecture** following Anthropic best practices

## 🚀 Quick Setup (Anyone Can Use!)

### 1. Clone & Install
```bash
git clone <this-repo>
cd Thunder_MCP
pip install pyyaml
```

### 2. Run Setup Helper
```bash
python ThunderTools/setup_mcp.py
```

Follow the prompts to generate config for your AI client!

### 3. Manual Setup

See **[MCP_SETUP.md](MCP_SETUP.md)** for detailed instructions for:
- 🖥️ **Claude Desktop** (Windows/Mac/Linux)
- 💻 **VS Code** with Copilot
- ✏️ **Cursor** Editor
- 🔧 **Other MCP Clients**

## 💬 Usage (Conversational & Interactive!)

The tools work through **natural conversation**. The AI assistant will ask you questions to gather what it needs!

**Quick examples:**
```
Generate a Thunder plugin
Review ThunderNanoServices/NetworkControl
Check this file for compliance issues
Create an AudioService plugin and review it
```

The AI will interactively ask for:
- Plugin name
- In-process or out-of-process (OOP)
- Interface files (if any)
- Subsystems (preconditions, terminations, controls)
- Any other needed details

**📖 See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed interactive workflows!**

## 🛠️ Available Tools

- **`generate_skeleton`** - Create plugin boilerplate
- **`review_plugin_directory`** - Check entire plugins
- **`review_plugin`** - Review specific files

## 📖 Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Interactive conversation examples (START HERE!)
- **[MCP_SETUP.md](MCP_SETUP.md)** - Universal setup guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Modular design (for developers)
- **[TOOLS_README.md](TOOLS_README.md)** - Complete tool documentation

## 🏗️ Architecture

```
ThunderTools/
├── server.py              # Main MCP server
├── tools/                 # Individual tool modules
│   ├── review_plugin.py
│   ├── review_directory.py
│   └── generate_skeleton.py
├── PluginReviewer/        # Review engine
└── PluginSkeletonGenerator/  # Generator engine
```

Each tool is **self-contained** and can be extended independently!

For release notes see: https://github.com/rdkcentral/Thunder/tree/master/ReleaseNotes
