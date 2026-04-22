# Thunder Tools MCP - VS Code Usage Guide

You have **two clean methods** to use your ThunderTools MCP server in VS Code Copilot:

---

## 🔴 CRITICAL: Agent Mode Required!

**MCP tools ONLY work in Agent mode!**

1. Open Copilot Chat
2. Click the **mode dropdown** at the top
3. Select **"Agent"** (NOT "Ask" or "Edit")

❌ Ask mode: Tools invisible  
❌ Edit mode: Tools invisible  
✅ Agent mode: Tools available

---

## 1. `#tool_name` inline mention (recommended)

Type `#tool_name` directly in Agent mode chat. Your three Thunder tools:

- `#review_plugin_directory` - Review entire plugin directory
- `#review_plugin` - Review specific files  
- `#generate_skeleton` - Generate new plugin

Just type the tool name in chat:

```
#review_plugin_directory Dictionary1
```

```
#review_plugin ThunderNanoServices/NetworkControl/NetworkControl.cpp
```

```
#generate_skeleton
```

**No folder setup, no prompt files needed.**

---

## 2. Natural language in Agent mode (zero config)

In Agent mode, Copilot will detect when you're describing a task that matches one of your MCP tools and automatically invoke it. If you don't know the tools available, you can type `#` and Copilot will suggest all tools from your MCP server with descriptions.

So you can just describe what you want naturally — Copilot picks the right tool automatically:

```
Review the Dictionary1 plugin for Thunder compliance issues
```

```
Check NetworkControl.cpp for framework violations
```

```
Generate a new Thunder plugin for network monitoring
```

**Copilot automatically calls the appropriate tool** — you don't need to know the exact tool names.

---

## ✅ Configuration Required

### Correct VS Code MCP Config

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

**Important:** VS Code uses `github.copilot.chat.mcp.servers` in `settings.json`

❌ **Don't use** `mcpServers` — that's for Claude Desktop/Cursor only!

### After Configuration

1. **Restart VS Code** (required!)
2. **Open Copilot Chat**  
3. **Switch to Agent mode** (top dropdown)
4. **Test:** Type `#review_plugin_directory Dictionary1`

---

## Quick Start

### Option A: Direct Tool Names (Recommended)

1. Ensure `.vscode/settings.json` has MCP config (see above)
2. Restart VS Code
3. Open Copilot Chat in **Agent mode**
4. Type `#review_plugin_directory Dictionary1`

### Option B: Natural Language (Easiest)

1. Ensure `.vscode/settings.json` has MCP config
2. Restart VS Code
3. Open Copilot Chat in **Agent mode**
4. Type "Review Dictionary1 plugin for compliance"

---

## Discover Available Tools

In Agent mode, type just `#` and VS Code will show a dropdown with all MCP tools:

```
#
```

You'll see:
- **review_plugin_directory** - Review all C++ files in a Thunder plugin directory recursively...
- **review_plugin** - Review specific Thunder plugin files for compliance...
- **generate_skeleton** - Generate a Thunder plugin skeleton...

---

## Example Usage

### Review a Plugin Directory

```
#review_plugin_directory NetworkControl
```

Or natural language:
```
Check the NetworkControl plugin for Thunder violations
```

### Review Specific Files

```
#review_plugin ThunderNanoServices/Dictionary1/Dictionary1.cpp ThunderNanoServices/Dictionary1/Dictionary1.h
```

Or natural language:
```
Review Dictionary1.cpp and Dictionary1.h for compliance issues
```

### Generate Plugin Skeleton

```
#generate_skeleton
```

Or natural language:
```
Generate a new Thunder plugin
```

Copilot will use the interactive questionnaire to gather requirements.

---

## Troubleshooting

### Tools Don't Appear

1. **Check Agent mode** - Tools only work in Agent mode, not Ask/Edit
2. **Restart VS Code** - After config changes, always restart
3. **Verify config** - Check `.vscode/settings.json` has correct format
4. **Test server** - Run `python ThunderTools/mcp/server.py` manually
5. **Check Output panel** - View → Output → Select "GitHub Copilot"

### "Tool not found"

- Make sure you're using exact tool names:
  - `review_plugin_directory` (not `review_plugin_dir` or `review_directory`)
  - `review_plugin` (not `review_file`)
  - `generate_skeleton` (not `generate`)

### Python/Import Errors

```powershell
# Install dependencies
pip install pyyaml

# Test imports
python -c "from ThunderTools.core import ReviewEngine; print('OK')"
```

---

## Bottom Line

**Fastest & Recommended:** Type `#review_plugin_directory Dictionary1` in Agent mode — works immediately after basic MCP config.

**Most Flexible:** Use natural language in Agent mode — just say "Review Dictionary1 plugin" and Copilot picks the right tool automatically.

**Both methods work perfectly without needing `.github/prompts/`!**

**Critical:** Always use **Agent mode** — tools are invisible in Ask/Edit modes!
