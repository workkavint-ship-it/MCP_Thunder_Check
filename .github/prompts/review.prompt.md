---
name: review
description: Review a Thunder plugin directory for C++ compliance issues
---

# Review Thunder Plugin

When the user asks to review a Thunder plugin (e.g., "Review Dictionary", "Check NetworkControl", "Analyze BluetoothAudio"):

## Required Action
**MUST call the MCP tool `review`** - Do NOT generate analysis manually.

## Tool Arguments
- `directory`: Plugin name (e.g., "Dictionary") or path (e.g., "ThunderNanoServices/Dictionary")
- `recursive`: true (default)

## Accepted Input Formats
The tool auto-resolves plugin names:
- Simple name: "Dictionary" → finds in ThunderNanoServices/Dictionary
- Partial path: "ThunderNanoServices/NetworkControl" → uses as-is
- Full path: "Thunder/Source/plugins/MyPlugin" → uses as-is

## Output Format
Present results with:
1. **Summary** - Files reviewed, total issues, severity breakdown
2. **Critical Issues** (🔴) - Must be fixed before production
3. **High Issues** (🟠) - Should be fixed soon
4. **Medium Issues** (🟡) - Recommended improvements
5. **Low Issues** (⚪) - Optional enhancements

For each finding, show:
- Rule ID and name
- Line number and code snippet
- Description of the issue
- Suggested fix (if available)

## Example Usage
```
User: "Review Dictionary"
→ Call: review(directory="Dictionary", recursive=true)

User: "Check NetworkControl for critical issues only"
→ Call: review(directory="NetworkControl", recursive=true)
→ Filter output to show only 🔴 CRITICAL findings

User: "Analyze BluetoothAudio"
→ Call: review(directory="BluetoothAudio", recursive=true)
```

## Important Rules
- ✅ Always call the tool - don't analyze manually
- ✅ Show severity icons (🔴🟠🟡⚪)
- ✅ Group by severity level
- ✅ Include line numbers for navigation
- ❌ Never skip calling the tool
- ❌ Never fabricate review results
