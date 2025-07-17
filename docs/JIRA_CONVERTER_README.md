# Jira Markdown Converter

A Python tool to convert markdown files to Jira markup format and publish them directly to Jira using the REST API. This tool maintains proper formatting, handles code blocks, tables, links, and other markdown elements for Jira issues and comments.

## Features

- ✅ **Markdown to Jira Conversion**: Converts markdown syntax to Jira markup
- ✅ **Direct API Publishing**: Posts content directly to Jira via REST API
- ✅ **Issue Management**: Creates new issues or updates existing ones
- ✅ **Comment Support**: Adds content as comments to existing issues
- ✅ **Code Block Support**: Preserves syntax highlighting for code blocks
- ✅ **Table Support**: Converts markdown tables to Jira tables
- ✅ **Link Preservation**: Maintains internal and external links
- ✅ **Batch Processing**: Convert multiple files at once
- ✅ **Configuration Management**: Secure credential storage

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Jira Account** with API access
3. **Jira API Token** (not your password)

## Installation

1. **Clone or download** the converter files to your project directory
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Get Your Jira API Token

1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name (e.g., "Markdown Converter")
4. Copy the generated token (you won't see it again!)

### 2. Configure Your Credentials

Run the interactive setup:
```bash
python jira_config.py --setup
```

This will prompt you for:
- **Jira Base URL**: Your Jira instance URL (e.g., `https://your-domain.atlassian.net`)
- **Username/Email**: Your Jira username or email
- **API Token**: The token you created in step 1
- **Project Key**: The Jira project key where issues will be created (e.g., `PROJ`)
- **Default Issue Type**: Default type for new issues (e.g., `Task`, `Bug`, `Story`)
- **Default Priority**: Default priority for new issues (e.g., `Medium`, `High`, `Low`)
- **Default Assignee**: Optional default assignee username

### 3. Test Your Configuration

```bash
python jira_config.py --test
```

This will verify your credentials and project access.

### 4. Generate Local Script

Generate a local script with your credentials embedded:

```bash
python jira_config.py --generate-script convert_jira.sh
```

This creates a `convert_jira.sh` script at the project root with:
- Your credentials from `jira_config.json`
- Template structure from `scripts/convert_jira.sh`
- Auto-generated header indicating it contains credentials
- Ready-to-use configuration

### 5. Customize and Run

Edit the generated script to customize:
- **ISSUE_TYPE**: Type of issue to create (Task, Bug, Story, etc.)
- **PRIORITY**: Issue priority (Low, Medium, High, etc.)
- **MARKDOWN_FILE**: Path to your markdown file
- **PARENT_KEY**: Optional parent issue key for child issues
- **ISSUE_KEY**: Optional existing issue key to update

Then run:
```bash
./convert_jira.sh
```

⚠️ **Security Note**: Generated scripts contain your API token and are automatically ignored by git!

## Usage

### Command Line

Convert and publish one or more Markdown files to Jira:

```bash
python jira_markdown_converter.py <file1.md> <file2.md> \
  --base-url https://your-domain.atlassian.net \
  --username your-email@example.com \
  --api-token your-jira-api-token \
  --project-key PROJ \
  [--issue-type "Task"] \
  [--priority "Medium"] \
  [--assignee "username"] \
  [--parent-key "PROJ-123"] \
  [--issue-key "PROJ-123"] \
  [--as-comment]
```

**Parameters:**
- `--base-url`: Your Jira base URL
- `--username`: Your Jira username/email
- `--api-token`: Your Jira API token (not password)
- `--project-key`: The Jira project key
- `--issue-type`: Type of issue to create (default: Task)
- `--priority`: Issue priority (default: Medium)
- `--assignee`: Optional assignee username
- `--parent-key`: Optional parent issue key for creating child issues
- `--issue-key`: Optional existing issue key to update
- `--as-comment`: If provided, add content as comment to existing issue

### Using Configuration File

If you've set up the configuration file, you can use a simplified command:

```bash
python jira_markdown_converter.py docs/example.md
```

### Examples

**Create a new issue:**
```bash
python jira_markdown_converter.py docs/bug_report.md \
  --base-url https://company.atlassian.net \
  --username user@company.com \
  --api-token <your-token> \
  --project-key PROJ \
  --issue-type Bug \
  --priority High
```

**Update existing issue:**
```bash
python jira_markdown_converter.py docs/updated_spec.md \
  --base-url https://company.atlassian.net \
  --username user@company.com \
  --api-token <your-token> \
  --project-key PROJ \
  --issue-key PROJ-123
```

**Create child issue:**
```bash
python jira_markdown_converter.py docs/subtask.md \
  --base-url https://company.atlassian.net \
  --username user@company.com \
  --api-token <your-token> \
  --project-key PROJ \
  --issue-type Sub-task \
  --parent-key PROJ-123
```

**Add as comment to existing issue:**
```bash
python jira_markdown_converter.py docs/additional_info.md \
  --base-url https://company.atlassian.net \
  --username user@company.com \
  --api-token <your-token> \
  --project-key PROJ \
  --issue-key PROJ-123 \
  --as-comment
```

## Limitations

⚠️ **Note:** Nested lists are currently not supported in the Jira converter. Only flat (single-level) lists will be converted correctly. If you use nested lists in your Markdown, they may not render as expected in Jira. Support for nested lists is planned for a future update.

---

## Project Structure

```
markdown_to_confluence.master/
├── jira_markdown_converter.py      # Main Jira converter
├── jira_config.py                  # Configuration management
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── .venv/                          # Virtual environment (not tracked)
├── docs/                           # Documentation
│   ├── JIRA_CONVERTER_README.md    # This file
│   └── example_comprehensive.md    # Example markdown file
└── tests/                          # Test suite
    └── test_jira_conversion.py     # Jira conversion tests
```

## Supported Markdown Features

| Markdown Feature | Jira Support | Notes |
|------------------|--------------|-------|
| **Headers** (H1-H6) | ✅ | Preserved as-is |
| **Bold/Italic** | ✅ | `*bold*` and `_italic_` |
| **Code Blocks** | ✅ | Syntax highlighting preserved |
| **Inline Code** | ✅ | `{{monospace}}` tags |
| **Links** | ✅ | Internal and external links |
| **Lists** (UL/OL) | ✅ | Bullet and numbered lists |
| **Tables** | ✅ | Markdown tables converted |
| **Blockquotes** | ✅ | Preserved formatting |
| **Line Breaks** | ✅ | Proper spacing maintained |
| **Strikethrough** | ✅ | `-strikethrough-` format |

## Configuration File

The `jira_config.json` file stores your credentials securely:

```json
{
  "base_url": "https://your-domain.atlassian.net",
  "username": "your-email@domain.com",
  "api_token": "your-api-token-here",
  "project_key": "PROJ",
  "default_issue_type": "Task",
  "default_priority": "Medium",
  "default_assignee": "username",
  "default_parent_key": "PROJ-123"
}
```

⚠️ **Security Note**:
- **`jira_config.json`** contains sensitive API tokens and credentials - never commit this file to version control!
- The `jira_config.json` file is automatically added to `.gitignore`

## Troubleshooting

### Common Issues

1. **"Configuration not set up"**
   - Run `python jira_config.py --setup` first

2. **"Authentication failed"**
   - Verify your API token is correct
   - Ensure your username/email is correct
   - Check that your Jira URL is correct

3. **"Project not found"**
   - Verify your project key is correct
   - Ensure you have access to the project

4. **"Issue creation failed"**
   - Check that you have permission to create issues in the project
   - Verify the issue type exists in your project

### Debug Mode

For detailed error information, you can modify the scripts to add debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Reference

### JiraMarkdownConverter Class

```python
converter = JiraMarkdownConverter(
    base_url="https://your-domain.atlassian.net",
    username="your-email@domain.com",
    api_token="your-api-token",
    project_key="PROJ"
)

# Convert and publish a file
result = converter.publish_markdown_file(
    file_path="README.md",
    issue_type="Task",  # Optional
    priority="Medium",   # Optional
    assignee="username"  # Optional
)
```

### Methods

- `convert_markdown_to_jira(markdown_content)` - Convert markdown to Jira markup
- `publish_markdown_file(file_path, issue_type, priority, assignee)` - Convert and publish a file
- `create_issue(summary, description, issue_type, priority, assignee)` - Create a new issue
- `update_issue(issue_key, summary, description)` - Update an existing issue
- `add_comment(issue_key, comment)` - Add a comment to an issue

## Integration with CI/CD

You can integrate this tool into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Convert and publish docs to Jira
  run: |
    pip install -r requirements.txt
    python jira_markdown_converter.py docs/README.md
  env:
    JIRA_BASE_URL: ${{ secrets.JIRA_BASE_URL }}
    JIRA_USERNAME: ${{ secrets.JIRA_USERNAME }}
    JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
    JIRA_PROJECT_KEY: ${{ secrets.JIRA_PROJECT_KEY }}
```

## Contributing

To extend the converter:

1. **Add new markdown features**: Modify the `_html_to_jira_markup` method
2. **Improve error handling**: Add more specific exception handling
3. **Add new output formats**: Extend the converter to support other platforms

## License

This tool is provided as-is for internal use. Modify as needed for your requirements.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Jira API permissions
3. Test with a simple markdown file first
4. Check the Jira REST API documentation for reference