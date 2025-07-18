# Markdown to Confluence & Jira Converter

Convert Markdown files to Confluence storage format and Jira markup, then publish them directly to your Atlassian tools using REST APIs.

## Features

### Confluence Converter
- ✅ Converts Markdown to Confluence storage format
- ✅ Supports code blocks, math, tables, images, footnotes, and more
- ✅ Handles definition lists, strikethrough, and advanced Markdown features
- ✅ Publishes pages to Confluence via REST API
- ✅ CLI for batch conversion and publishing

### Jira Converter
- ✅ Converts Markdown to Jira markup format
- ✅ Creates new issues or updates existing ones
- ✅ Adds content as comments to existing issues
- ✅ Supports parent-child relationships
- ✅ Handles code blocks, tables, links, and formatting
- ✅ Automatic header spacing and UTF-8 encoding
- ✅ Robust error handling with HTTP status codes

### Shared Features
- ✅ Configuration management with secure credential storage
- ✅ Test suite and comprehensive documentation
- ✅ Utility scripts for preprocessing markdown files
- ✅ Modern Python architecture with dataclasses and type hints

## Requirements
- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [markdown](https://pypi.org/project/Markdown/)
- [python-frontmatter](https://pypi.org/project/python-frontmatter/)
- [mdx-math](https://pypi.org/project/mdx-math/) (for math support)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Setup Configuration

**For Confluence:**
```bash
python confluence_config.py --setup
```

**For Jira:**
```bash
python jira_config.py --setup
```

### 2. Generate Local Scripts

**For Confluence:**
```bash
python confluence_config.py --generate-script
```

**For Jira:**
```bash
python jira_config.py --generate-script
```

### 3. Run Conversions

**Confluence:**
```bash
./convert_confluence.sh
```

**Jira:**
```bash
./convert_jira.sh
```

## Usage

### Confluence Converter

```bash
python confluence_markdown_converter.py <file1.md> <file2.md> \
  --base-url https://your-domain.atlassian.net \
  --username your-email@example.com \
  --api-token your-confluence-api-token \
  --space-key YOURSPACEKEY \
  [--parent-page "Parent Page Title"] \
  [--page-title "Custom Page Title"] \
  [--page-id "Confluence Page ID"] \
  [--enable-math]
```

### Jira Converter

```bash
python jira_markdown_converter.py <file1.md> <file2.md> \
  --base-url https://your-domain.atlassian.net \
  --username your-email@example.com \
  --api-token your-jira-api-token \
  --project-key PROJ \
  [--issue-type "Task"] \
  [--priority "Medium"] \
  [--assignee "username"] \
  [--time-estimate "2h"] \
  [--parent-key "PROJ-123"] \
  [--issue-key "PROJ-123"] \
  [--as-comment]
```

## Recent Improvements

### 🚀 **Jira Support**
- Full Jira markup conversion with proper formatting
- Issue creation, updates, and comment support
- Parent-child relationship handling
- Automatic time estimate parsing from markdown

### 🔧 **Code Quality**
- **CommandLine dataclass** for clean CLI argument handling
- **HTTP status code constants** using `http.HTTPStatus` library
- **Shared response handler** with proper UTF-8 encoding
- **Robust error handling** for JSON decode errors

### 📝 **Markdown Processing**
- **Automatic header spacing** for better Jira readability
- **Enhanced code block support** with syntax highlighting
- **Improved table conversion** for both Confluence and Jira
- **Better list handling** and formatting

### 🛡️ **Security & Configuration**
- **Input folder ignored** by Git for privacy
- **Secure credential storage** in configuration files
- **Environment-based configuration** support
- **Comprehensive API documentation** with limitations noted

## Development & Testing

Run the test suite:
```bash
python -m unittest discover tests
```

Test API connections:
```bash
python tests/test_jira_connection.py
python tests/test_confluence_connection.py
```

## Input Directory Structure

Create the following directory structure for your markdown files:
```
input/
├── confluence/
│   └── your_file.md
└── jira/
    └── your_file.md
```

⚠️ **Note**: The `input/` directory is ignored by Git for privacy and security.

## Tool Overview

### Confluence Converter
- **Purpose**: Convert Markdown to Confluence pages
- **Features**: Page creation/updates, hierarchical structure, code blocks, tables, links
- **Use Cases**: Documentation, project wikis, knowledge bases
- **📖 [Detailed Documentation](docs/CONFLUENCE_CONVERTER_README.md)**

### Jira Converter
- **Purpose**: Convert Markdown to Jira issues and comments
- **Features**: Issue creation/updates, comments, parent-child relationships, code blocks
- **Use Cases**: Bug reports, feature requests, technical specifications
- **📖 [Detailed Documentation](docs/JIRA_CONVERTER_README.md)**
- **📖 [API Documentation](docs/JIRA_API_DOCUMENTATION.md)**

## Utility Scripts

All utility scripts are located in the `scripts/` folder:

```bash
# Add header levels to markdown files
python scripts/add_header_level.py input.md > output.md

# Add separators between sections
python scripts/add_separators.py input.md > output.md

# Adjust header levels
python scripts/adjust_headers.py input.md > output.md
```

## Limitations

### Jira Converter
- **Nested lists**: Currently supports only flat (single-level) lists
- **Time tracking**: Must be set manually in Jira web interface (API limitation)
- **Field permissions**: Some fields may be restricted based on Jira configuration

### Confluence Converter
- **Math support**: Requires `--enable-math` flag for LaTeX rendering
- **Image handling**: Images must be accessible via URL or uploaded separately

## License
This project is licensed under the [Apache License 2.0](LICENSE).

---

## Documentation

- **📖 [Confluence Converter Guide](docs/CONFLUENCE_CONVERTER_README.md)** - Complete setup and usage guide
- **📖 [Jira Converter Guide](docs/JIRA_CONVERTER_README.md)** - Complete setup and usage guide
- **📖 [Jira API Documentation](docs/JIRA_API_DOCUMENTATION.md)** - API capabilities and limitations
- **📖 [Configuration Testing Guide](docs/CONFIG_TESTER_README.md)** - Test your API connections