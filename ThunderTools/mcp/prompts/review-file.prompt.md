---
name: review-file
description: Review specific Thunder plugin files for compliance
---

# Review Thunder Plugin Files

Use the **review_plugin** MCP tool to review specific C++ files against Thunder framework guidelines.

## When to Use

- User asks to review specific files
- User has files open and wants them checked
- User mentions checking "this file" or specific filenames

## How to Call

```
Call the MCP tool: review_plugin
Arguments:
  file_paths: [<file1>, <file2>, ...]
```

**Examples:**
- `review_plugin` with `file_paths: ["Dictionary1.cpp"]`
- `review_plugin` with `file_paths: ["NetworkControl.cpp", "NetworkControl.h"]`

## IMPORTANT

Only report findings that come directly from the MCP tool response. Do NOT add your own analysis or findings. Present ONLY what the tool returns.

## When to Use

- User asks to review specific files
- User has files open and wants them checked
- User mentions checking "this file" or specific filenames

## How to Call

```
Call the MCP tool: review-file
Arguments:
  file_paths: [<file1>, <file2>, ...]
```

**Examples:**
- `review-file` with `file_paths: ["Dictionary1.cpp"]`
- `review-file` with `file_paths: ["NetworkControl.cpp", "NetworkControl.h"]`
- `review-file` with `file_paths: ["ThunderNanoServices/WebProxy/WebProxy.cpp"]`

## File Path Handling

- Accept relative paths from workspace root
- Accept full paths
- Accept just filenames (will search for them)

## Output Format

Present findings as:

```markdown
# Thunder File Review

## Files Analyzed
- <filename1>
- <filename2>

## Summary
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
   - **Code**: `<code_snippet>`
   - **Issue**: <details>
   - **Fix**: <suggestion>
```

## Example Usage

**User says:** "Review Dictionary1.cpp"

**You do:**
1. Call tool `review-file` with `file_paths: ["Dictionary1.cpp"]`
2. Format and present results
3. Highlight critical issues

**User says:** "Check this file for compliance" (with file open)

**You do:**
1. Get the current file path
2. Call tool `review-file` with that file path
3. Present formatted results
