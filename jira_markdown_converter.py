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
Jira Markdown Converter and Publisher

This script converts markdown files to Jira markup format and publishes them
to Jira using the REST API. It handles markdown to Jira markup conversion
and maintains proper formatting for issues, comments, and descriptions.

Requirements:
    pip install requests markdown jira
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

class JiraMarkdownConverter:
    """Convert markdown to Jira markup and publish to Jira"""

    def __init__(self, base_url: str, username: str, api_token: str, project_key: str):
        """
        Initialize the converter with Jira credentials

        Args:
            base_url: Jira base URL (e.g., https://your-domain.atlassian.net)
            username: Jira username or email
            api_token: Jira API token (not password)
            project_key: Jira project key (e.g., PROJ)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.project_key = project_key
        self.session = requests.Session()
        self.session.auth = (username, api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def convert_markdown_to_jira(self, markdown_content: str) -> str:
        """
        Convert markdown content to Jira markup

        Args:
            markdown_content: Raw markdown text

        Returns:
            Jira markup string
        """
        # First convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=MARKDOWN_EXTENSIONS
        )

        # Convert HTML to Jira markup
        jira_markup = self._html_to_jira_markup(html_content, markdown_content)

        return jira_markup

    def _html_to_jira_markup(self, html_content: str, markdown_content: str) -> str:
        """
        Convert HTML to Jira markup

        Args:
            html_content: HTML content
            markdown_content: Original markdown content

        Returns:
            Jira markup string
        """
        markup = html_content

        # Headers (Jira uses h1-h6)
        markup = re.sub(r'<h1>(.*?)</h1>', r'<h1>\1</h1>', markup)
        markup = re.sub(r'<h2>(.*?)</h2>', r'<h2>\1</h2>', markup)
        markup = re.sub(r'<h3>(.*?)</h3>', r'<h3>\1</h3>', markup)
        markup = re.sub(r'<h4>(.*?)</h4>', r'<h4>\1</h4>', markup)
        markup = re.sub(r'<h5>(.*?)</h5>', r'<h5>\1</h5>', markup)
        markup = re.sub(r'<h6>(.*?)</h6>', r'<h6>\1</h6>', markup)

        # Bold and italic
        markup = re.sub(r'<strong>(.*?)</strong>', r'*{color:red}\1{color}*', markup)
        markup = re.sub(r'<em>(.*?)</em>', r'_{color:blue}\1{color}_', markup)

        # Strikethrough
        markup = re.sub(r'<del>(.*?)</del>', r'-{color:grey}\1{color}-', markup)
        markup = re.sub(r'<s>(.*?)</s>', r'-{color:grey}\1{color}-', markup)

        # Code blocks
        markup = re.sub(
            r'<pre><code class="language-([\w\-]+)">(.*?)</code></pre>',
            lambda m: f'{{code:{m.group(1)}}}\n{html.unescape(m.group(2)).strip()}\n{{code}}',
            markup,
            flags=re.DOTALL
        )
        markup = re.sub(
            r'<pre><code>(.*?)</code></pre>',
            lambda m: f'{{code}}\n{html.unescape(m.group(1)).strip()}\n{{code}}',
            markup,
            flags=re.DOTALL
        )

        # Inline code
        markup = re.sub(r'<code>(.*?)</code>', r'{{monospace}}\1{{monospace}}', markup)

        # Links
        markup = re.sub(r'<a href="([^"]+)">(.*?)</a>', r'[{color:blue}\2|{color}\1]', markup)

        # Lists - Simple conversion (nested lists not supported)
        markup = re.sub(r'<li>(.*?)</li>', r'* \1', markup, flags=re.DOTALL)
        markup = re.sub(r'</?ul>', '', markup)
        markup = re.sub(r'</?ol>', '', markup)

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

        # Handle strikethrough in post-processing
        markup = re.sub(r'~~(.*?)~~', r'-{color:grey}\1{color}-', markup)

        return markup

    def create_issue(self, summary: str, description: str, issue_type: str = "Task",
                    priority: str = "Medium", assignee: Optional[str] = None,
                    parent_key: Optional[str] = None) -> Dict:
        """
        Create a new issue in Jira

        Args:
            summary: Issue summary/title
            description: Issue description in Jira markup
            issue_type: Type of issue (Task, Bug, Story, etc.)
            priority: Issue priority (Highest, High, Medium, Low, Lowest)
            assignee: Optional assignee username
            parent_key: Optional parent issue key (e.g., PROJ-123)

        Returns:
            Response data from Jira API
        """
        url = f"{self.base_url}/rest/api/2/issue"

        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
                "priority": {"name": priority}
            }
        }

        if assignee:
            data["fields"]["assignee"] = {"name": assignee}

        if parent_key:
            data["fields"]["parent"] = {"key": parent_key}

        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def update_issue(self,
                     issue_key: str,
                     summary: Optional[str] = None,
                     description: Optional[str] = None
        ) -> Dict:
        """
        Update an existing issue in Jira

        Args:
            issue_key: Jira issue key (e.g., PROJ-123)
            summary: Optional new summary
            description: Optional new description

        Returns:
            Response data from Jira API
        """
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}"

        data = {"fields": {}}
        if summary:
            data["fields"]["summary"] = summary
        if description:
            data["fields"]["description"] = description

        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def add_comment(self, issue_key: str, comment: str) -> Dict:
        """
        Add a comment to an existing issue

        Args:
            issue_key: Jira issue key (e.g., PROJ-123)
            comment: Comment content in Jira markup

        Returns:
            Response data from Jira API
        """
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}/comment"

        data = {"body": comment}

        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def publish_markdown_file(self, file_path: str, issue_type: str = "Task",
                            priority: str = "Medium", assignee: Optional[str] = None,
                            issue_key: Optional[str] = None, as_comment: bool = False,
                            parent_key: Optional[str] = None) -> Dict:
        """
        Convert and publish a markdown file to Jira

        Args:
            file_path: Path to the markdown file
            issue_type: Type of issue to create
            priority: Issue priority
            assignee: Optional assignee username
            issue_key: Optional existing issue key to update
            as_comment: If True, add content as comment to existing issue
            parent_key: Optional parent issue key for creating child issues

        Returns:
            Response data from Jira API
        """
        # Read markdown file
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Determine issue summary from filename
        issue_summary = Path(file_path).stem.replace('_', ' ').title()

        # Convert markdown to Jira markup
        jira_content = self.convert_markdown_to_jira(markdown_content)

        if as_comment and issue_key:
            # Add as comment to existing issue
            print(f"Adding comment to issue: {issue_key}")
            result = self.add_comment(issue_key, jira_content)
            print(f"Comment added successfully to {issue_key}")
        elif issue_key:
            # Update existing issue
            print(f"Updating existing issue: {issue_key}")
            result = self.update_issue(issue_key, summary=issue_summary, description=jira_content)
            print(f"Issue updated successfully: {issue_key}")
        else:
            # Create new issue
            print(f"Creating new issue: {issue_summary}")
            if parent_key:
                print(f"Creating as child of: {parent_key}")
            result = self.create_issue(
                summary=issue_summary,
                description=jira_content,
                issue_type=issue_type,
                priority=priority,
                assignee=assignee,
                parent_key=parent_key
            )
            issue_key = result['key']
            print(f"Issue created successfully: {issue_key}")

        return result

def main():
    """Main function to handle command line arguments and execute conversion"""
    parser = argparse.ArgumentParser(description='Convert markdown files to Jira issues')
    parser.add_argument('files', nargs='+', help='Markdown files to convert')
    parser.add_argument('--base-url', required=True, help='Jira base URL')
    parser.add_argument('--username', required=True, help='Jira username/email')
    parser.add_argument('--api-token', required=True, help='Jira API token')
    parser.add_argument('--project-key', required=True, help='Jira project key')
    parser.add_argument('--issue-type', default='Task', help='Issue type (default: Task)')
    parser.add_argument('--priority', default='Medium', help='Issue priority (default: Medium)')
    parser.add_argument('--assignee', help='Assignee username (optional)')
    parser.add_argument('--issue-key', help='Existing issue key to update (optional)')
    parser.add_argument('--parent-key', help='Parent issue key for creating child issues (optional)')
    parser.add_argument('--as-comment', action='store_true', help='Add content as comment to existing issue')

    args = parser.parse_args()

    # Initialize converter
    converter = JiraMarkdownConverter(
        base_url=args.base_url,
        username=args.username,
        api_token=args.api_token,
        project_key=args.project_key
    )

    # Process each file
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            continue

        try:
            result = converter.publish_markdown_file(
                file_path=file_path,
                issue_type=args.issue_type,
                priority=args.priority,
                assignee=args.assignee,
                issue_key=args.issue_key,
                as_comment=args.as_comment,
                parent_key=args.parent_key
            )
            print(f"Successfully processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    main()