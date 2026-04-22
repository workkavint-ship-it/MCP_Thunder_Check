---
name: review
description: Review an entire Thunder plugin directory for compliance issues
---

# Review Thunder Plugin Directory

Use the **review_plugin_directory** MCP tool to review all C++ files in a Thunder plugin directory.

## How to Call

Call the MCP tool with:
- **Tool Name**: `review_plugin_directory`
- **Arguments**: `directory: "Dictionary1"` (plugin name or path)

## CRITICAL INSTRUCTIONS

1. **ONLY** call the `review_plugin_directory` tool
2. **ONLY** report findings that come directly from the tool response
3. Do **NOT** add your own analysis or findings
4. Do **NOT** suggest fixes beyond what the tool provides
5. Present EXACTLY what the tool returns - no modifications

## Output

Simply present the tool's findings in a clear format with:
- Summary (files reviewed, total findings, severity counts)
- Detailed findings by file
- Each finding with: Rule ID, Severity, Line, Issue, Fix (from tool)
