# Thunder MCP Prompts

This directory contains prompt files that enable **slash commands** in VS Code GitHub Copilot Chat.

## Location & Purpose

**Source Location:** `ThunderTools/mcp/prompts/` (you edit here)  
**Discovery Location:** `.github/prompts/` (auto-copied for VS Code)

These `.prompt.md` files define how AI assistants should invoke Thunder MCP tools through slash commands.

## Available Prompts

| File | Slash Command | Tool Called | Description |
|------|---------------|-------------|-------------|
| `review.prompt.md` | `/review` | `review-dir` or `review_plugin_directory` | Review entire plugin directory |
| `review-file.prompt.md` | `/review-file` | `review-file` or `review_plugin` | Review specific files |
| `generate.prompt.md` | `/generate` | `generate` or `generate_skeleton` | Generate new plugin skeleton |

## How It Works

1. **You edit prompts here:** `ThunderTools/mcp/prompts/*.prompt.md`
2. **Run setup:** `python ThunderTools/mcp/setup_mcp.py`
3. **Auto-copies to:** `.github/prompts/` (where VS Code discovers them)
4. **Restart VS Code** to activate slash commands
5. **Use in Copilot Chat:** `/review Dictionary1`

## Prompt File Format

Each `.prompt.md` file has:

```markdown
---
name: command-name
description: What the command does
---

# Instructions for AI

Detailed instructions on when and how to use the tool...
```

The frontmatter (between `---`) defines the slash command name and description shown in VS Code.

## Modifying Prompts

1. Edit files in `ThunderTools/mcp/prompts/`
2. Run `python ThunderTools/mcp/setup_mcp.py` (select VS Code)
3. It will auto-copy updated prompts to `.github/prompts/`
4. Restart VS Code to reload prompts

## Why Two Locations?

- **ThunderTools/mcp/prompts/** = Source of truth, part of your tool repository
- **.github/prompts/** = Where VS Code GitHub Copilot discovers prompts (hardcoded path)

We maintain prompts in ThunderTools and auto-copy to .github during setup to keep everything organized while meeting VS Code's requirements.

## Testing Prompts

After setup, in VS Code Copilot Chat:

```
/review Dictionary1
```

```
/review-file NetworkControl.cpp
```

```
/generate
```

You should see autocomplete suggestions for slash commands.

## Troubleshooting

**Slash commands not appearing?**
1. Check `.github/prompts/` exists with `.prompt.md` files
2. Restart VS Code completely
3. Open Copilot Chat and type `/` - should show custom commands

**Prompts not working?**
1. Verify frontmatter format (name, description between `---`)
2. Check file extension is `.prompt.md`
3. Look at VS Code Output panel → GitHub Copilot for errors

## See Also

- [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) - MCP setup diagnostics
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Tool invocation guide
