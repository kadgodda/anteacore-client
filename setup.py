"""
AnteaCore Client Package - MCP Tools for Claude Code
"""

from setuptools import setup, find_packages

setup(
    name="anteacore-client",
    version="0.1.0",
    author="AnteaCore",
    author_email="support@anteacore.com",
    description="MCP tools for Claude Code integration with AnteaCore network",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anteacore/anteacore-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
        "mcp>=0.1.0",
        "asyncio",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "anteacore-setup=anteacore_client.setup:main",
            "anteacore-test=anteacore_client.test:main",
        ],
    },
    include_package_data=True,
    package_data={
        "anteacore_client": ["templates/*", "mcp_servers/*"],
    },
)