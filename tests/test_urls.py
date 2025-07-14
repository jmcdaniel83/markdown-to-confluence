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
Test different possible Confluence URL variations
"""

import requests
from confluence_config import CONFLUENCE_CONFIG

def test_url_variations():
    """Test different possible Confluence URL variations"""
    
    base_urls = [
        "https://arganteal.atlassian.net",
        "https://arganteal.atlassian.net/wiki",
        "https://arganteal.atlassian.net/confluence",
        "https://arganteal.atlassian.net/rest/api",
    ]
    
    session = requests.Session()
    session.auth = (CONFLUENCE_CONFIG['username'], CONFLUENCE_CONFIG['api_token'])
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })
    
    for base_url in base_urls:
        print(f"\nTesting: {base_url}")
        print("-" * 50)
        
        # Test basic API endpoint
        try:
            url = f"{base_url}/rest/api/content"
            response = session.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✓ SUCCESS! This URL works!")
                print(f"Response preview: {response.text[:100]}...")
                return base_url
            elif response.status_code == 401:
                print("✗ Authentication failed (401)")
            elif response.status_code == 403:
                print("✗ Access forbidden (403)")
            elif response.status_code == 404:
                print("✗ Not found (404)")
            else:
                print(f"✗ Unexpected status: {response.status_code}")
                print(f"Response: {response.text[:100]}...")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    return None

if __name__ == "__main__":
    working_url = test_url_variations()
    if working_url:
        print(f"\n🎉 Found working URL: {working_url}")
    else:
        print("\n❌ No working URL found. Please check your Confluence instance URL.") 