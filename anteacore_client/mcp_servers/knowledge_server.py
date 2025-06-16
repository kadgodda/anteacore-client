#!/usr/bin/env python3
"""
AnteaCore Knowledge MCP Server
Provides read/write access to AnteaCore knowledge base
"""

import asyncio
import json
import os
from typing import Dict, Any, List
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

class AnteaCoreKnowledgeServer:
    """MCP server for AnteaCore knowledge base access."""
    
    def __init__(self):
        self.server = Server("anteacore-knowledge")
        self.api_key = os.getenv("ANTEACORE_API_KEY")
        self.api_url = os.getenv("ANTEACORE_API_URL", "https://api.anteacore.com")
        self.project_dir = os.getenv("ANTEACORE_PROJECT_DIR", os.getcwd())
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30.0
        )
        self.setup_tools()
    
    def setup_tools(self):
        """Define available tools."""
        tools = [
            Tool(
                name="search",
                description="Search AnteaCore knowledge base for patterns and solutions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "category": {
                            "type": "string",
                            "enum": ["pattern", "solution", "troubleshooting", "architecture", "any"],
                            "default": "any"
                        },
                        "language": {"type": "string", "description": "Programming language filter"},
                        "limit": {"type": "integer", "default": 10}
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="add_pattern",
                description="Contribute a development pattern to the knowledge base",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Pattern name"},
                        "category": {"type": "string", "description": "Category (e.g., frontend, backend, database)"},
                        "problem": {"type": "string", "description": "Problem this pattern solves"},
                        "solution": {"type": "string", "description": "Solution description"},
                        "code_example": {"type": "string", "description": "Code example (optional)"},
                        "language": {"type": "string", "description": "Programming language"},
                        "tags": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["name", "category", "problem", "solution"]
                }
            ),
            Tool(
                name="get_suggestions",
                description="Get relevant patterns based on current context",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "context": {"type": "string", "description": "Current development context"},
                        "file_type": {"type": "string", "description": "Type of file being worked on"},
                        "language": {"type": "string", "description": "Programming language"},
                        "frameworks": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["context"]
                }
            ),
            Tool(
                name="report_issue",
                description="Report an issue and get solutions from knowledge base",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue": {"type": "string", "description": "Issue description"},
                        "error_message": {"type": "string", "description": "Error message if any"},
                        "context": {"type": "string", "description": "Code context"},
                        "attempted_solutions": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["issue"]
                }
            ),
            Tool(
                name="validate_pattern",
                description="Check if a pattern already exists or get similar ones",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pattern_description": {"type": "string"},
                        "category": {"type": "string"}
                    },
                    "required": ["pattern_description"]
                }
            )
        ]
        
        for tool in tools:
            self.server.add_tool(tool)
    
    async def handle_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search knowledge base."""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/client/knowledge/search",
                json=args
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Search failed: {response.text}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_add_pattern(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new pattern to knowledge base."""
        try:
            # Add metadata
            args["source"] = "client_contribution"
            args["project_context"] = {
                "directory": self.project_dir,
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.client.post(
                f"{self.api_url}/api/client/knowledge/patterns",
                json=args
            )
            
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message": "Pattern added successfully",
                    "pattern_id": response.json().get("id")
                }
            else:
                return {"error": f"Failed to add pattern: {response.text}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_get_suggestions(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get pattern suggestions based on context."""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/client/knowledge/suggest",
                json=args
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get suggestions: {response.text}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_report_issue(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Report an issue and get solutions."""
        try:
            # First search for existing solutions
            search_response = await self.client.post(
                f"{self.api_url}/api/client/knowledge/search",
                json={
                    "query": args["issue"],
                    "category": "troubleshooting",
                    "limit": 5
                }
            )
            
            solutions = []
            if search_response.status_code == 200:
                solutions = search_response.json().get("results", [])
            
            # Log the issue for analysis
            await self.client.post(
                f"{self.api_url}/api/client/issues",
                json={
                    **args,
                    "found_solutions": len(solutions)
                }
            )
            
            return {
                "existing_solutions": solutions,
                "message": "Issue reported. Check existing solutions above."
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_validate_pattern(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if pattern exists."""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/client/knowledge/validate",
                json=args
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Validation failed: {response.text}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def run(self):
        """Run the MCP server."""
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "search":
                    result = await self.handle_search(arguments)
                elif name == "add_pattern":
                    result = await self.handle_add_pattern(arguments)
                elif name == "get_suggestions":
                    result = await self.handle_get_suggestions(arguments)
                elif name == "report_issue":
                    result = await self.handle_report_issue(arguments)
                elif name == "validate_pattern":
                    result = await self.handle_validate_pattern(arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]
        
        await self.server.run()

if __name__ == "__main__":
    from datetime import datetime
    server = AnteaCoreKnowledgeServer()
    asyncio.run(server.run())