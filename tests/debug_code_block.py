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