"""
Thunder Tools MCP Server

Clean, modular MCP server following Anthropic best practices.
Each tool is in its own file under tools/
"""

import sys
import json
from pathlib import Path
from typing import Any, Dict

# Ensure workspace root is on sys.path so absolute imports like
# `from ThunderTools.core import ...` work when launching this file directly.
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

# Import tool classes
from ThunderTools.mcp.tools.review_plugin import ReviewPluginTool
from ThunderTools.mcp.tools.review_directory import ReviewDirectoryTool
from ThunderTools.mcp.tools.generate_skeleton import GenerateSkeletonTool


class ThunderToolsServer:
    """MCP Server for Thunder development tools"""
    
    def __init__(self):
        self.server_info = {
            "name": "thunder-tools",
            "version": "1.0.0"
        }
        
        # Base path for workspace
        self.base_path = Path(__file__).parents[2]
        
        # Initialize tools
        self.tools = {
            "review_file": ReviewPluginTool(self.base_path),
            "review": ReviewDirectoryTool(self.base_path),
            "generate": GenerateSkeletonTool(self.base_path)
        }
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": self.server_info,
            "capabilities": {
                "tools": {}
            }
        }
    
    def handle_list_tools(self) -> Dict[str, Any]:
        """List all available tools"""
        tool_definitions = [
            tool.get_definition() for tool in self.tools.values()
        ]
        
        return {
            "tools": tool_definitions
        }
    
    def handle_tool_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool = self.tools[tool_name]
        return tool.execute(arguments)
    
    def run(self):
        """Run the MCP server (stdio transport)"""
        sys.stderr.write("Thunder Tools MCP Server started\n")
        sys.stderr.flush()
        
        for line in sys.stdin:
            try:
                line = line.strip()
                if not line:
                    continue
                
                request = json.loads(line)
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")
                
                try:
                    if method == "initialize":
                        result = self.handle_initialize(params)
                    elif method == "tools/list":
                        result = self.handle_list_tools()
                    elif method == "tools/call":
                        result = self.handle_tool_call(params)
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32601,
                                "message": f"Method not found: {method}"
                            }
                        }
                        print(json.dumps(response), flush=True)
                        continue
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                    print(json.dumps(response), flush=True)
                    
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": str(e)
                        }
                    }
                    print(json.dumps(response), flush=True)
                    
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                sys.stderr.write(f"Error: {str(e)}\n")
                sys.stderr.flush()


def main():
    """Main entry point"""
    server = ThunderToolsServer()
    server.run()


if __name__ == "__main__":
    main()
