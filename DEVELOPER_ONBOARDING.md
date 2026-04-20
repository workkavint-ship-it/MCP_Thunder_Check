# Developer Onboarding: MCP Server Integration

**For developers pulling the MCP server changes into their workspace.**

---

## 📋 What Changed

These updates add an **AI-powered MCP (Model Context Protocol) server** to Thunder Tools:

✅ **CLI relocated**: `thunder.py` moved to `ThunderTools/core/` with workspace-safe path resolution  
✅ **MCP Server**: Adds 3 intelligent tools to your AI assistant (Claude, Copilot, Cursor, etc.)  
✅ **Auto-detection**: Plugin names like `Dictionary` auto-resolve to full paths  
✅ **No breaking changes**: Existing workflows still work  

---

## 🚀 Quick Onboarding (5 minutes)

### Step 1: Install Python Dependency
```bash
pip install pyyaml
```
**Why**: The MCP server uses PyYAML to parse plugin review rules.

### Step 2: Configure Your AI Client

Choose your client below and follow **ONE** of these paths:

---

### **Option A: VS Code with GitHub Copilot** (Default)

✅ **Already configured** in `.vscode/settings.json`

**All you need to do:**
```
1. Restart VS Code (Ctrl+Shift+P → "Developer: Reload Window")
2. Open Copilot Chat
3. Ask: "What tools are available?"
4. You should see: review_plugin_directory, review_plugin, generate_skeleton
```

**If tools don't appear:**
- Check that `.vscode/settings.json` has `github.copilot.chat.mcp.servers` configured
- Verify Python is in PATH: `python --version`
- Check VS Code's Output panel (View → Output → "GitHub Copilot")

---

### **Option B: Claude Desktop** (For Universal Access)

Run the interactive setup helper:
```bash
python ThunderTools/setup_mcp.py
```

This will:
1. Detect your Thunder_MCP folder automatically
2. Show you where to add the config (`%APPDATA%\Claude\claude_desktop_config.json` on Windows)
3. Generate the exact JSON you need

Then:
1. Edit the config file and add the JSON
2. Restart Claude Desktop
3. Test: Ask "What tools are available?"

**Manual config** (if you prefer):

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "thunder-tools": {
      "command": "python",
      "args": [
        "C:/Users/YourUsername/Thunder_MCP/ThunderTools/server.py"
      ]
    }
  }
}
```
Replace `C:/Users/YourUsername/Thunder_MCP` with your actual path.

---

### **Option C: Cursor Editor**

Run the setup helper:
```bash
python ThunderTools/setup_mcp.py
```

Choose option 3 (Cursor Editor) and it will show you:
1. Where to add the config (`%APPDATA%\Cursor\mcp_settings.json` on Windows)
2. Exactly what JSON to add

Then:
1. Edit the config file
2. Restart Cursor
3. Test: Open Cursor Chat and ask "What tools are available?"

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] **Python dependency installed**: `pip show pyyaml`
- [ ] **AI client restarted** (full restart, not just reload)
- [ ] **MCP tools visible**: Ask your AI "What tools are available?"
  - Expected: `review_plugin_directory`, `review_plugin`, `generate_skeleton`
- [ ] **CLI works**: `python ThunderTools/core/thunder.py --help`
- [ ] **Plugin names auto-resolve**: Try `/review Dictionary` → Should find `ThunderNanoServices/Dictionary`

---

## 🎯 Usage Examples (After Setup)

### Review a Plugin
```
Review ThunderNanoServices/NetworkControl
Check Dictionary for critical issues
What problems does VolumeControl have?
```

### Generate a Plugin
```
Generate a Thunder plugin called MediaController
Create an OOP plugin with interface IMediaControl
Build a WiFi management plugin
```

### Combined Workflow
```
Generate a plugin called TestService and review it for issues
Create an AudioService and check for compliance problems
```

---

## 📍 Important Note: Path Resolution

The MCP server and CLI now use **intelligent path resolution**:

```
Input: "Dictionary" → Resolves to: ThunderNanoServices/Dictionary
Input: "NetworkControl" → Resolves to: ThunderNanoServices/NetworkControl  
Input: "ThunderNanoServices/Dictionary1" → Uses exact path
Input: "/absolute/path" → Uses absolute path as-is
```

**Why**: Makes the tools easier to use - you don't need to type full paths anymore.

---

## ⚙️ Troubleshooting

### "ModuleNotFoundError: No module named 'ThunderTools'"
**Fix**: Run from the workspace root:
```bash
cd /path/to/Thunder_MCP
python ThunderTools/core/thunder.py review --directory Dictionary
```

### "MCP tools not showing up"
**Checklist**:
1. Is PyYAML installed? → `pip install pyyaml`
2. Did you restart the AI client? (Full restart, not reload)
3. Is Python in PATH? → `python --version` should work
4. Check config file has `${workspaceFolder}` or correct absolute path

### "Directory not found"
**Fix**: The path resolution tries:
1. As absolute path
2. As workspace-relative
3. As plugin name in `ThunderNanoServices/`
4. As plugin name in `Thunder/Source/plugins/`

If still not found, use full path: `ThunderNanoServices/PluginName`

---

## 📖 Documentation

- **[README.md](ThunderTools/README.md)** - Overview and quick start
- **[MCP_SETUP.md](ThunderTools/MCP_SETUP.md)** - Detailed setup for all clients
- **[USAGE_GUIDE.md](ThunderTools/USAGE_GUIDE.md)** - Interactive workflow examples
- **[CLI_USAGE.md](ThunderTools/CLI_USAGE.md)** - Command-line interface guide
- **[ARCHITECTURE.md](ThunderTools/ARCHITECTURE.md)** - Technical architecture

---

## 🆘 Still Having Issues?

1. **Check the logs**: VS Code MCP output panel (View → Output → search for "thunder")
2. **Verify imports work**: 
   ```bash
   cd /path/to/Thunder_MCP
   python -c "from ThunderTools.core import ReviewEngine; print('✅ Imports work')"
   ```
3. **Test server directly**:
   ```bash
   python ThunderTools/server.py
   ```
   Should print: `Thunder Tools MCP Server started` (then hang waiting for input - that's normal)

---

## 🎉 That's It!

Once you've:
1. ✅ Installed PyYAML
2. ✅ Configured your AI client
3. ✅ Restarted your AI client
4. ✅ Verified tools are visible

You're ready to use the Thunder MCP tools! 🚀
