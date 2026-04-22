---
name: generate
description: Generate a new Thunder plugin skeleton with proper structure
---

# Generate Thunder Plugin Skeleton

Use the **generate** or **generate_skeleton** MCP tool to create a new Thunder plugin with proper structure and boilerplate.

## When to Use

- User wants to create a new Thunder plugin
- User asks to scaffold or generate a plugin
- User needs plugin skeleton code

## Two-Step Workflow (REQUIRED)

### Step 1: Collect Information with vscode_askQuestions

**ALWAYS use vscode_askQuestions FIRST** to gather all plugin configuration:

```javascript
vscode_askQuestions({
  questions: [
    {
      header: "Plugin Name",
      question: "What is the plugin name? (e.g., MyPlugin)",
      // No options = freeform text
    },
    {
      header: "Plugin Namespace",
      question: "What namespace should the plugin use? (e.g., Plugin)",
      // No options = freeform text
    },
    {
      header: "JSON-RPC Support",
      question: "Does this plugin need JSON-RPC interface?",
      options: [
        { label: "Yes", recommended: true },
        { label: "No" }
      ]
    },
    {
      header: "COM-RPC Interface",
      question: "Does this plugin need a COM-RPC interface?",
      options: [
        { label: "Yes", recommended: true },
        { label: "No" }
      ]
    },
    {
      header: "Preconditions",
      question: "Select required subsystems (comma-separated or multiple selection)",
      multiSelect: true,
      options: [
        { label: "PLATFORM" },
        { label: "NETWORK" },
        { label: "SECURITY" },
        { label: "INTERNET" },
        { label: "GRAPHICS" },
        { label: "None", recommended: true }
      ]
    },
    {
      header: "Output Location",
      question: "Where should the plugin be generated?",
      options: [
        { label: "ThunderNanoServices", recommended: true },
        { label: "Custom path" }
      ]
    }
  ]
})
```

### Step 2: Call generate Tool

After receiving ALL answers, call the tool:

```
Call the MCP tool: generate
Arguments:
  mode: "generate"
  plugin_name: <from answers>
  plugin_namespace: <from answers>
  jsonrpc: <true/false from answers>
  comrpc: <true/false from answers>
  preconditions: <array from answers, e.g., ["PLATFORM", "NETWORK"]>
  outdir: <from answers>
```

## DO NOT Skip the Form

**Never ask follow-up questions one-by-one.** Use the vscode_askQuestions form to collect everything at once.

## Output Format

After generation succeeds:

```markdown
# ✅ Thunder Plugin Generated: <PluginName>

## Generated Files

- `<PluginName>.h` - Plugin interface
- `<PluginName>.cpp` - Implementation
- `<PluginName>JsonRpc.cpp` - JSON-RPC interface (if enabled)
- `I<PluginName>.h` - COM-RPC interface (if enabled)
- `Module.h/cpp` - Module registration
- `CMakeLists.txt` - Build configuration
- `<PluginName>.json` - Plugin metadata

## Location
`<output_path>`

## Next Steps

1. Review generated code
2. Implement plugin logic in `<PluginName>::Initialize()`
3. Add methods to JSON-RPC interface (if applicable)
4. Update CMakeLists.txt if needed
5. Build: `cmake --build build`
```

## Example Usage

**User says:** "Generate a new Thunder plugin"

**You do:**
1. Call `vscode_askQuestions` with the full form above
2. Wait for user to fill in all fields
3. Call tool `generate` with mode="generate" and all parameters
4. Present formatted success message with generated files

**User says:** "Create a plugin called NetworkMonitor with JSON-RPC"

**You do:**
1. Still use vscode_askQuestions (pre-fill known values if possible)
2. Call generate tool with all parameters
3. Show results
