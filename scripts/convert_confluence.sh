#!/bin/bash

# Confluence Documentation Converter Script
# Converts markdown documentation to Confluence pages

set -e  # Exit on any error

echo "🚀 Confluence Documentation Converter"
echo "===================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Virtual environment not detected, attempting to activate..."

    # Check if .venv directory exists
    if [[ -d ".venv" ]]; then
        echo "✅ Found .venv directory"
        source .venv/bin/activate
    else
        echo "❌ Error: .venv directory not found!"
        echo "Please update the virtual environment path in this script or create one:"
        echo "  python3 -m venv .venv"
        echo "  source .venv/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
fi

# Configuration - pulled from confluence_config.json

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "❌ Error: jq is not installed."
    echo "Please install jq to automatically load configuration from JSON."
    echo "On macOS: brew install jq"
    echo "On Debian/Ubuntu: sudo apt-get install jq"
    echo "On Windows (with Scoop): scoop install jq"
    exit 1
fi

# Load configuration from confluence_config.json
CONFIG_FILE="confluence_config.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Error: Configuration file not found: $CONFIG_FILE"
    echo "Please run 'python confluence_config.py --setup' to create it."
    exit 1
fi

BASE_URL=$(jq -r '.base_url' "$CONFIG_FILE")
USERNAME=$(jq -r '.username' "$CONFIG_FILE")
API_TOKEN=$(jq -r '.api_token' "$CONFIG_FILE")
SPACE_KEY=$(jq -r '.space_key' "$CONFIG_FILE")

# Ensure all critical configurations are loaded
if [[ -z "$BASE_URL" || -z "$USERNAME" || -z "$API_TOKEN" || -z "$SPACE_KEY" ]]; then
    echo "❌ Error: Missing one or more critical configuration values in $CONFIG_FILE."
    echo "Please ensure base_url, username, api_token, and space_key are set."
    exit 1
fi

# Page configuration - UPDATE THESE FOR YOUR PAGES
# Uncomment and configure the page you want to update
PAGE_TITLE="Your Page Title"
PAGE_ID="1234567890"

# Input directory configuration
INPUT_BASE="input/confluence"

# Markdown file to convert - UPDATE THIS PATH
MARKDOWN_FILE="$INPUT_BASE/your_file.md"

# Check if markdown file exists
if [[ ! -f "$MARKDOWN_FILE" ]]; then
    echo "❌ Error: Markdown file not found: $MARKDOWN_FILE"
    echo "Please update the MARKDOWN_FILE variable to point to your markdown file"
    echo "Or create the input directory structure:"
    echo "  mkdir -p input/confluence"
    echo "  # Add your markdown files to input/confluence/"
    exit 1
fi

echo "📄 Converting: $MARKDOWN_FILE"
echo "📝 Page Title: $PAGE_TITLE"
echo "🌐 Space: $SPACE_KEY"
echo "👤 User: $USERNAME"
echo ""

# Run the converter
python confluence_markdown_converter.py "$MARKDOWN_FILE" \
    --base-url "$BASE_URL" \
    --username "$USERNAME" \
    --api-token "$API_TOKEN" \
    --space-key "$SPACE_KEY" \
    --page-title "$PAGE_TITLE" \
    --page-id "$PAGE_ID"

echo ""
echo "✅ Conversion complete!"
echo "📋 Check your Confluence space for the updated page."