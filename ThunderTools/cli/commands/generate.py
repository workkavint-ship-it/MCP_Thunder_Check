"""
Generate Command - Plugin Skeleton Generation

CLI command for generating Thunder plugin skeletons.
"""

import sys
from pathlib import Path
from argparse import Namespace

# Import core engine
from ThunderTools.core import SkeletonGenerator, PluginConfig


def run_generate(args: Namespace) -> int:
    """Execute the generate command"""

    # Resolve repository root from file location so CLI works from any cwd.
    workspace = Path(__file__).resolve().parents[3]
    
    # Parse mode
    out_of_process = args.mode in ['oop', 'out-of-process']
    
    # Parse lists
    interfaces = [str(_resolve_path(path, workspace)) for path in (args.interfaces or [])]
    preconditions = _parse_list(args.preconditions)
    terminations = _parse_list(args.terminations)
    controls = _parse_list(args.controls)
    output_directory = str(_resolve_path(args.output, workspace))
    
    # Create configuration
    config = PluginConfig(
        plugin_name=args.plugin_name,
        out_of_process=out_of_process,
        plugin_config=args.config,
        interface_paths=interfaces,
        output_directory=output_directory,
        preconditions=preconditions,
        terminations=terminations,
        controls=controls
    )
    
    # Create generator
    generator = SkeletonGenerator(workspace)
    
    # Generate
    result = generator.generate(config, verbose=not args.quiet)
    
    # Print result
    if result.success:
        if not args.quiet:
            print(f"\n✅ Success! Plugin generated: {result.output_path}")
            print(f"\nGenerated {len(result.generated_files)} files:")
            for file in result.generated_files:
                print(f"  - {file}")
            print(f"\n💡 Next steps:")
            print(f"  1. Implement plugin methods in {args.plugin_name}.cpp")
            print(f"  2. Build and test your plugin")
            print(f"  3. Run: python ThunderTools/core/thunder.py review --directory {result.output_path}")
        return 0
    else:
        print(f"❌ Error: {result.error_message}", file=sys.stderr)
        if result.stderr:
            print(f"\nDetails:\n{result.stderr}", file=sys.stderr)
        return 1


def _parse_list(value: str) -> list:
    """Parse comma-separated string to list"""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]


def _resolve_path(path_value: str, workspace: Path) -> Path:
    """Resolve user-provided path as absolute or workspace-relative."""
    path = Path(path_value)
    return path if path.is_absolute() else workspace / path
