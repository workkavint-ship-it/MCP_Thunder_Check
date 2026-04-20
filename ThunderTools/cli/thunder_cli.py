#!/usr/bin/env python3
"""
Thunder CLI - Main Entry Point

Command-line interface for Thunder development tools.

Usage:
    python -m ThunderTools.cli generate <options>
    python -m ThunderTools.cli review <options>
    python -m ThunderTools.cli --help
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='thunder-cli',
        description='Thunder Framework Development Tools',
        epilog='Use "thunder-cli <command> --help" for command-specific help'
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # ========================================================================
    # GENERATE command
    # ========================================================================
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate Thunder plugin skeleton',
        description='Generate a new Thunder plugin skeleton with all necessary files'
    )
    
    generate_parser.add_argument(
        '--plugin-name', '-n',
        required=True,
        help='Name of the plugin (e.g., NetworkControl)'
    )
    
    generate_parser.add_argument(
        '--mode', '-m',
        choices=['in-process', 'oop', 'out-of-process'],
        default='in-process',
        help='Plugin process mode (default: in-process)'
    )
    
    generate_parser.add_argument(
        '--interface', '-i',
        action='append',
        dest='interfaces',
        help='Path to interface header file (can specify multiple times)'
    )
    
    generate_parser.add_argument(
        '--output', '-o',
        default='.',
        help='Output directory (default: current directory)'
    )
    
    generate_parser.add_argument(
        '--config',
        action='store_true',
        default=True,
        help='Generate custom configuration support (default: True)'
    )
    
    generate_parser.add_argument(
        '--no-config',
        action='store_false',
        dest='config',
        help='Do not generate custom configuration support'
    )
    
    generate_parser.add_argument(
        '--preconditions',
        help='Comma-separated list of precondition subsystems (e.g., PLATFORM,NETWORK)'
    )
    
    generate_parser.add_argument(
        '--terminations',
        help='Comma-separated list of termination subsystems'
    )
    
    generate_parser.add_argument(
        '--controls',
        help='Comma-separated list of controlled subsystems'
    )
    
    generate_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress output messages'
    )
    
    # ========================================================================
    # REVIEW command
    # ========================================================================
    review_parser = subparsers.add_parser(
        'review',
        help='Review Thunder plugin code',
        description='Review C++ plugin files against Thunder framework guidelines'
    )
    
    review_group = review_parser.add_mutually_exclusive_group(required=True)
    
    review_group.add_argument(
        '--file', '-f',
        action='append',
        dest='files',
        help='File to review (can specify multiple times)'
    )
    
    review_group.add_argument(
        '--directory', '-d',
        help='Directory to review (reviews all C++ files)'
    )
    
    review_parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        default=True,
        help='Recursively review subdirectories (default: True)'
    )
    
    review_parser.add_argument(
        '--no-recursive',
        action='store_false',
        dest='recursive',
        help='Do not recurse into subdirectories'
    )
    
    review_parser.add_argument(
        '--format',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )
    
    review_parser.add_argument(
        '--severity',
        choices=['critical', 'high', 'medium', 'low', 'all'],
        default='all',
        help='Minimum severity level to show (default: all)'
    )
    
    review_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress output messages'
    )
    
    # ========================================================================
    # Parse and execute
    # ========================================================================
    args = parser.parse_args()
    
    # Dynamically import command handlers
    if args.command == 'generate':
        from ThunderTools.cli.commands.generate import run_generate
        return run_generate(args)
    elif args.command == 'review':
        from ThunderTools.cli.commands.review import run_review
        return run_review(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
