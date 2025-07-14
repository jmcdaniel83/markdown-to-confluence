#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/env python3
"""
Test script to debug placeholder conversion
"""

import markdown
import re
from confluence_markdown_converter import ConfluenceMarkdownConverter, MARKDOWN_EXTENSIONS

def test_placeholders():
    """Test placeholder conversion for strikethrough and images"""
    
    # Test markdown content with strikethrough and images
    test_markdown = """# Placeholder Test

This is normal text.

~~This text is strikethrough~~

Here's an image:

![Markdown Logo](https://markdown-here.com/img/icon256.png)

And another with title:

![GitHub Octocat](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png "GitHub Logo")

More text here.
"""
    
    print("Original Markdown:")
    print("=" * 50)
    print(test_markdown)
    print()
    
    # Convert to HTML using markdown library
    html_content = markdown.markdown(
        test_markdown,
        extensions=MARKDOWN_EXTENSIONS
    )
    
    print("Generated HTML:")
    print("=" * 50)
    print(html_content)
    print()
    
    # Test the conversion
    converter = ConfluenceMarkdownConverter(
        base_url="https://test.com",
        username="test",
        api_token="test",
        space_key="test"
    )
    
    confluence_markup = converter.convert_markdown_to_confluence(test_markdown)
    
    print("Confluence Markup:")
    print("=" * 50)
    print(confluence_markup)
    print()
    
    # Check for placeholders
    strikes = re.findall(r'\[STRIKE\].*?\[/STRIKE\]', confluence_markup)
    images = re.findall(r'\[IMAGE\].*?\[/IMAGE\]', confluence_markup)
    
    print("Found [STRIKE] placeholders:")
    print("=" * 50)
    for strike in strikes:
        print(f"'{strike}'")
    print()
    
    print("Found [IMAGE] placeholders:")
    print("=" * 50)
    for image in images:
        print(f"'{image}'")
    print()
    
    # Analyze what needs to be updated
    print("ANALYSIS:")
    print("=" * 50)
    
    # Check strikethrough handling
    if '<del>' in html_content:
        print("✓ HTML contains <del> tags for strikethrough")
    elif '<s>' in html_content:
        print("✓ HTML contains <s> tags for strikethrough")
    else:
        print("✗ HTML does not contain strikethrough tags")
    
    # Check image handling
    if '<img' in html_content:
        print("✓ HTML contains <img> tags")
        img_tags = re.findall(r'<img[^>]+>', html_content)
        print(f"  Found {len(img_tags)} image tags:")
        for i, img in enumerate(img_tags, 1):
            print(f"    {i}. {img}")
    else:
        print("✗ HTML does not contain image tags")
    
    # Check if placeholders are being created correctly
    if strikes:
        print(f"✓ Found {len(strikes)} [STRIKE] placeholders")
    else:
        print("✗ No [STRIKE] placeholders found")
    
    if images:
        print(f"✓ Found {len(images)} [IMAGE] placeholders")
    else:
        print("✗ No [IMAGE] placeholders found")
    
    # Debug image regex pattern
    print("\nDEBUGGING IMAGE REGEX:")
    print("=" * 50)
    
    # Test the current regex pattern from the converter
    current_pattern = r'<img src="([^"]+)" alt="([^"]*)"(?: title="([^"]*)")?\s*/?>'
    print(f"Current regex pattern: {current_pattern}")
    
    # Test against the actual HTML
    matches = re.findall(current_pattern, html_content)
    print(f"Matches found with current pattern: {len(matches)}")
    for i, match in enumerate(matches, 1):
        print(f"  {i}. src='{match[0]}', alt='{match[1]}', title='{match[2]}'")
    
    # Test a more flexible pattern that handles attribute order
    flexible_pattern = r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*(?:title="([^"]*)")?[^>]*/?>'
    print(f"\nFlexible regex pattern: {flexible_pattern}")
    
    flexible_matches = re.findall(flexible_pattern, html_content)
    print(f"Matches found with flexible pattern: {len(flexible_matches)}")
    for i, match in enumerate(flexible_matches, 1):
        print(f"  {i}. src='{match[0]}', alt='{match[1]}', title='{match[2]}'")
    
    # Test even more flexible pattern
    very_flexible_pattern = r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*/?>'
    print(f"\nVery flexible regex pattern: {very_flexible_pattern}")
    
    very_flexible_matches = re.findall(very_flexible_pattern, html_content)
    print(f"Matches found with very flexible pattern: {len(very_flexible_matches)}")
    for i, match in enumerate(very_flexible_matches, 1):
        print(f"  {i}. src='{match[0]}', alt='{match[1]}'")

if __name__ == "__main__":
    test_placeholders() 