---
name: generate
description: Generate a Thunder plugin skeleton with proper structure
---

# Generate Thunder Plugin Skeleton

When the user asks to generate/create a Thunder plugin (e.g., "Generate a plugin", "Create MediaController", "Build a new Thunder plugin"):

## Workflow - MUST Follow This Sequence

### Step 1: Gather Information
**Call `vscode_askQuestions`** with these questions (all in ONE call):

1. **Plugin Name** (required)
   - Question: "Plugin Name (required) — Name for the plugin folder and class"
   - Free text input

2. **Process Mode**
   - Question: "Process Mode — How should the plugin run?"
   - Options:
     * "In-Process" (recommended) - Plugin runs inside WPEFramework process
     * "Out-of-Process (OOP)" - Plugin runs in separate process (requires interfaces)

3. **Custom Configuration**
   - Question: "Custom Plugin Configuration — Need custom config block in JSON?"
   - Options:
     * "Yes" (recommended) - Plugin needs custom configuration
     * "No" - No custom configuration needed

4. **Interface Paths** (optional, required for OOP)
   - Question: "Interface Header Paths — Full paths to .h files (one per line, or leave empty)"
   - Example: `C:\Thunder_MCP\ThunderInterfaces\interfaces\IMyPlugin.h`
   - Free text, multiline

5. **Output Directory**
   - Question: "Output Directory — Where to create the plugin folder?"
   - Default: Current workspace root
   - Free text

6. **Preconditions** (optional)
   - Question: "Preconditions — Subsystems required before plugin activates (comma-separated)"
   - Available: PLATFORM, NETWORK, SECURITY, TIME, etc.
   - Free text

7. **Terminations** (optional)
   - Question: "Terminations — Subsystems whose loss triggers shutdown (comma-separated)"
   - Free text

8. **Controls** (optional)
   - Question: "Controls — Subsystems this plugin manages (comma-separated)"
   - Free text

### Step 2: Generate Plugin
After receiving ALL answers, **call the MCP tool `generate`**:

```javascript
generate({
  mode: "generate",
  plugin_name: "<answer-1>",
  out_of_process: <true if OOP, false otherwise>,
  plugin_config: <true if Yes, false if No>,
  interface_paths: [<array from answer-4>],
  output_directory: "<answer-5>",
  preconditions: [<array from answer-6>],
  terminations: [<array from answer-7>],
  controls: [<array from answer-8>]
})
```

## Output Format
After generation, show:
1. ✅ **Success message** with plugin location
2. **Generated files** (tree structure)
3. **Next steps**:
   - Review the generated code
   - Implement plugin methods
   - Update CMakeLists.txt if needed
   - Build and test

## Example Interaction
```
User: "Generate a Thunder plugin called MediaController"

AI: [Calls vscode_askQuestions with all 8 questions]

User: [Provides answers through VS Code UI]

AI: [Calls generate tool with all parameters]

Output:
✅ Plugin Skeleton Generated: MediaController

Location: `Thunder_MCP/MediaController`
Mode: In-Process

Generated Files:
📁 MediaController/
├── MediaController.cpp
├── MediaController.h
├── MediaControllerJsonRpc.cpp
├── Module.cpp
├── Module.h
└── CMakeLists.txt

Next Steps:
1. Review the generated code
2. Implement plugin methods in MediaController.cpp
3. Build and test your plugin
4. Run review to check for compliance issues
```

## Important Rules
- ✅ MUST ask ALL questions in ONE vscode_askQuestions call
- ✅ MUST wait for user answers before calling generate
- ✅ Do NOT ask follow-up questions one-by-one
- ✅ Include helpful examples in question text
- ❌ Never call generate without full parameters
- ❌ Never skip vscode_askQuestions step
- ❌ Never generate code manually

## Common Subsystems Reference
For questions 6-8, these are common Thunder subsystems:
- PLATFORM - Platform initialization required
- NETWORK - Network connectivity required
- SECURITY - Security subsystem
- IDENTIFIER - Device identification
- TIME - Time synchronization
- GRAPHICS - Graphics subsystem
- BLUETOOTH - Bluetooth connectivity
