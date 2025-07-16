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
]

# Math extensions (optional)
MATH_EXTENSIONS = [
    'mdx_math',
]

def strip_html_tags(text):
    """Remove all HTML tags from the given text."""
    return re.sub(r'<[^>]+>', '', text)

class ConfluenceMarkdownConverter:
    """Convert markdown to Confluence markup and publish to Confluence"""

    def __init__(self, base_url: str, username: str, api_token: str, space_key: str, enable_math: bool = False):
        """
        Initialize the converter with Confluence credentials

        Args:
            base_url: Confluence base URL (e.g., https://your-domain.atlassian.net)
            username: Confluence username or email
            api_token: Confluence API token (not password)
            space_key: Confluence space key
            enable_math: Whether to enable math conversion (default: False)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.space_key = space_key
        self.enable_math = enable_math
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

        # Determine which extensions to use
        extensions = MARKDOWN_EXTENSIONS.copy()
        if self.enable_math:
            extensions.extend(MATH_EXTENSIONS)

        # First convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=extensions
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
            lambda m: f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{m.group(1)}</ac:parameter><ac:plain-text-body><![CDATA[{html.unescape(m.group(2)).strip()}]]></ac:plain-text-body></ac:structured-macro>',
            markup,
            flags=re.DOTALL
        )
        # Handle code blocks without language specification
        markup = re.sub(
            r'<pre><code>(.*?)</code></pre>',
            lambda m: f'<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{html.unescape(m.group(1)).strip()}]]></ac:plain-text-body></ac:structured-macro>',
            markup,
            flags=re.DOTALL
        )

        # Handle math expressions (only if math is enabled)
        if self.enable_math:
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

        # Handle special blockquotes (Info, Warning, Error) before general blockquotes
        markup = self._convert_special_blockquotes(markup)

        # General blockquotes (fallback for any remaining)
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

    def _convert_special_blockquotes(self, markup: str) -> str:
        """
        Convert special blockquotes (Info, Warning, Error) to Confluence panel HTML.
        """
        # Convert Info blockquotes - match HTML structure with <strong>Info:</strong>
        markup = re.sub(
            r'<blockquote>\s*<p[^>]*><strong[^>]*>Info:</strong>\s*(.*?)</p>.*?</blockquote>',
            lambda m: f'<div class="ak-editor-panel cc-l5mesu" data-panel-type="info"><div class="ak-editor-panel__icon"><span data-vc="icon-undefined" role="img" aria-label="info panel" class="_1e0c1o8l _1o9zidpf _vyfuvuon _vwz4kb7n _1szv15vq _1tly15vq _rzyw1osq _17jb1osq _1ksvoz0e _3se1x1jp _re2rglyw _1veoyfq0 _1kg81r31 _jcxd1r8n _gq0g1onz _1trkwc43" style="--icon-primary-color: currentColor;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" role="presentation"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 22C9.34784 22 6.8043 20.9464 4.92893 19.0711C3.05357 17.1957 2 14.6522 2 12C2 9.34784 3.05357 6.8043 4.92893 4.92893C6.8043 3.05357 9.34784 2 12 2C14.6522 2 17.1957 3.05357 19.0711 4.92893C20.9464 6.8043 22 9.34784 22 12C22 14.6522 20.9464 17.1957 19.0711 19.0711C17.1957 20.9464 14.6522 22 12 22V22ZM12 11.375C11.6685 11.375 11.3505 11.5067 11.1161 11.7411C10.8817 11.9755 10.75 12.2935 10.75 12.625V15.75C10.75 16.0815 10.8817 16.3995 11.1161 16.6339C11.3505 16.8683 11.6685 17 12 17C12.3315 17 12.6495 16.8683 12.8839 16.6339C13.1183 16.3995 13.25 16.0815 13.25 15.75V12.625C13.25 12.2935 13.1183 11.9755 12.8839 11.7411C12.6495 11.5067 12.3315 11.375 12 11.375ZM12 9.96875C12.4558 9.96875 12.893 9.78767 13.2153 9.46534C13.5377 9.14301 13.7188 8.70584 13.7188 8.25C13.7188 7.79416 13.5377 7.35699 13.2153 7.03466C12.893 6.71233 12.4558 6.53125 12 6.53125C11.5442 6.53125 11.107 6.71233 10.7847 7.03466C10.4623 7.35699 10.2812 7.79416 10.2812 8.25C10.2812 8.70584 10.4623 9.14301 10.7847 9.46534C11.107 9.78767 11.5442 9.96875 12 9.96875Z" fill="currentColor"></path></svg></span></div><div class="ak-editor-panel__content"><p data-renderer-start-pos="87">{m.group(1).strip()}</p></div></div>',
            markup,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Convert Warning blockquotes - match HTML structure with <strong>Warning:</strong>
        markup = re.sub(
            r'<blockquote>\s*<p[^>]*><strong[^>]*>Warning:</strong>\s*(.*?)</p>.*?</blockquote>',
            lambda m: f'<div class="ak-editor-panel cc-l5mesu" data-panel-type="warning"><div class="ak-editor-panel__icon"><span data-vc="icon-undefined" role="img" aria-label="warning panel" class="_1e0c1o8l _1o9zidpf _vyfuvuon _vwz4kb7n _1szv15vq _1tly15vq _rzyw1osq _17jb1osq _1ksvoz0e _3se1x1jp _re2rglyw _1veoyfq0 _1kg81r31 _jcxd1r8n _gq0g1onz _1trkwc43" style="--icon-primary-color: currentColor;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" role="presentation"><path fill-rule="evenodd" clip-rule="evenodd" d="M13.4897 4.34592L21.8561 18.8611C21.9525 19.0288 22.0021 19.2181 21.9999 19.4101C21.9977 19.6021 21.9438 19.7903 21.8435 19.9559C21.7432 20.1215 21.6001 20.2588 21.4282 20.3542C21.2563 20.4497 21.0616 20.4999 20.8636 20.5H3.13707C2.93882 20.5 2.74401 20.4498 2.57196 20.3543C2.39992 20.2588 2.25663 20.1213 2.15631 19.9556C2.05598 19.7898 2.00212 19.6015 2.00006 19.4093C1.998 19.2171 2.04782 19.0278 2.14456 18.86L10.5121 4.34592C10.6602 4.08939 10.8762 3.87577 11.1377 3.72708C11.3993 3.57838 11.6971 3.5 12.0003 3.5C12.3036 3.5 12.6013 3.57838 12.8629 3.72708C13.1245 3.87577 13.3404 4.08939 13.4885 4.34592H13.4897ZM12.0003 7.82538C11.8232 7.82537 11.6482 7.86212 11.4869 7.93317C11.3257 8.00423 11.182 8.10793 11.0656 8.2373C10.9492 8.36668 10.8627 8.51872 10.8119 8.68321C10.7611 8.8477 10.7473 9.02083 10.7713 9.19093L11.3546 13.3416C11.3754 13.4933 11.4523 13.6326 11.5711 13.7334C11.6899 13.8343 11.8424 13.8899 12.0003 13.8899C12.1582 13.8899 12.3107 13.8343 12.4295 13.7334C12.5483 13.6326 12.6253 13.4933 12.6461 13.3416L13.2293 9.19093C13.2533 9.02083 13.2395 8.8477 13.1887 8.68321C13.138 8.51872 13.0515 8.36668 12.935 8.2373C12.8186 8.10793 12.6749 8.00423 12.5137 7.93317C12.3525 7.86212 12.1774 7.82537 12.0003 7.82538V7.82538ZM12.0003 17.3369C12.3395 17.3369 12.6649 17.2062 12.9047 16.9737C13.1446 16.7412 13.2793 16.4258 13.2793 16.0969C13.2793 15.7681 13.1446 15.4527 12.9047 15.2202C12.6649 14.9877 12.3395 14.857 12.0003 14.857C11.6611 14.857 11.3358 14.9877 11.0959 15.2202C10.8561 15.4527 10.7213 15.7681 10.7213 16.0969C10.7213 16.4258 10.8561 16.7412 11.0959 16.9737C11.3358 17.2062 11.6611 17.3369 12.0003 17.3369V17.3369Z" fill="currentColor"></path></svg></span></div><div class="ak-editor-panel__content"><p data-renderer-start-pos="148">{m.group(1).strip()}</p></div></div>',
            markup,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Convert Error blockquotes - match HTML structure with <strong>Error:</strong>
        markup = re.sub(
            r'<blockquote>\s*<p[^>]*><strong[^>]*>Error:</strong>\s*(.*?)</p>.*?</blockquote>',
            lambda m: f'<div class="ak-editor-panel cc-l5mesu" data-panel-type="error"><div class="ak-editor-panel__icon"><span data-vc="icon-undefined" role="img" aria-label="error panel" class="_1e0c1o8l _1o9zidpf _vyfuvuon _vwz4kb7n _1szv15vq _1tly15vq _rzyw1osq _17jb1osq _1ksvoz0e _3se1x1jp _re2rglyw _1veoyfq0 _1kg81r31 _jcxd1r8n _gq0g1onz _1trkwc43" style="--icon-primary-color: currentColor;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" role="presentation"><path fill-rule="evenodd" clip-rule="evenodd" d="M13.8562 11.9112L16.5088 9.26C16.7433 9.02545 16.8751 8.70733 16.8751 8.37563C16.8751 8.04392 16.7433 7.7258 16.5088 7.49125C16.2742 7.2567 15.9561 7.12493 15.6244 7.12493C15.2927 7.12493 14.9746 7.2567 14.74 7.49125L12.09 10.1438L9.4375 7.49125C9.20295 7.25686 8.8849 7.12526 8.55331 7.12537C8.22172 7.12549 7.90376 7.25732 7.66937 7.49188C7.43499 7.72643 7.30338 8.04448 7.3035 8.37607C7.30361 8.70766 7.43545 9.02561 7.67 9.26L10.32 11.91L7.67 14.5625C7.4423 14.7983 7.31631 15.114 7.31916 15.4418C7.32201 15.7695 7.45347 16.083 7.68523 16.3148C7.91699 16.5465 8.2305 16.678 8.55825 16.6808C8.88599 16.6837 9.20175 16.5577 9.4375 16.33L12.0888 13.68L14.74 16.33C14.8561 16.4461 14.9939 16.5383 15.1455 16.6012C15.2972 16.664 15.4597 16.6964 15.6239 16.6965C15.7881 16.6966 15.9507 16.6643 16.1024 16.6015C16.2541 16.5387 16.392 16.4467 16.5081 16.3306C16.6243 16.2146 16.7164 16.0768 16.7793 15.9251C16.8422 15.7734 16.8746 15.6109 16.8746 15.4467C16.8747 15.2825 16.8424 15.1199 16.7796 14.9682C16.7168 14.8165 16.6248 14.6786 16.5088 14.5625L13.8562 11.9112V11.9112ZM12 22C9.34784 22 6.8043 20.9464 4.92893 19.0711C3.05357 17.1957 2 14.6522 2 12C2 9.34784 3.05357 6.8043 4.92893 4.92893C6.8043 3.05357 9.34784 2 12 2C14.6522 2 17.1957 3.05357 19.0711 4.92893C20.9464 6.8043 22 9.34784 22 12C22 14.6522 20.9464 17.1957 19.0711 19.0711C17.1957 20.9464 14.6522 22 12 22V22Z" fill="currentColor"></path></svg></span></div><div class="ak-editor-panel__content"><p data-renderer-start-pos="318">{m.group(1).strip()}</p></div></div>',
            markup,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Handle multi-line content within the blockquotes
        # This handles cases where the content spans multiple lines
        def process_multiline_content(match):
            content = match.group(1).strip()
            # Replace line breaks with proper HTML
            content = re.sub(r'\n+', '</p><p>', content)
            # Clean up any empty paragraphs
            content = re.sub(r'<p>\s*</p>', '', content)
            return content

        # Apply multiline processing to info panels
        markup = re.sub(
            r'<div class="ak-editor-panel cc-l5mesu" data-panel-type="info">.*?<div class="ak-editor-panel__content"><p data-renderer-start-pos="87">(.*?)</p></div></div>',
            lambda m: f'<div class="ak-editor-panel cc-l5mesu" data-panel-type="info"><div class="ak-editor-panel__icon"><span data-vc="icon-undefined" role="img" aria-label="info panel" class="_1e0c1o8l _1o9zidpf _vyfuvuon _vwz4kb7n _1szv15vq _1tly15vq _rzyw1osq _17jb1osq _1ksvoz0e _3se1x1jp _re2rglyw _1veoyfq0 _1kg81r31 _jcxd1r8n _gq0g1onz _1trkwc43" style="--icon-primary-color: currentColor;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" role="presentation"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 22C9.34784 22 6.8043 20.9464 4.92893 19.0711C3.05357 17.1957 2 14.6522 2 12C2 9.34784 3.05357 6.8043 4.92893 4.92893C6.8043 3.05357 9.34784 2 12 2C14.6522 2 17.1957 3.05357 19.0711 4.92893C20.9464 6.8043 22 9.34784 22 12C22 14.6522 20.9464 17.1957 19.0711 19.0711C17.1957 20.9464 14.6522 22 12 22V22ZM12 11.375C11.6685 11.375 11.3505 11.5067 11.1161 11.7411C10.8817 11.9755 10.75 12.2935 10.75 12.625V15.75C10.75 16.0815 10.8817 16.3995 11.1161 16.6339C11.3505 16.8683 11.6685 17 12 17C12.3315 17 12.6495 16.8683 12.8839 16.6339C13.1183 16.3995 13.25 16.0815 13.25 15.75V12.625C13.25 12.2935 13.1183 11.9755 12.8839 11.7411C12.6495 11.5067 12.3315 11.375 12 11.375ZM12 9.96875C12.4558 9.96875 12.893 9.78767 13.2153 9.46534C13.5377 9.14301 13.7188 8.70584 13.7188 8.25C13.7188 7.79416 13.5377 7.35699 13.2153 7.03466C12.893 6.71233 12.4558 6.53125 12 6.53125C11.5442 6.53125 11.107 6.71233 10.7847 7.03466C10.4623 7.35699 10.2812 7.79416 10.2812 8.25C10.2812 8.70584 10.4623 9.14301 10.7847 9.46534C11.107 9.78767 11.5442 9.96875 12 9.96875Z" fill="currentColor"></path></svg></span></div><div class="ak-editor-panel__content"><p data-renderer-start-pos="87">{process_multiline_content(m)}</p></div></div>',
            markup,
            flags=re.DOTALL
        )

        # Apply multiline processing to warning panels
        markup = re.sub(
            r'<div class="ak-editor-panel cc-l5mesu" data-panel-type="warning">.*?<div class="ak-editor-panel__content"><p data-renderer-start-pos="148">(.*?)</p></div></div>',
            lambda m: f'<div class="ak-editor-panel cc-l5mesu" data-panel-type="warning"><div class="ak-editor-panel__icon"><span data-vc="icon-undefined" role="img" aria-label="warning panel" class="_1e0c1o8l _1o9zidpf _vyfuvuon _vwz4kb7n _1szv15vq _1tly15vq _rzyw1osq _17jb1osq _1ksvoz0e _3se1x1jp _re2rglyw _1veoyfq0 _1kg81r31 _jcxd1r8n _gq0g1onz _1trkwc43" style="--icon-primary-color: currentColor;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" role="presentation"><path fill-rule="evenodd" clip-rule="evenodd" d="M13.4897 4.34592L21.8561 18.8611C21.9525 19.0288 22.0021 19.2181 21.9999 19.4101C21.9977 19.6021 21.9438 19.7903 21.8435 19.9559C21.7432 20.1215 21.6001 20.2588 21.4282 20.3542C21.2563 20.4497 21.0616 20.4999 20.8636 20.5H3.13707C2.93882 20.5 2.74401 20.4498 2.57196 20.3543C2.39992 20.2588 2.25663 20.1213 2.15631 19.9556C2.05598 19.7898 2.00212 19.6015 2.00006 19.4093C1.998 19.2171 2.04782 19.0278 2.14456 18.86L10.5121 4.34592C10.6602 4.08939 10.8762 3.87577 11.1377 3.72708C11.3993 3.57838 11.6971 3.5 12.0003 3.5C12.3036 3.5 12.6013 3.57838 12.8629 3.72708C13.1245 3.87577 13.3404 4.08939 13.4885 4.34592H13.4897ZM12.0003 7.82538C11.8232 7.82537 11.6482 7.86212 11.4869 7.93317C11.3257 8.00423 11.182 8.10793 11.0656 8.2373C10.9492 8.36668 10.8627 8.51872 10.8119 8.68321C10.7611 8.8477 10.7473 9.02083 10.7713 9.19093L11.3546 13.3416C11.3754 13.4933 11.4523 13.6326 11.5711 13.7334C11.6899 13.8343 11.8424 13.8899 12.0003 13.8899C12.1582 13.8899 12.3107 13.8343 12.4295 13.7334C12.5483 13.6326 12.6253 13.4933 12.6461 13.3416L13.2293 9.19093C13.2533 9.02083 13.2395 8.8477 13.1887 8.68321C13.138 8.51872 13.0515 8.36668 12.935 8.2373C12.8186 8.10793 12.6749 8.00423 12.5137 7.93317C12.3525 7.86212 12.1774 7.82537 12.0003 7.82538V7.82538ZM12.0003 17.3369C12.3395 17.3369 12.6649 17.2062 12.9047 16.9737C13.1446 16.7412 13.2793 16.4258 13.2793 16.0969C13.2793 15.7681 13.1446 15.4527 12.9047 15.2202C12.6649 14.9877 12.3395 14.857 12.0003 14.857C11.6611 14.857 11.3358 14.9877 11.0959 15.2202C10.8561 15.4527 10.7213 15.7681 10.7213 16.0969C10.7213 16.4258 10.8561 16.7412 11.0959 16.9737C11.3358 17.2062 11.6611 17.3369 12.0003 17.3369V17.3369Z" fill="currentColor"></path></svg></span></div><div class="ak-editor-panel__content"><p data-renderer-start-pos="148">{process_multiline_content(m)}</p></div></div>',
            markup,
            flags=re.DOTALL
        )

        # Apply multiline processing to error panels
        markup = re.sub(
            r'<div class="ak-editor-panel cc-l5mesu" data-panel-type="error">.*?<div class="ak-editor-panel__content"><p data-renderer-start-pos="318">(.*?)</p></div></div>',
            lambda m: f'<div class="ak-editor-panel cc-l5mesu" data-panel-type="error"><div class="ak-editor-panel__icon"><span data-vc="icon-undefined" role="img" aria-label="error panel" class="_1e0c1o8l _1o9zidpf _vyfuvuon _vwz4kb7n _1szv15vq _1tly15vq _rzyw1osq _17jb1osq _1ksvoz0e _3se1x1jp _re2rglyw _1veoyfq0 _1kg81r31 _jcxd1r8n _gq0g1onz _1trkwc43" style="--icon-primary-color: currentColor;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" role="presentation"><path fill-rule="evenodd" clip-rule="evenodd" d="M13.8562 11.9112L16.5088 9.26C16.7433 9.02545 16.8751 8.70733 16.8751 8.37563C16.8751 8.04392 16.7433 7.7258 16.5088 7.49125C16.2742 7.2567 15.9561 7.12493 15.6244 7.12493C15.2927 7.12493 14.9746 7.2567 14.74 7.49125L12.09 10.1438L9.4375 7.49125C9.20295 7.25686 8.8849 7.12526 8.55331 7.12537C8.22172 7.12549 7.90376 7.25732 7.66937 7.49188C7.43499 7.72643 7.30338 8.04448 7.3035 8.37607C7.30361 8.70766 7.43545 9.02561 7.67 9.26L10.32 11.91L7.67 14.5625C7.4423 14.7983 7.31631 15.114 7.31916 15.4418C7.32201 15.7695 7.45347 16.083 7.68523 16.3148C7.91699 16.5465 8.2305 16.678 8.55825 16.6808C8.88599 16.6837 9.20175 16.5577 9.4375 16.33L12.0888 13.68L14.74 16.33C14.8561 16.4461 14.9939 16.5383 15.1455 16.6012C15.2972 16.664 15.4597 16.6964 15.6239 16.6965C15.7881 16.6966 15.9507 16.6643 16.1024 16.6015C16.2541 16.5387 16.392 16.4467 16.5081 16.3306C16.6243 16.2146 16.7164 16.0768 16.7793 15.9251C16.8422 15.7734 16.8746 15.6109 16.8746 15.4467C16.8747 15.2825 16.8424 15.1199 16.7796 14.9682C16.7168 14.8165 16.6248 14.6786 16.5088 14.5625L13.8562 11.9112V11.9112ZM12 22C9.34784 22 6.8043 20.9464 4.92893 19.0711C3.05357 17.1957 2 14.6522 2 12C2 9.34784 3.05357 6.8043 4.92893 4.92893C6.8043 3.05357 9.34784 2 12 2C14.6522 2 17.1957 3.05357 19.0711 4.92893C20.9464 6.8043 22 9.34784 22 12C22 14.6522 20.9464 17.1957 19.0711 19.0711C17.1957 20.9464 14.6522 22 12 22V22Z" fill="currentColor"></path></svg></span></div><div class="ak-editor-panel__content"><p data-renderer-start-pos="318">{process_multiline_content(m)}</p></div></div>',
            markup,
            flags=re.DOTALL
        )

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

    def publish_markdown_file(self,
            file_path: str,
            page_title: Optional[str] = None,
            parent_page_title: Optional[str] = None,
            page_id: Optional[str] = None
        ) -> Dict:
        """
        Convert and publish a markdown file to Confluence

        Args:
            file_path: Path to the markdown file
            page_title: Optional custom page title (defaults to filename)
            parent_page_title: Optional parent page title
            page_id: Optional specific page ID to update (if provided, will update existing page)

        Returns:
            Response data from Confluence API
        """
        # Read markdown file
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Determine page title
        if not page_title:
            # Check for renames.json mapping first
            renames_file = Path('renames.json')
            if renames_file.exists():
                try:
                    with open(renames_file, 'r', encoding='utf-8') as f:
                        renames = json.load(f)
                    filename = Path(file_path).name
                    if filename in renames:
                        page_title = renames[filename]
                    else:
                        page_title = Path(file_path).stem.replace('_', ' ').title()
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Could not load renames.json: {e}")
                    page_title = Path(file_path).stem.replace('_', ' ').title()
            else:
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
        existing_page_id = page_id if page_id else self.get_page_id(page_title)

        if existing_page_id:
            # Update existing page
            print(f"Updating existing page: {page_title} (ID: {existing_page_id})")
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
    parser.add_argument('--page-id', help='Specific page ID to update (optional)')
    parser.add_argument('--enable-math', action='store_true', help='Enable math conversion (default: False)')

    args = parser.parse_args()

    # Initialize converter
    converter = ConfluenceMarkdownConverter(
        base_url=args.base_url,
        username=args.username,
        api_token=args.api_token,
        space_key=args.space_key,
        enable_math=args.enable_math
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
                parent_page_title=args.parent_page,
                page_id=args.page_id
            )
            print(f"Successfully processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    main()