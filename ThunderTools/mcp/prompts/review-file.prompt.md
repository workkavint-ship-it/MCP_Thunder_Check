---
name: review-file
description: Review specific Thunder plugin files for compliance
---

# Review Thunder Plugin Files

Use the **review_plugin** MCP tool to review specific C++ files against Thunder framework guidelines.

## How to Call

Call the MCP tool with:
- **Tool Name**: `review_plugin`
- **Arguments**: `file_paths: ["Dictionary.cpp"]` (one or more filenames/paths)

## CRITICAL INSTRUCTIONS

1. **ONLY** call the `review_plugin` tool
2. **ONLY** report findings that come directly from the tool response
3. Do **NOT** add your own analysis or findings
4. Do **NOT** suggest fixes beyond what the tool provides
5. Present EXACTLY what the tool returns - no modifications

## Output

Simply present the tool's findings in a clear format with:
- Summary (files analyzed, total findings, severity counts)
- Detailed findings by file
- Each finding with: Rule ID, Severity, Line, Code, Issue, Fix (from tool)
