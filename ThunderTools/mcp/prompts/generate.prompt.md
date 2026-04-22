---
name: generate
description: Generate a new Thunder plugin skeleton
---

# Generate Thunder Plugin Skeleton

When the user runs `/generate`, immediately call `vscode_askQuestions` with all 8 questions in ONE call, then generate the plugin.

## Workflow

### Step 1: Call vscode_askQuestions (Required First Step)

Call `vscode_askQuestions` with these 8 questions in a single call:

```json
{
  "questions": [
    {
      "header": "plugin_name",
      "question": "Plugin Name — What should your plugin be called?",
      "options": []
    },
    {
      "header": "process_mode",
      "question": "Process Mode — How should the plugin run?",
      "options": [
        {
          "label": "In-Process",
          "description": "Runs inside WPEFramework process (simpler, faster)",
          "recommended": true
        },
        {
          "label": "Out-of-Process (OOP)",
          "description": "Runs in separate process (isolated, needs interfaces)"
        }
      ]
    },
    {
      "header": "plugin_config",
      "question": "Custom Configuration — Does plugin need custom JSON config?",
      "options": [
        {
          "label": "Yes",
          "description": "Plugin needs custom configuration block",
          "recommended": true
        },
        {
          "label": "No",
          "description": "No custom configuration needed"
        }
      ]
    },
    {
      "header": "interface_paths",
      "question": "Interface Header Paths — Full paths to .h files (one per line, or leave empty for In-Process)",
      "options": []
    },
    {
      "header": "output_directory",
      "question": "Output Directory — Where to create the plugin folder? (leave empty for workspace root)",
      "options": []
    },
    {
      "header": "preconditions",
      "question": "Preconditions — Subsystems required before activation (comma-separated)\nAvailable: PLATFORM, NETWORK, SECURITY, IDENTIFIER, INTERNET, LOCATION, TIME, PROVISIONING, DECRYPTION, GRAPHICS, WEBSOURCE, STREAMING, BLUETOOTH, CRYPTOGRAPHY, INSTALLATION",
      "options": []
    },
    {
      "header": "terminations",
      "question": "Terminations — Subsystems whose loss triggers shutdown (comma-separated)",
      "options": []
    },
    {
      "header": "controls",
      "question": "Controls — Subsystems this plugin manages (comma-separated)",
      "options": []
    }
  ]
}
```

### Step 2: Call generate_skeleton MCP Tool

After receiving all answers from `vscode_askQuestions`, call the `generate_skeleton` MCP tool with:

```json
{
  "mode": "generate",
  "plugin_name": "<answer from plugin_name>",
  "out_of_process": true if process_mode contains "Out-of-Process", else false,
  "plugin_config": true if plugin_config is "Yes", else false,
  "interface_paths": split interface_paths by newlines into array (empty -> []),
  "output_directory": "<answer from output_directory>" or ".",
  "preconditions": split preconditions by comma into array (empty -> []),
  "terminations": split terminations by comma into array (empty -> []),
  "controls": split controls by comma into array (empty -> [])
}
```

### Step 3: Present Results

Show the generation results from the tool, including:
- Success/failure status
- Generated files list
- Output directory path
- Next steps for the user

## Critical Rules

- **MUST** call `vscode_askQuestions` first with all 8 questions in ONE call
- **MUST** wait for user to complete the form before calling `generate_skeleton`
- Do **NOT** ask questions in chat messages
- Do **NOT** make multiple separate calls to collect answers
- Do **NOT** skip any of the 8 questions
---
name: generate
description: Generate a new Thunder plugin skeleton with questionnaire mode
---

# Generate Thunder Plugin Skeleton

Use the MCP tool `generate_skeleton`.

## Required Workflow

1. Call `generate_skeleton` with:
   - `mode: "questionnaire"`

2. Show the returned questionnaire to the user in one message and collect all answers.

3. Call `generate_skeleton` with:
   - `mode: "generate"`
   - `plugin_name`
   - `out_of_process`
   - `plugin_config`
   - `interface_paths`
   - `output_directory`
   - `preconditions`
   - `terminations`
   - `controls`

## Rules

- Always run questionnaire mode first.
- Do not skip any of the 8 answers.
- Convert comma-separated user answers into arrays for list fields.
- Return only the tool output for generation results.
