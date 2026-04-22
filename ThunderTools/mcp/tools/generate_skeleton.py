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
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class PluginConfig:
    """Plugin configuration for skeleton generation"""
    plugin_name: str
    out_of_process: bool = False
    plugin_config: bool = True
    interface_paths: List[str] = field(default_factory=list)
    output_directory: str = "."
    preconditions: List[str] = field(default_factory=list)
    terminations: List[str] = field(default_factory=list)
    controls: List[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    """Result of skeleton generation"""
    success: bool
    plugin_name: str
    output_path: Optional[Path] = None
    generated_files: List[str] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    error_message: str = ""


class GenerateSkeletonTool:
    """Generate Thunder plugin skeleton from configuration"""

    # Common subsystem names for reference in the form
    SUBSYSTEMS = [
        "PLATFORM", "NETWORK", "SECURITY", "IDENTIFIER", "INTERNET",
        "LOCATION", "TIME", "PROVISIONING", "DECRYPTION", "GRAPHICS",
        "WEBSOURCE", "STREAMING", "BLUETOOTH", "CRYPTOGRAPHY", "INSTALLATION"
    ]

    def __init__(self, base_path: Path):
        """Initialize generator with workspace base path"""
        self.base_path = base_path
        self.psg_path = Path(__file__).parent.parent.parent / "PluginSkeletonGenerator"

    def get_definition(self) -> Dict[str, Any]:
        """Get tool definition for MCP"""
        return {
            "name": "generate_skeleton",
            "description": (
                "Generate a Thunder plugin skeleton. "
                "WORKFLOW: First call this tool with mode='questionnaire' to get the list of questions. "
                "Then ask the user those questions directly in chat (one message with all questions). "
                "Once the user answers, call this tool again with mode='generate' and all parameters filled in. "
                "Do NOT use any external tools to collect answers."
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
        """Return the 8 questions as simple text that Copilot can present naturally."""
        questions_text = """# Thunder Plugin Generation Questions

Please provide answers to these 8 questions:

**1. Plugin Name**
   What should your plugin be called? (e.g., MyPlugin, Dictionary, NetworkControl)

**2. Process Mode**
   Should it run In-Process (inside WPEFramework) or Out-of-Process (separate process)?
   - In-Process: Simpler, faster, shares memory with framework
   - Out-of-Process (OOP): Isolated, more complex, needs interface files

**3. Custom Configuration**
   Does your plugin need custom JSON configuration? (Yes/No)

**4. Interface Header Paths**
   For OOP plugins: Full paths to interface .h files (one per line)
   For In-Process: Leave empty
   Example: /home/user/Thunder/ThunderInterfaces/interfaces/IMyPlugin.h

**5. Output Directory**
   Where to create the plugin folder? (leave empty for current directory)

**6. Preconditions**
   Which subsystems must be available before this plugin loads? (comma-separated, or empty)
   Available: PLATFORM, NETWORK, SECURITY, IDENTIFIER, INTERNET, LOCATION, TIME,
              PROVISIONING, DECRYPTION, GRAPHICS, WEBSOURCE, STREAMING, BLUETOOTH,
              CRYPTOGRAPHY, INSTALLATION

**7. Terminations**
   Which subsystems' shutdown should trigger this plugin to shutdown? (comma-separated, or empty)

**8. Controls**
   Which subsystems does this plugin manage? (comma-separated, or empty)

---

Please provide all 8 answers together (you can copy this list and fill in your answers)."""

        return {
            "content": [{
                "type": "text",
                "text": questions_text
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
        # Parse arguments into PluginConfig
        plugin_name = arguments.get("plugin_name")
        
        if not plugin_name:
            return {
                "content": [{
                    "type": "text",
                    "text": "❌ Error: plugin_name is required for mode='generate'."
                }]
            }
        
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
        
        # Create PluginConfig
        config = PluginConfig(
            plugin_name=plugin_name,
            out_of_process=out_of_process,
            plugin_config=plugin_config,
            interface_paths=interface_paths,
            output_directory=output_dir,
            preconditions=preconditions,
            terminations=terminations,
            controls=controls
        )
        
        # Generate using core logic
        result = self._generate_core(config)
        
        # Convert GenerationResult to MCP response
        return self._format_result(result)
    
    def _generate_core(self, config: PluginConfig) -> GenerationResult:
        """Core generation logic - uses PluginSkeletonGenerator.py"""
        # Handle empty interface paths - create dummy if needed
        interface_paths = config.interface_paths
        created_dummy = False
        
        if not interface_paths:
            dummy_interface = self._create_dummy_interface(config.plugin_name)
            interface_paths = [dummy_interface]
            created_dummy = True
        else:
            # Validate interface files exist
            missing_files = [p for p in interface_paths if not Path(p).exists()]
            if missing_files:
                return GenerationResult(
                    success=False,
                    plugin_name=config.plugin_name,
                    error_message=f"Interface files not found: {', '.join(missing_files)}"
                )
        
        # Create config YAML for PSG
        yaml_config = {
            "PluginName": config.plugin_name,
            "OutOfProcess": config.out_of_process,
            "PluginConfig": config.plugin_config,
            "Paths": interface_paths,
            "Preconditions": config.preconditions,
            "Terminations": config.terminations,
            "Controls": config.controls
        }
        
        # Write temp config
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(yaml_config, f)
            config_path = f.name
        
        try:
            # Prepare output directory
            raw_out = Path(config.output_directory)
            full_output_dir = raw_out if raw_out.is_absolute() else self.base_path / config.output_directory
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
            
            # Clean up
            os.unlink(config_path)
            if created_dummy and os.path.exists(interface_paths[0]):
                os.unlink(interface_paths[0])
            
            # Check result
            plugin_dir = full_output_dir / config.plugin_name
            
            if result.returncode == 0 and plugin_dir.exists():
                generated_files = self._list_files(plugin_dir)
                
                return GenerationResult(
                    success=True,
                    plugin_name=config.plugin_name,
                    output_path=plugin_dir,
                    generated_files=generated_files,
                    stdout=result.stdout,
                    stderr=result.stderr
                )
            else:
                return GenerationResult(
                    success=False,
                    plugin_name=config.plugin_name,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    error_message=f"Generation failed with return code {result.returncode}"
                )
        
        except subprocess.TimeoutExpired:
            os.unlink(config_path)
            if created_dummy and os.path.exists(interface_paths[0]):
                os.unlink(interface_paths[0])
            return GenerationResult(
                success=False,
                plugin_name=config.plugin_name,
                error_message="Generation timed out (>60s)"
            )
        except Exception as e:
            if os.path.exists(config_path):
                os.unlink(config_path)
            if created_dummy and os.path.exists(interface_paths[0]):
                os.unlink(interface_paths[0])
            return GenerationResult(
                success=False,
                plugin_name=config.plugin_name,
                error_message=f"Generation error: {str(e)}"
            )
    
    def _format_result(self, result: GenerationResult) -> Dict[str, Any]:
        """Convert GenerationResult to MCP response format"""
        if not result.success:
            output = f"# ❌ Plugin Generation Failed\n\n"
            output += f"**Plugin Name:** {result.plugin_name}\n\n"
            output += f"**Error:** {result.error_message}\n\n"
            
            if result.stderr:
                output += f"## Error Output\n\n```\n{result.stderr}\n```\n"
            if result.stdout:
                output += f"\n## Standard Output\n\n```\n{result.stdout}\n```\n"
        else:
            output = f"# ✅ Plugin Skeleton Generated: {result.plugin_name}\n\n"
            output += f"**Location:** `{result.output_path}`\n\n"
            output += "## Generated Files\n\n"
            output += self._format_file_list(result.generated_files)
            output += "\n\n## Next Steps\n\n"
            output += "1. Review the generated code\n"
            output += "2. Implement plugin methods in the .cpp file\n"
            output += "3. Update CMakeLists.txt if needed\n"
            output += "4. Build and test your plugin\n\n"
            output += "💡 **Tip:** Run `review_plugin_directory` to check for compliance issues.\n"
            
            if result.stdout:
                output += f"\n<details>\n<summary>Generator Output</summary>\n\n```\n{result.stdout}\n```\n</details>\n"
        
        return {
            "content": [{
                "type": "text",
                "text": output
            }]
        }
    
    def _format_file_list(self, files: List[str]) -> str:
        """Format file list for display"""
        if not files:
            return "No files generated"
        return "\n".join(f"- {f}" for f in files)
    
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
    
    def _list_files(self, plugin_dir: Path) -> List[str]:
        """List all generated files"""
        files = []
        for item in plugin_dir.rglob('*'):
            if item.is_file():
                files.append(str(item.relative_to(plugin_dir)))
        return sorted(files)
