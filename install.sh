#!/bin/bash
# AnteaCore Client Quick Install Script
# Usage: curl -sSL https://anteacore.com/install | bash

set -e

echo "🚀 AnteaCore Client Installer"
echo "============================"
echo

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_TYPE=Linux;;
    Darwin*)    OS_TYPE=Mac;;
    CYGWIN*)    OS_TYPE=Windows;;
    MINGW*)     OS_TYPE=Windows;;
    *)          OS_TYPE="UNKNOWN:${OS}"
esac

echo "📍 Detected OS: ${OS_TYPE}"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Python version: ${PYTHON_VERSION}"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "${TEMP_DIR}"

# Download installer
echo
echo "📥 Downloading AnteaCore client..."
curl -sSL https://raw.githubusercontent.com/anteacore/anteacore-client/main/install.py -o install.py

# Run installer
echo
echo "📦 Installing..."
python3 install.py

# Cleanup
cd - > /dev/null
rm -rf "${TEMP_DIR}"

echo
echo "✨ Installation complete!"
echo
echo "📚 Documentation: https://docs.anteacore.com/client"
echo "💬 Support: support@anteacore.com"