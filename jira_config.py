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

# Default script path
SCRIPT_PATH = "scripts/convert_jira.sh"

# Template script placeholders
JIRA_SCRIPT_PLACEHOLDERS = {
    'BASE_URL': 'BASE_URL="https://your-domain.atlassian.net"',
    'USERNAME': 'USERNAME="your-email@example.com"',
    'API_TOKEN': 'API_TOKEN="your-api-token-here"',
    'PROJECT_KEY': 'PROJECT_KEY="PROJ"',
    'HEADER_COMMENT': '# Jira Issue Converter Script'
}

class JiraCommandOptions:
    """Command line options for Jira configuration management"""

    def __init__(self, setup: bool = False, test: bool = False, show: bool = False,
                 generate_script: str = None):
        self.setup = setup
        self.test = test
        self.show = show
        self.generate_script = generate_script

    @classmethod
    def from_args(cls, args):
        """Create JiraCommandOptions from argparse Namespace"""
        return cls(
            setup=args.setup,
            test=args.test,
            show=args.show,
            generate_script=args.generate_script
        )

    def get_action(self) -> str:
        """Determine which action to take based on the options"""
        if self.setup:
            return 'setup'
        elif self.test:
            return 'test'
        elif self.show:
            return 'show'
        elif self.generate_script:
            return 'generate_script'
        else:
            return 'help'

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

    def generate_local_script(self, script_name: str = "convert_jira.sh") -> str:
        """
        Generate a local script with credentials from config by loading the template
        and replacing placeholders with actual configuration values.

        Args:
            script_name: Name of the generated script file (default: convert_jira.sh)

        Returns:
            Path to the generated script
        """
        if not self.is_configured():
            print("Configuration not complete. Run setup first.")
            return None

        # Load the template script
        template_path = Path("scripts/convert_jira.sh")
        if not template_path.exists():
            print(f"❌ Template script not found: {template_path}")
            return None

        try:
            with open(template_path, 'r') as f:
                script_content = f.read()
        except Exception as e:
            print(f"❌ Error reading template script: {e}")
            return None

        # Replace placeholders with actual configuration values
        script_content = script_content.replace(
            JIRA_SCRIPT_PLACEHOLDERS['BASE_URL'],
            f'BASE_URL="{self.base_url}"'
        )
        script_content = script_content.replace(
            JIRA_SCRIPT_PLACEHOLDERS['USERNAME'],
            f'USERNAME="{self.username}"'
        )
        script_content = script_content.replace(
            JIRA_SCRIPT_PLACEHOLDERS['API_TOKEN'],
            f'API_TOKEN="{self.api_token}"'
        )
        script_content = script_content.replace(
            JIRA_SCRIPT_PLACEHOLDERS['PROJECT_KEY'],
            f'PROJECT_KEY="{self.project_key}"'
        )

        # Add a comment at the top indicating this is auto-generated
        script_content = script_content.replace(
            JIRA_SCRIPT_PLACEHOLDERS['HEADER_COMMENT'],
            '# Auto-generated Jira Issue Converter Script\n# Generated from jira_config.json\n# DO NOT COMMIT THIS FILE - it contains your credentials!'
        )

        # Write the generated script to the solution level (same location as this script)
        script_path = Path(script_name)
        try:
            with open(script_path, 'w') as f:
                f.write(script_content)
        except Exception as e:
            print(f"❌ Error writing generated script: {e}")
            return None

        # Make executable
        script_path.chmod(0o755)

        print(f"✅ Generated local script: {script_path}")
        print("⚠️  IMPORTANT: This file contains your credentials - DO NOT commit it!")
        print(f"   The file '{script_name}' is already in .gitignore")
        print("\n🎯 Next steps:")
        print(f"   1. Edit {script_name} to customize issue types and file paths")
        print(f"   2. Run: ./{script_name}")

        return str(script_path)

def main():
    """Main function for command line usage"""
    import argparse

    parser = argparse.ArgumentParser(description='Jira Configuration Management')
    parser.add_argument('--setup', action='store_true', help='Run interactive setup')
    parser.add_argument('--test', action='store_true', help='Test Jira connection')
    parser.add_argument('--show', action='store_true', help='Show current configuration')
    parser.add_argument('--generate-script', default=SCRIPT_PATH, help='Generate local script with credentials')

    args = parser.parse_args()
    options = JiraCommandOptions.from_args(args)
    config = JiraConfig()

    # Use match statement to handle different actions
    match options.get_action():
        case 'setup':
            config.setup_interactive()

        case 'test':
            config.test_connection()

        case 'show':
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

        case 'generate_script':
            script_path = config.generate_local_script(options.generate_script)
            if script_path:
                print(f"\n🎯 Usage:")
                print(f"   ./{options.generate_script}")
                print(f"   # Edit the script to customize issue types and file paths")

        case 'help':
            parser.print_help()

if __name__ == "__main__":
    main()