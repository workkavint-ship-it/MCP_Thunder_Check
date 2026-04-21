# Thunder MCP Prompts

This directory contains prompt files that standardize how AI assistants interact with Thunder MCP tools.

## Available Prompts

### `/review` - Review Plugin Directory
**File:** `review.prompt.md`  
**Tool:** `review`  
**Usage:** `Review Dictionary`, `Check NetworkControl`, `Analyze BluetoothAudio`

Reviews all C++ files in a Thunder plugin directory recursively. Auto-resolves plugin names (e.g., "Dictionary" → "ThunderNanoServices/Dictionary").

**Output:** Findings grouped by severity (🔴🟠🟡⚪) with line numbers and fix suggestions.

---

### `/review-file` - Review Specific Files
**File:** `review-file.prompt.md`  
**Tool:** `review_file`  
**Usage:** `Review Dictionary.cpp`, `Check this file`, `Analyze MyPlugin.h and MyPlugin.cpp`

Reviews specific C++ files for Thunder compliance. Can review multiple files at once.

**Output:** Per-file findings with severity, line numbers, and actionable fixes.

---

### `/generate` - Generate Plugin Skeleton
**File:** `generate.prompt.md`  
**Tool:** `generate`  
**Usage:** `Generate a Thunder plugin`, `Create MediaController`, `Build a WiFi plugin`

Generates complete Thunder plugin skeleton with proper structure. Uses interactive questions to gather all configuration.

**Workflow:**
1. AI asks all configuration questions in one dialog
2. User provides answers
3. AI calls generate tool
4. Plugin scaffold created with all boilerplate

**Output:** Complete plugin directory with .cpp/.h files, CMakeLists.txt, and JSON-RPC stubs.

---

## How It Works

### For VS Code + GitHub Copilot:
1. Prompts in `.github/prompts/` are automatically discovered
2. Use natural language commands (e.g., "Review Dictionary")
3. Copilot uses prompt instructions to call MCP tools correctly
4. Standardized output formatting across all sessions

### For Other AI Clients:
These prompts serve as documentation for how to use Thunder MCP tools correctly, even if not automatically loaded.

---

## Prompt File Format

Each prompt follows this structure:

```markdown
---
name: tool-name
description: Brief description
---

# Detailed Instructions

When to use, how to call, output format, examples, rules.
```

---

## Benefits

✅ **Consistency** - Same behavior across different AI sessions  
✅ **Discoverability** - Users can type `/review` or natural language  
✅ **Reliability** - AI always calls tools correctly  
✅ **Standardized Output** - Predictable formatting with severity icons  
✅ **Cross-Platform** - Works on any laptop with VS Code + Copilot  

---

## Testing

After reloading VS Code, verify prompts work:

1. Reload: `Ctrl+Shift+P` → "Developer: Reload Window"
2. Open Copilot Chat
3. Type: `/review Dictionary`
4. Verify: Tool is called and output formatted correctly

Or try natural language:
- "Review the NetworkControl plugin"
- "Generate a plugin called MediaController"
- "Check Dictionary.cpp for compliance issues"
