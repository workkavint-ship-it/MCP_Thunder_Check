# Thunder Tools MCP Server

Model Context Protocol (MCP) server providing three tools for Thunder framework development:

## 🛠️ Available Tools

### 1. `review_plugin_directory`
Review all C++ files in a Thunder plugin directory recursively.

**Auto-detects plugins in:**
- `ThunderNanoServices/`
- `Thunder/Source/plugins/`

**Usage:**
```
#review_plugin_directory Dictionary1
#review_plugin_directory NetworkControl
```

### 2. `review_plugin`
Review specific Thunder plugin files for compliance.

**Usage:**
```
#review_plugin Dictionary1.cpp Dictionary1.h
#review_plugin ThunderNanoServices/NetworkControl/NetworkControl.cpp
```

### 3. `generate_skeleton`
Generate a Thunder plugin skeleton with interactive questionnaire.

**Usage:**
```
#generate_skeleton
```

Then answer the interactive form with plugin details.

---

## 🚀 Quick Start (VS Code)

### 1. Configure MCP Server

Ensure `.vscode/settings.json` contains:

```json
{
  "github.copilot.chat.mcp.servers": {
    "thunder-tools": {
      "command": "python",
      "args": ["${workspaceFolder}/ThunderTools/mcp/server.py"]
    }
  }
}
```

Or run the setup helper:
```powershell
python ThunderTools/mcp/setup_mcp.py
```

### 2. Restart VS Code

**Required after configuration changes.**

### 3. Use in Agent Mode

**⚠️ CRITICAL:** Open Copilot Chat → Select **"Agent"** mode (not Ask/Edit)

MCP tools are only available in Agent mode!

---

## 💡 Three Ways to Use Tools

### Option 1: Direct Tool Invocation (Fastest)

Type `#tool_name` in Copilot Chat:

```
#review_plugin_directory Dictionary1
```

### Option 2: Natural Language (Easiest)

Just describe what you want:

```
Review Dictionary1 plugin for Thunder compliance issues
```

```
Check NetworkControl for framework violations
```

```
Generate a new Thunder plugin for network monitoring
```

Copilot automatically picks the right tool.

### Option 3: Toolsets (Best for Teams)

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "thunder-tools": {
      "command": "python",
      "args": ["${workspaceFolder}/ThunderTools/mcp/server.py"]
    }
  },
  "toolsets": {
    "thunder": {
      "tools": [
        "review_plugin_directory",
        "review_plugin",
        "generate_skeleton"
      ]
    }
  }
}
```

Then use:
```
#thunder review Dictionary1
```

This loads all tools in the toolset. **Commit `.vscode/mcp.json` to git** so your team gets it automatically!

---

## 📚 Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete usage guide with all three methods
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[MCP_SETUP.md](../../MCP_SETUP.md)** - Multi-client setup guide

---

## 🔧 Requirements

- Python 3.8+
- PyYAML: `pip install pyyaml`
- VS Code with GitHub Copilot extension
- Copilot Chat in **Agent mode**

---

## 🧪 Testing

### Test Server Starts

```powershell
python ThunderTools/mcp/server.py
```

**Expected output:**
```
Loaded 13 rule categories
Loaded 13 rule categories
Thunder Tools MCP Server started
```

Press `Ctrl+C` to stop.

### Test in VS Code

1. Open Copilot Chat
2. Switch to **Agent mode**
3. Type `#` to see available tools
4. Try: `#review_plugin_directory Dictionary1`

---

## 📁 File Structure

```
ThunderTools/mcp/
├── server.py                    # MCP server entry point
├── setup_mcp.py                 # Interactive setup helper
├── mcp_config.json              # Generic MCP config template
├── tools/                       # Tool implementations
│   ├── review_plugin.py         # Single file review
│   ├── review_directory.py      # Directory review
│   ├── generate_skeleton.py     # Plugin generator
│   └── review_rules.yml         # Review rules database
├── USAGE_GUIDE.md               # Complete usage guide ⭐
├── TROUBLESHOOTING.md           # Troubleshooting guide
└── README.md                    # This file
```

---

## 🎯 Examples

### Review a Plugin

```
#review_plugin_directory NetworkControl
```

### Review Specific Files

```
#review_plugin Dictionary1.cpp Dictionary1.h Module.cpp
```

### Generate New Plugin

```
#generate_skeleton
```

### Natural Language

```
Review the BluetoothControl plugin for compliance issues
```

```
Check all files in the Streamer plugin
```

```
Create a new plugin for device monitoring
```

---

## ⚠️ Common Issues

### Tools Don't Appear in Chat

- ✅ Check you're in **Agent mode** (not Ask/Edit)
- ✅ Restart VS Code after config changes
- ✅ Verify `.vscode/settings.json` has correct format
- ✅ Check GitHub Copilot extension is enabled

### "ModuleNotFoundError"

```powershell
# Ensure PyYAML is installed
pip install pyyaml

# Test imports
python -c "from ThunderTools.core import ReviewEngine; print('OK')"
```

### Wrong Config Format

**VS Code uses different format than Claude Desktop!**

✅ VS Code: `github.copilot.chat.mcp.servers` in `settings.json`  
❌ NOT: `mcpServers` (that's for Claude Desktop/Cursor)

---

## 🤝 Team Setup

To share with your team:

1. **Commit `.vscode/settings.json`** with MCP config
2. **Commit `.vscode/mcp.json`** with toolsets (optional)
3. **Add to README:**
   ```markdown
   ## Thunder Tools Setup
   
   ```powershell
   pip install pyyaml
   # Restart VS Code
   # Use Copilot Chat in Agent mode
   ```
   
4. **Share this guide:** Point team to `ThunderTools/mcp/USAGE_GUIDE.md`

---

## 📖 Learn More

- [MCP Documentation](https://modelcontextprotocol.io/)
- [VS Code Copilot MCP Guide](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [Thunder Framework Documentation](../docs/)

---

**Bottom line:** Use `#review_plugin_directory` in Agent mode — it's that simple! See [USAGE_GUIDE.md](USAGE_GUIDE.md) for all the details.
