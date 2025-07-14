# Comprehensive Markdown Example

This is a comprehensive example markdown file that demonstrates all the features that can be converted to Confluence format.

## Table of Contents

- [Headers](#headers)
- [Text Formatting](#text-formatting)
- [Lists](#lists)
- [Code Blocks](#code-blocks)
- [Tables](#tables)
- [Links and Images](#links-and-images)
- [Blockquotes](#blockquotes)
- [Horizontal Rules](#horizontal-rules)
- [Task Lists](#task-lists)
- [Mathematical Expressions](#mathematical-expressions)

---

## Headers

### Level 3 Header
#### Level 4 Header
##### Level 5 Header
###### Level 6 Header

## Text Formatting

This paragraph contains **bold text**, *italic text*, and ***bold italic text***.

You can also use `inline code` within text.

Here's some ~~strikethrough text~~ for demonstration.

### Emphasis Examples

- **Bold text** using `**text**`
- *Italic text* using `*text*`
- ***Bold italic*** using `***text***`
- `Code` using backticks

## Lists

### Unordered Lists

- First item
- Second item
  - Nested item
  - Another nested item
- Third item
  - Deeply nested
    - Even deeper
      - Very deep indeed

### Ordered Lists

1. First numbered item
2. Second numbered item
   1. Nested numbered item
   2. Another nested item
3. Third numbered item

### Mixed Lists

1. Numbered item
   - Bullet point under numbered
   - Another bullet
2. Another numbered item
   - More bullets
     1. Numbered under bullet
     2. Another numbered

## Code Blocks

### Basic Code Block

```
This is a basic code block
with multiple lines
and no syntax highlighting
```

### Syntax Highlighted Code

```python
def hello_world():
    """A simple function that prints hello world"""
    print("Hello, World!")
    return "Hello, World!"

# This is a comment
class ExampleClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"
```

```javascript
// JavaScript example
function calculateSum(a, b) {
    return a + b;
}

const result = calculateSum(5, 3);
console.log(`The sum is: ${result}`);

// Arrow function example
const multiply = (x, y) => x * y;
```

```bash
#!/bin/bash
# Shell script example
echo "Starting deployment..."

# Check if directory exists
if [ -d "/var/www" ]; then
    echo "Directory exists"
    cd /var/www
    git pull origin main
else
    echo "Directory not found"
    exit 1
fi
```

### Inline Code Examples

Use `git status` to check the current state of your repository.

The `config.json` file contains your application settings.

## Tables

### Basic Table

| Name | Age | City | Occupation |
|------|-----|------|------------|
| John Doe | 30 | New York | Developer |
| Jane Smith | 25 | Los Angeles | Designer |
| Bob Johnson | 35 | Chicago | Manager |

### Table with Alignment

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| This is left | This is center | This is right |
| More left | More center | More right |
| Even more left | Even more center | Even more right |

### Complex Table

| Feature | Markdown | Confluence | Status |
|---------|----------|------------|--------|
| Headers | `# ## ###` | `<h1> <h2> <h3>` | ✅ Supported |
| Bold | `**text**` | `<strong>text</strong>` | ✅ Supported |
| Italic | `*text*` | `<em>text</em>` | ✅ Supported |
| Code | `` `code` `` | `<code>code</code>` | ✅ Supported |
| Links | `[text](url)` | `<a href="url">text</a>` | ✅ Supported |
| Images | `![alt](url)` | `<img src="url" alt="alt">` | ⚠️ Limited |

## Links and Images

### External Links

- [Google](https://www.google.com)
- [GitHub](https://github.com)
- [Stack Overflow](https://stackoverflow.com)

### Internal Links

- [Headers Section](#headers)
- [Code Blocks](#code-blocks)
- [Tables](#tables)

### Images

![Markdown Logo](https://markdown-here.com/img/icon256.png)

![GitHub Octocat](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)

### Links with Titles

[Visit our documentation](https://docs.example.com "Official Documentation")

## Blockquotes

> This is a simple blockquote.
> It can span multiple lines.

> **Important Note:** This is a blockquote with formatting.
> 
> It can contain:
> - Lists
> - **Bold text**
> - `Code snippets`

> > This is a nested blockquote
> > 
> > It demonstrates how blockquotes can be nested within each other.

## Horizontal Rules

You can create horizontal rules using three or more dashes, asterisks, or underscores:

---

***

___

## Task Lists

- [x] Create markdown file
- [x] Add comprehensive examples
- [ ] Test conversion to Confluence
- [ ] Verify all formatting works
- [ ] Document any issues
- [ ] Create user guide

### Nested Task Lists

- [x] Main task
  - [x] Sub-task 1
  - [ ] Sub-task 2
    - [ ] Sub-sub-task A
    - [x] Sub-sub-task B
  - [x] Sub-task 3

## Mathematical Expressions

### Inline Math

The quadratic formula is: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

### Block Math

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

$$
\begin{align}
y &= mx + b \\
&= 2x + 3
\end{align}
$$

## Special Characters

### Escaping Characters

- Use `\*` to display an asterisk: \*
- Use `\` to display a backtick: \`
- Use `\[` to display a bracket: \[
- Use `\(` to display a parenthesis: \(

### HTML Entities

- &amp; for &
- &lt; for <
- &gt; for >
- &quot; for "
- &apos; for '

## Definition Lists

Term 1
: Definition 1

Term 2
: Definition 2
: Another definition for term 2

## Footnotes

Here's a sentence with a footnote[^1].

And another sentence with a different footnote[^2].

[^1]: This is the first footnote.
[^2]: This is the second footnote with **bold text** and `code`.

## Abbreviations

*[HTML]: HyperText Markup Language
*[CSS]: Cascading Style Sheets
*[JS]: JavaScript

The HTML specification is maintained by the W3C.

## Strikethrough and Underline

~~This text is strikethrough~~

<u>This text is underlined</u>

## Subscript and Superscript

H<sub>2</sub>O is water.

E = mc<sup>2</sup> is Einstein's famous equation.

## Keyboard Input

Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to copy.

Use <kbd>F1</kbd> for help.

## Conclusion

This comprehensive markdown file demonstrates all the major features that can be converted to Confluence format. The converter should handle:

- ✅ All header levels (H1-H6)
- ✅ Text formatting (bold, italic, code)
- ✅ Ordered and unordered lists
- ✅ Nested lists
- ✅ Code blocks with syntax highlighting
- ✅ Tables with alignment
- ✅ Links and images
- ✅ Blockquotes
- ✅ Horizontal rules
- ✅ Task lists
- ✅ Mathematical expressions
- ✅ Special characters
- ✅ And more!

---

*This document was created to test the Markdown to Confluence converter functionality.* 