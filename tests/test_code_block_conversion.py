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
Test script to debug code block conversion
"""

import markdown
import re
from confluence_markdown_converter import ConfluenceMarkdownConverter

def test_code_block_conversion():
    """Test how code blocks are being converted"""
    
    # Test markdown content
    test_markdown = """# Test Document

This is a basic code block:

```python
def hello_world():
    print("Hello, World!")
    return True
```

And another without language:

```
This is plain text
with multiple lines
```

And inline code: `print("hello")`
"""
    
    print("Original Markdown:")
    print("=" * 50)
    print(test_markdown)
    print()
    
    # Convert to HTML using markdown library
    html = markdown.markdown(
        test_markdown,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
    )
    
    print("Generated HTML:")
    print("=" * 50)
    print(html)
    print()
    
    # Test the current conversion
    converter = ConfluenceMarkdownConverter(
        base_url="https://test.com",
        username="test",
        api_token="test",
        space_key="test"
    )
    
    confluence_markup = converter.convert_markdown_to_confluence(test_markdown)
    
    print("Current Confluence Markup:")
    print("=" * 50)
    print(confluence_markup)
    print()
    
    # Test improved conversion
    improved_markup = convert_markdown_to_confluence_improved(test_markdown)
    
    print("Improved Confluence Markup:")
    print("=" * 50)
    print(improved_markup)

def convert_markdown_to_confluence_improved(markdown_content: str) -> str:
    """Improved conversion that handles code blocks better"""
    
    # First convert markdown to HTML
    html = markdown.markdown(
        markdown_content,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
    )
    
    # Convert HTML to Confluence markup with better code block handling
    markup = html
    
    # Improved code block handling
    # Handle code blocks with language specification
    markup = re.sub(
        r'<pre><code class="language-(\w+)">(.*?)</code></pre>',
        lambda m: f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{m.group(1)}</ac:parameter><ac:plain-text-body><![CDATA[{m.group(2)}]]></ac:plain-text-body></ac:structured-macro>',
        markup,
        flags=re.DOTALL
    )
    
    # Handle code blocks without language specification
    markup = re.sub(
        r'<pre><code>(.*?)</code></pre>',
        lambda m: f'<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{m.group(1)}]]></ac:plain-text-body></ac:structured-macro>',
        markup,
        flags=re.DOTALL
    )
    
    # Handle inline code
    markup = re.sub(r'<code>(.*?)</code>', r'<code>\1</code>', markup)
    
    # Handle other elements (simplified for this test)
    markup = re.sub(r'<h1>(.*?)</h1>', r'<h1>\1</h1>', markup)
    markup = re.sub(r'<h2>(.*?)</h2>', r'<h2>\1</h2>', markup)
    markup = re.sub(r'<h3>(.*?)</h3>', r'<h3>\1</h3>', markup)
    markup = re.sub(r'<p>(.*?)</p>', r'<p>\1</p>', markup)
    
    return markup

if __name__ == "__main__":
    test_code_block_conversion() 