# Markdown to Confluence Converter & Publisher

Convert Markdown files to Confluence storage format and publish them directly to your Confluence space using the REST API.

## Features
- Converts Markdown to Confluence storage format
- Supports code blocks, math, tables, images, footnotes, and more
- Handles definition lists, strikethrough, and advanced Markdown features
- Publishes pages to Confluence via REST API
- CLI for batch conversion and publishing
- Test suite and example documentation included

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

## Usage

### Command Line
Convert and publish one or more Markdown files to Confluence:

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

- `--base-url`: Your Confluence base URL
- `--username`: Your Confluence username/email
- `--api-token`: Your Confluence API token (not password)
- `--space-key`: The Confluence space key
- `--parent-page`: (Optional) Title of the parent page
- `--page-title`: (Optional) Custom page title
- `--page-id`: (Optional) Specific Confluence page ID to update (if provided, will update existing page)
- `--enable-math`: (Optional) Enable math conversion (for LaTeX/math support)

### Example
```bash
python confluence_markdown_converter.py docs/example_comprehensive.md \
  --base-url https://your-domain.atlassian.net \
  --username you@example.com \
  --api-token <your-api-token> \
  --space-key DOCS
```

## Development & Testing
Run the test suite with:
```bash
python -m unittest discover tests
```

## Utility Scripts
All utility scripts are now located in the `scripts/` folder. To use them, run:
```bash
python scripts/<script_name>.py [options]
```
For example:
```bash
python scripts/adjust_headers.py input.md > output.md
python scripts/add_separators.py input.md > output.md
```

To use the provided Bash automation script:
```bash
bash scripts/convert_pva_docs.sh
```

## License
- This project is licensed under the [Apache License 2.0](LICENSE).

---

For more details, see the documentation in `docs/CONFLUENCE_CONVERTER_README.md`.