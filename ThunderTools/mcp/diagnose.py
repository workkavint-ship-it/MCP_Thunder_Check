# MCP Debugging Script for VS Code

import sys
import json
from pathlib import Path

# Add workspace to path
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WORKSPACE_ROOT))

print("=" * 70)
print("Thunder MCP Server Diagnostic")
print("=" * 70)
print()

# Test 1: Import server
print("Test 1: Importing MCP server...")
try:
    from ThunderTools.mcp.server import ThunderToolsServer
    print("✅ Server imports successfully")
except Exception as e:
    print(f"❌ Failed to import server: {e}")
    sys.exit(1)

print()

# Test 2: Initialize server
print("Test 2: Initializing server...")
try:
    server = ThunderToolsServer()
    print(f"✅ Server initialized: {server.server_info['name']} v{server.server_info['version']}")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    sys.exit(1)

print()

# Test 3: List tools
print("Test 3: Listing available tools...")
try:
    tools_response = server.handle_list_tools()
    tools = tools_response.get('tools', [])
    print(f"✅ Found {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool['name']}")
except Exception as e:
    print(f"❌ Failed to list tools: {e}")
    sys.exit(1)

print()

# Test 4: Check VS Code settings
print("Test 4: Checking VS Code configuration...")
vscode_settings = WORKSPACE_ROOT / ".vscode" / "settings.json"
if vscode_settings.exists():
    try:
        with open(vscode_settings) as f:
            settings = json.load(f)
        
        mcp_config = settings.get("github.copilot.chat.mcp.servers", {})
        
        if "thunder-tools" in mcp_config:
            print("✅ thunder-tools server configured in settings.json")
            config = mcp_config["thunder-tools"]
            print(f"   Command: {config.get('command')}")
            print(f"   Args: {config.get('args')}")
        else:
            print("❌ thunder-tools NOT found in github.copilot.chat.mcp.servers")
    except Exception as e:
        print(f"❌ Error reading settings.json: {e}")
else:
    print("❌ .vscode/settings.json not found")

print()

# Test 5: Simulate tool call
print("Test 5: Testing tool invocation...")
try:
    test_params = {
        "name": "review_plugin_directory",
        "arguments": {
            "directory": "Dictionary1"
        }
    }
    result = server.handle_tool_call(test_params)
    print("✅ Tool invocation successful")
    print(f"   Content length: {len(result.get('content', [{}])[0].get('text', ''))} characters")
except Exception as e:
    print(f"❌ Tool invocation failed: {e}")

print()
print("=" * 70)
print("Diagnostic Summary")
print("=" * 70)
print()
print("If all tests passed, the MCP server is working correctly.")
print("If #review_plugin_directory still doesn't work in VS Code:")
print()
print("1. Check VS Code Output panel:")
print("   - View → Output")
print("   - Select 'GitHub Copilot' from dropdown")
print("   - Look for MCP-related errors")
print()
print("2. Verify you're in Agent mode:")
print("   - Open Copilot Chat")
print("   - Look at mode selector at top")
print("   - Must show 'Agent' not 'Ask' or 'Edit'")
print()
print("3. Try natural language instead:")
print("   'Review Dictionary1 plugin for compliance issues'")
print()
print("4. Restart VS Code completely:")
print("   Close all windows and reopen")
print()
print("5. Check GitHub Copilot version:")
print("   Extensions → GitHub Copilot")
print("   Make sure it's up to date")
print()
