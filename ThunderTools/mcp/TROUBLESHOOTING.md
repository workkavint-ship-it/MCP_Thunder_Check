# Thunder MCP Troubleshooting Guide

## MCP Tools Not Working in VS Code

If `#review_plugin_directory`, `#review_plugin`, or `#generate_skeleton` don't invoke the tools, follow these steps:

### 1. Verify Configuration

Check `.vscode/settings.json` contains:

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

### 2. Restart VS Code

**Critical:** After any MCP configuration changes, you MUST restart VS Code:
- `Ctrl+Shift+P` → "Developer: Reload Window" (or full restart)

### 3. Check Python Environment

Test the server starts:

```powershell
# Navigate to workspace root
cd C:\Users\krenga226\Downloads\Thunder_MCP

# Activate virtualenv (if using one)
.venv\Scripts\Activate.ps1

# Test server directly
python ThunderTools\mcp\server.py
```

**Expected output:**
```
Loaded 13 rule categories
Loaded 13 rule categories
Thunder Tools MCP Server started
```

Press `Ctrl+C` to stop.

### 4. Verify PyYAML is Installed

```powershell
pip install pyyaml
```

### 5. Check VS Code Output Panel

Open VS Code Output panel and select "GitHub Copilot" from the dropdown to see MCP server logs.

### 6. Test Tool Availability

In Copilot Chat, ask:
```
What MCP tools are available?
```

Should list:
- `review_plugin_directory`
- `review_plugin`
- `generate_skeleton`

### 7. Alternative: Use Natural Language

If `#` syntax doesn't work, GitHub Copilot should still invoke tools via natural language:

```
Review the Dictionary1 plugin for compliance issues
```

```
Check ThunderNanoServices/NetworkControl for Thunder violations
```

```
Generate a new Thunder plugin
```

The AI will automatically call the appropriate MCP tool.

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'ThunderTools'"

**Solution:** The server.py has workspace path handling. Ensure you're running from workspace root or virtualenv is activated.

### Issue: "Rules file not found"

**Solution:** The rules are at `ThunderTools/mcp/tools/review_rules.yml`. Check this file exists.

### Issue: Tools don't appear in chat

**Solution:** 
1. Ensure GitHub Copilot extension is enabled and logged in
2. Restart VS Code after configuration changes
3. Check the MCP server is running (Output panel)

### Issue: "command 'python' not found"

**Solution:** Either:
- Install Python 3.8+ and add to PATH
- Or change `.vscode/settings.json` to use full Python path:
  ```json
  "command": "C:\\Python311\\python.exe"
  ```

## Testing on Another Computer

When setting up on a new machine:

1. **Clone the repository**
2. **Install Python** (3.8+)
3. **Install dependencies:**
   ```powershell
   pip install pyyaml
   ```
4. **Run setup helper:**
   ```powershell
   python ThunderTools\mcp\setup_mcp.py
   ```
   Select option 2 (VS Code) and save to `.vscode/settings.json`

5. **Restart VS Code**

6. **Test in Copilot Chat:**
   ```
   #review_plugin_directory Dictionary1
   ```
   Or use natural language:
   ```
   Review Dictionary1 plugin
   ```

## Verify Setup Script

Run the setup script to ensure configuration is correct:

```powershell
python ThunderTools\mcp\setup_mcp.py
```

This will show you the proper configuration and can auto-save to `.vscode/settings.json`.

## Support

If issues persist:
1. Check VS Code's Output panel for error messages
2. Test the server starts manually: `python ThunderTools\mcp\server.py`
3. Verify Python version: `python --version` (should be 3.8+)
4. Check PyYAML is installed: `python -c "import yaml; print('OK')"`
