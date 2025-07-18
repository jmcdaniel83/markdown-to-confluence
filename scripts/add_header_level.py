#!/usr/bin/env python3
"""
Script to add one level of header to all markdown files.
Converts # to ##, ## to ###, etc.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Constants
SCRIPT_EXAMPLES = """
Examples:
  python add_header_level.py input/jira/spike
  python add_header_level.py docs/
  python add_header_level.py .
"""

def add_header_level(content: str) -> str:
    """Add one level to all headers in the content"""
    # Pattern to match headers (1-6 # symbols at start of line)
    header_pattern = r'^(#{1,6})\s+(.+)$'

    def replace_header(match):
        level = match.group(1)
        text = match.group(2)
        # Add one more # to the level
        new_level = '#' + level
        return f"{new_level} {text}"

    # Apply the replacement to each line
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        if re.match(header_pattern, line):
            new_lines.append(re.sub(header_pattern, replace_header, line))
        else:
            new_lines.append(line)

    return '\n'.join(new_lines)

def process_directory(directory_path: str):
    """Process all markdown files in the given directory"""
    directory = Path(directory_path)

    if not directory.exists():
        print(f"Directory not found: {directory_path}")
        return

    # Find all markdown files
    markdown_files = list(directory.glob("*.md"))

    if not markdown_files:
        print(f"No markdown files found in {directory_path}")
        return

    print(f"Found {len(markdown_files)} markdown files to process:")

    for file_path in markdown_files:
        print(f"Processing: {file_path.name}")

        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add header level
        new_content = add_header_level(content)

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✓ Updated {file_path.name}")

    print(f"\nCompleted processing {len(markdown_files)} files.")

def main():
    """Main function to handle command line arguments and process files"""
    parser = argparse.ArgumentParser(
        description="Add one level of header to all markdown files in a directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=SCRIPT_EXAMPLES
    )

    parser.add_argument(
        'directory',
        help='Directory containing markdown files to process'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )

    args = parser.parse_args()

    # Validate directory exists
    if not Path(args.directory).exists():
        print(f"❌ Error: Directory '{args.directory}' does not exist")
        sys.exit(1)

    if args.dry_run:
        print(f"🔍 Dry run mode - no changes will be made")
        print(f"📁 Processing directory: {args.directory}")
        # For dry run, we'll just show what files would be processed
        directory = Path(args.directory)
        markdown_files = list(directory.glob("*.md"))

        if not markdown_files:
            print(f"❌ No markdown files found in {args.directory}")
            sys.exit(1)

        print(f"📄 Found {len(markdown_files)} markdown files:")
        for file_path in markdown_files:
            print(f"   - {file_path.name}")

        print(f"\n💡 Run without --dry-run to actually process these files")
    else:
        process_directory(args.directory)


if __name__ == "__main__":
    main()