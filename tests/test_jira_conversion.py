#!/usr/bin/env python3
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
"""
Test script to verify Jira markdown conversion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jira_markdown_converter import JiraMarkdownConverter

def test_jira_conversion():
    """Test how markdown is converted to Jira markup"""

    # Test markdown content
    test_markdown = """# Test Document

This is a **bold** text and this is *italic* text.

## Code Example

Here's a Python code block:

```python
def hello_world():
    print("Hello, World!")
    return True
```

## Lists (Markdown style - 4 spaces)

- Item 1
- Item 2
    - Nested item (4 spaces)
        - Deeper nested item (8 spaces)
- Item 3

## Lists (Jira style - needs pre-processing)

* Item 1
* Item 2
** Nested item
* Item 3

## Strikethrough

~~This text is strikethrough~~

## Links

[Google](https://www.google.com)

## Inline Code

Use `print()` function to output text.
"""

    print("Original Markdown:")
    print("=" * 50)
    print(test_markdown)
    print()

    # Test the conversion
    converter = JiraMarkdownConverter(
        base_url="https://test.com",
        username="test",
        api_token="test",
        project_key="TEST"
    )

    # Show the raw HTML from markdown library
    import markdown
    raw_html = markdown.markdown(
        test_markdown,
        extensions=['markdown.extensions.def_list', 'markdown.extensions.fenced_code', 'markdown.extensions.nl2br', 'markdown.extensions.tables', 'markdown.extensions.toc']
    )

    print("Raw HTML from Markdown Library:")
    print("=" * 50)
    print(raw_html)
    print()

    jira_markup = converter.convert_markdown_to_jira(test_markdown)

    print("Jira Markup:")
    print("=" * 50)
    print(jira_markup)
    print()

def test_jira_config():
    """Test Jira configuration management"""
    from jira_config import JiraConfig

    print("Testing Jira Configuration:")
    print("=" * 50)

    # Create a test config
    config = JiraConfig("test_jira_config.json")

    # Test properties
    config.base_url = "https://test.atlassian.net"
    config.username = "test@example.com"
    config.api_token = "test-token"
    config.project_key = "TEST"
    config.default_issue_type = "Bug"
    config.default_priority = "High"

    print(f"Base URL: {config.base_url}")
    print(f"Username: {config.username}")
    print(f"Project Key: {config.project_key}")
    print(f"Default Issue Type: {config.default_issue_type}")
    print(f"Default Priority: {config.default_priority}")
    print(f"Is Configured: {config.is_configured()}")

    # Clean up test file
    if config.config_file.exists():
        config.config_file.unlink()

if __name__ == "__main__":
    print("Testing Jira Markdown Converter")
    print("=" * 60)
    print()

    test_jira_conversion()
    test_jira_config()

    print("Tests completed!")