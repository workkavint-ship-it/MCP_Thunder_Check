#!/usr/bin/env python3
"""
Thunder Plugin Reviewer MCP Server

An MCP server that provides Thunder plugin code review functionality.
Exposes tools for reviewing C++ plugins against Thunder framework guidelines.

Usage:
    python mcp_server.py
"""

import sys
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

# Import the review functionality
from review_plugin import PluginReviewer, ReviewResult, Severity


class ThunderReviewMCPServer:
    """MCP Server for Thunder Plugin Review"""
    
    def __init__(self):
        self.server_info = {
            "name": "thunder-plugin-reviewer",
            "version": "1.0.0"
        }
        
        # Initialize reviewer with rules file
        rules_file = Path(__file__).parent / "review_rules.yml"
        self.reviewer = PluginReviewer(rules_file)
        
        # Base path for Thunder workspace
        self.base_path = Path(__file__).parent.parent.parent  # Thunder_MCP root
    
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
        """List available tools"""
        return {
            "tools": [
                {
                    "name": "review_plugin",
                    "description": "Review Thunder plugin files for compliance with framework guidelines. Checks C++ files against 50+ rules covering lifecycle, reference counting, JSON-RPC, threading, and code style.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "file_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of C++ file paths to review (relative to Thunder workspace root)"
                            }
                        },
                        "required": ["file_paths"]
                    }
                },
                {
                    "name": "review_plugin_directory",
                    "description": "Review all C++ files in a plugin directory. Recursively scans for .cpp and .h files and checks them against Thunder framework guidelines.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory path to review (e.g., 'ThunderNanoServices/NetworkControl')"
                            },
                            "recursive": {
                                "type": "boolean",
                                "description": "Recursively review subdirectories",
                                "default": True
                            }
                        },
                        "required": ["directory"]
                    }
                },
                {
                    "name": "get_review_summary",
                    "description": "Get a summary of review findings by severity. Returns counts of critical, high, medium, and low severity issues.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory path to review"
                            }
                        },
                        "required": ["directory"]
                    }
                }
            ]
        }
    
    async def handle_tool_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "review_plugin":
            return await self.review_plugin(arguments)
        elif tool_name == "review_plugin_directory":
            return await self.review_plugin_directory(arguments)
        elif tool_name == "get_review_summary":
            return await self.get_review_summary(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def review_plugin(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Review specific plugin files"""
        file_paths = args.get("file_paths", [])
        
        if not file_paths:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: No file paths provided"
                    }
                ]
            }
        
        results = []
        for file_path in file_paths:
            full_path = self.base_path / file_path
            if not full_path.exists():
                results.append(f"File not found: {file_path}")
                continue
            
            result = self.reviewer.review_file(str(full_path))
            results.append(self._format_review_result(result, file_path))
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": "\n\n".join(results)
                }
            ]
        }
    
    async def review_plugin_directory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Review all files in a plugin directory"""
        directory = args.get("directory", "")
        recursive = args.get("recursive", True)
        
        if not directory:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: No directory provided"
                    }
                ]
            }
        
        full_path = self.base_path / directory
        if not full_path.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Directory not found: {directory}"
                    }
                ]
            }
        
        results = self.reviewer.review_directory(str(full_path), recursive)
        
        # Format output
        output = self._format_directory_results(results, directory)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": output
                }
            ]
        }
    
    async def get_review_summary(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get review summary for a directory"""
        directory = args.get("directory", "")
        
        full_path = self.base_path / directory
        if not full_path.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Directory not found: {directory}"
                    }
                ]
            }
        
        results = self.reviewer.review_directory(str(full_path), recursive=True)
        summary = self._generate_summary(results)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": summary
                }
            ]
        }
    
    def _format_review_result(self, result: ReviewResult, file_path: str) -> str:
        """Format a single file review result"""
        output = f"# Review: {file_path}\n\n"
        output += f"**Lines:** {result.total_lines}\n"
        output += f"**Findings:** {len(result.findings)}\n\n"
        
        if not result.findings:
            output += "✅ No issues found\n"
            return output
        
        # Group by severity
        by_severity = {}
        for finding in result.findings:
            sev = finding.severity.value
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(finding)
        
        # Output by severity
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            findings = by_severity.get(severity.value, [])
            if findings:
                output += f"\n## {severity.value.upper()} ({len(findings)} issues)\n\n"
                for finding in findings:
                    output += f"**{finding.rule_id}**: {finding.rule_name}\n"
                    output += f"- Location: `{file_path}:{finding.line_number}:{finding.column}`\n"
                    output += f"- Issue: {finding.description}\n"
                    if finding.code_snippet:
                        output += f"- Code: `{finding.code_snippet.strip()}`\n"
                    if finding.suggestion:
                        output += f"- Fix: {finding.suggestion}\n"
                    output += "\n"
        
        return output
    
    def _format_directory_results(self, results: List[ReviewResult], directory: str) -> str:
        """Format directory review results"""
        output = f"# Thunder Plugin Review: {directory}\n\n"
        
        total_files = len(results)
        total_findings = sum(len(r.findings) for r in results)
        files_with_issues = sum(1 for r in results if r.findings)
        files_with_critical = sum(1 for r in results if r.has_critical_issues())
        
        # Summary
        output += "## Summary\n\n"
        output += f"- Files reviewed: {total_files}\n"
        output += f"- Files with issues: {files_with_issues}\n"
        output += f"- Files with critical issues: {files_with_critical}\n"
        output += f"- Total findings: {total_findings}\n\n"
        
        # Severity breakdown
        severity_counts = {sev.value: 0 for sev in Severity}
        for result in results:
            for finding in result.findings:
                severity_counts[finding.severity.value] += 1
        
        if total_findings > 0:
            output += "### By Severity\n\n"
            for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
                count = severity_counts[sev.value]
                if count > 0:
                    icon = "🔴" if sev == Severity.CRITICAL else "🟠" if sev == Severity.HIGH else "🟡" if sev == Severity.MEDIUM else "⚪"
                    output += f"- {icon} **{sev.value.upper()}**: {count}\n"
            output += "\n"
        
        # Critical files
        if files_with_critical > 0:
            output += "## ⚠️ Files with Critical Issues\n\n"
            for result in results:
                if result.has_critical_issues():
                    critical_count = sum(1 for f in result.findings if f.severity == Severity.CRITICAL)
                    rel_path = os.path.relpath(result.file_path, self.base_path)
                    output += f"- `{rel_path}` ({critical_count} critical)\n"
            output += "\n"
        
        # Detailed findings
        output += "## Detailed Findings\n\n"
        for result in results:
            if result.findings:
                rel_path = os.path.relpath(result.file_path, self.base_path)
                output += self._format_review_result(result, rel_path)
                output += "\n---\n\n"
        
        return output
    
    def _generate_summary(self, results: List[ReviewResult]) -> str:
        """Generate a summary of review results"""
        total_files = len(results)
        total_findings = sum(len(r.findings) for r in results)
        
        severity_counts = {sev.value: 0 for sev in Severity}
        for result in results:
            for finding in result.findings:
                severity_counts[finding.severity.value] += 1
        
        output = "# Review Summary\n\n"
        output += f"**Files:** {total_files}\n"
        output += f"**Total Issues:** {total_findings}\n\n"
        
        for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            count = severity_counts[sev.value]
            output += f"- {sev.value.upper()}: {count}\n"
        
        return output
    
    def run(self):
        """Run the MCP server with stdio transport"""
        import sys
        
        # Send initial ready message
        sys.stderr.write("Thunder Plugin Reviewer MCP Server started\n")
        sys.stderr.flush()
        
        for line in sys.stdin:
            try:
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON-RPC request
                request = json.loads(line)
                
                # Handle request synchronously (convert async to sync for simplicity)
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")
                
                try:
                    if method == "initialize":
                        result = self.handle_initialize(params)
                    elif method == "tools/list":
                        result = self.handle_list_tools()
                    elif method == "tools/call":
                        result = self.handle_tool_call_sync(params)
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
    
    def handle_tool_call_sync(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call synchronously"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "review_plugin":
            return self.review_plugin_sync(arguments)
        elif tool_name == "review_plugin_directory":
            return self.review_plugin_directory_sync(arguments)
        elif tool_name == "get_review_summary":
            return self.get_review_summary_sync(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def review_plugin_sync(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Review specific plugin files (sync version)"""
        file_paths = args.get("file_paths", [])
        
        if not file_paths:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: No file paths provided"
                    }
                ]
            }
        
        results = []
        for file_path in file_paths:
            full_path = self.base_path / file_path
            if not full_path.exists():
                results.append(f"File not found: {file_path}")
                continue
            
            result = self.reviewer.review_file(str(full_path))
            results.append(self._format_review_result(result, file_path))
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": "\n\n".join(results)
                }
            ]
        }
    
    def review_plugin_directory_sync(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Review all files in a plugin directory (sync version)"""
        directory = args.get("directory", "")
        recursive = args.get("recursive", True)
        
        if not directory:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: No directory provided"
                    }
                ]
            }
        
        full_path = self.base_path / directory
        if not full_path.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Directory not found: {directory}"
                    }
                ]
            }
        
        results = self.reviewer.review_directory(str(full_path), recursive)
        
        # Format output
        output = self._format_directory_results(results, directory)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": output
                }
            ]
        }
    
    def get_review_summary_sync(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get review summary for a directory (sync version)"""
        directory = args.get("directory", "")
        
        full_path = self.base_path / directory
        if not full_path.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Directory not found: {directory}"
                    }
                ]
            }
        
        results = self.reviewer.review_directory(str(full_path), recursive=True)
        summary = self._generate_summary(results)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": summary
                }
            ]
        }


def main():
    """Main entry point"""
    server = ThunderReviewMCPServer()
    server.run()


if __name__ == "__main__":
    main()
