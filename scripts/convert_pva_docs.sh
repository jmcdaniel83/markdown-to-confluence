#!/bin/bash

# PVA Documentation Converter Script
# Converts the TDD documentation to Confluence

set -e  # Exit on any error

echo "🚀 PVA Documentation Converter"
echo "=============================="

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

# Configuration - UPDATE THESE VALUES FOR YOUR ENVIRONMENT
# You can also use environment variables or a config file
BASE_URL="https://your-domain.atlassian.net/wiki"   # Replace with your Confluence URL
USERNAME="your-email@example.com"                   # Replace with your username
API_TOKEN="your-api-token-here"                     # Replace with your API token
SPACE_KEY="YOURSPACE"                               # Replace with your space key

# Page configuration - UPDATE THESE FOR YOUR PAGES
# Uncomment and configure the page you want to update
PAGE_TITLE="Your Page Title Here"
PAGE_ID="your-page-id-here"

# Input directory configuration
INPUT_BASE="your-input-directory"

# Markdown file to convert - UPDATE THIS PATH
MARKDOWN_FILE="$INPUT_BASE/child/your-markdown-file.md"

# Check if markdown file exists
if [[ ! -f "$MARKDOWN_FILE" ]]; then
    echo "❌ Error: Markdown file not found: $MARKDOWN_FILE"
    echo "Please update the MARKDOWN_FILE variable to point to your markdown file"
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