# Confluence Configuration Tester

This directory contains tools for testing and setting up your Confluence markdown converter configuration.

## Files

- `tests/test_confluence_config.py` - Comprehensive configuration testing tool
- `confluence_config.py` - Configuration setup and management tool
- `CONFIG_TESTER_README.md` - This documentation file

## Quick Start

### 1. Test Your Current Configuration

```bash
# Run the comprehensive config tester (directly)
python tests/test_confluence_config.py

# Or with verbose output
python tests/test_confluence_config.py --verbose

# Or as part of the test suite
pytest tests/test_confluence_config.py
```

### 2. Set Up Configuration (if needed)

```bash
# Run interactive setup
python confluence_config.py --setup
```

### 3. Verify Configuration

```bash
# Show current configuration
python confluence_config.py --show

# Test configuration
python confluence_config.py --test
```

## Configuration Tester Features

The `test_confluence_config.py` performs the following tests:

### ✅ Configuration Tests
- **Config File Exists** - Checks for configuration files
- **Config Structure** - Validates configuration format
- **Required Fields** - Ensures all required fields are present

### 🌐 Network Tests
- **URL Format** - Validates Confluence URL format
- **Network Connectivity** - Tests basic connectivity to Confluence

### 🔐 Authentication Tests
- **API Authentication** - Tests credentials with Confluence API
- **Space Access** - Verifies access to specified space
- **API Endpoints** - Tests basic API functionality

### 🛠️ Integration Tests
- **Converter Initialization** - Tests ConfluenceMarkdownConverter setup

## Test Results

The tester provides clear status indicators:

- ✅ **PASS** - Test completed successfully
- ❌ **FAIL** - Test failed (needs attention)
- ⚠️ **WARNING** - Test completed with warnings
- ⏭️ **SKIP** - Test skipped (usually due to missing prerequisites)

## Example Output

```
🔧 Confluence Configuration Tester
==================================================
✅ Config File Exists: Found configuration file: confluence_config.json
✅ Config Structure: Found valid JSON configuration file
✅ Required Fields: All required fields present
✅ URL Format: Valid URL format: https://your-domain.atlassian.net
✅ Network Connectivity: Successfully connected to https://your-domain.atlassian.net (Status: 200)
✅ API Authentication: Authentication successful for user: John Doe
✅ Space Access: Successfully accessed space: Team Documentation
✅ API Endpoints: Content API endpoint accessible
✅ Converter Initialization: ConfluenceMarkdownConverter initialized successfully

==================================================
📊 Test Summary
==================================================
✅ Passed: 9
❌ Failed: 0
⚠️  Warnings: 0
⏭️  Skipped: 0
📈 Total: 9

💡 Recommendations:
• All tests passed! Your configuration is ready to use.
```

## Configuration Setup

The `confluence_config.py` provides an interactive setup process:

### What You'll Need

1. **Confluence Base URL**
   - Example: `https://your-domain.atlassian.net`
   - Example: `https://your-company.atlassian.net`

2. **Username/Email**
   - Your Confluence username or email address

3. **API Token** (NOT your password!)
   - Create at: https://id.atlassian.com/manage-profile/security/api-tokens
   - Give it a descriptive name (e.g., "Markdown Converter")

4. **Space Key**
   - Short identifier for your Confluence space
   - Examples: `TEAM`, `DOCS`, `PROJECT`
   - Found in Confluence URL or space settings

### Setup Process

```bash
python confluence_config.py --setup
```

The setup will:
1. Prompt for each required field
2. Validate input format
3. Save configuration to `confluence_config.json`
4. Provide security recommendations
5. Show next steps

## Security Notes

- Configuration files contain sensitive API tokens
- The `confluence_config.json` file is automatically added to `.gitignore`
- Never commit configuration files to version control
- Keep your API token secure and rotate it periodically

## Troubleshooting

### Common Issues

1. **"No configuration file found"**
   - Run setup: `python confluence_config.py --setup`

2. **"Authentication failed"**
   - Verify your API token is correct
   - Ensure you're using an API token, not your password
   - Check that your username/email is correct

3. **"Space not found"**
   - Verify your space key is correct
   - Ensure you have access to the space
   - Check space permissions

4. **"Network connectivity failed"**
   - Check your internet connection
   - Verify the Confluence URL is correct
   - Check if Confluence is accessible from your network

### Debug Mode

For detailed debugging, use the verbose flag:

```bash
python tests/test_confluence_config.py --verbose
```

This will show additional details about each test step.

## Integration with CI/CD

You can integrate the config tester into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Test Confluence Configuration
  run: |
    python tests/test_confluence_config.py
  env:
    CONFLUENCE_BASE_URL: ${{ secrets.CONFLUENCE_BASE_URL }}
    CONFLUENCE_USERNAME: ${{ secrets.CONFLUENCE_USERNAME }}
    CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
    CONFLUENCE_SPACE_KEY: ${{ secrets.CONFLUENCE_SPACE_KEY }}
```

## Exit Codes

The config tester uses the following exit codes:

- `0` - All tests passed or only warnings
- `1` - One or more tests failed
- `2` - All tests skipped (no configuration)

This allows for easy integration with automated systems and scripts.

## Next Steps

After successful configuration:

1. **Test with a simple file:**
   ```bash
   python confluence_markdown_converter.py README.md
   ```

2. **Convert your documentation:**
   ```bash
   python convert_arganteal_docs.py
   ```

3. **Run the full test suite:**
   ```bash
   python -m pytest tests/
   ```