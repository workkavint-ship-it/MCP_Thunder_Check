---
name: review
description: Review an entire Thunder plugin directory for compliance issues
---

# Review Thunder Plugin Directory

Use the **review-dir** or **review_plugin_directory** MCP tool to review all C++ files in a Thunder plugin directory.

## When to Use

- User asks to review a plugin
- User wants to check compliance for an entire plugin directory
- User mentions checking "Dictionary", "NetworkControl", or other Thunder plugins

## How to Call

```
Call the MCP tool: review-dir
Arguments:
  directory: <plugin_name_or_path>
```

**Examples:**
- `review-dir Dictionary1`
- `review-dir NetworkControl`
- `review-dir ThunderNanoServices/WebProxy`

## Auto-Resolution

The tool automatically finds plugins in:
- `ThunderNanoServices/<plugin_name>`
- `Thunder/Source/plugins/<plugin_name>`

You can pass just the plugin name (e.g., "Dictionary1") or a full path.

## Output Format

Present findings as:

```markdown
# Thunder Plugin Review: <Plugin Name>

## Summary
- Files reviewed: <count>
- Files with issues: <count>
- Total findings: <count>

### By Severity
- 🔴 **CRITICAL**: <count>
- 🟠 **HIGH**: <count>
- 🟡 **MEDIUM**: <count>
- ⚪ **LOW**: <count>

## Detailed Findings

### <filename>

1. **<RULE_ID>**: <description>
   - **Severity**: <emoji> <level>
   - **Line**: <line_number>
   - **Issue**: <details>
   - **Fix**: <suggestion>
```

## Example Usage

**User says:** "Review Dictionary1 plugin"

**You do:**
1. Call tool `review-dir` with argument `directory: "Dictionary1"`
2. Format and present the results
3. Summarize critical issues at the top

**User says:** "Check NetworkControl for compliance"

**You do:**
1. Call tool `review-dir` with argument `directory: "NetworkControl"`
2. Present formatted results
