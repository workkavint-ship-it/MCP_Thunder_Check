# Thunder Tools MCP Setup Guide

Universal setup guide for Thunder Tools MCP Server across different AI clients and editors.

## 📋 Prerequisites

```bash
# Required for all setups
pip install pyyaml
```

Verify Python is in PATH:
```bash
python --version  # Should show Python 3.6+
```

---

## 🎯 Setup for Different Clients

### Option 1: Claude Desktop (Recommended for Universal Access)

**Location:** User home directory

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

**Configuration:**
```json
{
  "mcpServers": {
    "thunder-tools": {
      "command": "python",
      "args": [
        "C:/Users/YourUsername/Thunder_MCP/ThunderTools/mcp_server.py"
      ]
    }
  }
}
```

Replace `C:/Users/YourUsername/Thunder_MCP` with your **absolute path** to the cloned repo.

**Restart Claude Desktop** after saving.

---

### Option 2: VS Code with GitHub Copilot

**Location:** Workspace settings

`.vscode/settings.json` (already created in this repo):

```json
{
  "github.copilot.chat.mcp.servers": {
    "thunder-tools": {
      "command": "python",
      "args": [
        "${workspaceFolder}/ThunderTools/mcp_server.py"
      ]
    }
  }
}
```

**Note:** `${workspaceFolder}` auto-resolves to the workspace root. No absolute paths needed.

**Restart VS Code** after changes.

---

### Option 3: Cursor Editor

**Location:** User settings

**macOS/Linux:**
```
~/.cursor/mcp_settings.json
```

**Windows:**
```
%APPDATA%\Cursor\mcp_settings.json
```

**Configuration:**
```json
{
  "mcpServers": {
    "thunder-tools": {
      "command": "python",
      "args": [
        "/absolute/path/to/Thunder_MCP/ThunderTools/mcp_server.py"
      ]
    }
  }
}
```

---

### Option 4: Other MCP Clients

For any MCP-compatible client, use this generic config:

```json
{
  "mcpServers": {
    "thunder-tools": {
      "command": "python",
      "args": ["/path/to/Thunder_MCP/ThunderTools/mcp_server.py"],
      "env": {}
    }
  }
}
```

Common client config locations:
- **Zed Editor:** `~/.config/zed/mcp.json`
- **Continue.dev:** `~/.continue/config.json`
- **Custom MCP Client:** Check documentation for config file location

---

## 🔍 Finding Your Absolute Path

### Windows (PowerShell)
```powershell
cd C:\Users\YourUsername\Thunder_MCP
(Get-Location).Path
# Outputs: C:\Users\YourUsername\Thunder_MCP
```

### macOS/Linux
```bash
cd ~/Thunder_MCP
pwd
# Outputs: /home/username/Thunder_MCP
```

Copy this path and use it in your MCP config.

---

## ✅ Verify Setup

After configuration:

1. **Restart** your AI client/editor completely
2. **Test** with:
   ```
   @workspace what tools are available?
   ```
   or
   ```
   What MCP tools do you have?
   ```

3. **Expected response:**
   - `review_plugin`
   - `review_plugin_directory`
   - `generate_skeleton`

---

## 🚀 Quick Setup Script

Run this to get your configuration:

**Windows (PowerShell):**
```powershell
cd Thunder_MCP
$path = (Get-Location).Path
$mcp_path = "$path\ThunderTools\mcp_server.py"

Write-Host "Add this to your MCP client config:"
Write-Host ""
@"
{
  "mcpServers": {
    "thunder-tools": {
      "command": "python",
      "args": ["$($mcp_path.Replace('\', '\\'))"]
    }
  }
}
"@
```

**macOS/Linux (Bash):**
```bash
cd Thunder_MCP
mcp_path="$(pwd)/ThunderTools/mcp_server.py"

echo "Add this to your MCP client config:"
echo ""
cat << EOF
{
  "mcpServers": {
    "thunder-tools": {
      "command": "python",
      "args": ["$mcp_path"]
    }
  }
}
EOF
```

---

## 📱 Usage Examples (Works in All Clients)

Once configured, use natural language in any MCP client:

### Review Plugins
```
Review ThunderNanoServices/NetworkControl
Check this file for Thunder compliance
What critical issues are in BluetoothAudio?
```

### Generate Plugins
```
Generate a Thunder plugin called MediaController
Create an OOP plugin with IMediaControl interface
Generate a plugin for WiFi management
```

### Combined
```
Generate a plugin called TestService then review it
```

---

## 🐛 Troubleshooting

### Issue: "Tools not found" or "MCP server not connected"

**Solutions:**
1. Check Python is in PATH: `python --version`
2. Verify absolute path is correct (no `~` or relative paths)
3. Ensure PyYAML is installed: `pip install pyyaml`
4. Restart your client **completely** (not just reload)
5. Check client logs for errors

### Issue: "Command not found: python"

**Windows:** Use `python` or `py`
**macOS/Linux:** Try `python3` instead:
```json
"command": "python3"
```

### Issue: "Permission denied"

**macOS/Linux:** Make script executable:
```bash
chmod +x ThunderTools/mcp_server.py
```

### Issue: Path with spaces not working

Ensure paths are quoted properly in JSON:
```json
"args": ["C:/Program Files/Thunder_MCP/ThunderTools/mcp_server.py"]
```

---

## 🔄 For Cloned Repos

If someone clones your Thunder_MCP repo:

1. **They run:**
   ```bash
   git clone <your-repo-url>
   cd Thunder_MCP
   pip install pyyaml
   ```

2. **They get their path:**
   ```bash
   # Windows
   (Get-Location).Path
   
   # macOS/Linux
   pwd
   ```

3. **They add to their MCP client** using the path from step 2

4. **Restart client and test**

No repo modifications needed - it's all client-side configuration!

---

## 📄 Configuration File Locations Reference

| Client | Config Location |
|--------|----------------|
| **Claude Desktop (Win)** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Desktop (Mac)** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Desktop (Linux)** | `~/.config/Claude/claude_desktop_config.json` |
| **VS Code** | `.vscode/settings.json` (workspace) |
| **Cursor** | `~/.cursor/mcp_settings.json` |
| **Zed** | `~/.config/zed/mcp.json` |
| **Continue** | `~/.continue/config.json` |

---

## 💡 Pro Tips

### Per-Project vs Global

- **Global config** (Claude Desktop, Cursor): Works for all Thunder projects
- **Workspace config** (VS Code): Auto-resolves paths, works when you share the repo

### Multiple Thunder Repos

You can configure multiple Thunder installations:
```json
{
  "mcpServers": {
    "thunder-tools-main": {
      "command": "python",
      "args": ["/path/to/main/Thunder_MCP/ThunderTools/mcp_server.py"]
    },
    "thunder-tools-dev": {
      "command": "python",
      "args": ["/path/to/dev/Thunder_MCP/ThunderTools/mcp_server.py"]
    }
  }
}
```

### Virtual Environments

If using Python venv:
```json
{
  "command": "/path/to/venv/bin/python",
  "args": ["/path/to/Thunder_MCP/ThunderTools/mcp_server.py"]
}
```

---

## 📚 Additional Resources

- **MCP Protocol:** https://modelcontextprotocol.io/
- **Tool Documentation:** [TOOLS_README.md](TOOLS_README.md)
- **Thunder Guidelines:** https://rdkcentral.github.io/Thunder/

---

**Need Help?** Check logs in your AI client's output panel or console for specific error messages.
