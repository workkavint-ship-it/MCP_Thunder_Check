---
name: review-file
description: Review specific Thunder plugin files for compliance
---

# Review Thunder Plugin Files

Use the MCP tool `review_plugin`.

## Required Workflow

1. Ask for file path(s) if missing.
2. Call `review_plugin` with:
   - `file_paths`: array of files
3. Present only the returned findings.

## Rules

- Do not add manual findings.
- Keep output grouped by file and severity.
