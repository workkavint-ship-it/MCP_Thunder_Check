"""
Thunder Plugin Skeleton Generator

Core logic for generating Thunder plugin skeletons using PluginSkeletonGenerator.
"""

import sys
import os
import subprocess
import tempfile
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PluginConfig:
    """Plugin configuration for skeleton generation"""
    plugin_name: str
    out_of_process: bool = False
    plugin_config: bool = True
    interface_paths: List[str] = None
    output_directory: str = "."
    preconditions: List[str] = None
    terminations: List[str] = None
    controls: List[str] = None
    
    def __post_init__(self):
        if self.interface_paths is None:
            self.interface_paths = []
        if self.preconditions is None:
            self.preconditions = []
        if self.terminations is None:
            self.terminations = []
        if self.controls is None:
            self.controls = []


@dataclass
class GenerationResult:
    """Result of skeleton generation"""
    success: bool
    plugin_name: str
    output_path: Optional[Path] = None
    generated_files: List[str] = None
    stdout: str = ""
    stderr: str = ""
    error_message: str = ""
    
    def __post_init__(self):
        if self.generated_files is None:
            self.generated_files = []


class SkeletonGenerator:
    """Core skeleton generator - uses PluginSkeletonGenerator.py"""
    
    SUBSYSTEMS = [
        "PLATFORM", "NETWORK", "SECURITY", "IDENTIFIER", "INTERNET",
        "LOCATION", "TIME", "PROVISIONING", "DECRYPTION", "GRAPHICS",
        "WEBSOURCE", "STREAMING", "BLUETOOTH", "CRYPTOGRAPHY", "INSTALLATION"
    ]
    
    def __init__(self, base_path: Path):
        """Initialize generator with workspace base path"""
        self.base_path = base_path
        self.psg_path = base_path / "ThunderTools" / "PluginSkeletonGenerator"
    
    def generate(self, config: PluginConfig, verbose: bool = True) -> GenerationResult:
        """Generate plugin skeleton based on configuration"""
        
        # Validate
        if not config.plugin_name:
            return GenerationResult(
                success=False,
                plugin_name="",
                error_message="Plugin name is required"
            )
        
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
            
            if verbose:
                print(f"Generating plugin: {config.plugin_name}")
                print(f"Output directory: {full_output_dir}")
            
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
                
                if verbose:
                    print(f"✓ Plugin generated successfully at {plugin_dir}")
                
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
    
    def _create_dummy_interface(self, plugin_name: str) -> str:
        """Create minimal dummy interface for basic skeleton"""
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
