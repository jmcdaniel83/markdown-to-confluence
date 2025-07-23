#!/usr/bin/env python3
"""
Script to add triple dash separators after every level 1 header in markdown files.
"""

import re
import argparse
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
            # Check the next line to see if a separator already exists
            if i + 1 < len(lines) and lines[i+1].strip() == '---':
                continue  # Separator already exists, do nothing
            else:
                # Add separator on the next line
                result_lines.append('---')

    return '\n'.join(result_lines)

def process_folder(folder_path: Path): # Renamed and added folder_path argument
    """Process all markdown files in the specified folder"""
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_path}")
        return

    markdown_files = list(folder_path.glob('*.md'))

    if not markdown_files:
        print(f"❌ No markdown files found in {folder_path}")
        return

    print(f"📁 Processing {len(markdown_files)} markdown files in {folder_path}")
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
    parser = argparse.ArgumentParser(description='Add triple dash separators after level 1 headers in markdown files.')
    parser.add_argument('--folder', type=str, help='The path to the folder containing markdown files to process.')
    args = parser.parse_args()

    target_folder = Path(args.folder)
    process_folder(target_folder)