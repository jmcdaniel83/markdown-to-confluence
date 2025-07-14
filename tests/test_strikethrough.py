#!/usr/bin/env python3
"""
Test script to debug strikethrough conversion
"""

import markdown
from confluence_markdown_converter import ConfluenceMarkdownConverter, MARKDOWN_EXTENSIONS

def test_strikethrough():
    """Test how strikethrough is being converted"""
    
    # Test markdown content with strikethrough
    test_markdown = """# Strikethrough Test

This is normal text.

~~This text is strikethrough~~

This is more normal text.
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

if __name__ == "__main__":
    test_strikethrough() 