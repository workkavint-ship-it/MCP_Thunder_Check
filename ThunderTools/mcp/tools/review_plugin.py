"""
Thunder Plugin Reviewer Tool

MCP tool for reviewing Thunder plugins against framework guidelines.
Reviews are based on Thunder/.github/instructions/plugins.instructions.md

This tool is a thin MCP wrapper around core.ReviewEngine.
"""

from pathlib import Path
from typing import Any, Dict

# Import core engine
from ThunderTools.core import ReviewEngine, Severity, ReviewResult


class ReviewPluginTool:
    """Review Thunder plugin files for compliance - MCP interface"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        
        # Primary source: plugins.instructions.md
        self.instructions_file = base_path / "Thunder" / ".github" / "instructions" / "plugins.instructions.md"
        
        # Rules file in tools folder
        rules_file = Path(__file__).parent / "review_rules.yml"
        
        # Create core engine
        self.engine = ReviewEngine(rules_file)
        
        # Load instructions content for AI-assisted review
        self.instructions_content = self._load_instructions()
    
    def _load_instructions(self) -> str:
        """Load the plugins.instructions.md for reference"""
        if self.instructions_file.exists():
            try:
                return self.instructions_file.read_text(encoding='utf-8')
            except Exception as e:
                return f"# Error loading instructions: {e}\n"
        return "# Instructions file not found\n"
    
    def get_definition(self) -> Dict[str, Any]:
        """Get tool definition for MCP"""
        return {
            "name": "review_file",
            "description": (
                "Review specific Thunder plugin files for compliance with framework guidelines. "
                "Checks C++ code against Thunder/.github/instructions/plugins.instructions.md "
                "covering IPlugin lifecycle, reference counting, JSON-RPC, IShell usage, "
                "subsystems, interface maps, and 50+ specific rules."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of C++ file paths to review (relative to workspace root)"
                    },
                    "include_guidelines": {
                        "type": "boolean",
                        "description": "Include full plugin guidelines from plugins.instructions.md in output",
                        "default": False
                    }
                },
                "required": ["file_paths"]
            }
        }
    
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the review tool"""
        file_paths = arguments.get("file_paths", [])
        include_guidelines = arguments.get("include_guidelines", False)
        
        if not file_paths:
            return {
                "content": [{
                    "type": "text",
                    "text": "❌ Error: No file paths provided"
                }]
            }
        
        # Add guidelines header if requested
        output_parts = []
        
        if include_guidelines:
            output_parts.append(f"# Thunder Plugin Guidelines\n\n{self.instructions_content}\n\n---\n")
        
        # Review each file
        results = []
        for file_path in file_paths:
            full_path = self.base_path / file_path
            if not full_path.exists():
                results.append(f"❌ File not found: {file_path}")
                continue
            
            result = self.engine.review_file(str(full_path))
            results.append(self._format_result(result, file_path))
        
        output_parts.extend(results)
        
        # Add reference to guidelines at the end
        if not include_guidelines and self.instructions_file.exists():
            output_parts.append(
                f"\n\n---\n"
                f"📖 **Review based on:** `{self.instructions_file.relative_to(self.base_path)}`\n"
                f"Use `include_guidelines: true` to see full framework guidelines."
            )
        
        return {
            "content": [{
                "type": "text",
                "text": "\n\n".join(output_parts)
            }]
        }
    
    def _format_result(self, result: ReviewResult, file_path: str) -> str:
        """Format review result"""
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
                icon = "🔴" if severity == Severity.CRITICAL else "🟠" if severity == Severity.HIGH else "🟡" if severity == Severity.MEDIUM else "⚪"
                output += f"\n## {icon} {severity.value.upper()} ({len(findings)} issues)\n\n"
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
