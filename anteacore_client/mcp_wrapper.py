"""
MCP Wrapper for AnteaCore Client
Provides the quick_mcp_call function for easy tool usage
"""

import subprocess
import json
import sys
from typing import Dict, Any

def quick_mcp_call(server: str, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call an AnteaCore MCP tool.
    
    This is a simplified version that works within the client package.
    In Claude Desktop, the actual MCP servers handle these calls.
    """
    # This is a placeholder that demonstrates the interface
    # In reality, Claude Desktop handles MCP communication
    
    if server == "anteacore-knowledge":
        # Import and use the client directly
        from .client import AnteaCoreClient
        
        client = AnteaCoreClient()
        
        if tool == "search":
            return client.search_knowledge(**params)
        elif tool == "add_pattern":
            return client.add_pattern(**params)
        elif tool == "get_suggestions":
            return client.get_suggestions(**params)
        elif tool == "report_issue":
            return client.report_issue(**params)
        else:
            return {"error": f"Unknown tool: {tool}"}
    
    return {"error": f"Unknown server: {server}"}

# For backward compatibility
def call_mcp_tool(server: str, tool: str, params: Dict[str, Any]) -> tuple[bool, Dict[str, Any]]:
    """Legacy function for compatibility."""
    result = quick_mcp_call(server, tool, params)
    success = "error" not in result
    return success, result