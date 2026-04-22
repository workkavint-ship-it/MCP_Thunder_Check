"""
Thunder Review Engine

Core review functionality - checks C++ plugin code against Thunder framework guidelines.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional
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


@dataclass
class ReviewResult:
    """Aggregated review results for a file"""
    file_path: str
    findings: List[Finding] = field(default_factory=list)
    total_lines: int = 0
    
    def has_critical_issues(self) -> bool:
        return any(f.severity == Severity.CRITICAL for f in self.findings)
    
    def get_summary(self) -> Dict[str, int]:
        """Get count by severity"""
        summary = {sev.value: 0 for sev in Severity}
        for finding in self.findings:
            summary[finding.severity.value] += 1
        return summary


class ReviewEngine:
    """Core review engine - checks C++ files against rules"""
    
    def __init__(self, rules_file: Path):
        """Initialize with rules file path"""
        self.rules = self._load_rules(rules_file)
        self.file_cache: Dict[str, List[str]] = {}
    
    def _load_rules(self, rules_file: Path) -> Dict:
        """Load review rules from YAML"""
        if not rules_file.exists():
            print(f"Warning: Rules file not found: {rules_file}")
            return {'categories': []}
        
        with open(rules_file, 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)

        num_categories = len(rules.get('categories', []))
        print(f"Loaded {num_categories} rule categories")
        return rules
    
    def review_file(self, file_path: str) -> ReviewResult:
        """Review a single C++ file"""
        result = ReviewResult(file_path=file_path)
        
        if not os.path.exists(file_path):
            return result
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        result.total_lines = len(content.split('\n'))
        
        # Apply all rule categories
        for category in self.rules.get('categories', []):
            severity = category.get('severity', 'medium')
            
            for rule in category.get('rules', []):
                if 'pattern' in rule and 'check_matching' not in rule:
                    findings = self._check_pattern(content, file_path, rule, severity)
                    result.findings.extend(findings)
                elif 'antipattern' in rule:
                    findings = self._check_antipattern(content, file_path, rule, severity)
                    result.findings.extend(findings)
        
        return result
    
    def review_directory(self, directory: str, recursive: bool = True, verbose: bool = True) -> List[ReviewResult]:
        """Review all C++ files in a directory"""
        results = []
        path = Path(directory)
        
        if not path.exists():
            if verbose:
                print(f"Directory not found: {directory}")
            return results
        
        # Find C++ files
        patterns = ['**/*.cpp', '**/*.h'] if recursive else ['*.cpp', '*.h']
        cpp_files = []
        for pattern in patterns:
            cpp_files.extend(path.glob(pattern))
        
        if verbose:
            print(f"Found {len(cpp_files)} C++ files to review")
        
        for cpp_file in cpp_files:
            if verbose:
                print(f"Reviewing {cpp_file.name}...")
            results.append(self.review_file(str(cpp_file)))
        
        return results
    
    def _check_pattern(self, content: str, file_path: str, rule: Dict, severity: str) -> List[Finding]:
        """Check for pattern matches in content"""
        findings = []
        lines = content.split('\n')
        
        try:
            pattern_re = re.compile(rule['pattern'], re.MULTILINE)
            for line_num, line in enumerate(lines, 1):
                for match in pattern_re.finditer(line):
                    findings.append(Finding(
                        rule_id=rule['id'],
                        rule_name=rule['name'],
                        severity=Severity[severity.upper()],
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start() + 1,
                        description=rule['description'],
                        suggestion=rule.get('suggestion'),
                        code_snippet=line.strip()
                    ))
        except (re.error, KeyError):
            pass
        
        return findings
    
    def _check_antipattern(self, content: str, file_path: str, rule: Dict, severity: str) -> List[Finding]:
        """Check for antipattern matches (things that should NOT be present)"""
        findings = []
        lines = content.split('\n')
        antipatterns = rule.get('antipattern', [])
        if isinstance(antipatterns, str):
            antipatterns = [antipatterns]
        
        for antipattern in antipatterns:
            try:
                pattern_re = re.compile(antipattern, re.MULTILINE)
                for line_num, line in enumerate(lines, 1):
                    for match in pattern_re.finditer(line):
                        findings.append(Finding(
                            rule_id=rule['id'],
                            rule_name=rule['name'],
                            severity=Severity[severity.upper()],
                            file_path=file_path,
                            line_number=line_num,
                            column=match.start() + 1,
                            description=f"{rule['description']} - Found: {match.group()}",
                            suggestion=rule.get('suggestion'),
                            code_snippet=line.strip()
                        ))
            except (re.error, KeyError):
                pass
        
        return findings
