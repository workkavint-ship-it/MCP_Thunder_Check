#!/usr/bin/env python3
"""
Thunder Tools MCP Setup Helper

Generates platform-specific MCP configuration for Thunder Tools.
Run this in your Thunder_MCP directory to get the right config.
"""

import sys
import os
import json
from pathlib import Path
import platform


def get_mcp_server_path():
    """Get absolute path to MCP server"""
    script_dir = Path(__file__).parent
    mcp_server = script_dir / "server.py"
    return str(mcp_server.absolute())


def get_config_locations():
    """Get MCP config file locations for different clients"""
    system = platform.system()
    home = Path.home()
    
    locations = {
        "Claude Desktop": None,
        "VS Code": ".vscode/settings.json (in workspace)",
        "Cursor": None,
    }
    
    if system == "Windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            locations["Claude Desktop"] = f"{appdata}\\Claude\\claude_desktop_config.json"
            locations["Cursor"] = f"{appdata}\\Cursor\\mcp_settings.json"
    elif system == "Darwin":  # macOS
        locations["Claude Desktop"] = f"{home}/Library/Application Support/Claude/claude_desktop_config.json"
        locations["Cursor"] = f"{home}/.cursor/mcp_settings.json"
    else:  # Linux
        locations["Claude Desktop"] = f"{home}/.config/Claude/claude_desktop_config.json"
        locations["Cursor"] = f"{home}/.cursor/mcp_settings.json"
    
    return locations


def generate_config(client_type):
    """Generate MCP configuration for specific client"""
    mcp_path = get_mcp_server_path()
    
    if client_type == "vscode":
        return {
            "github.copilot.chat.mcp.servers": {
                "thunder-tools": {
                    "command": "python",
                    "args": ["${workspaceFolder}/ThunderTools/mcp/server.py"]
                }
            }
        }
    else:  # Generic (Claude Desktop, Cursor, etc.)
        # Use forward slashes for cross-platform compatibility
        mcp_path_forward = mcp_path.replace("\\", "/")
        return {
            "mcpServers": {
                "thunder-tools": {
                    "command": "python",
                    "args": [mcp_path_forward]
                }
            }
        }


def main():
    """Main setup helper"""
    print("=" * 70)
    print("  Thunder Tools MCP Setup Helper")
    print("=" * 70)
    print()
    
    mcp_path = get_mcp_server_path()
    locations = get_config_locations()
    
    print(f"🔍 Detected MCP Server Path:\n   {mcp_path}\n")
    
    print("📋 Select your AI client:")
    print()
    print("  1. Claude Desktop (universal, works everywhere)")
    print("  2. VS Code with GitHub Copilot")
    print("  3. Cursor Editor")
    print("  4. Other MCP Client (generic config)")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    print()
    
    configs = {
        "1": ("claude", "Claude Desktop"),
        "2": ("vscode", "VS Code"),
        "3": ("cursor", "Cursor"),
        "4": ("generic", "Generic MCP Client")
    }
    
    if choice not in configs:
        print("❌ Invalid choice")
        return 1
    
    config_type, client_name = configs[choice]
    config = generate_config(config_type)
    
    print("=" * 70)
    print(f"✅ Configuration for: {client_name}")
    print("=" * 70)
    print()
    
    # Show config location
    if config_type in ["claude", "cursor"]:
        location = locations.get(client_name)
        if location:
            print(f"📁 Config File Location:\n   {location}\n")
            
            # Check if file exists
            if os.path.exists(location):
                print("   ⚠️  File exists - you'll need to merge this config\n")
            else:
                print("   📝 File doesn't exist - you can create it with this content\n")
    elif config_type == "vscode":
        print(f"📁 Config File Location:\n   .vscode/settings.json (in your workspace)\n")
        workspace_settings = Path(".vscode/settings.json")
        if workspace_settings.exists():
            print("   ✅ Already configured in this workspace!\n")
    
    # Show the config
    print("📄 Configuration to add:")
    print("-" * 70)
    print(json.dumps(config, indent=2))
    print("-" * 70)
    print()
    
    # Instructions
    print("📝 Next Steps:")
    print()
    
    if config_type == "claude":
        print("  1. Open (or create) the config file shown above")
        print("  2. Add the configuration JSON")
        print("  3. Restart Claude Desktop")
        print("  4. Test: Ask 'What tools are available?'")
    elif config_type == "vscode":
        print("  1. Open .vscode/settings.json in your workspace")
        print("  2. Add the configuration JSON")
        print("  3. Restart VS Code")
        print("  4. Test: In Copilot Chat, use #review_plugin_directory Dictionary1")
        print()
        print("  💡 Use # syntax to call tools directly:")
        print("     - #review_plugin_directory Dictionary")
        print("     - #review_plugin Dictionary.cpp")
        print("     - #generate_skeleton")
    elif config_type == "cursor":
        print("  1. Open (or create) the config file shown above")
        print("  2. Add the configuration JSON")
        print("  3. Restart Cursor")
        print("  4. Test: Ask 'What tools are available?'")
    else:
        print("  1. Find your MCP client's configuration file")
        print("  2. Add the configuration JSON above")
        print("  3. Restart your client")
        print("  4. Test: Ask 'What tools are available?'")
    
    print()
    print("🔧 Troubleshooting:")
    print("   - Ensure Python is in PATH: python --version")
    print("   - Install PyYAML: pip install pyyaml")
    print("   - See MCP_SETUP.md for detailed help")
    print()
    
    # Option to save config
    if config_type == "vscode":
        save_choice = input("💾 Save to .vscode/settings.json? (y/n): ").strip().lower()
        if save_choice == 'y':
            vscode_dir = Path(".vscode")
            vscode_dir.mkdir(exist_ok=True)
            settings_file = vscode_dir / "settings.json"
            
            # Merge if exists
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    existing = json.load(f)
                existing.update(config)
                config = existing
            
            with open(settings_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Saved to {settings_file}")
            print("   Restart VS Code to use the Thunder Tools!")
            print()
            print("   💡 Use # syntax in Copilot Chat:")
            print("      - #review_plugin_directory Dictionary")
            print("      - #review_plugin Dictionary.cpp")
            print("      - #generate_skeleton")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
