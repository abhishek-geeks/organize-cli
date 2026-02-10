# Contributing to Organize CLI

Thank you for your interest in contributing to Organize CLI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Report issues professionally

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/abhishek-geeks/organize-cli.git
cd organize-cli

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core.py -v

# Run with coverage report
pytest tests/ --cov=organize --cov-report=html
```

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep lines under 100 characters

### Project Structure

```
organize-cli/
├── organize/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command-line interface
│   ├── core.py              # Core organization logic
│   ├── filetypes.py         # File type definitions
│   └── restore.py           # Restore functionality
├── tests/
│   ├── __init__.py
│   ├── test_core.py         # Core functionality tests
│   ├── test_cli.py          # CLI tests
│   ├── test_restore.py      # Restore tests
│   └── test_edge_cases.py   # Edge case tests
├── pyproject.toml           # Project configuration
├── README.md                # User documentation
├── CHANGELOG.md             # Release notes
└── LICENSE                  # MIT License
```

## Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clean, well-documented code
- Add docstrings following Google style
- Test your changes locally

### 3. Write/Update Tests

- All new features must have tests
- All bug fixes must include a test that reproduces the issue
- Maintain or improve code coverage

### 4. Run Tests

```bash
# Ensure all tests pass
pytest tests/ -v

# Check code coverage
pytest tests/ --cov=organize
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Descriptive commit message"
```

Use clear, descriptive commit messages:
- ✓ "Fix: handle permission errors gracefully in safe_move"
- ✗ "Fix bug"

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues (#123)
- Screenshots/examples if applicable

## What to Contribute

### Great for Beginners
- [ ] Add support for additional file types
- [ ] Improve error messages
- [ ] Add more test cases
- [ ] Improve documentation

### Areas Needing Help
- [ ] Custom category configuration
- [ ] Performance optimizations
- [ ] Logging levels (--verbose, --quiet)
- [ ] Interactive mode
- [ ] Progress bar for large folders
- [ ] Parallel processing support

### Reporting Issues

When reporting bugs:
1. Use descriptive titles
2. Include Python version and OS
3. Provide minimal reproducible example
4. Attach relevant output/logs
5. Mention the expected vs actual behavior

### Feature Requests

For feature requests:
1. Describe the use case
2. Explain why it's useful
3. Provide examples if possible
4. Consider implementation approach

## Testing Guidelines

### Test Coverage

- Aim for 90%+ code coverage
- Test both happy paths and error cases
- Test edge cases (special characters, empty files, etc.)
- Test integration between components

### Example Test Structure

```python
def test_feature_specific_scenario(self):
    """Brief description of what's being tested"""
    # Arrange: Set up test data
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("test content unique")
        
        # Act: Perform the operation
        result = some_function(str(tmpdir))
        
        # Assert: Verify the result
        assert result == expected_value
```

## Documentation Guidelines

### Code Comments

- Explain "why", not "what"
- Keep comments up-to-date with code
- Use single-line comments for brief explanations

### Docstrings

Follow Google style docstrings:

```python
def organize(folder, dry_run=False):
    """
    Organize files in a folder by categorizing them.
    
    Args:
        folder (str): Path to the folder to organize
        dry_run (bool): If True, preview changes without making them
        
    Returns:
        None
        
    Raises:
        ValueError: If folder doesn't exist
        PermissionError: If folder cannot be accessed
    """
```

### README Updates

- Keep README accurate with current features
- Include examples of common use cases
- Document command-line options
- Add troubleshooting section if needed

## Release Process

Releases are managed by maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Merge to main branch
4. Tag release (e.g., `v1.0.1`)
5. PyPI package is auto-published

## Questions?

- Check [README.md](README.md) for usage
- Review existing issues and discussions
- Create a new discussion for questions

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

Thank you for contributing! 🎉
