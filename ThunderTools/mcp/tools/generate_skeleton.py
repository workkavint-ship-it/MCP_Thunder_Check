"""
Thunder Plugin Skeleton Generator Tool

MCP tool for generating Thunder plugin skeletons.

Two-mode design:
  mode="questionnaire"  → returns a single all-in-one intake form for the user to fill in
  mode="generate"       → runs PSG with all provided parameters
"""

import sys
import os
import subprocess
import tempfile
import yaml
from pathlib import Path
from typing import Any, Dict


class GenerateSkeletonTool:
    """Generate Thunder plugin skeleton from configuration"""

    # Common subsystem names for reference in the form
    SUBSYSTEMS = [
        "PLATFORM", "NETWORK", "SECURITY", "IDENTIFIER", "INTERNET",
        "LOCATION", "TIME", "PROVISIONING", "DECRYPTION", "GRAPHICS",
        "WEBSOURCE", "STREAMING", "BLUETOOTH", "CRYPTOGRAPHY", "INSTALLATION"
    ]

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.psg_path = Path(__file__).parent.parent / "PluginSkeletonGenerator"

    def get_definition(self) -> Dict[str, Any]:
        """Get tool definition for MCP"""
        return {
            "name": "generate",
            "description": (
                "Generate a Thunder plugin skeleton. "
                "WORKFLOW — you MUST follow this exactly:\n"
                "STEP 1: Call vscode_askQuestions (NOT this tool) with the interactive form "
                "containing all plugin configuration questions with dropdowns and input fields. "
                "STEP 2: Once you receive ALL answers from vscode_askQuestions, "
                "call THIS tool with mode='generate' and all parameter values filled from the answers. "
                "Do NOT ask follow-up questions. The mode='questionnaire' is ONLY for getting "
                "the question structure if needed for reference."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["questionnaire", "generate"],
                        "description": (
                            "'questionnaire' → returns the intake form to show the user. "
                            "'generate' → generates the plugin with the supplied parameters."
                        )
                    },
                    "plugin_name": {
                        "type": "string",
                        "description": "Name of the plugin (from user answer Q1)."
                    },
                    "out_of_process": {
                        "type": "boolean",
                        "description": "true = Out-of-Process (OOP), false = In-Process (from user answer Q2).",
                        "default": False
                    },
                    "plugin_config": {
                        "type": "boolean",
                        "description": "true if plugin needs custom configuration (from user answer Q3).",
                        "default": True
                    },
                    "interface_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Full absolute paths to interface .h files (from user answer Q4). "
                            "Required for OOP plugins. Pass [] if none."
                        ),
                        "default": []
                    },
                    "output_directory": {
                        "type": "string",
                        "description": "Absolute path where the plugin folder will be created (from user answer Q5).",
                        "default": "."
                    },
                    "preconditions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Subsystems required before plugin activates (from user answer Q6a). Pass [] if none.",
                        "default": []
                    },
                    "terminations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Subsystems that trigger plugin shutdown (from user answer Q6b). Pass [] if none.",
                        "default": []
                    },
                    "controls": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Subsystems this plugin manages (from user answer Q6c). Pass [] if none.",
                        "default": []
                    }
                },
                "required": ["mode"]
            }
        }
    
    # ------------------------------------------------------------------ #
    #  QUESTIONNAIRE                                                       #
    # ------------------------------------------------------------------ #
    def _questionnaire(self) -> Dict[str, Any]:
        """Return structured questions for vscode_askQuestions."""
        default_out = str(self.base_path)
        
        # Return the structure that the AI should use with vscode_askQuestions
        questions_structure = {
            "questions": [
                {
                    "header": "plugin_name",
                    "question": "Plugin Name (required) — Name for the plugin folder and class",
                    "options": []  # Free text
                },
                {
                    "header": "process_mode",
                    "question": "Process Mode — How should the plugin run?",
                    "options": [
                        {
                            "label": "In-Process",
                            "description": "Plugin runs inside the WPEFramework process",
                            "recommended": True
                        },
                        {
                            "label": "Out-of-Process (OOP)",
                            "description": "Plugin runs in its own separate process (requires interface paths)"
                        }
                    ]
                },
                {
                    "header": "plugin_config",
                    "question": "Custom Plugin Configuration — Need custom config block in JSON?",
                    "options": [
                        {
                            "label": "Yes",
                            "description": "Plugin needs custom configuration",
                            "recommended": True
                        },
                        {
                            "label": "No",
                            "description": "No custom configuration needed"
                        }
                    ]
                },
                {
                    "header": "interface_paths",
                    "question": f"Interface Header Paths — Full paths to .h files (one per line, or leave empty)\nExample: {default_out}\\ThunderInterfaces\\interfaces\\IMyPlugin.h",
                    "options": []  # Free text, multiline
                },
                {
                    "header": "output_directory",
                    "question": f"Output Directory — Where to create the plugin folder?\nDefault: {default_out}",
                    "options": []  # Free text
                },
                {
                    "header": "preconditions",
                    "question": f"Preconditions — Subsystems required before plugin activates (comma-separated or leave empty)\nAvailable: {', '.join(self.SUBSYSTEMS)}",
                    "options": []  # Free text
                },
                {
                    "header": "terminations",
                    "question": f"Terminations — Subsystems whose loss triggers plugin shutdown (comma-separated or leave empty)\nAvailable: {', '.join(self.SUBSYSTEMS)}",
                    "options": []  # Free text
                },
                {
                    "header": "controls",
                    "question": f"Controls — Subsystems this plugin manages (comma-separated or leave empty)\nAvailable: {', '.join(self.SUBSYSTEMS)}",
                    "options": []  # Free text
                }
            ]
        }
        
        return {
            "content": [{
                "type": "text",
                "text": f"USE_VSCODE_ASK_QUESTIONS\n\n{str(questions_structure)}"
            }]
        }

    # ------------------------------------------------------------------ #
    #  EXECUTE (router)                                                    #
    # ------------------------------------------------------------------ #
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to questionnaire or generate based on mode."""
        mode = arguments.get("mode", "generate")

        if mode == "questionnaire":
            return self._questionnaire()

        # mode == "generate" — fall through to skeleton generation
        return self._generate(arguments)
    
    # ------------------------------------------------------------------ #
    #  HELPERS                                                             #
    # ------------------------------------------------------------------ #
    def _parse_list(self, value: Any) -> list:
        """Parse comma-separated string or newline-separated string into list."""
        if not value:
            return []
        if isinstance(value, list):
            return value
        # Split by comma or newline, strip whitespace, filter empty
        items = []
        for item in str(value).replace('\n', ',').split(','):
            item = item.strip()
            if item and item.lower() not in ['none', 'null', 'empty', '']:
                items.append(item)
        return items

    # ------------------------------------------------------------------ #
    #  GENERATE                                                            #
    # ------------------------------------------------------------------ #
    def _generate(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the plugin skeleton using PSG."""
        plugin_name = arguments.get("plugin_name")
        
        # Parse process_mode - handle both boolean and string labels
        process_mode_raw = arguments.get("out_of_process", arguments.get("process_mode", False))
        if isinstance(process_mode_raw, str):
            out_of_process = "oop" in process_mode_raw.lower() or "out" in process_mode_raw.lower()
        else:
            out_of_process = bool(process_mode_raw)
        
        # Parse plugin_config - handle both boolean and string labels
        config_raw = arguments.get("plugin_config", True)
        if isinstance(config_raw, str):
            plugin_config = config_raw.lower() in ['yes', 'y', 'true', '1']
        else:
            plugin_config = bool(config_raw)
        
        # Parse lists - handle both arrays and comma/newline-separated strings
        interface_paths = self._parse_list(arguments.get("interface_paths", []))
        preconditions = self._parse_list(arguments.get("preconditions", []))
        terminations = self._parse_list(arguments.get("terminations", []))
        controls = self._parse_list(arguments.get("controls", []))
        
        # Parse output directory - handle "default" keyword
        output_dir = arguments.get("output_directory", ".")
        if isinstance(output_dir, str) and output_dir.lower() in ['default', '']:
            output_dir = "."

        if not plugin_name:
            return {
                "content": [{
                    "type": "text",
                    "text": "❌ Error: plugin_name is required for mode='generate'."
                }]
            }

        # Handle empty interface paths - create a minimal placeholder interface
        if not interface_paths:
            # Create a minimal dummy interface for basic skeleton
            dummy_interface = self._create_dummy_interface(plugin_name)
            interface_paths = [dummy_interface]
            created_dummy = True
        else:
            created_dummy = False
            # Validate that interface files exist
            missing_files = [p for p in interface_paths if not Path(p).exists()]
            if missing_files:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Error: Interface files not found:\n" + "\n".join(f"  - {f}" for f in missing_files) +
                                "\n\n💡 Provide full paths to interface header files in ThunderInterfaces/interfaces/"
                    }]
                }
        
        # Create config YAML
        config = {
            "PluginName": plugin_name,
            "OutOfProcess": out_of_process,
            "PluginConfig": plugin_config,
            "Paths": interface_paths,
            "Preconditions": preconditions,
            "Terminations": terminations,
            "Controls": controls
        }
        
        # Write to temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            # Prepare output directory — honour absolute paths from the user
            raw_out = Path(output_dir)
            full_output_dir = raw_out if raw_out.is_absolute() else self.base_path / output_dir
            full_output_dir.mkdir(parents=True, exist_ok=True)

            # Run PluginSkeletonGenerator
            psg_script = self.psg_path / "PluginSkeletonGenerator.py"
            
            result = subprocess.run(
                [sys.executable, str(psg_script), "--config", config_path],
                cwd=str(full_output_dir),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up temp files
            os.unlink(config_path)
            if created_dummy and os.path.exists(interface_paths[0]):
                os.unlink(interface_paths[0])
            
            # Check for generated plugin directory
            plugin_dir = full_output_dir / plugin_name
            
            if result.returncode == 0 and plugin_dir.exists():
                # Success
                generated_files = self._list_files(plugin_dir)
                
                output = f"# ✅ Plugin Skeleton Generated: {plugin_name}\n\n"
                output += f"**Location:** `{full_output_dir / plugin_name}`\n"
                output += f"**Mode:** {'Out-of-Process (OOP)' if out_of_process else 'In-Process'}\n\n"
                if created_dummy:
                    output += "⚠️ **Note:** Generated with minimal interface (no custom interfaces specified)\n\n"
                output += "## Generated Files\n\n"
                output += generated_files
                output += "\n\n## Next Steps\n\n"
                output += "1. Review the generated code\n"
                output += "2. Implement plugin methods in the .cpp file\n"
                output += "3. Update CMakeLists.txt if needed\n"
                output += "4. Build and test your plugin\n\n"
                output += "💡 **Tip:** Run `review_plugin_directory` to check for compliance issues.\n"
                
                if result.stdout:
                    output += f"\n<details>\n<summary>Generator Output</summary>\n\n```\n{result.stdout}\n```\n</details>\n"
                
            else:
                # Failure
                output = f"# ❌ Plugin Generation Failed\n\n"
                output += f"**Plugin Name:** {plugin_name}\n\n"
                
                if result.stderr:
                    output += f"## Error Output\n\n```\n{result.stderr}\n```\n"
                if result.stdout:
                    output += f"\n## Standard Output\n\n```\n{result.stdout}\n```\n"
                
                output += f"\n**Return Code:** {result.returncode}\n"
            
            return {
                "content": [{
                    "type": "text",
                    "text": output
                }]
            }
            
        except subprocess.TimeoutExpired:
            os.unlink(config_path)
            if created_dummy and os.path.exists(interface_paths[0]):
                os.unlink(interface_paths[0])
            return {
                "content": [{
                    "type": "text",
                    "text": "❌ Error: Plugin generation timed out (>60s)"
                }]
            }
        except Exception as e:
            if os.path.exists(config_path):
                os.unlink(config_path)
            if created_dummy and os.path.exists(interface_paths[0]):
                os.unlink(interface_paths[0])
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Error generating plugin: {str(e)}"
                }]
            }
    
    def _create_dummy_interface(self, plugin_name: str) -> str:
        """Create a minimal dummy interface for basic skeleton generation"""
        interface_content = f"""#pragma once

#include "Module.h"

namespace Thunder {{
namespace Exchange {{

    struct I{plugin_name} : virtual public Core::IUnknown {{
        enum {{ ID = 0x00000000 }};

        virtual ~I{plugin_name}() = default;

        // Add your interface methods here
    }};

}} // namespace Exchange
}} // namespace Thunder
"""
        # Create temp interface file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.h', delete=False, prefix=f'I{plugin_name}_') as f:
            f.write(interface_content)
            return f.name
    
    def _list_files(self, plugin_dir: Path) -> str:
        """List all generated files in tree format"""
        output = []
        
        def add_tree(path: Path, prefix: str = ""):
            try:
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    output.append(f"{prefix}{current_prefix}{item.name}")
                    
                    if item.is_dir() and not item.name.startswith('.'):
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        add_tree(item, next_prefix)
            except PermissionError:
                pass
        
        output.append(f"📁 {plugin_dir.name}/")
        add_tree(plugin_dir)
        
        return "\n".join(output)
