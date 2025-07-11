"""
AnteaCore Client API
Main client for interacting with AnteaCore network
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import httpx
from datetime import datetime, timedelta

class AnteaCoreClient:
    """Client for AnteaCore API interactions."""
    
    def __init__(self, privileged_token: Optional[str] = None):
        """Initialize client with anonymous session."""
        from .anonymous_identity import get_anonymous_headers
        
        self.api_url = os.getenv("ANTEACORE_API_URL", "https://anteacore-publicapi.up.railway.app")
        self.privileged_token = privileged_token
        
        # Get anonymous headers (includes session ID)
        headers = get_anonymous_headers()
        headers["User-Agent"] = "AnteaCore-Client/0.1.0"
        
        if self.privileged_token:
            headers["X-Privileged-Token"] = self.privileged_token
            
        self.client = httpx.Client(
            headers=headers,
            timeout=30.0
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API connection."""
        try:
            response = self.client.get(f"{self.api_url}/api/client/health")
            if response.status_code == 200:
                return {
                    "success": True,
                    "server": self.api_url,
                    "version": response.json().get("version", "Unknown")
                }
            else:
                return {
                    "success": False,
                    "error": f"Server returned {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def activate_privileged_mode(self, secret: str) -> Dict[str, Any]:
        """Activate privileged mode with master secret."""
        try:
            response = self.client.post(
                f"{self.api_url}/api/client/privileged/activate",
                json={"secret": secret}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    # Update client with privileged token
                    self.privileged_token = data["token"]
                    self.client.headers["X-Privileged-Token"] = self.privileged_token
                    return data
            
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def search_knowledge(
        self,
        query: str,
        category: Optional[str] = None,
        language: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Search knowledge base."""
        params = {
            "query": query,
            "limit": limit
        }
        if category:
            params["category"] = category
        if language:
            params["language"] = language
        
        try:
            response = self.client.post(
                f"{self.api_url}/api/client/knowledge/search",
                json=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def add_pattern(
        self,
        name: str,
        category: str,
        problem: str,
        solution: str,
        code_example: Optional[str] = None,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Add a development pattern."""
        data = {
            "name": name,
            "category": category,
            "problem": problem,
            "solution": solution,
            "source": "client_contribution",
            "created_at": datetime.now().isoformat()
        }
        
        if code_example:
            data["code_example"] = code_example
        if language:
            data["language"] = language
        if tags:
            data["tags"] = tags
        
        try:
            response = self.client.post(
                f"{self.api_url}/api/client/knowledge/patterns",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_suggestions(
        self,
        context: str,
        file_type: Optional[str] = None,
        language: Optional[str] = None,
        frameworks: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get pattern suggestions based on context."""
        data = {
            "context": context
        }
        
        if file_type:
            data["file_type"] = file_type
        if language:
            data["language"] = language
        if frameworks:
            data["frameworks"] = frameworks
        
        try:
            response = self.client.post(
                f"{self.api_url}/api/client/knowledge/suggest",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def report_issue(
        self,
        issue: str,
        error_message: Optional[str] = None,
        context: Optional[str] = None,
        attempted_solutions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Report an issue and get solutions."""
        data = {
            "issue": issue,
            "reported_at": datetime.now().isoformat()
        }
        
        if error_message:
            data["error_message"] = error_message
        if context:
            data["context"] = context
        if attempted_solutions:
            data["attempted_solutions"] = attempted_solutions
        
        try:
            # First search for solutions
            search_response = self.search_knowledge(issue, category="troubleshooting")
            
            # Then report the issue
            response = self.client.post(
                f"{self.api_url}/api/client/issues",
                json=data
            )
            
            return {
                "existing_solutions": search_response.get("results", []),
                "issue_reported": response.status_code in [200, 201]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get user contribution statistics."""
        try:
            response = self.client.get(f"{self.api_url}/api/client/stats")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current anonymous session information."""
        from .anonymous_identity import load_or_create_session, get_display_name
        
        session = load_or_create_session()
        return {
            "display_name": get_display_name(),
            "session_id": session.session_id,
            "created_at": session.created_at.isoformat(),
            "expires_at": (session.created_at + timedelta(hours=24)).isoformat(),
            "submission_count": session.submission_count,
            "anonymous": True
        }