# 🌩️ Thunder Tools MCP Server

Universal AI-powered development tools for Thunder framework. Works with **any MCP-compatible AI client**.

## ✨ What's This?

An MCP (Model Context Protocol) server that gives AI assistants the ability to:
- 🔍 **Review** Thunder plugins for compliance (50+ framework rules)
- 🛠️ **Generate** complete plugin skeletons with boilerplate
- ✅ Check reference counting, lifecycle, JSON-RPC, threading, and more

## 🚀 Quick Start (For Anyone!)

### 1. Clone & Install
```bash
git clone https://github.com/your-repo/Thunder_MCP.git
cd Thunder_MCP
pip install pyyaml
```

### 2. Setup Your AI Client

#### Option A: Interactive Setup (Easiest)
```bash
python ThunderTools/setup_mcp.py
```

Choose your client, get the config, done! ✅

#### Option B: Manual Setup

See **[ThunderTools/MCP_SETUP.md](ThunderTools/MCP_SETUP.md)** for:
- Claude Desktop (Windows/Mac/Linux)
- VS Code with Copilot  
- Cursor Editor
- Any other MCP client

### 3. Use With Natural Language

```
Generate a Thunder plugin called MediaController
Review ThunderNanoServices/NetworkControl
Check this file for compliance issues
```

## 🎯 Who Can Use This?

- ✅ **Claude Desktop users** - Universal AI assistant
- ✅ **VS Code developers** - GitHub Copilot integration
- ✅ **Cursor users** - Built-in AI with MCP
- ✅ **Any MCP client** - Standard protocol support

**No VS Code required!** Works anywhere MCP is supported.

## 🛠️ Available Tools

| Tool | What It Does |
|------|--------------|
| `generate_skeleton` | Create complete plugin structure from interface specs |
| `review_plugin_directory` | Scan entire plugin for Thunder guideline violations |
| `review_plugin` | Check specific C++ files for compliance |

## 📖 Documentation

- **[ThunderTools/MCP_SETUP.md](ThunderTools/MCP_SETUP.md)** - Setup for all clients
- **[ThunderTools/TOOLS_README.md](ThunderTools/TOOLS_README.md)** - Complete documentation
- **[ThunderTools/README.md](ThunderTools/README.md)** - Quick reference

## 💡 Example: Complete Workflow

```
You: Generate a Thunder plugin for WiFi management

AI: I'll create a WiFi plugin for you.
    [Generates complete plugin structure]
    ✅ Created WiFiManager/ with all boilerplate code
    
You: Review it for issues

AI: [Scans generated code]
    Found 1 medium issue:
    - Line 45: Consider initializing this variable
    
You: Fix that issue

AI: [Provides corrected code]
    ✅ All compliance checks pass!
```

## 🔧 For Repository Maintainers

This MCP server is **client-agnostic**. When users clone your repo:

1. They install PyYAML: `pip install pyyaml`
2. They run: `python ThunderTools/setup_mcp.py`
3. They configure their preferred AI client
4. It just works! ✨

No need to include client-specific configs in the repo - the setup script generates them.

## 🌍 Platform Support

- ✅ Windows
- ✅ macOS  
- ✅ Linux

Works with Python 3.6+ (tested on 3.8+)

## 🤝 Contributing

See [Thunder contribution guidelines](Thunder/CONTRIBUTING.md)

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE)

---

**Questions?** See [MCP_SETUP.md](ThunderTools/MCP_SETUP.md) or open an issue!
