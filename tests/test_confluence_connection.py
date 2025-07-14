#!/usr/bin/env python3
"""
Test script to diagnose Confluence API connection issues
"""

import requests
from confluence_config import CONFLUENCE_CONFIG

def test_confluence_connection():
    """Test basic connection to Confluence API"""
    
    print("Testing Confluence API connection...")
    print(f"Base URL: {CONFLUENCE_CONFIG['base_url']}")
    print(f"Username: {CONFLUENCE_CONFIG['username']}")
    print(f"Space Key: {CONFLUENCE_CONFIG['space_key']}")
    print(f"API Token: {'*' * len(CONFLUENCE_CONFIG['api_token']) if CONFLUENCE_CONFIG['api_token'] else 'NOT SET'}")
    print()
    
    # Create session with authentication
    session = requests.Session()
    session.auth = (CONFLUENCE_CONFIG['username'], CONFLUENCE_CONFIG['api_token'])
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })
    
    # Test 1: Basic API endpoint
    print("Test 1: Basic API endpoint...")
    try:
        url = f"{CONFLUENCE_CONFIG['base_url']}/rest/api/content"
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
        url = f"{CONFLUENCE_CONFIG['base_url']}/rest/api/space/{CONFLUENCE_CONFIG['space_key']}"
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
        url = f"{CONFLUENCE_CONFIG['base_url']}/rest/api/user/current"
        response = session.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

if __name__ == "__main__":
    test_confluence_connection() 