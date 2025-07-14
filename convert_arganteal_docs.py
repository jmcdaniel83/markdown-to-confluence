#!/usr/bin/env python3
"""
Arganteal SCT Documentation Converter

This script converts the Arganteal SCT project documentation to Confluence pages.
It's specifically tailored for the README.md and DEPLOYMENT.md files in this project.
"""

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

import os
from confluence_config import ConfluenceConfig

def main():
    """Convert Arganteal SCT documentation to Confluence"""
    
    print("=== Arganteal SCT Documentation Converter ===\n")
    
    # Check if markdown files exist
    markdown_files = ['README.md', 'DEPLOYMENT.md']
    existing_files = []
    
    for file in markdown_files:
        if os.path.exists(file):
            existing_files.append(file)
            print(f"✓ Found: {file}")
        else:
            print(f"✗ Missing: {file}")
    
    if not existing_files:
        print("\nNo markdown files found! Please ensure README.md and DEPLOYMENT.md exist.")
        return
    
    print(f"\nFound {len(existing_files)} markdown file(s) to convert.")
    
    # Initialize configuration
    try:
        config = ConfluenceConfig()
        
        # Check if configuration exists
        if not config.config:
            print("\nConfiguration not found. Please run setup first:")
            print("python confluence_config.py --setup")
            return
        
        print("\nConfiguration loaded successfully.")
        
        # Define custom page titles for better organization
        custom_titles = {
            'README.md': 'Arganteal SCT - Project Overview',
            'DEPLOYMENT.md': 'Arganteal SCT - Deployment Guide'
        }
        
        # Convert files with parent page structure
        print("\nConverting documentation to Confluence...")
        
        # Create a parent page for all project documentation
        parent_page_title = "Arganteal SCT Documentation"
        
        # Convert each file
        for file_path in existing_files:
            page_title = custom_titles.get(file_path, file_path.replace('.md', '').title())
            
            print(f"\nProcessing: {file_path} -> {page_title}")
            
            try:
                result = config.get_converter().publish_markdown_file(
                    file_path=file_path,
                    page_title=page_title,
                    parent_page_title=parent_page_title
                )
                print(f"✓ Successfully published: {page_title}")
                
                # Print the Confluence page URL
                if '_links' in result and 'webui' in result['_links']:
                    print(f"  📄 Page URL: {result['_links']['webui']}")
                    
            except Exception as e:
                print(f"✗ Error processing {file_path}: {str(e)}")
        
        print(f"\n=== Conversion Complete ===")
        print(f"All documentation has been published to Confluence under '{parent_page_title}'")
        
    except Exception as e:
        print(f"Configuration error: {str(e)}")
        print("Please run: python confluence_config.py --setup")

if __name__ == "__main__":
    main() 