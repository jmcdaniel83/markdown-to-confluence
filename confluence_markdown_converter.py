#!/usr/bin/env python3
"""
Confluence Markdown Converter and Publisher

This script converts markdown files to Confluence format and publishes them
to Confluence using the REST API. It handles markdown to Confluence markup
conversion and maintains proper formatting.

Requirements:
    pip install requests markdown python-frontmatter
"""

import os
import sys
import json
import requests
import markdown
import re
import html
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin
import argparse
from pathlib import Path

# List of markdown extensions used for conversion
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.def_list',
    'markdown.extensions.fenced_code',
    'markdown.extensions.nl2br',
    'markdown.extensions.tables',
    'markdown.extensions.toc',
    'mdx_math',
]

def strip_html_tags(text):
    """Remove all HTML tags from the given text."""
    return re.sub(r'<[^>]+>', '', text)

class ConfluenceMarkdownConverter:
    """Convert markdown to Confluence markup and publish to Confluence"""
    
    def __init__(self, base_url: str, username: str, api_token: str, space_key: str):
        """
        Initialize the converter with Confluence credentials
        
        Args:
            base_url: Confluence base URL (e.g., https://your-domain.atlassian.net)
            username: Confluence username or email
            api_token: Confluence API token (not password)
            space_key: Confluence space key
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.space_key = space_key
        self.session = requests.Session()
        self.session.auth = (username, api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def convert_markdown_to_confluence(self, markdown_content: str) -> str:
        """
        Convert markdown content to Confluence markup
        
        Args:
            markdown_content: Raw markdown text
            
        Returns:
            Confluence markup string
        """
        
        # First convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=MARKDOWN_EXTENSIONS
        )
        
        # Convert HTML to Confluence markup
        confluence_markup = self._html_to_confluence_markup(html_content, markdown_content)
        
        return confluence_markup
    
    def _html_to_confluence_markup(self, html_content: str, markdown_content: str) -> str:
        """
        Convert HTML to Confluence markup
        
        Args:
            html_content: HTML content
            
        Returns:
            Confluence markup string
        """
        # Replace HTML tags with Confluence markup
        markup = html_content
        
        # Headers
        markup = re.sub(r'<h1>(.*?)</h1>', r'<h1>\1</h1>', markup)
        markup = re.sub(r'<h2>(.*?)</h2>', r'<h2>\1</h2>', markup)
        markup = re.sub(r'<h3>(.*?)</h3>', r'<h3>\1</h3>', markup)
        markup = re.sub(r'<h4>(.*?)</h4>', r'<h4>\1</h4>', markup)
        markup = re.sub(r'<h5>(.*?)</h5>', r'<h5>\1</h5>', markup)
        markup = re.sub(r'<h6>(.*?)</h6>', r'<h6>\1</h6>', markup)
        
        # Bold and italic
        markup = re.sub(r'<strong>(.*?)</strong>', r'<strong>\1</strong>', markup)
        markup = re.sub(r'<em>(.*?)</em>', r'<em>\1</em>', markup)
        
        # Strikethrough
        markup = re.sub(r'<del>(.*?)</del>', r'<span style="text-decoration: line-through;">\1</span>', markup)
        markup = re.sub(r'<s>(.*?)</s>', r'<span style="text-decoration: line-through;">\1</span>', markup)
        
        # Code blocks - handle standard markdown output (without codehilite)
        # Handle code blocks with language specification
        markup = re.sub(
            r'<pre><code class="language-([\w\-]+)">(.*?)</code></pre>',
            lambda m: f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{m.group(1)}</ac:parameter><ac:plain-text-body><![CDATA[{strip_html_tags(html.unescape(m.group(2)))}]]></ac:plain-text-body></ac:structured-macro>',
            markup,
            flags=re.DOTALL
        )
        # Handle code blocks without language specification
        markup = re.sub(
            r'<pre><code>(.*?)</code></pre>',
            lambda m: f'<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{strip_html_tags(html.unescape(m.group(1)))}]]></ac:plain-text-body></ac:structured-macro>',
            markup,
            flags=re.DOTALL
        )
        
        # Handle math expressions
        # Block math (script type="math/tex; mode=display")
        markup = re.sub(
            r'<script type="math/tex; mode=display">(.*?)</script>',
            lambda m: f'<ac:structured-macro ac:name="math"><ac:parameter ac:name="display">block</ac:parameter><ac:plain-text-body><![CDATA[{m.group(1)}]]></ac:plain-text-body></ac:structured-macro>',
            markup,
            flags=re.DOTALL
        )
        
        # Inline math (script type="math/tex")
        markup = re.sub(
            r'<script type="math/tex">(.*?)</script>',
            lambda m: f'<ac:structured-macro ac:name="math"><ac:plain-text-body><![CDATA[{m.group(1)}]]></ac:plain-text-body></ac:structured-macro>',
            markup,
            flags=re.DOTALL
        )
        
        # Also handle raw LaTeX in text (fallback for inline math)
        markup = re.sub(
            r'\$([^$]+)\$',
            lambda m: f'<ac:structured-macro ac:name="math"><ac:plain-text-body><![CDATA[{m.group(1)}]]></ac:plain-text-body></ac:structured-macro>',
            markup
        )
        
        # Inline code
        markup = re.sub(r'<code>(.*?)</code>', r'<code>\1</code>', markup)
        
        # Links
        markup = re.sub(r'<a href="([^"]+)">(.*?)</a>', r'<a href="\1">\2</a>', markup)
        
        # Lists
        markup = re.sub(r'<ul>(.*?)</ul>', r'<ul>\1</ul>', markup, flags=re.DOTALL)
        markup = re.sub(r'<ol>(.*?)</ol>', r'<ol>\1</ol>', markup, flags=re.DOTALL)
        markup = re.sub(r'<li>(.*?)</li>', r'<li>\1</li>', markup)
        
        # Tables
        markup = re.sub(r'<table>(.*?)</table>', r'<table>\1</table>', markup, flags=re.DOTALL)
        markup = re.sub(r'<thead>(.*?)</thead>', r'<thead>\1</thead>', markup, flags=re.DOTALL)
        markup = re.sub(r'<tbody>(.*?)</tbody>', r'<tbody>\1</tbody>', markup, flags=re.DOTALL)
        markup = re.sub(r'<tr>(.*?)</tr>', r'<tr>\1</tr>', markup, flags=re.DOTALL)
        markup = re.sub(r'<th>(.*?)</th>', r'<th>\1</th>', markup)
        markup = re.sub(r'<td>(.*?)</td>', r'<td>\1</td>', markup)
        
        # Blockquotes
        markup = re.sub(r'<blockquote>(.*?)</blockquote>', r'<blockquote>\1</blockquote>', markup, flags=re.DOTALL)
        
        # Paragraphs
        markup = re.sub(r'<p>(.*?)</p>', r'<p>\1</p>', markup)
        
        # Line breaks
        markup = re.sub(r'<br/?>', r'<br/>', markup)
        
        # Handle definition lists
        markup = re.sub(
            r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>',
            lambda m: f'<p><strong>{m.group(1)}:</strong> {m.group(2)}</p>',
            markup,
            flags=re.DOTALL
        )

        # Handle footnotes (Markdown style)
        markup = self._convert_footnotes(markup, markdown_content)
        
        # Handle strikethrough (~~text~~) in post-processing (robust)
        markup = re.sub(r'~~(.*?)~~', r'[STRIKE]\1[/STRIKE]', markup)
        # Also handle <del> tags from pre-processing
        markup = re.sub(r'<del>(.*?)</del>', r'[STRIKE]\1[/STRIKE]', markup)
        # Also handle <s> tags
        markup = re.sub(r'<s>(.*?)</s>', r'[STRIKE]\1[/STRIKE]', markup)

        # Add [IMAGE] <file_name> | <footer_text> [/IMAGE] below each image
        def image_footer(match):
            img_tag = match.group(0)
            # Extract src, alt, and title attributes
            src_match = re.search(r'src="([^"]+)"', img_tag)
            alt_match = re.search(r'alt="([^"]*)"', img_tag)
            title_match = re.search(r'title="([^"]*)"', img_tag)
            src = src_match.group(1) if src_match else ''
            alt = alt_match.group(1) if alt_match else ''
            title = title_match.group(1) if title_match else ''
            file_name = src.split('/')[-1] if src else ''
            return f'{img_tag}<br/>[IMAGE] {file_name} | {title} [/IMAGE]'
        # Match <img ...> tags, possibly spanning multiple lines
        markup = re.sub(r'<img[^>]*>', image_footer, markup, flags=re.DOTALL)
        
        return markup
    
    def _convert_footnotes(self, markup: str, markdown_content: str) -> str:
        """
        Convert markdown footnotes to Confluence-style anchor links and footnote list.
        """
        import re
        # Find all footnote definitions in the original markdown
        footnote_defs = re.findall(r'^\[\^([\w\d]+)\]:\s*(.*)$', markdown_content, re.MULTILINE)
        if not footnote_defs:
            return markup
        # Replace in-text references with anchor links
        for num, _ in footnote_defs:
            markup = re.sub(r'\[\^' + re.escape(num) + r'\]', f'<sup><a href="##footnote-{num}">[{num}]</a></sup>', markup)
        # Build footnote section
        footnote_section = '\n<hr/><h3>Footnotes</h3>\n'
        for num, text in footnote_defs:
            footnote_section += f'<p><a class="cc-i7tlu0" data-group="deeplink" name="#footnote-{num}"></a>[{num}] {text}</p>\n'
        # Remove original footnote definitions if present
        markup = re.sub(r'<p>\[\^([\w\d]+)\]:.*?</p>', '', markup)
        # Append footnote section to the end
        markup += footnote_section
        return markup
    
    def get_page_id(self, page_title: str) -> Optional[str]:
        """
        Get page ID by title
        
        Args:
            page_title: Title of the page
            
        Returns:
            Page ID if found, None otherwise
        """
        url = f"{self.base_url}/rest/api/content"
        params = {
            'title': page_title,
            'spaceKey': self.space_key,
            'expand': 'version'
        }
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                return results[0]['id']
        return None
    
    def create_page(self, title: str, content: str, parent_id: Optional[str] = None) -> Dict:
        """
        Create a new page in Confluence
        
        Args:
            title: Page title
            content: Page content in Confluence markup
            parent_id: Optional parent page ID
            
        Returns:
            Response data from Confluence API
        """
        url = f"{self.base_url}/rest/api/content"
        
        data = {
            "type": "page",
            "title": title,
            "space": {"key": self.space_key},
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            },
            "version": {"number": 1}
        }
        
        if parent_id:
            data["ancestors"] = [{"id": parent_id}]
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def update_page(self, page_id: str, title: str, content: str, version: int) -> Dict:
        """
        Update an existing page in Confluence
        
        Args:
            page_id: ID of the page to update
            title: New page title
            content: New page content in Confluence markup
            version: Current version number
            
        Returns:
            Response data from Confluence API
        """
        url = f"{self.base_url}/rest/api/content/{page_id}"
        
        data = {
            "version": {"number": version + 1},
            "title": title,
            "type": "page",
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }
        
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def publish_markdown_file(self, file_path: str, page_title: Optional[str] = None, 
                            parent_page_title: Optional[str] = None) -> Dict:
        """
        Convert and publish a markdown file to Confluence
        
        Args:
            file_path: Path to the markdown file
            page_title: Optional custom page title (defaults to filename)
            parent_page_title: Optional parent page title
            
        Returns:
            Response data from Confluence API
        """
        # Read markdown file
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Determine page title
        if not page_title:
            page_title = Path(file_path).stem.replace('_', ' ').title()
        
        # Convert markdown to Confluence markup
        confluence_content = self.convert_markdown_to_confluence(markdown_content)
        
        # Get parent page ID if specified
        parent_id = None
        if parent_page_title:
            parent_id = self.get_page_id(parent_page_title)
            if not parent_id:
                print(f"Warning: Parent page '{parent_page_title}' not found")
        
        # Check if page already exists
        existing_page_id = self.get_page_id(page_title)
        
        if existing_page_id:
            # Update existing page
            print(f"Updating existing page: {page_title}")
            # Get current version
            url = f"{self.base_url}/rest/api/content/{existing_page_id}"
            response = self.session.get(url)
            response.raise_for_status()
            current_version = response.json()['version']['number']
            
            result = self.update_page(existing_page_id, page_title, confluence_content, current_version)
            print(f"Page updated successfully: {result['_links']['webui']}")
        else:
            # Create new page
            print(f"Creating new page: {page_title}")
            result = self.create_page(page_title, confluence_content, parent_id)
            print(f"Page created successfully: {result['_links']['webui']}")
        
        return result

def main():
    """Main function to handle command line arguments and execute conversion"""
    parser = argparse.ArgumentParser(description='Convert markdown files to Confluence pages')
    parser.add_argument('files', nargs='+', help='Markdown files to convert')
    parser.add_argument('--base-url', required=True, help='Confluence base URL')
    parser.add_argument('--username', required=True, help='Confluence username/email')
    parser.add_argument('--api-token', required=True, help='Confluence API token')
    parser.add_argument('--space-key', required=True, help='Confluence space key')
    parser.add_argument('--parent-page', help='Parent page title (optional)')
    parser.add_argument('--page-title', help='Custom page title (optional)')
    
    args = parser.parse_args()
    
    # Initialize converter
    converter = ConfluenceMarkdownConverter(
        base_url=args.base_url,
        username=args.username,
        api_token=args.api_token,
        space_key=args.space_key
    )
    
    # Process each file
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            continue
            
        try:
            result = converter.publish_markdown_file(
                file_path=file_path,
                page_title=args.page_title,
                parent_page_title=args.parent_page
            )
            print(f"Successfully processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    main() 