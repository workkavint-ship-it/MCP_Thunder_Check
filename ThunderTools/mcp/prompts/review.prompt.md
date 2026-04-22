---
name: review
description: Review an entire Thunder plugin directory for compliance issues
---

# Review Thunder Plugin Directory

Use the MCP tool `review_plugin_directory`.

## Required Workflow

1. Ask for plugin directory if missing.
2. Call `review_plugin_directory` with:
   - `directory`: plugin name or path
3. Present only the returned findings.

## Rules

- Do not add manual findings.
- Keep output grouped by file and severity.
