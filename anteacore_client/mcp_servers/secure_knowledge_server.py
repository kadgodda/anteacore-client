#!/usr/bin/env python3
"""
Secure AnteaCore Knowledge MCP Server for Clients
Restricted functionality with built-in security
"""

import asyncio
import json
import os
import hashlib
import platform
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

class SecureKnowledgeServer:
    """Secure MCP server for client knowledge base access."""
    
    # Strictly define allowed tools
    ALLOWED_TOOLS = {
        "search_knowledge",
        "add_pattern", 
        "report_issue",
        "get_suggestions",
        "validate_pattern",
        "get_my_contributions"
    }
    
    def __init__(self):
        self.server = Server("anteacore-knowledge")
        self.api_url = os.getenv("ANTEACORE_API_URL", "https://api.anteacore.com")
        self.project_dir = os.getenv("ANTEACORE_PROJECT_DIR", os.getcwd())
        self.version = "0.1.0"
        self.machine_id = self._load_machine_id()
        self.client = httpx.AsyncClient(
            headers={
                "X-Machine-ID": self.machine_id,
                "X-Client-Version": self.version,
                "User-Agent": f"AnteaCore-Client/{self.version}"
            },
            timeout=30.0
        )
        self._setup_allowed_tools_only()
    
    def _load_machine_id(self) -> str:
        """Load machine ID from identity file."""
        identity_file = Path.home() / ".anteacore" / "identity.json"
        
        if not identity_file.exists():
            raise RuntimeError("Machine identity not found. Run: anteacore-setup")
        
        with open(identity_file, 'r') as f:
            identity = json.load(f)
        
        return identity['machine_id']
    
    def _setup_allowed_tools_only(self):
        """Setup only allowed tools for clients."""
        tools = [
            Tool(
                name="search_knowledge",
                description="Search AnteaCore knowledge base (read-only)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "minLength": 3},
                        "category": {"type": "string"},
                        "language": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50}
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="add_pattern",
                description="Contribute a new pattern (cannot update/delete)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "minLength": 5},
                        "category": {"type": "string", "minLength": 3},
                        "problem": {"type": "string", "minLength": 20},
                        "solution": {"type": "string", "minLength": 30},
                        "code_example": {"type": "string"},
                        "language": {"type": "string"},
                        "tags": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["name", "category", "problem", "solution"]
                }
            ),
            Tool(
                name="report_issue",
                description="Report an issue to get help",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue": {"type": "string", "minLength": 10},
                        "error_message": {"type": "string"},
                        "context": {"type": "string"}
                    },
                    "required": ["issue"]
                }
            ),
            Tool(
                name="get_suggestions",
                description="Get pattern suggestions for current context",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "context": {"type": "string", "minLength": 10},
                        "file_type": {"type": "string"},
                        "language": {"type": "string"}
                    },
                    "required": ["context"]
                }
            ),
            Tool(
                name="validate_pattern",
                description="Check if pattern exists before adding",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pattern_description": {"type": "string", "minLength": 10},
                        "category": {"type": "string"}
                    },
                    "required": ["pattern_description"]
                }
            ),
            Tool(
                name="get_my_contributions",
                description="View your contribution history",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "minimum": 1, "maximum": 100}
                    }
                }
            )
        ]
        
        for tool in tools:
            self.server.add_tool(tool)
    
    def _validate_content(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate content for security and quality."""
        # Basic validation - detailed patterns on server side
        
        # Note: Real validation happens server-side
        # This is just basic client-side filtering
        
        # Basic length validation
        for field, value in data.items():
            if isinstance(value, str):
                # Check minimum content quality
                if field in ['problem', 'solution'] and len(value.strip()) < 20:
                    return False, f"{field} is too short or low quality"
                
                # Very basic checks - server does comprehensive validation
                if len(value) > 10000:  # Prevent huge payloads
                    return False, f"{field} is too long"
        
        # Ensure no null/empty values for required fields
        required_fields = ['name', 'category', 'problem', 'solution']
        for field in required_fields:
            if field in data:
                value = data[field]
                if not value or (isinstance(value, str) and not value.strip()):
                    return False, f"{field} cannot be empty"
        
        return True, None
    
    def _get_ip_hash(self) -> str:
        """Get hashed IP for rate limiting (privacy-preserving)."""
        # In production, this would get the actual IP from the request
        # For now, use machine ID + date for rate limiting
        today = datetime.utcnow().strftime("%Y-%m-%d")
        return hashlib.sha256(f"{self.machine_id}{today}".encode()).hexdigest()[:16]
    
    async def handle_search_knowledge(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search knowledge base (read-only)."""
        try:
            # Limit results to prevent abuse
            args['limit'] = min(args.get('limit', 10), 50)
            
            response = await self.client.post(
                f"{self.api_url}/api/client/knowledge/search",
                json=args
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Search failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Search error: {str(e)}"}
    
    async def handle_add_pattern(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add new pattern with security validation."""
        try:
            # Validate content
            is_valid, error_msg = self._validate_content(args)
            if not is_valid:
                return {
                    "error": error_msg,
                    "code": "VALIDATION_ERROR"
                }
            
            # Add metadata
            pattern_data = {
                **args,
                "machine_id": self.machine_id,
                "client_version": self.version,
                "ip_hash": self._get_ip_hash(),
                "project_context": {
                    "directory": os.path.basename(self.project_dir),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            response = await self.client.post(
                f"{self.api_url}/api/client/knowledge/patterns",
                json=pattern_data
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "success": True,
                    "pattern_id": result.get("pattern_id"),
                    "message": "Pattern submitted successfully",
                    "status": result.get("status", "pending_review")
                }
            elif response.status_code == 429:
                return {
                    "error": "Rate limit exceeded. Please try again later.",
                    "code": "RATE_LIMIT"
                }
            else:
                return {
                    "error": f"Failed to add pattern: {response.status_code}",
                    "code": "API_ERROR"
                }
                
        except Exception as e:
            return {"error": f"Error adding pattern: {str(e)}"}
    
    async def handle_report_issue(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Report issue (create only, no updates)."""
        try:
            # Basic validation
            if len(args.get('issue', '').strip()) < 10:
                return {"error": "Issue description too short"}
            
            issue_data = {
                **args,
                "machine_id": self.machine_id,
                "reported_at": datetime.utcnow().isoformat()
            }
            
            response = await self.client.post(
                f"{self.api_url}/api/client/issues",
                json=issue_data
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return {"error": f"Failed to report issue: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error reporting issue: {str(e)}"}
    
    async def handle_get_my_contributions(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get user's own contributions."""
        try:
            limit = min(args.get('limit', 10), 100)
            
            response = await self.client.get(
                f"{self.api_url}/api/client/contributions",
                params={"limit": limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to get contributions"}
                
        except Exception as e:
            return {"error": f"Error getting contributions: {str(e)}"}
    
    async def run(self):
        """Run the secure MCP server."""
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle only allowed tool calls."""
            
            # Security: Strict tool whitelist
            if name not in self.ALLOWED_TOOLS:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Tool '{name}' is not allowed for client access",
                        "allowed_tools": list(self.ALLOWED_TOOLS)
                    }, indent=2)
                )]
            
            try:
                if name == "search_knowledge":
                    result = await self.handle_search_knowledge(arguments)
                elif name == "add_pattern":
                    result = await self.handle_add_pattern(arguments)
                elif name == "report_issue":
                    result = await self.handle_report_issue(arguments)
                elif name == "get_suggestions":
                    # Simplified for security
                    result = await self.handle_search_knowledge({
                        "query": arguments.get("context", ""),
                        "limit": 5
                    })
                elif name == "validate_pattern":
                    # Check if similar exists
                    result = await self.handle_search_knowledge({
                        "query": arguments.get("pattern_description", ""),
                        "limit": 3
                    })
                elif name == "get_my_contributions":
                    result = await self.handle_get_my_contributions(arguments)
                else:
                    result = {"error": f"Tool '{name}' not implemented"}
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Tool execution failed: {str(e)}",
                        "tool": name
                    }, indent=2)
                )]
        
        await self.server.run()

if __name__ == "__main__":
    server = SecureKnowledgeServer()
    asyncio.run(server.run())