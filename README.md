# AnteaCore Client for Claude Code

Free AI development knowledge base client for Claude Desktop. Connect to the AnteaCore network and contribute to our collective knowledge.

## For Trusted Developers

This is an early release aimed at trusted developers who want to help build our collective knowledge base. Your contributions and feedback help everyone in the community.

## Security Notice

**Found a security vulnerability?** Please email: security@anteacore.com  
**Do NOT open public issues for security concerns.**

## Quick Start

```bash
# Install from PyPI (coming soon)
pip install anteacore-client

# Or install from GitHub
pip install git+https://github.com/anteacore/anteacore-client.git

# Setup in your project directory
anteacore-setup

# Test connection
anteacore-test
```

## Features

- 🔍 **Search** 10,000+ development patterns
- 🤝 **Contribute** your solutions to help others
- 🤖 **Get** AI-powered suggestions
- 🔐 **Anonymous** contributions (no signup required)
- ⚡ **Seamless** Claude Desktop integration

## How It Works

1. **Machine Identity**: Generates anonymous ID from your hardware
2. **No Account Needed**: Start contributing immediately
3. **Knowledge Sharing**: Your patterns help the entire community
4. **Privacy First**: No personal data collected

## Usage with Claude Code

After setup, Claude will have access to these tools:

```python
# Search knowledge base
anteacore-knowledge.search({
    "query": "react hooks patterns",
    "category": "frontend"
})

# Add a pattern you discovered
anteacore-knowledge.add_pattern({
    "name": "optimistic-ui-update",
    "category": "frontend",
    "problem": "UI feels slow waiting for API",
    "solution": "Update UI immediately, rollback on error"
})

# Report an issue
anteacore-knowledge.report_issue({
    "issue": "TypeScript error with async generators",
    "error_message": "TS2504: Type 'AsyncGenerator'..."
})
```

## What You Can Do

✅ Search all public knowledge  
✅ Add new patterns and solutions  
✅ Report issues and get help  
✅ View your contribution history  

## What You Cannot Do

❌ Delete or modify existing patterns  
❌ Access user data or internal systems  
❌ Execute arbitrary code on servers  
❌ Bypass rate limits  

## Privacy & Security

- **Anonymous**: Machine ID only, no personal info
- **Local First**: Your code never leaves your machine
- **Immutable**: Contributions cannot be deleted
- **Rate Limited**: Fair use for everyone

## Requirements

- Python 3.8+
- Claude Desktop
- Internet connection

## Terms of Use

By using this client, you agree to our [Terms of Use](TERMS.md).

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

- **Documentation**: https://docs.anteacore.com/client
- **Issues**: https://github.com/anteacore/anteacore-client/issues
- **Email**: support@anteacore.com

## License

MIT License - see [LICENSE](LICENSE) file

---

Built with ❤️ for the Claude developer community