#!/usr/bin/env python3
"""
Confluence Configuration Setup

This script handles the setup and management of Confluence API credentials.
It provides an interactive setup process and configuration management.

Usage:
    python confluence_config.py --setup
    python confluence_config.py --test
    python confluence_config.py --show
"""

import os
import sys
import json
import getpass
import argparse
from typing import Dict, Optional

# Default configuration file path
CONFIG_FILE = "confluence_config.json"

class ConfluenceConfig:
    """Configuration manager for Confluence API credentials"""

    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Optional[Dict]:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading configuration: {e}")
                return None
        return None

    def _save_config(self, config: Dict) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False

    def setup_interactive(self) -> bool:
        """Interactive setup process"""
        print("🔧 Confluence Configuration Setup")
        print("=" * 50)
        print("This will help you configure your Confluence API credentials.")
        print("You'll need your Confluence URL, username, API token, and space key.")
        print()

        # Get Confluence base URL
        print("1. Confluence Base URL")
        print("   Examples:")
        print("   - https://your-domain.atlassian.net/wiki")
        print("   - https://your-company.atlassian.net/wiki")
        print("   - https://confluence.your-company.com/wiki")
        print()

        base_url = input("Enter your Confluence base URL: ").strip()
        if not base_url:
            print("❌ Base URL is required")
            return False

        # Ensure URL has proper scheme
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url

        # Get username/email
        print("\n2. Username/Email")
        print("   This is your Confluence username or email address")
        print()

        username = input("Enter your Confluence username/email: ").strip()
        if not username:
            print("❌ Username is required")
            return False

        # Get API token
        print("\n3. API Token")
        print("   This is NOT your password! You need to create an API token:")
        print("   1. Go to https://id.atlassian.com/manage-profile/security/api-tokens")
        print("   2. Click 'Create API token'")
        print("   3. Give it a name (e.g., 'Markdown Converter')")
        print("   4. Copy the generated token")
        print()

        api_token = getpass.getpass("Enter your API token: ").strip()
        if not api_token:
            print("❌ API token is required")
            return False

        # Get space key
        print("\n4. Space Key")
        print("   This is the short identifier for your Confluence space")
        print("   Examples: 'TEAM', 'DOCS', 'PROJECT'")
        print("   You can find this in your Confluence URL or space settings")
        print()

        space_key = input("Enter your space key: ").strip().upper()
        if not space_key:
            print("❌ Space key is required")
            return False

        # Create configuration
        config = {
            "base_url": base_url,
            "username": username,
            "api_token": api_token,
            "space_key": space_key
        }

        # Save configuration
        if self._save_config(config):
            print(f"\n✅ Configuration saved to {self.config_file}")
            print("\n🔒 Security Note:")
            print(f"   - Keep {self.config_file} secure and don't commit it to version control")
            print("   - The file is already in .gitignore")
            print("\n🧪 Next Steps:")
            print("   - Test your configuration: python config_tester.py")
            print("   - Convert your first file: python confluence_markdown_converter.py README.md")
            return True
        else:
            print("❌ Failed to save configuration")
            return False

    def get_converter(self):
        """Get a configured ConfluenceMarkdownConverter instance"""
        if not self.config:
            raise ValueError("No configuration loaded. Run setup first.")

        from confluence_markdown_converter import ConfluenceMarkdownConverter

        return ConfluenceMarkdownConverter(
            base_url=self.config['base_url'],
            username=self.config['username'],
            api_token=self.config['api_token'],
            space_key=self.config['space_key']
        )

    def show_config(self) -> None:
        """Display current configuration (without sensitive data)"""
        if not self.config:
            print("❌ No configuration found")
            print("Run setup first: python confluence_config.py --setup")
            return

        print("📋 Current Configuration")
        print("=" * 30)
        print(f"Base URL: {self.config['base_url']}")
        print(f"Username: {self.config['username']}")
        print(f"API Token: {'*' * len(self.config['api_token'])}")
        print(f"Space Key: {self.config['space_key']}")
        print(f"Config File: {self.config_file}")

    def test_config(self) -> bool:
        """Test the current configuration"""
        if not self.config:
            print("❌ No configuration found")
            return False

        try:
            converter = self.get_converter()
            print("✅ Configuration test successful")
            print("   Converter initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Configuration test failed: {e}")
            return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Confluence configuration management')
    parser.add_argument('--setup', action='store_true', help='Run interactive setup')
    parser.add_argument('--test', action='store_true', help='Test current configuration')
    parser.add_argument('--show', action='store_true', help='Show current configuration')
    parser.add_argument('--config-file', default=CONFIG_FILE, help='Configuration file path')

    args = parser.parse_args()

    config = ConfluenceConfig(args.config_file)

    if args.setup:
        success = config.setup_interactive()
        sys.exit(0 if success else 1)
    elif args.test:
        success = config.test_config()
        sys.exit(0 if success else 1)
    elif args.show:
        config.show_config()
    else:
        # Default: show help if no arguments
        parser.print_help()

if __name__ == "__main__":
    main()
