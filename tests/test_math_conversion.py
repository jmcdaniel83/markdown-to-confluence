#!/usr/bin/env python3
"""
Test script to verify math expression conversion
"""

import markdown
from confluence_markdown_converter import ConfluenceMarkdownConverter

def test_math_conversion():
    """Test how math expressions are being converted"""
    
    # Test markdown content with math
    test_markdown = """# Math Test

## Inline Math
The quadratic formula is: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$

## Block Math
$$
\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}
$$

$$
\\begin{align}
y &= mx + b \\\\
&= 2x + 3
\\end{align}
$$
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
    test_math_conversion() 