# Thunder Plugin Reviewer MCP Server

An MCP (Model Context Protocol) server for reviewing Thunder framework plugins against coding guidelines.

## 📦 What's Included

- `mcp_server.py` - MCP server (stdio transport)
- `review_plugin.py` - Core review engine
- `review_rules.yml` - 50+ Thunder framework rules

## 🚀 Quick Start

###  1. Install Dependencies

```bash
pip install pyyaml
```

### 2. Configure Your MCP Client

**For Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "thunder-reviewer": {
      "command": "python",
      "args": ["C:/path/to/Thunder_MCP/ThunderTools/PluginReviewer/mcp_server.py"]
    }
  }
}
```

**For VS Code with Copilot** (`.vscode/settings.json`):
```json
{
  "github.copilot.chat.mcp.servers": {
    "thunder-reviewer": {
      "command": "python",
      "args": ["${workspaceFolder}/ThunderTools/PluginReviewer/mcp_server.py"]
    }
  }
}
```

### 3. Use with ChatCommands

Once configured, simply ask your AI assistant:

```
Review ThunderNanoServices/NetworkControl
Check this file for Thunder compliance
What critical issues are in my plugin?
```

## 🛠️ Available MCP Tools

| Tool | Description | Arguments |
|------|-------------|-----------|
| `review_plugin_directory` | Review all C++ files in a directory | `directory` (string), `recursive` (bool) |
| `review_plugin` | Review specific files | `file_paths` (array of strings) |
| `get_review_summary` | Get summary by severity | `directory` (string) |

## 💬 Example Usage

**With Claude/ChatGPT:**
```
User: Review ThunderNanoServices/NetworkControl

AI: [Invokes review_plugin_directory tool]
    Found 22 issues:
    - 3 Critical (IShell lifetime, missing AddRef)
    - 11 High (JSON-RPC misuse, threading)
    - 8 Medium (code style)
    
User: Show me how to fix the critical issues

AI: [Provides specific code fixes]
```

**Direct Tool Call:**
```json
{
  "name": "review_plugin_directory",
  "arguments": {
    "directory": "ThunderNanoServices/NetworkControl",
    "recursive": false
  }
}
```

## 📊 What Gets Checked

✅ **Critical (3 types)**
- Plugin lifecycle violations
- Reference counting errors
- Layer dependency violations

✅ **High Priority (11 types)**
- JSON-RPC registration mismatches
- IPC misuse
- Threading violations
- Exception usage

✅ **Medium (19 types)**
- Code style (C-casts, types)
- Logging patterns
- Configuration handling

✅ **Low**
- Minor improvements

## 📝 Output Example

```markdown
# Thunder Plugin Review: ThunderNanoServices/NetworkControl

## Summary
- Files reviewed: 7
- Files with issues: 3  
- Critical issues: 3
- Total findings: 22

## ⚠️ Files with Critical Issues
- `NetworkControl.cpp` (2 critical)
- `NetworkControlImplementation.cpp` (1 critical)

## CRITICAL

**LIFECYCLE_005**: IShell* must be AddRef'd when stored
- Location: `NetworkControl.cpp:66:9`
- Issue: Missing service->AddRef() when storing IShell*
- Code: `_service = service;`
- Fix: Add _service->AddRef() after assignment
```

## 🔧 Standalone CLI Usage

You can also use the reviewer directly without MCP:

```bash
# Review a directory
python review_plugin.py --dir ThunderNanoServices/NetworkControl

# Review specific files  
python review_plugin.py NetworkControl.cpp NetworkControl.h

# Summary only
python review_plugin.py --dir MyPlugin --summary-only
```

## 🎯 Customizing Rules

Edit `review_rules.yml`:

```yaml
categories:
  - name: "My Custom Checks"
    severity: "high"
    rules:
      - id: "CUSTOM_001"
        name: "Company naming convention"
        description: "All plugins must use MyCompany prefix"
        pattern: 'class\s+(?!MyCompany)'
        suggestion: "Rename to MyCompanyPluginName"
```

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: yaml` | Run `pip install pyyaml` |
| Directory not found | Paths are relative to Thunder_MCP root |
| No MCP connection | Check Python in PATH, verify config path |
| Permission denied | Mark mcp_server.py executable: `chmod +x` |

## 📚 See Also

- [Thunder Coding Guidelines](../../Thunder/.github/instructions/)
- [Review Rules](review_rules.yml) - All 50+ rules
- [MCP Protocol](https://modelcontextprotocol.io/)

---

**Exit Codes:** Returns 1 if critical issues found (useful for CI/CD)
