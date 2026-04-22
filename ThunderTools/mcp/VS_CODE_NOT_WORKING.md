# VS Code MCP Not Working - Troubleshooting Guide

## Issue: `#review_plugin_directory Dictionary1` doesn't invoke the tool

Your MCP server works perfectly (all diagnostics pass), but VS Code isn't using it.

---

## ✅ Step 1: Check VS Code Output Panel (CRITICAL!)

This will show you WHY VS Code isn't loading your MCP server:

1. Open VS Code
2. Go to **View** → **Output** (or `Ctrl+Shift+U`)
3. In the dropdown at the top-right, select **"GitHub Copilot"**
4. Look for errors mentioning:
   - "MCP" or "thunder-tools"
   - "Failed to start"
   - "Connection refused"
   - Import errors
   - Python errors

**Screenshot or copy any errors you see!**

---

## ✅ Step 2: Verify GitHub Copilot Extension Version

MCP support is relatively new in VS Code GitHub Copilot.

1. Go to Extensions (`Ctrl+Shift+X`)
2. Search for "GitHub Copilot"
3. Check version - you need a recent version (2024+)
4. If outdated, click **Update**
5. Restart VS Code after updating

---

## ✅ Step 3: Try Natural Language (Workaround)

The `#tool_name` syntax might not be fully working yet. Try natural language instead:

**Instead of:**
```
#review_plugin_directory Dictionary1
```

**Try:**
```
Review the Dictionary1 plugin for Thunder compliance issues
```

or

```
Use the review_plugin_directory tool to check Dictionary1
```

or

```
@workspace Review Dictionary1 plugin
```

GitHub Copilot should automatically detect and call your MCP tool.

---

## ✅ Step 4: Check MCP Server Process

When you open Copilot Chat, VS Code should start your MCP server. Let's verify:

### Windows (PowerShell):
```powershell
Get-Process python | Where-Object { $_.CommandLine -like "*ThunderTools/mcp/server.py*" }
```

### Alternative - Check Task Manager:
1. Open Task Manager (`Ctrl+Shift+Esc`)
2. Look for `python.exe` processes
3. Right-click → Go to details
4. Check if command line contains `server.py`

**If no process is running:** VS Code isn't starting your MCP server!

---

## ✅ Step 5: Verify Python Path in VS Code

VS Code needs to find Python. Check:

```powershell
# In VS Code terminal
python --version
which python  # or: Get-Command python

# Should show: Python 3.8+ and a valid path
```

If Python isn't found, you need to either:
- Add Python to PATH
- Or update `.vscode/settings.json` with full Python path:

```json
{
  "github.copilot.chat.mcp.servers": {
    "thunder-tools": {
      "command": "C:\\Users\\krenga226\\Downloads\\Thunder_MCP\\.venv\\Scripts\\python.exe",
      "args": ["${workspaceFolder}/ThunderTools/mcp/server.py"]
    }
  }
}
```

---

## ✅ Step 6: Test with Minimal Configuration

Create a test file `.vscode/test-mcp.json`:

```json
{
  "github.copilot.chat.mcp.servers": {
    "thunder-tools": {
      "command": "C:\\Users\\krenga226\\Downloads\\Thunder_MCP\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\krenga226\\Downloads\\Thunder_MCP\\ThunderTools\\mcp\\server.py"]
    }
  }
}
```

Use absolute paths (no `${workspaceFolder}`). If this works, there's an issue with variable expansion.

---

## ✅ Step 7: Check VS Code Insiders/Stable

MCP support might be in VS Code Insiders only. Check if you're using:
- VS Code Stable (regular)
- VS Code Insiders (preview features)

Try VS Code Insiders if stable doesn't work: https://code.visualstudio.com/insiders/

---

## ✅ Step 8: Enable VS Code Developer Tools

Check browser console for errors:

1. In VS Code, press `Ctrl+Shift+I` (or `Cmd+Opt+I` on Mac)
2. Go to **Console** tab
3. Type something in Copilot Chat
4. Look for errors related to MCP or tools

---

## 🔍 Common Fixes

### Fix 1: GitHub Copilot Not Updated

**Solution:** Update GitHub Copilot extension, restart VS Code

### Fix 2: Python Environment Issues

**Solution:** Use absolute path to Python in virtualenv:
```json
"command": "C:\\Users\\krenga226\\Downloads\\Thunder_MCP\\.venv\\Scripts\\python.exe"
```

### Fix 3: MCP Not Supported Yet

**Solution:** Use natural language:
```
Review Dictionary1 plugin for compliance
```

Copilot will still call your MCP tool, just without the `#` syntax.

### Fix 4: Workspace Variable Not Expanding

**Solution:** Use absolute paths in config instead of `${workspaceFolder}`

### Fix 5: Server Starts But Crashes

**Solution:** Check VS Code Output panel for Python errors. Usually PyYAML missing:
```powershell
.venv\Scripts\pip.exe install pyyaml
```

---

## 📋 Diagnostic Checklist

Run through this checklist and note where it fails:

- [ ] `python ThunderTools/mcp/diagnose.py` - All tests pass ✅
- [ ] GitHub Copilot extension installed and up-to-date
- [ ] VS Code restarted after configuration changes
- [ ] Copilot Chat in **Agent mode** (not Ask/Edit)
- [ ] VS Code Output panel shows MCP server loaded
- [ ] `python.exe` process running with `server.py` in command line
- [ ] Natural language works: "Review Dictionary1 plugin"
- [ ] `#` key shows tool suggestions in Agent mode

---

## 🆘 If Still Not Working

### Option A: Use Natural Language (Recommended)

Just describe what you want:
```
Review Dictionary1 plugin for Thunder compliance issues
```

GitHub Copilot will automatically invoke your `review_plugin_directory` tool even without `#` syntax.

### Option B: Check VS Code GitHub Issues

Search for:
- "MCP support VS Code"
- "GitHub Copilot MCP"
- Your specific error from Output panel

MCP in VS Code is relatively new, there may be known issues.

### Option C: Test in Claude Desktop

Your MCP server definitely works (diagnostics pass). Test it in Claude Desktop to confirm:

1. Create `~/.config/claude/claude_desktop_config.json` (Linux/Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
2. Add:
```json
{
  "mcpServers": {
    "thunder-tools": {
      "command": "C:\\Users\\krenga226\\Downloads\\Thunder_MCP\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\krenga226\\Downloads\\Thunder_MCP\\ThunderTools\\mcp\\server.py"]
    }
  }
}
```
3. Restart Claude Desktop
4. Test: "Review Dictionary1 plugin"

This confirms your MCP server works correctly - the issue is VS Code integration.

---

## 📖 Next Steps

1. **Check VS Code Output panel** - This is the most important step!
2. **Try natural language** - Might work even if `#` syntax doesn't
3. **Update GitHub Copilot** - Ensure latest version
4. **Use absolute Python path** - Avoid path resolution issues

**Report back what you see in the Output panel!** That will show the exact issue.
