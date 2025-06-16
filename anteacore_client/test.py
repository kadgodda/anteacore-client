#!/usr/bin/env python3
"""
Test script for AnteaCore Client
Verifies MCP tools are working correctly
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

class AnteaCoreTest:
    """Test AnteaCore client installation."""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.config_dir = self.project_dir / ".anteacore"
        self.passed = 0
        self.failed = 0
    
    def test_configuration(self) -> bool:
        """Test if configuration exists."""
        print("\n1️⃣  Testing Configuration")
        print("-" * 40)
        
        # Check global config
        global_config = Path.home() / ".anteacore" / "config.json"
        if global_config.exists():
            print("✅ Global configuration found")
            self.passed += 1
        else:
            print("❌ Global configuration not found")
            print("   Run: anteacore-setup")
            self.failed += 1
            return False
        
        # Check project config
        project_config = self.config_dir / "project.json"
        if project_config.exists():
            print("✅ Project configuration found")
            self.passed += 1
        else:
            print("❌ Project configuration not found")
            self.failed += 1
        
        # Check MCP servers
        mcp_dir = self.config_dir / "mcp_servers"
        if mcp_dir.exists() and list(mcp_dir.glob("*.py")):
            print("✅ MCP servers installed")
            self.passed += 1
        else:
            print("❌ MCP servers not found")
            self.failed += 1
        
        return True
    
    def test_api_connection(self) -> bool:
        """Test API connection."""
        print("\n2️⃣  Testing API Connection")
        print("-" * 40)
        
        try:
            # Try to import and use the client
            from anteacore_client.client import AnteaCoreClient
            
            client = AnteaCoreClient()
            result = client.test_connection()
            
            if result.get("success"):
                print("✅ API connection successful")
                print(f"   Connected to: {result.get('server', 'Unknown')}")
                print(f"   API version: {result.get('version', 'Unknown')}")
                self.passed += 1
                return True
            else:
                print("❌ API connection failed")
                print(f"   Error: {result.get('error', 'Unknown error')}")
                self.failed += 1
                return False
                
        except Exception as e:
            print(f"❌ Failed to test API: {e}")
            self.failed += 1
            return False
    
    def test_mcp_tools(self) -> bool:
        """Test MCP tool functionality."""
        print("\n3️⃣  Testing MCP Tools")
        print("-" * 40)
        
        try:
            # Test search functionality
            from anteacore_client.mcp_wrapper import quick_mcp_call
            
            print("Testing knowledge search...")
            result = quick_mcp_call('anteacore-knowledge', 'search', {
                'query': 'react hooks',
                'limit': 3
            })
            
            if isinstance(result, dict) and 'error' not in result:
                print("✅ Knowledge search working")
                if 'results' in result:
                    print(f"   Found {len(result['results'])} results")
                self.passed += 1
            else:
                print("❌ Knowledge search failed")
                print(f"   Error: {result.get('error', 'Unknown error')}")
                self.failed += 1
            
            # Test pattern validation
            print("\nTesting pattern validation...")
            result = quick_mcp_call('anteacore-knowledge', 'validate_pattern', {
                'pattern_description': 'Using React hooks for state management'
            })
            
            if isinstance(result, dict) and 'error' not in result:
                print("✅ Pattern validation working")
                self.passed += 1
            else:
                print("❌ Pattern validation failed")
                self.failed += 1
                
        except Exception as e:
            print(f"❌ MCP tools test failed: {e}")
            self.failed += 1
            return False
        
        return True
    
    def test_claude_integration(self) -> bool:
        """Test Claude Desktop integration."""
        print("\n4️⃣  Testing Claude Desktop Integration")
        print("-" * 40)
        
        # Check Claude config
        import platform
        system = platform.system()
        
        if system == "Darwin":  # macOS
            config_path = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
        elif system == "Windows":
            config_path = Path(os.environ["APPDATA"]) / "Claude/claude_desktop_config.json"
        else:  # Linux
            config_path = Path.home() / ".config/Claude/claude_desktop_config.json"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            if "mcpServers" in config and "anteacore-knowledge" in config["mcpServers"]:
                print("✅ Claude Desktop configured")
                print("   MCP servers:")
                for server in ["anteacore-knowledge", "anteacore-client"]:
                    if server in config["mcpServers"]:
                        print(f"   ✓ {server}")
                self.passed += 1
                return True
            else:
                print("❌ AnteaCore not found in Claude config")
                self.failed += 1
        else:
            print("❌ Claude Desktop config not found")
            self.failed += 1
        
        return False
    
    def run_tests(self):
        """Run all tests."""
        print("\n🧪 AnteaCore Client Test Suite")
        print("=" * 50)
        
        # Run tests
        self.test_configuration()
        self.test_api_connection()
        self.test_mcp_tools()
        self.test_claude_integration()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        
        if self.failed == 0:
            print("\n🎉 All tests passed!")
            print("\n✨ You're ready to use AnteaCore with Claude Code!")
            print("\nTry these commands in Claude:")
            print("- Search: quick_mcp_call('anteacore-knowledge', 'search', {'query': 'your topic'})")
            print("- Add pattern: quick_mcp_call('anteacore-knowledge', 'add_pattern', {...})")
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
            print("\nTroubleshooting:")
            print("1. Run: anteacore-setup")
            print("2. Restart Claude Desktop")
            print("3. Check docs: https://docs.anteacore.com/client/troubleshooting")
        
        return self.failed == 0

def main():
    """Main entry point."""
    tester = AnteaCoreTest()
    success = tester.run_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()