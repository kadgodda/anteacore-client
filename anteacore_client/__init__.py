"""
AnteaCore Client Package
MCP tools for Claude Code integration
"""

__version__ = "0.1.0"
__author__ = "AnteaCore"

from .client import AnteaCoreClient
from .mcp_wrapper import quick_mcp_call

__all__ = ["AnteaCoreClient", "quick_mcp_call"]