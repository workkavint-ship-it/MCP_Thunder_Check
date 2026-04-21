# Thunder MCP Tools - Quick Reference

## 🚀 Tool Invocation Syntax

### Using # Syntax (Direct Tool Calls)

In VS Code Copilot Chat, use `#` followed by tool name:

```
#review-dir Dictionary1
```

```
#review-file ThunderNanoServices/NetworkControl/NetworkControl.cpp
```

```
#generate
```

### Available Tools

| Short Name | Full Name | Description |
|------------|-----------|-------------|
| `#review-dir` | `#review_plugin_directory` | Review entire plugin directory |
| `#review-file` | `#review_plugin` | Review specific C++ files |
| `#generate` | `#generate_skeleton` | Generate new plugin skeleton |

**Both short and full names work** - use whichever you prefer!

## 📋 Examples

### Review Entire Plugin
```
#review-dir Dictionary1
```
Auto-detects plugin location in `ThunderNanoServices/` or `Thunder/Source/plugins/`

### Review Specific Files
```
#review-file Dictionary.cpp Dictionary.h
```

```
#review-file ThunderNanoServices/NetworkControl/NetworkControl.cpp
```

### Generate New Plugin
```
#generate
```
Opens interactive form to configure your plugin

## 🔧 Troubleshooting

### `#` Syntax Not Working?

1. **Restart VS Code** after configuration changes
   - `Ctrl+Shift+P` → "Developer: Reload Window"

2. **Check configuration** in `.vscode/settings.json`:
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

3. **Test server starts**:
   ```powershell
   python ThunderTools\mcp\server.py
   ```
   Should show: `"Thunder Tools MCP Server started"`

4. **Use natural language fallback**:
   If `#` doesn't work, try:
   ```
   Review Dictionary1 plugin for compliance
   ```
   Copilot will invoke the tool automatically.

### Check Tool Availability

In Copilot Chat:
```
What MCP tools are available?
```

Should list all 6 tool names (3 short + 3 full).

## 💡 Tips

- **Shorter names** (`#review-dir`) are easier to type
- **Full names** (`#review_plugin_directory`) are more descriptive
- **Natural language** always works as fallback
- **Tab completion** may help with tool names in some clients

## 🆘 Support

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed diagnostics.
