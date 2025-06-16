# Contributing to AnteaCore Client

Thank you for your interest in contributing to AnteaCore Client! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/anteacore-client.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/anteacore/anteacore-client.git
cd anteacore-client

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## What We're Looking For

### Welcome Contributions

- 🐛 Bug fixes
- 📝 Documentation improvements
- ✅ Test coverage improvements
- 🎨 UI/UX enhancements
- 🌐 Internationalization
- ♿ Accessibility improvements

### Please Discuss First

- 🏗️ Major architectural changes
- 🔧 New MCP tool additions
- 🔐 Security-related changes
- 📡 API endpoint modifications

## Code Standards

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and small
- Write tests for new features

## Testing

Before submitting:

```bash
# Run tests
pytest

# Check code style
black --check .

# Type checking
mypy anteacore_client
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Ensure all tests pass
3. Update the version number if appropriate
4. Reference any related issues
5. Request review from maintainers

## Security

If you find a security issue, please DO NOT open a public issue. Email security@anteacore.com instead.

## Questions?

Feel free to open an issue for discussion or clarification.

Thank you for contributing! 🙏