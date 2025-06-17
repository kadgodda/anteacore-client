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
pip install git+https://github.com/kadgodda/anteacore-client.git

# Setup in your project directory
anteacore-setup

# Test connection
anteacore-test
```

## Features

- 🔍 **Search** 10,000+ development patterns
- 🤝 **Contribute** your solutions to help others
- 🤖 **Get** AI-powered suggestions
- 🔐 **Truly Anonymous** contributions with privacy-first design
- ⚡ **Seamless** Claude Desktop integration
- 🎭 **Fun Display Names** like "Swift Fox" or "Wise Owl"
- 🔄 **Session-Based** temporary identifiers (24-hour expiration)

## How It Works

1. **Anonymous Sessions**: Temporary session IDs that expire after 24 hours
2. **No Tracking**: No hardware fingerprinting or persistent identification
3. **Knowledge Sharing**: Your patterns help the entire community
4. **Privacy by Design**: No personal or hardware data ever collected
5. **User Control**: Clear your session anytime with `anteacore-clear`

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

## Privacy & Security

### Your Privacy Matters
- **No Hardware Tracking**: We don't collect MAC addresses, CPU info, or any hardware identifiers
- **Anonymous Sessions**: Temporary IDs that expire after 24 hours
- **No Personal Data**: We never ask for or store personal information
- **User Control**: Clear your session anytime with `python -m anteacore_client.anonymous_identity --clear`

### Security Features
- **Read-Only by Default**: Most operations are read-only
- **Rate Limiting**: Prevents abuse while maintaining anonymity
- **Content Validation**: All contributions are validated before acceptance
- **No Persistent Storage**: Nothing stored between sessions unless you explicitly save it

### Transparency
- **Open Source**: Review our code to verify our privacy claims
- **No Hidden Tracking**: What you see is what you get
- **GDPR/CCPA Compliant**: Privacy by design

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