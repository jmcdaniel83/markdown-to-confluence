#!/usr/bin/env python3
"""
Confluence Configuration Tester

This script provides comprehensive testing and diagnostics for the Confluence
markdown converter configuration. It tests various aspects including:
- Configuration file existence and validity
- API credentials and authentication
- Network connectivity
- Space access permissions
- Basic API functionality

Usage:
    python config_tester.py [--verbose] [--test-all]
"""

import os
import sys
import json
import requests
import argparse
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

# Configuration file paths
CONFIG_FILES = {
    'python_config': 'confluence_config.py',
    'json_config': 'confluence_config.json',
    'hidden_json_config': '.confluence_config.json'
}

class ConfigTester:
    """Comprehensive configuration tester for Confluence integration"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = []
        self.config = None

    def log(self, message: str, level: str = "INFO"):
        """Log a message with optional verbosity control"""
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(f"[{level}] {message}")

    def add_result(self, test_name: str, status: str, message: str, details: Optional[Dict] = None):
        """Add a test result"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "details": details or {}
        }
        self.results.append(result)

        # Print status indicator
        status_icon = {
            "PASS": "✅",
            "FAIL": "❌",
            "WARNING": "⚠️",
            "SKIP": "⏭️"
        }.get(status, "❓")

        print(f"{status_icon} {test_name}: {message}")

    def test_config_file_exists(self) -> bool:
        """Test if configuration file exists"""
        python_config = CONFIG_FILES['python_config']
        json_config = CONFIG_FILES['json_config']
        hidden_json_config = CONFIG_FILES['hidden_json_config']

        config_files = [python_config, json_config, hidden_json_config]

        for config_file in config_files:
            if os.path.exists(config_file):
                self.add_result(
                    "Config File Exists",
                    "PASS",
                    f"Found configuration file: {config_file}"
                )
                return True

        self.add_result(
            "Config File Exists",
            "FAIL",
            "No configuration file found. Expected one of: " + ", ".join(config_files)
        )
        return False

    def test_config_file_structure(self) -> bool:
        """Test configuration file structure and content"""
        # Try to import the config
        try:
            python_config = CONFIG_FILES['python_config']
            json_config = CONFIG_FILES['json_config']

            # Check for Python config file
            if os.path.exists(python_config):
                import importlib.util
                spec = importlib.util.spec_from_file_location("confluence_config", python_config)
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)

                # Check for CONFLUENCE_CONFIG or ConfluenceConfig class
                if hasattr(config_module, 'CONFLUENCE_CONFIG'):
                    self.config = config_module.CONFLUENCE_CONFIG
                    self.add_result(
                        "Config Structure",
                        "PASS",
                        "Found CONFLUENCE_CONFIG dictionary"
                    )
                    return True
                elif hasattr(config_module, 'ConfluenceConfig'):
                    config_class = config_module.ConfluenceConfig()
                    if hasattr(config_class, 'config') and config_class.config:
                        self.config = config_class.config
                        self.add_result(
                            "Config Structure",
                            "PASS",
                            "Found ConfluenceConfig class with valid config"
                        )
                        return True
                    else:
                        self.add_result(
                            "Config Structure",
                            "FAIL",
                            "ConfluenceConfig class found but no valid configuration"
                        )
                        return False
                else:
                    self.add_result(
                        "Config Structure",
                        "FAIL",
                        "No CONFLUENCE_CONFIG or ConfluenceConfig found in confluence_config.py"
                    )
                    return False

            # Check for JSON config file
            elif os.path.exists(json_config):
                with open(json_config, 'r') as f:
                    self.config = json.load(f)
                self.add_result(
                    "Config Structure",
                    "PASS",
                    "Found valid JSON configuration file"
                )
                return True

        except Exception as e:
            self.add_result(
                "Config Structure",
                "FAIL",
                f"Error loading configuration: {str(e)}"
            )
            return False

        return False

    def test_config_required_fields(self) -> bool:
        """Test that all required configuration fields are present"""
        if not self.config:
            self.add_result(
                "Required Fields",
                "SKIP",
                "No configuration loaded"
            )
            return False

        required_fields = ['base_url', 'username', 'api_token', 'space_key']
        missing_fields = []

        for field in required_fields:
            if field not in self.config or not self.config[field]:
                missing_fields.append(field)

        if missing_fields:
            self.add_result(
                "Required Fields",
                "FAIL",
                f"Missing required fields: {', '.join(missing_fields)}"
            )
            return False

        self.add_result(
            "Required Fields",
            "PASS",
            "All required fields present"
        )
        return True

    def test_url_format(self) -> bool:
        """Test that the base URL is properly formatted"""
        if not self.config or 'base_url' not in self.config:
            self.add_result(
                "URL Format",
                "SKIP",
                "No base_url in configuration"
            )
            return False

        base_url = self.config['base_url']

        try:
            parsed = urlparse(base_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL format")

            if parsed.scheme not in ['http', 'https']:
                raise ValueError("URL must use HTTP or HTTPS")

            self.add_result(
                "URL Format",
                "PASS",
                f"Valid URL format: {base_url}"
            )
            return True

        except Exception as e:
            self.add_result(
                "URL Format",
                "FAIL",
                f"Invalid URL format: {str(e)}"
            )
            return False

    def test_network_connectivity(self) -> bool:
        """Test basic network connectivity to Confluence"""
        if not self.config or 'base_url' not in self.config:
            self.add_result(
                "Network Connectivity",
                "SKIP",
                "No base_url in configuration"
            )
            return False

        try:
            # Test basic connectivity
            response = requests.get(self.config['base_url'], timeout=10)
            self.add_result(
                "Network Connectivity",
                "PASS",
                f"Successfully connected to {self.config['base_url']} (Status: {response.status_code})"
            )
            return True

        except requests.exceptions.ConnectionError:
            self.add_result(
                "Network Connectivity",
                "FAIL",
                "Connection failed - check your internet connection and Confluence URL"
            )
            return False
        except requests.exceptions.Timeout:
            self.add_result(
                "Network Connectivity",
                "FAIL",
                "Connection timeout - Confluence server may be slow or unreachable"
            )
            return False
        except Exception as e:
            self.add_result(
                "Network Connectivity",
                "FAIL",
                f"Unexpected error: {str(e)}"
            )
            return False

    def test_api_authentication(self) -> bool:
        """Test API authentication with provided credentials"""
        if not self.config:
            self.add_result(
                "API Authentication",
                "SKIP",
                "No configuration loaded"
            )
            return False

        try:
            session = requests.Session()
            session.auth = (self.config['username'], self.config['api_token'])
            session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })

            # Test authentication with user info endpoint
            url = f"{self.config['base_url']}/rest/api/user/current"
            response = session.get(url, timeout=10)

            if response.status_code == 200:
                user_info = response.json()
                self.add_result(
                    "API Authentication",
                    "PASS",
                    f"Authentication successful for user: {user_info.get('displayName', 'Unknown')}"
                )
                return True
            elif response.status_code == 401:
                self.add_result(
                    "API Authentication",
                    "FAIL",
                    "Authentication failed - check username and API token"
                )
                return False
            else:
                self.add_result(
                    "API Authentication",
                    "WARNING",
                    f"Unexpected status code: {response.status_code}"
                )
                return False

        except Exception as e:
            self.add_result(
                "API Authentication",
                "FAIL",
                f"Authentication test failed: {str(e)}"
            )
            return False

    def test_space_access(self) -> bool:
        """Test access to the specified Confluence space"""
        if not self.config:
            self.add_result(
                "Space Access",
                "SKIP",
                "No configuration loaded"
            )
            return False

        try:
            session = requests.Session()
            session.auth = (self.config['username'], self.config['api_token'])
            session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })

            # Test space access
            url = f"{self.config['base_url']}/rest/api/space/{self.config['space_key']}"
            response = session.get(url, timeout=10)

            if response.status_code == 200:
                space_info = response.json()
                self.add_result(
                    "Space Access",
                    "PASS",
                    f"Successfully accessed space: {space_info.get('name', self.config['space_key'])}"
                )
                return True
            elif response.status_code == 404:
                self.add_result(
                    "Space Access",
                    "FAIL",
                    f"Space '{self.config['space_key']}' not found or no access"
                )
                return False
            else:
                self.add_result(
                    "Space Access",
                    "WARNING",
                    f"Unexpected status code: {response.status_code}"
                )
                return False

        except Exception as e:
            self.add_result(
                "Space Access",
                "FAIL",
                f"Space access test failed: {str(e)}"
            )
            return False

    def test_api_endpoints(self) -> bool:
        """Test basic API endpoints functionality"""
        if not self.config:
            self.add_result(
                "API Endpoints",
                "SKIP",
                "No configuration loaded"
            )
            return False

        try:
            session = requests.Session()
            session.auth = (self.config['username'], self.config['api_token'])
            session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })

            # Test content endpoint
            url = f"{self.config['base_url']}/rest/api/content"
            response = session.get(url, params={'spaceKey': self.config['space_key'], 'limit': 1}, timeout=10)

            if response.status_code == 200:
                self.add_result(
                    "API Endpoints",
                    "PASS",
                    "Content API endpoint accessible"
                )
                return True
            else:
                self.add_result(
                    "API Endpoints",
                    "WARNING",
                    f"Content API returned status: {response.status_code}"
                )
                return False

        except Exception as e:
            self.add_result(
                "API Endpoints",
                "FAIL",
                f"API endpoint test failed: {str(e)}"
            )
            return False

    def test_converter_initialization(self) -> bool:
        """Test if the ConfluenceMarkdownConverter can be initialized"""
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from confluence_markdown_converter import ConfluenceMarkdownConverter

            if not self.config:
                self.add_result(
                    "Converter Initialization",
                    "SKIP",
                    "No configuration loaded"
                )
                return False

            converter = ConfluenceMarkdownConverter(
                base_url=self.config['base_url'],
                username=self.config['username'],
                api_token=self.config['api_token'],
                space_key=self.config['space_key']
            )

            self.add_result(
                "Converter Initialization",
                "PASS",
                "ConfluenceMarkdownConverter initialized successfully"
            )
            return True

        except ImportError:
            self.add_result(
                "Converter Initialization",
                "FAIL",
                "Could not import ConfluenceMarkdownConverter"
            )
            return False
        except Exception as e:
            self.add_result(
                "Converter Initialization",
                "FAIL",
                f"Converter initialization failed: {str(e)}"
            )
            return False

    def run_all_tests(self) -> Dict:
        """Run all configuration tests"""
        print("🔧 Confluence Configuration Tester")
        print("=" * 50)

        tests = [
            ("Config File Exists", self.test_config_file_exists),
            ("Config Structure", self.test_config_file_structure),
            ("Required Fields", self.test_config_required_fields),
            ("URL Format", self.test_url_format),
            ("Network Connectivity", self.test_network_connectivity),
            ("API Authentication", self.test_api_authentication),
            ("Space Access", self.test_space_access),
            ("API Endpoints", self.test_api_endpoints),
            ("Converter Initialization", self.test_converter_initialization),
        ]

        passed = 0
        failed = 0
        warnings = 0
        skipped = 0

        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed += 1
                else:
                    # Check the last result to determine if it was a failure or skip
                    if self.results and self.results[-1]['status'] == 'SKIP':
                        skipped += 1
                    else:
                        failed += 1
            except Exception as e:
                self.add_result(test_name, "FAIL", f"Test crashed: {str(e)}")
                failed += 1

        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"📈 Total: {len(tests)}")

        # Recommendations
        print("\n💡 Recommendations:")
        if failed > 0:
            print("• Fix the failed tests before using the converter")
        if not self.config:
            print("• Run setup to create configuration: python confluence_config.py --setup")
        if passed == len(tests):
            print("• All tests passed! Your configuration is ready to use.")

        return {
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "skipped": skipped,
            "total": len(tests),
            "results": self.results
        }

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test Confluence configuration')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--test-all', action='store_true', help='Run all tests (default)')

    args = parser.parse_args()

    tester = ConfigTester(verbose=args.verbose)
    results = tester.run_all_tests()

    # Exit with appropriate code
    if results['failed'] > 0:
        sys.exit(1)
    elif results['skipped'] == results['total']:
        sys.exit(2)  # All tests skipped
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()