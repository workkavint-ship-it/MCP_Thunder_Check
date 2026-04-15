#!/usr/bin/env python3
"""
Thunder Plugin Reviewer

A code review tool for Thunder framework plugins that checks C++ files 
against Thunder coding guidelines and best practices.

Usage:
    review_plugin.py <file_path> [<file_path> ...]
    review_plugin.py --dir <directory>
    review_plugin.py --ai-review <file_path>
"""

import sys
import os
import re
import yaml
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Finding:
    """Represents a single review finding"""
    rule_id: str
    rule_name: str
    severity: Severity
    file_path: str
    line_number: int
    column: int
    description: str
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    context: Optional[str] = None

    def __str__(self) -> str:
        result = f"\n[{self.severity.value.upper()}] {self.rule_id}: {self.rule_name}\n"
        result += f"  File: {self.file_path}:{self.line_number}:{self.column}\n"
        result += f"  Issue: {self.description}\n"
        if self.code_snippet:
            result += f"  Code: {self.code_snippet}\n"
        if self.suggestion:
            result += f"  Fix: {self.suggestion}\n"
        return result


@dataclass
class ReviewResult:
    """Aggregated review results"""
    file_path: str
    findings: List[Finding] = field(default_factory=list)
    total_lines: int = 0
    
    def add_finding(self, finding: Finding):
        self.findings.append(finding)
    
    def get_summary(self) -> Dict[str, int]:
        """Get summary counts by severity"""
        summary = {sev.value: 0 for sev in Severity}
        for finding in self.findings:
            summary[finding.severity.value] += 1
        return summary
    
    def has_critical_issues(self) -> bool:
        """Check if there are any critical issues"""
        return any(f.severity == Severity.CRITICAL for f in self.findings)


class PluginReviewer:
    """Main plugin reviewer class"""
    
    def __init__(self, rules_file: Path):
        """Initialize reviewer with rules file"""
        self.rules = self._load_rules(rules_file)
        self.file_cache: Dict[str, List[str]] = {}
    
    def _load_rules(self, rules_file: Path) -> Dict:
        """Load review rules from YAML file"""
        if not rules_file.exists():
            raise FileNotFoundError(f"Rules file not found: {rules_file}")
        
        with open(rules_file, 'r') as f:
            rules = yaml.safe_load(f)
        
        print(f"Loaded {len(rules.get('categories', []))} rule categories")
        return rules
    
    def _read_file_lines(self, file_path: str) -> List[str]:
        """Read file lines with caching"""
        if file_path not in self.file_cache:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.file_cache[file_path] = f.readlines()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                return []
        return self.file_cache[file_path]
    
    def _get_context(self, file_path: str, line_num: int, context_lines: int = 2) -> str:
        """Get code context around a line"""
        lines = self._read_file_lines(file_path)
        start = max(0, line_num - context_lines - 1)
        end = min(len(lines), line_num + context_lines)
        
        context = []
        for i in range(start, end):
            marker = ">>>" if i == line_num - 1 else "   "
            context.append(f"{marker} {i+1:4d}: {lines[i].rstrip()}")
        
        return "\n".join(context)
    
    def _check_pattern(self, content: str, pattern: str, file_path: str, 
                       rule_id: str, rule_name: str, severity: str,
                       description: str, suggestion: Optional[str] = None) -> List[Finding]:
        """Check for pattern matches in content"""
        findings = []
        lines = content.split('\n')
        
        try:
            pattern_re = re.compile(pattern, re.MULTILINE)
            for line_num, line in enumerate(lines, 1):
                matches = pattern_re.finditer(line)
                for match in matches:
                    finding = Finding(
                        rule_id=rule_id,
                        rule_name=rule_name,
                        severity=Severity[severity.upper()],
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start() + 1,
                        description=description,
                        suggestion=suggestion,
                        code_snippet=line.strip()
                    )
                    findings.append(finding)
        except re.error as e:
            print(f"Invalid regex pattern '{pattern}' in rule {rule_id}: {e}")
        
        return findings
    
    def _check_antipattern(self, content: str, antipatterns: List[str], 
                           file_path: str, rule_id: str, rule_name: str,
                           severity: str, description: str, 
                           suggestion: Optional[str] = None) -> List[Finding]:
        """Check for antipattern matches (things that should NOT be present)"""
        findings = []
        lines = content.split('\n')
        
        for antipattern in antipatterns:
            try:
                pattern_re = re.compile(antipattern, re.MULTILINE)
                for line_num, line in enumerate(lines, 1):
                    matches = pattern_re.finditer(line)
                    for match in matches:
                        finding = Finding(
                            rule_id=rule_id,
                            rule_name=rule_name,
                            severity=Severity[severity.upper()],
                            file_path=file_path,
                            line_number=line_num,
                            column=match.start() + 1,
                            description=f"{description} - Found: {match.group()}",
                            suggestion=suggestion,
                            code_snippet=line.strip()
                        )
                        findings.append(finding)
            except re.error as e:
                print(f"Invalid antipattern '{antipattern}' in rule {rule_id}: {e}")
        
        return findings
    
    def _check_class_inheritance(self, content: str, file_path: str,
                                  rule: Dict, severity: str) -> List[Finding]:
        """Check if class properly inherits required interface"""
        findings = []
        pattern = rule.get('pattern', '')
        required_methods = rule.get('required_methods', [])
        
        # Find classes matching the pattern
        class_matches = re.finditer(pattern, content, re.MULTILINE)
        
        for match in class_matches:
            class_start = match.start()
            # Find the class name
            class_name_match = re.search(r'class\s+(\w+)', match.group())
            if not class_name_match:
                continue
            
            class_name = class_name_match.group(1)
            
            # Check if required methods are present
            for method in required_methods:
                method_pattern = rf'\b{method}\s*\([^)]*\)'
                if not re.search(method_pattern, content):
                    line_num = content[:class_start].count('\n') + 1
                    finding = Finding(
                        rule_id=rule['id'],
                        rule_name=rule['name'],
                        severity=Severity[severity.upper()],
                        file_path=file_path,
                        line_number=line_num,
                        column=1,
                        description=f"Class {class_name} missing required method: {method}",
                        suggestion=f"Implement {method}() method in {class_name}"
                    )
                    findings.append(finding)
        
        return findings
    
    def _check_matching_pairs(self, content: str, file_path: str, 
                             rule: Dict, severity: str) -> List[Finding]:
        """Check for matching pairs (e.g., Register/Unregister)"""
        findings = []
        pattern = rule.get('pattern', '')
        matching_pattern = rule.get('check_matching', '')
        
        # Find all Register calls
        registers = {}
        try:
            for match in re.finditer(pattern, content, re.MULTILINE):
                if match.groups():
                    method_name = match.group(1)
                    line_num = content[:match.start()].count('\n') + 1
                    registers[method_name] = line_num
        except re.error as e:
            print(f"Invalid regex pattern '{pattern}' in rule {rule.get('id')}: {e}")
            return findings
        
        # Check if each has a matching Unregister
        for method_name, line_num in registers.items():
            # Replace PLACEHOLDER with the actual method name
            unregister_pattern = matching_pattern.replace('PLACEHOLDER', re.escape(method_name))
            if not re.search(unregister_pattern, content):
                finding = Finding(
                    rule_id=rule['id'],
                    rule_name=rule['name'],
                    severity=Severity[severity.upper()],
                    file_path=file_path,
                    line_number=line_num,
                    column=1,
                    description=f"Missing Unregister for method '{method_name}'",
                    suggestion=f"Add Unregister(_T(\"{method_name}\")) in Deinitialize()"
                )
                findings.append(finding)
        
        return findings
        
        return findings
    
    def review_file(self, file_path: str) -> ReviewResult:
        """Review a single C++ file"""
        result = ReviewResult(file_path=file_path)
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return result
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        result.total_lines = len(content.split('\n'))
        
        # Determine file context (which layer it belongs to)
        file_context = self._determine_context(file_path)
        
        # Process each category of rules
        for category in self.rules.get('categories', []):
            category_name = category.get('name', 'Unknown')
            severity = category.get('severity', 'medium')
            
            for rule in category.get('rules', []):
                rule_id = rule.get('id')
                rule_name = rule.get('name')
                description = rule.get('description')
                suggestion = rule.get('suggestion')
                context_filter = rule.get('context')
                
                # Skip if context doesn't match
                if context_filter and context_filter != file_context:
                    continue
                
                # Different check types
                check_type = rule.get('check_type')
                
                if check_type == 'class_inheritance':
                    findings = self._check_class_inheritance(content, file_path, rule, severity)
                    result.findings.extend(findings)
                
                elif 'pattern' in rule and 'check_matching' in rule:
                    findings = self._check_matching_pairs(content, file_path, rule, severity)
                    result.findings.extend(findings)
                
                elif 'pattern' in rule:
                    findings = self._check_pattern(
                        content, rule['pattern'], file_path,
                        rule_id, rule_name, severity, description, suggestion
                    )
                    result.findings.extend(findings)
                
                elif 'antipattern' in rule:
                    antipatterns = rule['antipattern']
                    if isinstance(antipatterns, str):
                        antipatterns = [antipatterns]
                    
                    findings = self._check_antipattern(
                        content, antipatterns, file_path,
                        rule_id, rule_name, severity, description, suggestion
                    )
                    result.findings.extend(findings)
        
        return result
    
    def _determine_context(self, file_path: str) -> str:
        """Determine which Thunder layer a file belongs to"""
        path_lower = file_path.lower()
        
        if 'source/core/' in path_lower:
            return 'core_layer'
        elif 'source/plugins/' in path_lower:
            return 'plugins_layer'
        elif 'source/com/' in path_lower:
            return 'com_layer'
        elif 'source/thunder/' in path_lower:
            return 'thunder_layer'
        elif 'thundernanoservices/' in path_lower:
            return 'plugin'
        
        return 'unknown'
    
    def review_directory(self, directory: str, recursive: bool = True) -> List[ReviewResult]:
        """Review all C++ files in a directory"""
        results = []
        
        path = Path(directory)
        if not path.exists():
            print(f"Directory not found: {directory}")
            return results
        
        # Find all C++ files
        patterns = ['**/*.cpp', '**/*.h'] if recursive else ['*.cpp', '*.h']
        cpp_files = []
        for pattern in patterns:
            cpp_files.extend(path.glob(pattern))
        
        print(f"Found {len(cpp_files)} C++ files to review")
        
        for cpp_file in cpp_files:
            print(f"Reviewing {cpp_file}...")
            result = self.review_file(str(cpp_file))
            results.append(result)
        
        return results
    
    def get_ai_prompt(self, file_path: str, findings: List[Finding]) -> str:
        """Generate AI prompt for detailed review"""
        prompt_template = self.rules.get('ai_prompts', {}).get('review_request', '')
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        prompt = f"{prompt_template}\n\n"
        prompt += f"File: {file_path}\n\n"
        prompt += "Automated findings:\n"
        
        for finding in findings:
            prompt += f"- [{finding.severity.value}] {finding.rule_id}: {finding.description}\n"
            prompt += f"  Line {finding.line_number}: {finding.code_snippet}\n"
        
        prompt += f"\n\nFull file content:\n```cpp\n{content}\n```\n"
        
        return prompt


def print_summary(results: List[ReviewResult]):
    """Print summary of all review results"""
    print("\n" + "="*80)
    print("REVIEW SUMMARY")
    print("="*80)
    
    total_files = len(results)
    total_findings = sum(len(r.findings) for r in results)
    files_with_issues = sum(1 for r in results if r.findings)
    files_with_critical = sum(1 for r in results if r.has_critical_issues())
    
    # Aggregate severity counts
    severity_counts = {sev.value: 0 for sev in Severity}
    for result in results:
        summary = result.get_summary()
        for sev, count in summary.items():
            severity_counts[sev] += count
    
    print(f"\nFiles reviewed: {total_files}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Files with critical issues: {files_with_critical}")
    print(f"Total findings: {total_findings}")
    print(f"\nFindings by severity:")
    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        count = severity_counts[sev.value]
        if count > 0:
            print(f"  {sev.value.upper()}: {count}")
    
    # List files with critical issues
    if files_with_critical > 0:
        print(f"\n⚠️  Files with CRITICAL issues:")
        for result in results:
            if result.has_critical_issues():
                critical_count = sum(1 for f in result.findings if f.severity == Severity.CRITICAL)
                print(f"  - {result.file_path} ({critical_count} critical)")


def print_detailed_results(results: List[ReviewResult], show_all: bool = False):
    """Print detailed findings"""
    for result in results:
        if not result.findings and not show_all:
            continue
        
        print(f"\n{'='*80}")
        print(f"File: {result.file_path}")
        print(f"Lines: {result.total_lines}")
        print(f"Findings: {len(result.findings)}")
        print('='*80)
        
        if not result.findings:
            print("✓ No issues found")
            continue
        
        # Group by severity
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            severity_findings = [f for f in result.findings if f.severity == severity]
            if severity_findings:
                print(f"\n{severity.value.upper()} Issues ({len(severity_findings)}):")
                for finding in severity_findings:
                    print(finding)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Thunder Plugin Code Reviewer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a single file
  review_plugin.py MyPlugin.cpp
  
  # Review multiple files
  review_plugin.py MyPlugin.cpp MyPlugin.h
  
  # Review entire directory
  review_plugin.py --dir ThunderNanoServices/MyPlugin
  
  # Generate AI review prompt
  review_plugin.py --ai-review MyPlugin.cpp > prompt.txt
        """
    )
    
    parser.add_argument('files', nargs='*', help='C++ files to review')
    parser.add_argument('--dir', '-d', help='Review all files in directory')
    parser.add_argument('--recursive', '-r', action='store_true', 
                       help='Recursively review subdirectories')
    parser.add_argument('--rules', default=None,
                       help='Path to custom rules YAML file')
    parser.add_argument('--ai-review', help='Generate AI review prompt for file')
    parser.add_argument('--summary-only', '-s', action='store_true',
                       help='Show only summary, not detailed findings')
    parser.add_argument('--show-all', '-a', action='store_true',
                       help='Show all files, even those without issues')
    
    args = parser.parse_args()
    
    # Find rules file
    if args.rules:
        rules_file = Path(args.rules)
    else:
        # Look for rules file in same directory as script
        script_dir = Path(__file__).parent
        rules_file = script_dir / 'review_rules.yml'
    
    if not rules_file.exists():
        print(f"Error: Rules file not found: {rules_file}")
        print("Please specify --rules or ensure review_rules.yml is in the script directory")
        return 1
    
    # Initialize reviewer
    try:
        reviewer = PluginReviewer(rules_file)
    except Exception as e:
        print(f"Error initializing reviewer: {e}")
        return 1
    
    # Handle AI review mode
    if args.ai_review:
        result = reviewer.review_file(args.ai_review)
        prompt = reviewer.get_ai_prompt(args.ai_review, result.findings)
        print(prompt)
        return 0
    
    # Collect results
    results = []
    
    if args.dir:
        results = reviewer.review_directory(args.dir, args.recursive)
    elif args.files:
        for file_path in args.files:
            result = reviewer.review_file(file_path)
            results.append(result)
    else:
        parser.print_help()
        return 1
    
    # Print results
    if not args.summary_only:
        print_detailed_results(results, args.show_all)
    
    print_summary(results)
    
    # Return exit code based on findings
    has_critical = any(r.has_critical_issues() for r in results)
    return 1 if has_critical else 0


if __name__ == '__main__':
    sys.exit(main())
