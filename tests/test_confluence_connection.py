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
#!/usr/bin/env python3
"""
Test script to diagnose Confluence API connection issues
"""

import requests
from confluence_config import ConfluenceConfig

def test_confluence_connection():
    """Test basic connection to Confluence API"""

    config = ConfluenceConfig()
    if not config.config:
        print("❌ No configuration found. Run setup first: python confluence_config.py --setup")
        return

    print("Testing Confluence API connection...")
    print(f"Base URL: {config.config['base_url']}")
    print(f"Username: {config.config['username']}")
    print(f"Space Key: {config.config['space_key']}")
    print(f"API Token: {'*' * len(config.config['api_token']) if config.config['api_token'] else 'NOT SET'}")
    print()

    # Create session with authentication
    session = requests.Session()
    session.auth = (config.config['username'], config.config['api_token'])
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

    # Test 1: Basic API endpoint
    print("Test 1: Basic API endpoint...")
    try:
        url = f"{config.config['base_url']}/rest/api/content"
        response = session.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # Test 2: Space information
    print("Test 2: Space information...")
    try:
        url = f"{config.config['base_url']}/rest/api/space/{config.config['space_key']}"
        response = session.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # Test 3: User information
    print("Test 3: User information...")
    try:
        url = f"{config.config['base_url']}/rest/api/user/current"
        response = session.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

if __name__ == "__main__":
    test_confluence_connection()