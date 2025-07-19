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

# Standard library imports
import argparse
import html
import http
import json
import logging
import os
import re

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

# Third-party imports
import markdown
import requests

# Local imports
from jira_constants import Components, Categories, IssueTypes, Priorities, CustomFields

# List of markdown extensions used for conversion
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.def_list',
    'markdown.extensions.fenced_code',
    'markdown.extensions.nl2br',
    'markdown.extensions.tables',
    'markdown.extensions.toc',
]

# patterns to match the estimated time frame with their extraction functions
ESTIMATED_TIME_FRAME_PATTERNS = [
    {
        'pattern': re.compile(r'(\d+)-(\d+)\s*days'),
        'extract': lambda match: max(int(match.group(1)), int(match.group(2)))
    },
    {
        'pattern': re.compile(r'(\d+)\s*days'),
        'extract': lambda match: int(match.group(1))
    },
]

def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration with { style formatting"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='{asctime} - {name} - {levelname} - {message}',
        style='{',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

@dataclass
class CommandLine:
    """Command line arguments for Jira markdown converter"""
    files: List[str]
    base_url: str
    username: str
    api_token: str
    project_key: str
    issue_type: str = IssueTypes.TASK
    priority: str = Priorities.MEDIUM
    assignee: Optional[str] = None
    time_estimate: Optional[str] = None
    issue_key: Optional[str] = None
    parent_key: Optional[str] = None
    as_comment: bool = False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> 'CommandLine':
        """Create CommandLine instance from argparse Namespace"""
        return cls(
            files=args.files,
            base_url=args.base_url,
            username=args.username,
            api_token=args.api_token,
            project_key=args.project_key,
            issue_type=args.issue_type,
            priority=args.priority,
            assignee=args.assignee,
            time_estimate=args.time_estimate,
            issue_key=args.issue_key,
            parent_key=args.parent_key,
            as_comment=args.as_comment
        )

class JiraMarkdownConverter:
    """Convert markdown to Jira markup and publish to Jira"""

    def __init__(self, cmd: CommandLine):
        """
        Initialize the converter with Jira credentials

        Args:
            cmd: CommandLine object containing all configuration options
        """
        self.logger = logging.getLogger(__name__)
        self.base_url = cmd.base_url.rstrip('/')
        self.username = cmd.username
        self.api_token = cmd.api_token
        self.project_key = cmd.project_key
        self.session = requests.Session()
        self.session.auth = (cmd.username, cmd.api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def _handle_response(self, response) -> Dict:
        """
        Handle HTTP response and return appropriate data based on status code

        Args:
            response: requests.Response object

        Returns:
            Dict containing response data or empty dict for no-content responses
        """
        response.raise_for_status()
        response.encoding = 'utf-8'
        status_code = response.status_code

        # Check status codes that typically don't return content
        no_content_codes = [
            http.HTTPStatus.NO_CONTENT,  # 204
            http.HTTPStatus.RESET_CONTENT,  # 205
        ]

        if status_code in no_content_codes or not response.content:
            # get our response phrase
            response_phrase = http.HTTPStatus(status_code).phrase
            self.logger.debug(f"Response {status_code} ({response_phrase}): No content to parse")
            return {}

        try:
            return response.json()
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse JSON response: {e}")
            self.logger.debug(f"Response content: {response.text}")
            return {}

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

    def _html_to_jira_markup(
        self,
        html_content: str,
        markdown_content: str
    ) -> str:
        """
        Convert HTML to Jira markup

        Args:
            html_content: HTML content
            markdown_content: Original markdown content

        Returns:
            Jira markup string
        """
        markup = html_content

        # Headers (Jira uses h1. h2. h3. etc.)
        markup = re.sub(r'<h1 id="([^"]+)">(.*?)</h1>', r'h1. \2', markup)
        markup = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', r'h2. \2', markup)
        markup = re.sub(r'<h3 id="([^"]+)">(.*?)</h3>', r'h3. \2', markup)
        markup = re.sub(r'<h4 id="([^"]+)">(.*?)</h4>', r'h4. \2', markup)
        markup = re.sub(r'<h5 id="([^"]+)">(.*?)</h5>', r'h5. \2', markup)
        markup = re.sub(r'<h6 id="([^"]+)">(.*?)</h6>', r'h6. \2', markup)

        # Bold and italic
        markup = re.sub(r'<strong>(.*?)</strong>', r'*\1*', markup)
        markup = re.sub(r'<em>(.*?)</em>', r'_\1_', markup)

        # Strikethrough
        markup = re.sub(r'<del>(.*?)</del>', r'-\1-', markup)
        markup = re.sub(r'<s>(.*?)</s>', r'-\1-', markup)

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
        markup = re.sub(r'<code>(.*?)</code>', r'{{\1}}', markup)

        # Links
        markup = re.sub(r'<a href="([^"]+)">(.*?)</a>', r'[\2|\1]', markup)

        # Lists - Convert to Jira list format
        # Handle unordered lists
        markup = re.sub(r'<ul>(.*?)</ul>', lambda m: self._convert_list_items(m.group(1), '*'), markup, flags=re.DOTALL)
        # Handle ordered lists
        markup = re.sub(r'<ol>(.*?)</ol>', lambda m: self._convert_list_items(m.group(1), '#'), markup, flags=re.DOTALL)

        # Tables - Convert to Jira table format
        markup = re.sub(r'<table>(.*?)</table>', lambda m: self._convert_table(m.group(1)), markup, flags=re.DOTALL)

        # Blockquotes
        markup = re.sub(r'<blockquote>(.*?)</blockquote>', r'bq. \1', markup, flags=re.DOTALL)

        # Paragraphs - just get the text content
        markup = re.sub(r'<p>(.*?)</p>', r'\1', markup)

        # Line breaks
        markup = re.sub(r'<br/?>', r'\n', markup)

        # Handle strikethrough in post-processing
        markup = re.sub(r'~~(.*?)~~', r'-\1-', markup)

        # Clean up any remaining HTML tags
        markup = re.sub(r'<[^>]+>', '', markup)

        # Clean up extra whitespace
        markup = re.sub(r'\n\s*\n\s*\n', '\n\n', markup)
        markup = markup.strip()

        # Add proper spacing around headers
        markup = self._add_header_spacing(markup)

        return markup

    def _convert_list_items(
        self,
        list_content: str,
        marker: str
    ) -> str:
        """Convert list items to Jira format"""
        # Find all list items
        items = re.findall(r'<li>(.*?)</li>', list_content, flags=re.DOTALL)
        if not items:
            return list_content

        # Convert each item to Jira format
        jira_items = []
        for item in items:
            # Clean up the item content
            item = re.sub(r'<[^>]+>', '', item).strip()
            jira_items.append(f'{marker} {item}')

        return '\n'.join(jira_items)

    def _convert_table(self, table_content: str) -> str:
        """Convert HTML table to Jira table format"""
        # Find table rows
        rows = re.findall(r'<tr>(.*?)</tr>', table_content, flags=re.DOTALL)
        if not rows:
            return table_content

        jira_rows = []
        for row in rows:
            # Find cells (th or td)
            cells = re.findall(r'<(?:th|td)>(.*?)</(?:th|td)>', row, flags=re.DOTALL)
            if cells:
                # Clean up cell content
                clean_cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
                jira_rows.append('||' + '||'.join(clean_cells) + '||')

        return '\n'.join(jira_rows)

    def _add_header_spacing(self, markup: str) -> str:
        """
        Add proper spacing around headers in Jira markup

        Args:
            markup: Jira markup content

        Returns:
            Jira markup with proper header spacing
        """
        lines = markup.split('\n')
        result_lines = []

        for i, line in enumerate(lines):
            # Check if this line is a header (starts with h1., h2., etc.)
            if re.match(r'^h[1-6]\.\s', line):
                # If this is the first header (index 0), only add newline after
                if i == 0:
                    result_lines.append(line)
                    result_lines.append('')
                else:
                    # For all other headers, add newline before and after
                    result_lines.append('')
                    result_lines.append(line)
                    result_lines.append('')
            else:
                # Non-header lines are added as-is
                result_lines.append(line)

        # Join lines back together
        result = '\n'.join(result_lines)

        # Clean up any excessive newlines (more than 2 consecutive)
        result = re.sub(r'\n{3,}', '\n\n', result)

        return result

    def _parse_time_estimate(self, time_str: str) -> Optional[int]:
        """
        Parse time estimate string to seconds

        Args:
            time_str: Time string (e.g., "2h", "1d", "30m", "1w", "3600s")

        Returns:
            Time in seconds, or None if parsing fails
        """
        # Remove whitespace and convert to lowercase
        time_str = time_str.strip().lower()

        # Pattern to match: number + unit (w, d, h, m, s)
        pattern = r'^(\d+(?:\.\d+)?)\s*(w|d|h|m|s)$'
        match = re.match(pattern, time_str)

        if not match:
            self.logger.warning(f"Invalid time format '{time_str}'. Use format like '2h', '1d', '30m', '1w'")
            return None

        value = float(match.group(1))
        unit = match.group(2)

        # Convert to seconds
        conversions = {
            'w': 7 * 24 * 60 * 60,  # weeks to seconds
            'd': 24 * 60 * 60,      # days to seconds
            'h': 60 * 60,           # hours to seconds
            'm': 60,                # minutes to seconds
            's': 1                  # seconds
        }

        return int(value * conversions[unit])

    def create_issue(
        self,
        summary: str,
        description: str,
        cmd: CommandLine
    ) -> Dict:
        """
        Create a new issue in Jira

        Args:
            summary: Issue summary/title
            description: Issue description in Jira markup
            cmd: CommandLine object containing all configuration options

        Returns:
            Response data from Jira API
        """
        url = f"{self.base_url}/rest/api/2/issue"

        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": cmd.issue_type},
                "priority": {"name": cmd.priority},
                "components": [{"id": Components.OTHER}],  # "Other" component
                CustomFields.CATEGORY: {"value": Categories.SOFTWARE_RESEARCH_DEV}  # Category
            }
        }

        if cmd.assignee:
            data["fields"]["assignee"] = {"name": cmd.assignee}

        if cmd.parent_key:
            data["fields"]["parent"] = {"key": cmd.parent_key}

        # Debug: Log the data being sent
        self.logger.debug(f"Sending data to Jira API: URL={url}")
        self.logger.debug(f"Request data: {json.dumps(data, indent=2)}")

        response = self.session.post(url, json=data)
        status_code = response.status_code

        if status_code != http.HTTPStatus.CREATED:
            status_phrase = http.HTTPStatus(status_code).phrase
            self.logger.debug(f"Response status: {status_code} ({status_phrase})")
            self.logger.debug(f"Response headers: {dict(response.headers)}")
            self.logger.debug(f"Response body: {response.text}")
            response.raise_for_status()

        return self._handle_response(response)

    def update_issue(
        self,
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
        return self._handle_response(response)

    def add_comment(
        self,
        issue_key: str,
        comment: str
    ) -> Dict:
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
        return self._handle_response(response)

    def update_time_estimate(
        self,
        issue_key: str,
        time_estimate: str
    ) -> None:
        """
        Update the time estimate for an existing issue.
        Args:
            issue_key: Jira issue key (e.g., PROJ-123)
            time_estimate: Time estimate string (e.g., "2h", "1d")
        """
        seconds = self._parse_time_estimate(time_estimate)
        if not seconds:
            self.logger.warning(f"Could not parse time estimate '{time_estimate}'")
            return
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}"
        data = {
            "fields": {
                "timetracking": {
                    "originalEstimate": f"{seconds}s"
                }
            }
        }
        self.logger.debug(f"Updating time estimate for {issue_key} to {seconds}s")
        response = self.session.put(url, json=data)
        status_code = response.status_code

        if status_code != http.HTTPStatus.NO_CONTENT:
            status_phrase = http.HTTPStatus(status_code).phrase
            self.logger.debug(f"Failed to update time estimate. Status: {status_code} ({status_phrase})")
            self.logger.debug(f"Response body: {response.text}")
        else:
            self.logger.info(f"Time estimate updated for {issue_key}")

    def _extract_issue_summary(self, markdown_content: str) -> str:
        """
        Extract issue summary from the first line of markdown file

        Args:
            markdown_content: Raw markdown content

        Returns:
            Issue summary string
        """
        # Split the markdown file into lines
        markdown_lines = markdown_content.split('\n')

        # Get the summary from the first line of the markdown file
        # removing the markdown header
        issue_summary = markdown_lines[0].strip()
        issue_summary = issue_summary.replace('#', '').strip()

        return issue_summary

    def _extract_time_estimate_and_content(
        self,
        markdown_content: str,
        cmd: CommandLine
    ) -> str:
        """
        Extract time estimate from markdown and process content

        Args:
            markdown_content: Raw markdown content
            cmd: CommandLine object to update with time estimate

        Returns:
            Processed content without time estimate section
        """
        # split the markdown file into lines
        markdown_lines = markdown_content.split('\n')

        # remove the first two lines of the markdown file
        markdown_lines = markdown_lines[2:]

        # get the estimated time from the markdown file
        for idx, l in enumerate(markdown_lines):
            if 'Estimated Time Frame' in l:
                for pattern_info in ESTIMATED_TIME_FRAME_PATTERNS:
                    match = pattern_info['pattern'].search(l)
                    if match:
                        # get the maximum number of days
                        days = pattern_info['extract'](match)
                        estimated_time = f"{days}d"
                        self.logger.info(f"Estimated time: {estimated_time}")

                        # update the provided command line object with the estimated time
                        cmd.time_estimate = estimated_time
                        break
                # Break out of the outer loop once we've found and processed the time estimate
                break

        # we will only contain the data before the estimated time frame
        markdown_lines = markdown_lines[:idx]

        # join the markdown lines back together
        processed_content = '\n'.join(markdown_lines)

        return processed_content

    def publish_markdown_file(
        self,
        file_path: str,
        cmd: CommandLine
    ) -> Dict:
        """
        Convert and publish a markdown file to Jira

        Args:
            file_path: Path to the markdown file
            cmd: CommandLine object containing all configuration options

        Returns:
            Response data from Jira API
        """
        # Read markdown file
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Extract issue summary
        issue_summary = self._extract_issue_summary(markdown_content)

        # Process content and extract time estimate
        processed_content = self._extract_time_estimate_and_content(markdown_content, cmd)

        # Convert markdown to Jira markup
        jira_content = self.convert_markdown_to_jira(processed_content)
        jira_content_lines = jira_content.split('\n')
        jira_content = '\n'.join(jira_content_lines)

        # Debug: Log what we're about to send
        self.logger.debug(f"Issue summary: '{issue_summary}'")
        self.logger.debug(f"Jira content length: {len(jira_content)} characters")
        self.logger.debug(f"First 200 chars of content: {jira_content[:200]}...")

        #return 0

        if cmd.as_comment and cmd.issue_key:
            # Add as comment to existing issue
            self.logger.info(f"Adding comment to issue: {cmd.issue_key}")
            result = self.add_comment(cmd.issue_key, jira_content)
            self.logger.info(f"Comment added successfully to {cmd.issue_key}")
        elif cmd.issue_key:
            # Update existing issue
            self.logger.info(f"Updating existing issue: {cmd.issue_key}")
            result = self.update_issue(
                cmd.issue_key,
                summary=issue_summary,
                description=jira_content
            )
            self.logger.info(f"Issue updated successfully: {cmd.issue_key}")
            # If we have a time estimate, update it after creation
            #if cmd.time_estimate:
            #    self.update_time_estimate(cmd.issue_key, cmd.time_estimate)
        else:
            # Create new issue
            self.logger.info(f"Creating new issue: {issue_summary}")
            if cmd.parent_key:
                self.logger.info(f"Creating as child of: {cmd.parent_key}")
            result = self.create_issue(
                issue_summary,
                jira_content,
                cmd
            )
            issue_key = result['key']
            self.logger.info(f"Issue created successfully: {issue_key}")
            # If we have a time estimate, update it after creation
            #if cmd.time_estimate:
            #    self.update_time_estimate(issue_key, cmd.time_estimate)
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
    parser.add_argument('--time-estimate', help='Time estimate (e.g., "2h", "1d", "30m", "1w") (optional)')
    parser.add_argument('--issue-key', help='Existing issue key to update (optional)')
    parser.add_argument('--parent-key', help='Parent issue key for creating child issues (optional)')
    parser.add_argument('--as-comment', action='store_true', help='Add content as comment to existing issue')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    cmd = CommandLine.from_args(args)

    # Initialize converter
    converter = JiraMarkdownConverter(cmd)

    # Process each file
    for file_path in cmd.files:
        if not os.path.exists(file_path):
            logger.error("File not found: {file_path}", extra={'file_path': file_path})
            continue

        try:
            result = converter.publish_markdown_file(file_path, cmd)
            logger.info(f"Successfully processed: {file_path}")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    main()