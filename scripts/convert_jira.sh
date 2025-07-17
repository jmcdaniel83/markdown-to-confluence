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

# Configuration - UPDATE THESE VALUES FOR YOUR ENVIRONMENT
# You can also use environment variables or a config file
BASE_URL="https://your-domain.atlassian.net"
USERNAME="your-email@example.com"
API_TOKEN="your-api-token-here"
PROJECT_KEY="PROJ"

# Issue configuration - UPDATE THESE FOR YOUR ISSUES
# Uncomment and configure the issue you want to create/update
ISSUE_TYPE="Task"
PRIORITY="Medium"
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
echo "📋 Issue Type: ${ISSUE_TYPE:-Task}"
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