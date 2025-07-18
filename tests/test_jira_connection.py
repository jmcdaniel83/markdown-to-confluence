#!/usr/bin/env python3
"""
Test script to check Jira connection and available issue types and priorities
"""

import requests
import json
import sys
import os

# Add the parent directory to the path so we can import jira_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jira_config import JiraConfig

def test_connection(config: JiraConfig):
    """Test basic connection to Jira"""
    if not config.is_configured():
        print("❌ Configuration not complete. Run setup first.")
        print("   Use: python jira_config.py --setup")
        return False

    session = requests.Session()
    session.auth = (config.username, config.api_token)
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

    # Test basic connection
    url = f"{config.base_url}/rest/api/2/myself"
    response = session.get(url)
    print(f"Connection test status: {response.status_code}")
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ Connected as: {user_info.get('displayName', 'Unknown')}")
        return True
    else:
        print(f"❌ Connection failed: {response.text}")
        return False

def get_project_info(config: JiraConfig):
    """Get project information"""
    session = requests.Session()
    session.auth = (config.username, config.api_token)
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

    url = f"{config.base_url}/rest/api/2/project/{config.project_key}"
    response = session.get(url)
    print(f"\nProject info status: {response.status_code}")
    if response.status_code == 200:
        project_info = response.json()
        print(f"✅ Project: {project_info.get('name', 'Unknown')} ({project_info.get('key', 'Unknown')})")
        print(f"   Project ID: {project_info.get('id', 'Unknown')}")
        return project_info
    else:
        print(f"❌ Failed to get project info: {response.text}")
        return None

def get_issue_types(config: JiraConfig):
    """Get available issue types for the project"""
    session = requests.Session()
    session.auth = (config.username, config.api_token)
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

    url = f"{config.base_url}/rest/api/2/project/{config.project_key}"
    response = session.get(url)
    if response.status_code == 200:
        project_info = response.json()
        project_id = project_info.get('id')

        # Get issue types for this project
        url = f"{config.base_url}/rest/api/2/project/{project_id}/statuses"
        response = session.get(url)
        print(f"\nIssue types status: {response.status_code}")
        if response.status_code == 200:
            issue_types = response.json()
            print("✅ Available issue types:")
            for issue_type in issue_types:
                print(f"   - {issue_type.get('name', 'Unknown')}")
        else:
            print(f"❌ Failed to get issue types: {response.text}")
    else:
        print(f"❌ Failed to get project info for issue types: {response.text}")

def get_priorities(config: JiraConfig):
    """Get available priorities"""
    session = requests.Session()
    session.auth = (config.username, config.api_token)
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

    url = f"{config.base_url}/rest/api/2/priority"
    response = session.get(url)
    print(f"\nPriorities status: {response.status_code}")
    if response.status_code == 200:
        priorities = response.json()
        print("✅ Available priorities:")
        for priority in priorities:
            print(f"   - {priority.get('name', 'Unknown')}")
    else:
        print(f"❌ Failed to get priorities: {response.text}")

def get_components(config: JiraConfig):
    """Get available components for the project"""
    session = requests.Session()
    session.auth = (config.username, config.api_token)
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

    url = f"{config.base_url}/rest/api/2/project/{config.project_key}/components"
    response = session.get(url)
    print(f"\nComponents status: {response.status_code}")
    if response.status_code == 200:
        components = response.json()
        print("✅ Available components:")
        for component in components:
            print(f"   - {component.get('name', 'Unknown')} (ID: {component.get('id', 'Unknown')})")
    else:
        print(f"❌ Failed to get components: {response.text}")

if __name__ == "__main__":
    print("Testing Jira connection and configuration...")

    # Load configuration
    config = JiraConfig()

    if test_connection(config):
        get_project_info(config)
        get_issue_types(config)
        get_priorities(config)
        get_components(config)
    else:
        print("Cannot proceed with other tests due to connection failure.")
        print("\nTo set up configuration, run:")
        print("  python jira_config.py --setup")