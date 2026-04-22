---
name: generate
description: Generate a new Thunder plugin skeleton with proper structure
---

# Generate Thunder Plugin Skeleton

Use the **generate_skeleton** MCP tool to create a new Thunder plugin.

## Workflow (REQUIRED)

### Step 1: Collect Configuration

Use **vscode_askQuestions** to collect:
- Plugin name
- Plugin namespace
- JSON-RPC support (yes/no)
- COM-RPC support (yes/no)
- Preconditions (subsystems)
- Output location

### Step 2: Call the Tool

Call the MCP tool with:
- **Tool Name**: `generate_skeleton`
- **Mode**: `"generate"`
- **All parameters** from user's answers above

## CRITICAL INSTRUCTIONS

1. **ALWAYS** use vscode_askQuestions FIRST to collect all information
2. **ONLY** call the `generate_skeleton` tool with mode="generate"
3. **ONLY** report what the tool returns
4. Do **NOT** ask follow-up questions one-by-one
5. Do **NOT** add your own analysis

## Output

Present the tool's results exactly as returned, including:
- Generated files list
- File locations
- Next steps provided by tool
