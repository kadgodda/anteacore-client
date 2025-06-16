#!/usr/bin/env python3
"""
AnteaCore Client Installer
One-line installation script for users
"""

import subprocess
import sys
import os
import tempfile
import urllib.request
import json
from pathlib import Path

PACKAGE_URL = "https://github.com/anteacore/anteacore-client/archive/main.zip"
API_URL = "https://api.anteacore.com"

def install():
    """Install AnteaCore client package."""
    print("🚀 Installing AnteaCore Client for Claude Code")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        sys.exit(1)
    
    # Install package
    print("\n📦 Installing package...")
    try:
        # For production, this would install from your private PyPI
        # For now, using GitHub
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "git+https://github.com/anteacore/anteacore-client.git",
            "--upgrade"
        ])
        print("✅ Package installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install package")
        sys.exit(1)
    
    # Run setup
    print("\n⚙️  Running setup...")
    try:
        subprocess.check_call([sys.executable, "-m", "anteacore_client.setup"])
    except subprocess.CalledProcessError:
        print("❌ Setup failed")
        sys.exit(1)
    
    print("\n✅ Installation complete!")
    print("\n📚 Next steps:")
    print("1. Restart Claude Desktop")
    print("2. Run: anteacore-test")
    print("\nHappy coding with AnteaCore! 🎉")

if __name__ == "__main__":
    install()