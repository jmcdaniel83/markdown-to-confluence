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
Debug script to see exact HTML structure for code blocks
"""

import markdown

def debug_code_block_html():
    """Debug the exact HTML structure for code blocks"""
    
    test_markdown = """```python
def hello_world():
    print("Hello, World!")
    return True
```"""
    
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
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
    )
    
    print("Generated HTML:")
    print("=" * 50)
    print(html_content)
    print()
    
    # Also test without codehilite
    html_content_no_highlight = markdown.markdown(
        test_markdown,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
    )
    
    print("Generated HTML (without codehilite):")
    print("=" * 50)
    print(html_content_no_highlight)

if __name__ == "__main__":
    debug_code_block_html() 