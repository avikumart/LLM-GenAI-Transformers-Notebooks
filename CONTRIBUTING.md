# Contributing to LLM-GenAI-Transformers-Notebooks

Thank you for your interest in contributing to this repository! By contributing, you help create a valuable resource for the GenAI and LLM community. This guide will help you get started with contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Submitting Contributions](#submitting-contributions)
- [Documentation Style](#documentation-style)
- [Issue Reporting Guidelines](#issue-reporting-guidelines)
- [Review Process](#review-process)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

There are several ways you can contribute:

1. **Add New Notebooks**: Create tutorials, demonstrations, or projects that showcase LLM, GenAI, or transformer applications
2. **Improve Existing Content**: Enhance clarity, fix bugs, or update content in existing notebooks
3. **Add Educational Resources**: Contribute learning materials, articles, or course recommendations
4. **Documentation**: Improve documentation, READMEs, or add explanatory content
5. **Bug Fixes**: Fix issues in existing notebooks or code samples
6. **Tool Integration**: Add examples of new tools or libraries relevant to GenAI

## Setting Up the Development Environment

1. **Fork the Repository**

```bash
# Clone your fork locally
git clone https://github.com/avikumart/LLM-GenAI-Transformers-Notebooks.git
cd LLM-GenAI-Transformers-Notebooks

# Add the original repository as upstream
git remote add upstream https://github.com/avikumart/LLM-GenAI-Transformers-Notebooks.git
```

2. **Create a Virtual Environment**

```bash
# Using conda
conda create -n genai-notebooks python=3.10
conda activate genai-notebooks

# Or using venv
python -m venv genai-env
source genai-env/bin/activate  # On Windows: genai-env\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Create a New Branch**

```bash
git checkout -b feature/your-feature-name
```

## Submitting Contributions

1. **Make Your Changes**

2. **Test Your Changes**
   - Ensure all code runs without errors
   - Run all cells in your notebooks if contributing Jupyter notebooks

3. **Commit Your Changes**

```bash
git add .
git commit -m "Brief description of your changes"
```

4. **Push to Your Fork**

```bash
git push origin feature/your-feature-name
```

5. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "Pull Request"
   - Select your fork and branch
   - Fill in the PR template with details about your changes

### Documentation

- Include a header with title, author, date, and description
- Document functions and classes with docstrings
- Add explanatory markdown cells between code sections
- Include references to papers, articles, or other resources

## Documentation Style

- Use clear, concise language
- Include code examples where appropriate
- Use markdown formatting for headings, lists, code blocks, etc.
- Include diagrams or visualizations when they help explain concepts

Example markdown formatting:

```markdown
# Main Heading

## Subheading

### Sub-subheading

**Bold text** for emphasis

*Italic text* for definitions or emphasis

`inline code` for code snippets or variable names

```python
# Code block for longer code examples
def example_function():
    return "This is an example"
```

> Blockquote for important notes or quotes

- Bullet points for lists
- Another item

1. Numbered lists when sequence matters
2. Second item

[Link text](URL) for references
```

## Issue Reporting Guidelines

When reporting issues, please use the issue templates and include:

1. Issue description
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, package versions)
6. Screenshots or error logs if applicable

## Review Process

Pull requests will be reviewed by maintainers according to these criteria:

1. Code quality and adherence to guidelines
2. Correctness and accuracy of content
3. Value added to the repository
4. Documentation quality

Feedback may be provided, and changes may be requested before merging.

---

Thank you for contributing to LLM-GenAI-Transformers-Notebooks! Your efforts help build a better resource for everyone in the GenAI community.
