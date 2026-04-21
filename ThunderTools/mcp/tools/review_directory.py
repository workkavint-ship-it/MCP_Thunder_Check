"""
Thunder Plugin Directory Reviewer Tool

MCP tool for reviewing entire plugin directories.
Reviews are based on Thunder/.github/instructions/plugins.instructions.md

This tool is a thin MCP wrapper around core.ReviewEngine.
"""

import os
from pathlib import Path
from typing import Any, Dict, List

# Import core engine
from ThunderTools.core import ReviewEngine, Severity, ReviewResult


class ReviewDirectoryTool:
    """Review all C++ files in a plugin directory - MCP interface"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        
        # Primary source: plugins.instructions.md
        self.instructions_file = base_path / "Thunder" / ".github" / "instructions" / "plugins.instructions.md"
        
        # Rules file in tools folder
        rules_file = Path(__file__).parent / "review_rules.yml"
        
        # Create core engine
        self.engine = ReviewEngine(rules_file)
    
    def get_definition(self) -> Dict[str, Any]:
        """Get tool definition for MCP"""
        return {
            "name": "review",
            "description": (
                "Review all C++ files in a Thunder plugin directory recursively. "
                "Accepts either a plugin name (e.g., 'Dictionary1') or full path (e.g., 'ThunderNanoServices/Dictionary1'). "
                "Automatically searches ThunderNanoServices/ and Thunder/Source/plugins/ for the plugin. "
                "Checks against Thunder/.github/instructions/plugins.instructions.md "
                "covering IPlugin lifecycle, JSON-RPC, subsystems, and framework best practices. "
                "Provides detailed findings with severity levels and fix suggestions."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Plugin name (e.g., 'Dictionary1') or directory path (e.g., 'ThunderNanoServices/NetworkControl')"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Recursively review subdirectories (default: true)",
                        "default": True
                    }
                },
                "required": ["directory"]
            }
        }
    
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the directory review tool"""
        directory = arguments.get("directory", "")
        recursive = arguments.get("recursive", True)
        
        if not directory:
            return {
                "content": [{
                    "type": "text",
                    "text": "❌ Error: No directory provided"
                }]
            }
        
        # Try to find the directory - handle both full paths and plugin names
        full_path = self._resolve_directory(directory)
        
        if not full_path or not full_path.exists():
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Directory not found: {directory}\n\nTried: {full_path if full_path else 'N/A'}"
                }]
            }
        
        results = self.engine.review_directory(str(full_path), recursive)
        output = self._format_results(results, directory)
        
        return {
            "content": [{
                "type": "text",
                "text": output
            }]
        }
    
    def _resolve_directory(self, directory: str) -> Path:
        """Resolve directory path - try multiple common locations"""
        # Try as-is first (full path)
        full_path = self.base_path / directory
        if full_path.exists():
            return full_path
        
        # Try as plugin name in ThunderNanoServices
        nano_path = self.base_path / "ThunderNanoServices" / directory
        if nano_path.exists():
            return nano_path
        
        # Try Thunder/Source/plugins
        thunder_plugins = self.base_path / "Thunder" / "Source" / "plugins" / directory
        if thunder_plugins.exists():
            return thunder_plugins
        
        # Return original path if nothing found
        return full_path
    
    def _format_results(self, results: List[ReviewResult], directory: str) -> str:
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
        
        # Detailed findings (first 5 files with issues)
        if files_with_issues > 0:
            output += "## Detailed Findings\n\n"
            shown = 0
            for result in results:
                if result.findings and shown < 5:
                    rel_path = os.path.relpath(result.file_path, self.base_path)
                    output += f"### {rel_path}\n\n"
                    
                    # Show first 3 findings per file
                    for i, finding in enumerate(result.findings[:3], 1):
                        output += f"{i}. **{finding.rule_id}**: {finding.rule_name}\n"
                        output += f"   - Line {finding.line_number}: {finding.description}\n"
                        if finding.suggestion:
                            output += f"   - Fix: {finding.suggestion}\n"
                    
                    if len(result.findings) > 3:
                        output += f"\n   ... and {len(result.findings) - 3} more issues\n"
                    output += "\n"
                    shown += 1
            
            if files_with_issues > 5:
                output += f"\n*Showing first 5 of {files_with_issues} files with issues*\n"
        
        # Add reference to guidelines
        if self.instructions_file.exists():
            output += (
                f"\n\n---\n"
                f"📖 **Review based on:** `{self.instructions_file.relative_to(self.base_path)}`\n"
            )
        
        return output
