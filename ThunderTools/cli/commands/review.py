"""
Review Command - Plugin Code Review

CLI command for reviewing Thunder plugin code.
"""

import sys
import json
from pathlib import Path
from argparse import Namespace

# Import core engine
from ThunderTools.core import ReviewEngine, Severity


def run_review(args: Namespace) -> int:
    """Execute the review command"""

    # Resolve repository root from file location so CLI works from any cwd.
    workspace = Path(__file__).resolve().parents[3]
    rules_file = Path(__file__).parent.parent.parent / "mcp" / "tools" / "review_rules.yml"
    
    # Create engine
    engine = ReviewEngine(rules_file)
    
    # Perform review
    if args.files:
        # Review specific files
        results = []
        for file_path in args.files:
            full_path = _resolve_path(file_path, workspace)
            if not full_path.exists():
                if not args.quiet:
                    print(f"⚠️  File not found: {file_path}", file=sys.stderr)
                continue
            result = engine.review_file(str(full_path))
            results.append(result)
    else:
        # Review directory
        directory = _resolve_path(args.directory, workspace)
        results = engine.review_directory(str(directory), recursive=args.recursive, verbose=not args.quiet)
    
    # Filter by severity if requested
    if args.severity != 'all':
        min_severity = Severity[args.severity.upper()]
        severity_order = {Severity.CRITICAL: 0, Severity.HIGH: 1, Severity.MEDIUM: 2, Severity.LOW: 3}
        min_level = severity_order[min_severity]
        
        for result in results:
            result.findings = [
                f for f in result.findings
                if severity_order[f.severity] <= min_level
            ]
    
    # Format output
    if args.format == 'json':
        _print_json(results)
    elif args.format == 'markdown':
        _print_markdown(results)
    else:
        _print_text(results)
    
    # Return code: 0 if no critical issues, 1 if critical issues found
    has_critical = any(r.has_critical_issues() for r in results)
    return 1 if has_critical else 0


def _print_text(results):
    """Print results in plain text format"""
    total_files = len(results)
    total_findings = sum(len(r.findings) for r in results)
    files_with_issues = sum(1 for r in results if r.findings)
    files_with_critical = sum(1 for r in results if r.has_critical_issues())
    
    print(f"\n{'=' * 80}")
    print(f"THUNDER PLUGIN REVIEW")
    print(f"{'=' * 80}\n")
    
    print(f"Files reviewed: {total_files}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Files with critical issues: {files_with_critical}")
    print(f"Total findings: {total_findings}\n")
    
    if total_findings == 0:
        print("✅ No issues found!\n")
        return
    
    # Severity summary
    severity_counts = {sev.value: 0 for sev in Severity}
    for result in results:
        for finding in result.findings:
            severity_counts[finding.severity.value] += 1
    
    print("By Severity:")
    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        count = severity_counts[sev.value]
        if count > 0:
            icon = "🔴" if sev == Severity.CRITICAL else "🟠" if sev == Severity.HIGH else "🟡" if sev == Severity.MEDIUM else "⚪"
            print(f"  {icon} {sev.value.upper()}: {count}")
    
    print()
    
    # Show findings for files with issues
    for result in results:
        if not result.findings:
            continue
        
        print(f"\n{'─' * 80}")
        print(f"📄 {Path(result.file_path).name}")
        print(f"{'─' * 80}\n")
        
        for finding in result.findings:
            icon = "🔴" if finding.severity == Severity.CRITICAL else "🟠" if finding.severity == Severity.HIGH else "🟡" if finding.severity == Severity.MEDIUM else "⚪"
            print(f"{icon} {finding.rule_id}: {finding.rule_name}")
            print(f"   Line {finding.line_number}: {finding.description}")
            if finding.code_snippet:
                print(f"   Code: {finding.code_snippet}")
            if finding.suggestion:
                print(f"   Fix: {finding.suggestion}")
            print()


def _print_json(results):
    """Print results in JSON format"""
    output = []
    for result in results:
        findings_data = []
        for finding in result.findings:
            findings_data.append({
                'rule_id': finding.rule_id,
                'rule_name': finding.rule_name,
                'severity': finding.severity.value,
                'line': finding.line_number,
                'column': finding.column,
                'description': finding.description,
                'suggestion': finding.suggestion,
                'code': finding.code_snippet
            })
        
        output.append({
            'file': result.file_path,
            'total_lines': result.total_lines,
            'findings': findings_data,
            'has_critical': result.has_critical_issues()
        })
    
    print(json.dumps(output, indent=2))


def _print_markdown(results):
    """Print results in Markdown format"""
    total_files = len(results)
    total_findings = sum(len(r.findings) for r in results)
    files_with_issues = sum(1 for r in results if r.findings)
    
    print(f"# Thunder Plugin Review\n")
    print(f"## Summary\n")
    print(f"- Files reviewed: {total_files}")
    print(f"- Files with issues: {files_with_issues}")
    print(f"- Total findings: {total_findings}\n")
    
    if total_findings == 0:
        print("✅ No issues found!\n")
        return
    
    # Severity summary
    severity_counts = {sev.value: 0 for sev in Severity}
    for result in results:
        for finding in result.findings:
            severity_counts[finding.severity.value] += 1
    
    print("### By Severity\n")
    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        count = severity_counts[sev.value]
        if count > 0:
            icon = "🔴" if sev == Severity.CRITICAL else "🟠" if sev == Severity.HIGH else "🟡" if sev == Severity.MEDIUM else "⚪"
            print(f"- {icon} **{sev.value.upper()}**: {count}")
    
    print()
    
    # Detailed findings
    for result in results:
        if not result.findings:
            continue
        
        print(f"## {Path(result.file_path).name}\n")
        
        for finding in result.findings:
            icon = "🔴" if finding.severity == Severity.CRITICAL else "🟠" if finding.severity == Severity.HIGH else "🟡" if finding.severity == Severity.MEDIUM else "⚪"
            print(f"{icon} **{finding.rule_id}**: {finding.rule_name}")
            print(f"- Line {finding.line_number}: {finding.description}")
            if finding.code_snippet:
                print(f"- Code: `{finding.code_snippet}`")
            if finding.suggestion:
                print(f"- Fix: {finding.suggestion}")
            print()


def _resolve_path(path_value: str, workspace: Path) -> Path:
    """Resolve user-provided path - try multiple common locations.
    
    Tries:
    1. As absolute path (if provided)
    2. As workspace-relative path
    3. As plugin name in ThunderNanoServices
    4. As plugin name in Thunder/Source/plugins
    """
    # Try as absolute path first
    path = Path(path_value)
    if path.is_absolute() and path.exists():
        return path
    
    # Try as workspace-relative path
    full_path = workspace / path_value
    if full_path.exists():
        return full_path
    
    # Try as plugin name in ThunderNanoServices
    nano_path = workspace / "ThunderNanoServices" / path_value
    if nano_path.exists():
        return nano_path
    
    # Try Thunder/Source/plugins
    thunder_plugins = workspace / "Thunder" / "Source" / "plugins" / path_value
    if thunder_plugins.exists():
        return thunder_plugins
    
    # Return full workspace-relative path if nothing found
    return full_path
