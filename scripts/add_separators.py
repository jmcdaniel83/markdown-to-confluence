#!/usr/bin/env python3
"""
Script to add triple dash separators after every level 1 header in markdown files.
"""

import re
from pathlib import Path

def add_separators_after_h1(markdown_content: str) -> str:
    """
    Add triple dash separators after every level 1 header

    Args:
        markdown_content: Raw markdown text

    Returns:
        Markdown content with separators added
    """
    lines = markdown_content.split('\n')
    result_lines = []

    for i, line in enumerate(lines):
        result_lines.append(line)

        # Check if this is a level 1 header (starts with # followed by space)
        if re.match(r'^#\s+', line):
            # Add separator on the next line
            result_lines.append('---')

    return '\n'.join(result_lines)

def process_child_folder():
    """Process all markdown files in the child folder"""
    child_folder = Path('input/pva.1/child')

    if not child_folder.exists():
        print(f"❌ Child folder not found: {child_folder}")
        return

    markdown_files = list(child_folder.glob('*.md'))

    if not markdown_files:
        print("❌ No markdown files found in child folder")
        return

    print(f"📁 Processing {len(markdown_files)} markdown files in {child_folder}")
    print("=" * 50)

    for file_path in markdown_files:
        print(f"📄 Processing: {file_path.name}")

        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Add separators after H1 headers
            updated_content = add_separators_after_h1(content)

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print(f"✅ Updated: {file_path.name}")

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")

    print("=" * 50)
    print("🎉 Separator addition complete!")

if __name__ == "__main__":
    process_child_folder()