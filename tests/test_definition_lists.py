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
Test script to verify definition list conversion
"""

import markdown
from confluence_markdown_converter import ConfluenceMarkdownConverter

def test_definition_lists():
    """Test how definition lists are being converted"""
    
    # Test markdown content with definition lists
    test_markdown = """# Definition List Test

## Basic Definition List

Term 1
: Definition 1

Term 2
: Definition 2
: Another definition for term 2

## More Complex Definitions

HTML
: HyperText Markup Language

CSS
: Cascading Style Sheets

JavaScript
: A programming language for the web
"""
    
    print("Original Markdown:")
    print("=" * 50)
    print(test_markdown)
    print()
    
    # Convert to HTML using markdown library
    html_content = markdown.markdown(
        test_markdown,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br',
            'mdx_math'
        ]
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

if __name__ == "__main__":
    test_definition_lists() 