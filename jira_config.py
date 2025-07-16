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
Jira Configuration Management

This module provides a class-based approach to manage Jira configuration
including credentials, project settings, and default values.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

class JiraConfig:
    """Manage Jira configuration and credentials"""

    def __init__(self, config_file: str = "jira_config.json"):
        """
        Initialize Jira configuration

        Args:
            config_file: Path to configuration file
        """
        self.config_file = Path(config_file)
        self._config = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load {self.config_file}: {e}")
                self._config = {}
        else:
            self._config = {}

    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Error saving configuration: {e}")

    @property
    def base_url(self) -> Optional[str]:
        """Get Jira base URL"""
        return self._config.get('base_url')

    @base_url.setter
    def base_url(self, value: str):
        """Set Jira base URL"""
        self._config['base_url'] = value
        self._save_config()

    @property
    def username(self) -> Optional[str]:
        """Get Jira username/email"""
        return self._config.get('username')

    @username.setter
    def username(self, value: str):
        """Set Jira username/email"""
        self._config['username'] = value
        self._save_config()

    @property
    def api_token(self) -> Optional[str]:
        """Get Jira API token"""
        return self._config.get('api_token')

    @api_token.setter
    def api_token(self, value: str):
        """Set Jira API token"""
        self._config['api_token'] = value
        self._save_config()

    @property
    def project_key(self) -> Optional[str]:
        """Get Jira project key"""
        return self._config.get('project_key')

    @project_key.setter
    def project_key(self, value: str):
        """Set Jira project key"""
        self._config['project_key'] = value
        self._save_config()

    @property
    def default_issue_type(self) -> str:
        """Get default issue type"""
        return self._config.get('default_issue_type', 'Task')

    @default_issue_type.setter
    def default_issue_type(self, value: str):
        """Set default issue type"""
        self._config['default_issue_type'] = value
        self._save_config()

    @property
    def default_priority(self) -> str:
        """Get default priority"""
        return self._config.get('default_priority', 'Medium')

    @default_priority.setter
    def default_priority(self, value: str):
        """Set default priority"""
        self._config['default_priority'] = value
        self._save_config()

    @property
    def default_assignee(self) -> Optional[str]:
        """Get default assignee"""
        return self._config.get('default_assignee')

    @default_assignee.setter
    def default_assignee(self, value: str):
        """Set default assignee"""
        self._config['default_assignee'] = value
        self._save_config()

    @property
    def default_parent_key(self) -> Optional[str]:
        """Get default parent issue key"""
        return self._config.get('default_parent_key')

    @default_parent_key.setter
    def default_parent_key(self, value: str):
        """Set default parent issue key"""
        self._config['default_parent_key'] = value
        self._save_config()

    def is_configured(self) -> bool:
        """Check if configuration is complete"""
        required_fields = ['base_url', 'username', 'api_token', 'project_key']
        return all(self._config.get(field) for field in required_fields)

    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return self._config.copy()

    def setup_interactive(self):
        """Interactive setup for Jira configuration"""
        print("Jira Configuration Setup")
        print("=" * 40)

        # Get base URL
        base_url = input("Jira Base URL (e.g., https://your-domain.atlassian.net): ").strip()
        if not base_url:
            print("Base URL is required")
            return False

        # Get username
        username = input("Jira Username/Email: ").strip()
        if not username:
            print("Username is required")
            return False

        # Get API token
        api_token = input("Jira API Token: ").strip()
        if not api_token:
            print("API token is required")
            return False

        # Get project key
        project_key = input("Jira Project Key (e.g., PROJ): ").strip()
        if not project_key:
            print("Project key is required")
            return False

        # Optional settings
        default_issue_type = input("Default Issue Type (default: Task): ").strip() or "Task"
        default_priority = input("Default Priority (default: Medium): ").strip() or "Medium"
        default_assignee = input("Default Assignee (optional): ").strip() or None
        default_parent_key = input("Default Parent Issue Key (optional): ").strip() or None

        # Save configuration
        self.base_url = base_url
        self.username = username
        self.api_token = api_token
        self.project_key = project_key
        self.default_issue_type = default_issue_type
        self.default_priority = default_priority
        if default_assignee:
            self.default_assignee = default_assignee
        if default_parent_key:
            self.default_parent_key = default_parent_key

        print(f"\nConfiguration saved to {self.config_file}")
        print("⚠️  IMPORTANT: Keep your API token secure and never commit it to version control!")

        return True

    def test_connection(self) -> bool:
        """Test Jira API connection"""
        if not self.is_configured():
            print("Configuration not complete. Run setup first.")
            return False

        try:
            import requests
            session = requests.Session()
            session.auth = (self.username, self.api_token)
            session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })

            # Test connection by getting project info
            url = f"{self.base_url}/rest/api/2/project/{self.project_key}"
            response = session.get(url)

            if response.status_code == 200:
                project_info = response.json()
                print(f"✅ Connection successful!")
                print(f"Project: {project_info.get('name', 'Unknown')} ({project_info.get('key', 'Unknown')})")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

def main():
    """Main function for command line usage"""
    import argparse

    parser = argparse.ArgumentParser(description='Jira Configuration Management')
    parser.add_argument('--setup', action='store_true', help='Run interactive setup')
    parser.add_argument('--test', action='store_true', help='Test Jira connection')
    parser.add_argument('--show', action='store_true', help='Show current configuration')

    args = parser.parse_args()

    config = JiraConfig()

    if args.setup:
        config.setup_interactive()
    elif args.test:
        config.test_connection()
    elif args.show:
        if config.is_configured():
            print("Current Configuration:")
            print(f"  Base URL: {config.base_url}")
            print(f"  Username: {config.username}")
            print(f"  Project Key: {config.project_key}")
            print(f"  Default Issue Type: {config.default_issue_type}")
            print(f"  Default Priority: {config.default_priority}")
            if config.default_assignee:
                print(f"  Default Assignee: {config.default_assignee}")
            if config.default_parent_key:
                print(f"  Default Parent Key: {config.default_parent_key}")
        else:
            print("Configuration not set up. Run --setup to configure.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()