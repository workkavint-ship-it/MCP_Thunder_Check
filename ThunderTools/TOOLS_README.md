# Thunder MCP Tools - Complete Documentation

**Universal MCP server** for Thunder plugin development: **review** and **generate** plugins with AI assistance.

✅ Works with: Claude Desktop, VS Code, Cursor, and any MCP-compatible client

## 🚀 Quick Setup

```bash
# 1. Install dependencies
pip install pyyaml

# 2. Run setup helper (generates config for your client)
python ThunderTools/setup_mcp.py

# 3. OR manually configure - see MCP_SETUP.md
```

For detailed setup instructions, see **[MCP_SETUP.md](MCP_SETUP.md)**

## 💬 Usage (Same for All Clients!)

### Review Plugins
```
Review ThunderNanoServices/NetworkControl
Check this file for Thunder compliance issues
What critical issues are in BluetoothAudio?
```

### Generate Plugins
```
Generate a Thunder plugin called MediaController
Create an OOP plugin with IMediaControl interface
Generate a plugin for WiFi management
```

### Combined Workflows
```
Generate a plugin called TestPlugin, then review it
Create AudioService and check for compliance issues
```

## 🛠️ Available Tools

- **`review_plugin_directory`** - Check C++ code against 50+ Thunder rules
- **`review_plugin`** - Review specific files
- **`generate_skeleton`** - Create plugin boilerplate from config

## 📖 Full Documentation

See [TOOLS_README.md](TOOLS_README.md) for complete documentation.

## CLI Usage

```bash
# Review
python PluginReviewer/review_plugin.py --dir ThunderNanoServices/MyPlugin

# Generate  
python PluginSkeletonGenerator/PluginSkeletonGenerator.py --config config.yaml
```
