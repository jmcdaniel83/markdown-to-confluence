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
Test script to debug strikethrough conversion in the comprehensive example
"""

import markdown
from confluence_markdown_converter import ConfluenceMarkdownConverter, MARKDOWN_EXTENSIONS

def test_comprehensive_strikethrough():
    """Test strikethrough conversion in the comprehensive example"""

    # Read the comprehensive example file
    with open('docs/example_comprehensive.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Find the strikethrough line
    import re
    strikethrough_lines = re.findall(r'.*~~.*~~.*', markdown_content, re.MULTILINE)

    print("Found strikethrough lines in comprehensive file:")
    print("=" * 50)
    for line in strikethrough_lines:
        print(f"'{line.strip()}'")
    print()

    # Test the conversion step by step
    print("Step 1: Pre-processing strikethrough")
    print("=" * 50)
    # Pre-process strikethrough (~~text~~ -> <del>text</del>)
    processed_content = re.sub(r'~~(.*?)~~', r'<del>\1</del>', markdown_content)
    strikethrough_processed = re.findall(r'.*<del>.*</del>.*', processed_content, re.MULTILINE)
    for line in strikethrough_processed:
        print(f"'{line.strip()}'")
    print()

    print("Step 2: Markdown to HTML conversion")
    print("=" * 50)
    html_content = markdown.markdown(
        processed_content,
        extensions=MARKDOWN_EXTENSIONS
    )
    # Find strikethrough in HTML
    strikethrough_html = re.findall(r'.*<del>.*</del>.*', html_content, re.MULTILINE)
    for line in strikethrough_html:
        print(f"'{line.strip()}'")
    print()

    print("Step 3: Final Confluence conversion")
    print("=" * 50)
    converter = ConfluenceMarkdownConverter(
        base_url="https://test.com",
        username="test",
        api_token="test",
        space_key="test"
    )

    confluence_markup = converter.convert_markdown_to_confluence(markdown_content)

    # Find strikethrough in final output
    strikethrough_final = re.findall(r'.*text-decoration: line-through.*', confluence_markup, re.MULTILINE)
    for line in strikethrough_final:
        print(f"'{line.strip()}'")
    print()

if __name__ == "__main__":
    test_comprehensive_strikethrough()