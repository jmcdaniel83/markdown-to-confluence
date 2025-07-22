#!/bin/bash

# Jira Issue Converter Script
# Converts markdown documentation to Jira issues

set -e  # Exit on any error

echo "🚀 Jira Issue Converter"
echo "======================="

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

# Configuration - pulled from jira_config.json

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

# Load configuration from jira_config.json
CONFIG_FILE="jira_config.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Error: Configuration file not found: $CONFIG_FILE"
    echo "Please run 'python jira_config.py --setup' to create it."
    exit 1
fi

BASE_URL=$(jq -r '.base_url' "$CONFIG_FILE")
USERNAME=$(jq -r '.username' "$CONFIG_FILE")
API_TOKEN=$(jq -r '.api_token' "$CONFIG_FILE")
PROJECT_KEY=$(jq -r '.project_key' "$CONFIG_FILE")

# Optional configurations from JSON, with fallback to hardcoded if not present in JSON
ISSUE_TYPE=$(jq -r '.default_issue_type // "Story"' "$CONFIG_FILE")
PRIORITY=$(jq -r '.default_priority // "Medium"' "$CONFIG_FILE")
PARENT_KEY=$(jq -r '.default_parent_key // ""' "$CONFIG_FILE") # Default to empty string if not found

# Ensure all critical configurations are loaded
if [[ -z "$BASE_URL" || -z "$USERNAME" || -z "$API_TOKEN" || -z "$PROJECT_KEY" ]]; then
    echo "❌ Error: Missing one or more critical configuration values in $CONFIG_FILE."
    echo "Please ensure base_url, username, api_token, and project_key are set."
    exit 1
fi

# Issue configuration - UPDATE THESE FOR YOUR ISSUES
# Uncomment and configure the issue you want to create/update
#ISSUE_TYPE="Story"
#PRIORITY="Medium"
#ASSIGNEE="username"
#PARENT_KEY="PROJ-123"  # Optional: for creating child issues
#ISSUE_KEY="PROJ-456"   # Optional: for updating existing issues
#AS_COMMENT="false"     # Set to "true" to add as comment instead of description

# Example configurations for different use cases:
#ISSUE_TYPE="Bug"
#PRIORITY="High"
#ASSIGNEE="user.name"
#PARENT_KEY="PROJ-123"

# Input directory configuration
INPUT_BASE="input/jira"

# Markdown file to convert - UPDATE THIS PATH
MARKDOWN_FILE="$INPUT_BASE/your_file.md"

# Check if markdown file exists
if [[ ! -f "$MARKDOWN_FILE" ]]; then
    echo "❌ Error: Markdown file not found: $MARKDOWN_FILE"
    echo "Please update the MARKDOWN_FILE variable to point to your markdown file"
    echo "Or create the input directory structure:"
    echo "  mkdir -p input/jira"
    echo "  # Add your markdown files to input/jira/"
    exit 1
fi

echo "📄 Converting: $MARKDOWN_FILE"
echo "🏷️  Project: $PROJECT_KEY"
echo "📋 Issue Type: ${ISSUE_TYPE:-Story}"
echo "⚡ Priority: ${PRIORITY:-Medium}"
if [[ -n "$ASSIGNEE" ]]; then
    echo "👤 Assignee: $ASSIGNEE"
fi
if [[ -n "$PARENT_KEY" ]]; then
    echo "👨‍👩‍👧‍👦 Parent Issue: $PARENT_KEY"
fi
if [[ -n "$ISSUE_KEY" ]]; then
    echo "🔑 Update Issue: $ISSUE_KEY"
fi
if [[ "$AS_COMMENT" == "true" ]]; then
    echo "💬 Adding as comment"
fi
echo ""

# Build the command
CMD="python jira_markdown_converter.py \"$MARKDOWN_FILE\" \
    --base-url \"$BASE_URL\" \
    --username \"$USERNAME\" \
    --api-token \"$API_TOKEN\" \
    --project-key \"$PROJECT_KEY\""

# Add optional parameters
if [[ -n "$ISSUE_TYPE" ]]; then
    CMD="$CMD --issue-type \"$ISSUE_TYPE\""
fi
if [[ -n "$PRIORITY" ]]; then
    CMD="$CMD --priority \"$PRIORITY\""
fi
if [[ -n "$ASSIGNEE" ]]; then
    CMD="$CMD --assignee \"$ASSIGNEE\""
fi
if [[ -n "$PARENT_KEY" ]]; then
    CMD="$CMD --parent-key \"$PARENT_KEY\""
fi
if [[ -n "$ISSUE_KEY" ]]; then
    CMD="$CMD --issue-key \"$ISSUE_KEY\""
fi
if [[ "$AS_COMMENT" == "true" ]]; then
    CMD="$CMD --as-comment"
fi

# Run the converter
echo "🔄 Running: $CMD"
echo ""
eval $CMD

echo ""
echo "✅ Conversion complete!"
echo "📋 Check your Jira project for the created/updated issue."
echo ""
echo "💡 Tips:"
echo "  - Use --parent-key to create child issues"
echo "  - Use --issue-key to update existing issues"
echo "  - Use --as-comment to add content as a comment"
echo "  - Use --issue-type Bug/Story/Task/Sub-task as needed"