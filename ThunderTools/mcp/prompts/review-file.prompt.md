---
name: review-file
description: Review specific C++ files for Thunder compliance
---

# Review Specific Thunder Plugin Files

When the user asks to review specific C++ files (e.g., "Review Dictionary.cpp", "Check this file", "Analyze MyPlugin.h and MyPlugin.cpp"):

## Required Action
**MUST call the MCP tool `review_file`** - Do NOT generate analysis manually.

## Tool Arguments
- `file_paths`: Array of file paths relative to workspace root
- `include_guidelines`: false (set to true if user asks for full guidelines)

## Input Examples
```
User: "Review Dictionary.cpp"
→ file_paths: ["ThunderNanoServices/Dictionary/Dictionary.cpp"]

User: "Check these files: Dictionary.h and Dictionary.cpp"
→ file_paths: [
    "ThunderNanoServices/Dictionary/Dictionary.h",
    "ThunderNanoServices/Dictionary/Dictionary.cpp"
  ]

User: "Review this file" (when file is open in editor)
→ file_paths: [<current-file-path>]
```

## Output Format
For each file, show:
1. **File name** and line count
2. **Findings grouped by severity**:
   - 🔴 CRITICAL - Must fix immediately
   - 🟠 HIGH - Should fix soon
   - 🟡 MEDIUM - Recommended
   - ⚪ LOW - Optional

For each finding:
- **Rule ID**: e.g., LIFECYCLE_003
- **Rule Name**: e.g., "No activation logic in constructor"
- **Location**: Line number and column
- **Issue**: Clear description
- **Code**: The problematic code snippet
- **Fix**: Suggested correction (if available)

## Example Usage
```
User: "Review Dictionary.cpp"
→ Call: review_file(file_paths=["ThunderNanoServices/Dictionary/Dictionary.cpp"])

User: "Check this file for compliance"
→ Call: review_file(file_paths=["<current-file-path>"])
```

## Important Rules
- ✅ Always call the tool - don't analyze manually
- ✅ Show severity icons
- ✅ Include actionable fix suggestions
- ✅ Provide line numbers for navigation
- ❌ Never skip calling the tool
- ❌ Never fabricate findings
