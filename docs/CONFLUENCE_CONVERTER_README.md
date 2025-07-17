# Confluence Markdown Converter

A Python tool to convert markdown files to Confluence format and publish them directly to Confluence using the REST API. This tool maintains proper formatting, handles code blocks, tables, links, and other markdown elements.

## Features

- ✅ **Markdown to Confluence Conversion**: Converts markdown syntax to Confluence markup
- ✅ **Direct API Publishing**: Posts content directly to Confluence via REST API
- ✅ **Page Management**: Creates new pages or updates existing ones
- ✅ **Hierarchical Structure**: Supports parent-child page relationships
- ✅ **Code Block Support**: Preserves syntax highlighting for code blocks
- ✅ **Table Support**: Converts markdown tables to Confluence tables
- ✅ **Link Preservation**: Maintains internal and external links
- ✅ **Batch Processing**: Convert multiple files at once
- ✅ **Configuration Management**: Secure credential storage

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Confluence Account** with API access
3. **Confluence API Token** (not your password)

## Installation

1. **Clone or download** the converter files to your project directory
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Get Your Confluence API Token

1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name (e.g., "Markdown Converter")
4. Copy the generated token (you won't see it again!)

### 2. Configure Your Credentials

Run the interactive setup:
```bash
python confluence_config.py --setup
```

This will prompt you for:
- **Confluence Base URL**: Your Confluence instance URL (e.g., `https://your-domain.atlassian.net`)
- **Username/Email**: Your Confluence username or email
- **API Token**: The token you created in step 1
- **Space Key**: The Confluence space where pages will be created

The configuration will be saved to `confluence_config.json` for future use.

## Usage

### Basic Usage

Convert a single markdown file:
```bash
python confluence_config.py --files README.md
```

Convert multiple files:
```bash
python confluence_config.py --files README.md DEPLOYMENT.md
```

### Advanced Usage

Create pages under a parent page:
```bash
python confluence_config.py --files README.md --parent-page "Project Documentation"
```

### Direct API Usage

For more control, use the converter directly:
```bash
python confluence_markdown_converter.py README.md \
  --base-url "https://your-domain.atlassian.net" \
  --username "your-email@domain.com" \
  --api-token "your-api-token" \
  --space-key "YOURSPACE"
```

## Examples

### Example 1: Convert Project Documentation

```bash
# Setup credentials (first time only)
python confluence_config.py --setup

# Test your configuration
python confluence_config.py --test

# Generate a local script with your credentials
python confluence_config.py --generate-script convert_confluence.sh

# Edit the script to customize page titles and file paths
nano convert_confluence.sh

# Run the script
./convert_confluence.sh
```

### Example 2: Update Existing Pages

The tool automatically detects existing pages and updates them:
```bash
python confluence_config.py --files README.md
# If "README" page exists, it will be updated
# If not, a new page will be created
```

### Example 3: Batch Convert All Markdown Files

```bash
# Convert all .md files in current directory
python confluence_config.py --files *.md --parent-page "Project Documentation"
```

## File Structure

```
your-project/
├── confluence_markdown_converter.py  # Main converter script
├── confluence_config.py              # Configuration management (safe to commit)
├── confluence_config.json            # Your credentials (DO NOT COMMIT)
├── requirements.txt                  # Python dependencies
├── requirements-minimal.txt          # Minimal dependencies
├── README.md                         # Project documentation
├── LICENSE                           # Apache 2.0 license
├── .gitignore                        # Git ignore rules
├── .venv/                            # Virtual environment (not tracked)
├── docs/                             # Documentation
│   ├── CONFLUENCE_CONVERTER_README.md # This file
│   ├── CONFIG_TESTER_README.md        # Configuration testing guide
│   └── example_comprehensive.md       # Example markdown file
├── scripts/                         # Utility scripts and templates
│   ├── convert_confluence.sh        # Template script (safe to commit)
│   ├── convert_jira.sh              # Template script (safe to commit)
│   ├── adjust_headers.py            # Header adjustment utility
│   └── add_separators.py            # Separator addition utility
└── tests/                           # Test suite
    ├── test_confluence_config.py     # Configuration testing
    ├── test_confluence_connection.py # API connection tests
    ├── test_urls.py                  # URL validation tests
    ├── test_code_block_conversion.py # Code block conversion tests
    ├── test_math_conversion.py       # Math conversion tests
    ├── test_strikethrough.py         # Strikethrough tests
    ├── test_definition_lists.py      # Definition list tests
    ├── test_placeholders.py          # Placeholder tests
    ├── test_comprehensive_strikethrough.py # Comprehensive tests
    └── debug_code_block.py          # Debug utilities
```

## Supported Markdown Features

| Markdown Feature | Confluence Support | Notes |
|------------------|-------------------|-------|
| **Headers** (H1-H6) | ✅ | Preserved as-is |
| **Bold/Italic** | ✅ | `<strong>` and `<em>` tags |
| **Code Blocks** | ✅ | Syntax highlighting preserved |
| **Inline Code** | ✅ | `<code>` tags |
| **Links** | ✅ | Internal and external links |
| **Lists** (UL/OL) | ✅ | Bullet and numbered lists |
| **Tables** | ✅ | Markdown tables converted |
| **Blockquotes** | ✅ | Preserved formatting |
| **Line Breaks** | ✅ | Proper spacing maintained |
| **Images** | ⚠️ | Basic support (URLs only) |

## Script Generation

The configuration system can automatically generate local scripts with your credentials embedded:

### Generate Local Script

```bash
python confluence_config.py --generate-script convert_confluence.sh
```

This creates a `convert_confluence.sh` script at the project root with:
- Your credentials from `confluence_config.json`
- Template structure from `scripts/convert_confluence.sh`
- Auto-generated header indicating it contains credentials
- Ready-to-use configuration

### Customize Generated Script

Edit the generated script to customize:
- **PAGE_TITLE**: The title for your Confluence page
- **PAGE_ID**: Optional - for updating existing pages
- **MARKDOWN_FILE**: Path to your markdown file

### Security

- Generated scripts contain your credentials and are **automatically ignored by git**
- The `.gitignore` file includes `/convert_*.sh` to prevent accidental commits
- Template scripts in `scripts/` are safe to commit (they contain placeholders only)

## Configuration File

The `confluence_config.json` file stores your credentials securely:

```json
{
  "base_url": "https://your-domain.atlassian.net",
  "username": "your-email@domain.com",
  "api_token": "your-api-token-here",
  "space_key": "YOURSPACE"
}
```

⚠️ **Security Note**:
- **`confluence_config.json`** contains sensitive API tokens and credentials - never commit this file to version control!
- The `confluence_config.json` file is automatically added to `.gitignore`

## Troubleshooting

### Common Issues

1. **"Configuration not set up"**
   - Run `python confluence_config.py --setup` first

2. **"Authentication failed"**
   - Verify your API token is correct
   - Ensure your username/email is correct
   - Check that your Confluence URL is correct

3. **"Space not found"**
   - Verify your space key is correct
   - Ensure you have access to the space

4. **"Page creation failed"**
   - Check that you have permission to create pages in the space
   - Verify the parent page exists (if specified)

### Debug Mode

For detailed error information, you can modify the scripts to add debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Reference

### ConfluenceMarkdownConverter Class

```python
converter = ConfluenceMarkdownConverter(
    base_url="https://your-domain.atlassian.net",
    username="your-email@domain.com",
    api_token="your-api-token",
    space_key="YOURSPACE"
)

# Convert and publish a file
result = converter.publish_markdown_file(
    file_path="README.md",
    page_title="Custom Title",  # Optional
    parent_page_title="Parent Page"  # Optional
)
```

### Methods

- `convert_markdown_to_confluence(markdown_content)` - Convert markdown to Confluence markup
- `publish_markdown_file(file_path, page_title, parent_page_title)` - Convert and publish a file
- `create_page(title, content, parent_id)` - Create a new page
- `update_page(page_id, title, content, version)` - Update an existing page
- `get_page_id(page_title)` - Get page ID by title

## Integration with CI/CD

You can integrate this tool into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Convert and publish docs to Confluence
  run: |
    pip install -r requirements.txt
    python confluence_config.py --files README.md DEPLOYMENT.md
  env:
    CONFLUENCE_BASE_URL: ${{ secrets.CONFLUENCE_BASE_URL }}
    CONFLUENCE_USERNAME: ${{ secrets.CONFLUENCE_USERNAME }}
    CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
    CONFLUENCE_SPACE_KEY: ${{ secrets.CONFLUENCE_SPACE_KEY }}
```

## Contributing

To extend the converter:

1. **Add new markdown features**: Modify the `_html_to_confluence_markup` method
2. **Improve error handling**: Add more specific exception handling
3. **Add new output formats**: Extend the converter to support other platforms

## License

This tool is provided as-is for internal use. Modify as needed for your requirements.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Confluence API permissions
3. Test with a simple markdown file first
4. Check the Confluence REST API documentation for reference