#!/usr/bin/env python3
"""
Script to adjust header levels in markdown files within the child folder.
Reduces all headers by 1 level except the first header which remains as the page title.
"""

import os
import re
from pathlib import Path

def adjust_header_levels(markdown_content: str) -> str:
    """
    Adjust header levels by reducing all headers by 1 level
    (except the first header which remains as the page title)

    Args:
        markdown_content: Raw markdown text

    Returns:
        Markdown content with adjusted header levels
    """
    lines = markdown_content.split('\n')
    adjusted_lines = []
    first_header_found = False

    for line in lines:
        # Check if this is a header line
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            header_level = len(header_match.group(1))
            header_text = header_match.group(2)

            if not first_header_found:
                # Keep the first header as is (page title)
                adjusted_lines.append(line)
                first_header_found = True
            else:
                # Reduce header level by 1 for all subsequent headers
                new_level = max(1, header_level - 1)
                new_header = '#' * new_level + ' ' + header_text
                adjusted_lines.append(new_header)
        else:
            adjusted_lines.append(line)

    return '\n'.join(adjusted_lines)

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

            # Adjust header levels
            adjusted_content = adjust_header_levels(content)

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(adjusted_content)

            print(f"✅ Updated: {file_path.name}")

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")

    print("=" * 50)
    print("🎉 Header adjustment complete!")

if __name__ == "__main__":
    process_child_folder()