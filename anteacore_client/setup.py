#!/usr/bin/env python3
"""
Setup script for AnteaCore Client
Configures MCP tools for Claude Desktop
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path
import hashlib
import requests
from typing import Dict, Optional

class AnteaCoreSetup:
    """Setup and configure AnteaCore client for Claude Code."""
    
    def __init__(self):
        self.api_key = None
        self.api_url = "https://api.anteacore.com"  # Production API
        self.config_dir = Path.home() / ".anteacore"
        self.config_file = self.config_dir / "config.json"
        
    def get_claude_config_path(self) -> Path:
        """Get Claude Desktop config path for current OS."""
        system = platform.system()
        if system == "Darwin":  # macOS
            return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
        elif system == "Windows":
            return Path(os.environ["APPDATA"]) / "Claude/claude_desktop_config.json"
        else:  # Linux
            return Path.home() / ".config/Claude/claude_desktop_config.json"
    
    def setup_machine_identity(self) -> bool:
        """Setup machine identity for secure access."""
        print("\n🔐 Setting up Machine Identity")
        print("=" * 50)
        
        from .identity import ensure_machine_identity, get_anonymous_display_id
        
        # Generate or load machine identity
        identity = ensure_machine_identity()
        self.machine_id = identity['machine_id']
        
        print(f"✅ Machine ID: {get_anonymous_display_id()}")
        print("   This anonymous ID tracks your contributions")
        print("   No personal information is collected")
        
        return True
    
    def verify_network_access(self) -> bool:
        """Verify access to AnteaCore network."""
        print("\n🌐 Verifying Network Access")
        print("=" * 50)
        
        try:
            # Test connection with machine ID
            response = requests.get(
                f"{self.api_url}/api/client/health",
                headers={
                    "X-Machine-ID": self.machine_id,
                    "User-Agent": "AnteaCore-Client/0.1.0"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Connected to AnteaCore network")
                return True
            else:
                print(f"❌ Network access failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Cannot connect to AnteaCore network: {e}")
            print("   Please check your internet connection")
            return False
    
    def install_mcp_servers(self) -> bool:
        """Install MCP server files."""
        print("\n📦 Installing MCP Servers")
        print("=" * 50)
        
        # Get directory where command was run
        project_dir = Path.cwd()
        mcp_dir = project_dir / ".anteacore" / "mcp_servers"
        mcp_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy MCP server files from package
        package_dir = Path(__file__).parent
        mcp_source = package_dir / "mcp_servers"
        
        servers = [
            "secure_knowledge_server.py"
        ]
        
        for server in servers:
            source = mcp_source / server
            dest = mcp_dir / server
            
            if source.exists():
                with open(source, 'r') as f:
                    content = f.read()
                
                # No placeholders needed - server loads identity directly
                
                with open(dest, 'w') as f:
                    f.write(content)
                
                print(f"✅ Installed: {server}")
            else:
                print(f"⚠️  Server file not found: {server}")
        
        return True
    
    def configure_claude_desktop(self) -> bool:
        """Configure Claude Desktop to use AnteaCore MCP servers."""
        print("\n⚙️  Configuring Claude Desktop")
        print("=" * 50)
        
        config_path = self.get_claude_config_path()
        project_dir = Path.cwd()
        mcp_dir = project_dir / ".anteacore" / "mcp_servers"
        
        # Load existing config
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}
            config_path.parent.mkdir(parents=True, exist_ok=True)
        
        if "mcpServers" not in config:
            config["mcpServers"] = {}
        
        # Add AnteaCore MCP servers
        anteacore_servers = {
            "anteacore-knowledge": {
                "command": sys.executable,
                "args": [str(mcp_dir / "secure_knowledge_server.py")],
                "env": {
                    "ANTEACORE_API_URL": self.api_url,
                    "ANTEACORE_PROJECT_DIR": str(project_dir),
                    "ANTEACORE_MACHINE_ID": self.machine_id  # For verification
                }
            }
        }
        
        # Update config
        config["mcpServers"].update(anteacore_servers)
        
        # Save config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Updated Claude config: {config_path}")
        print(f"✅ Project directory: {project_dir}")
        
        return True
    
    def create_project_config(self) -> bool:
        """Create project-specific configuration."""
        print("\n📁 Creating Project Configuration")
        print("=" * 50)
        
        project_config = {
            "project_name": Path.cwd().name,
            "languages": [],
            "frameworks": [],
            "contribution_settings": {
                "auto_suggest": True,
                "share_patterns": True,
                "anonymize": True
            }
        }
        
        # Save to project
        config_file = Path.cwd() / ".anteacore" / "project.json"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(project_config, f, indent=2)
        
        # Add to .gitignore
        gitignore = Path.cwd() / ".gitignore"
        if gitignore.exists():
            with open(gitignore, 'r') as f:
                content = f.read()
            
            if '.anteacore/' not in content:
                with open(gitignore, 'a') as f:
                    f.write('\n# AnteaCore client\n.anteacore/\n')
                print("✅ Added .anteacore to .gitignore")
        
        print(f"✅ Created project config: {config_file}")
        
        return True
    
    def run_setup(self) -> bool:
        """Run complete setup process."""
        print("\n🚀 AnteaCore Client Setup")
        print("=" * 50)
        print("Free access to AI development knowledge base")
        print("No signup required - anonymous contribution enabled")
        
        # Step 1: Machine Identity
        if not self.setup_machine_identity():
            return False
        
        # Step 2: Verify network access
        if not self.verify_network_access():
            return False
        
        # Step 3: Install MCP servers
        if not self.install_mcp_servers():
            return False
        
        # Step 4: Configure Claude Desktop
        if not self.configure_claude_desktop():
            return False
        
        # Step 5: Create project config
        if not self.create_project_config():
            return False
        
        print("\n✅ Setup Complete!")
        from .identity import get_anonymous_display_id
        print(f"\n🆔 Your anonymous ID: {get_anonymous_display_id()}")
        print("\n⚡ Next Steps:")
        print("1. Restart Claude Desktop")
        print("2. Open this project in Claude Code")
        print("3. Test with: anteacore-test")
        print("\n🔐 Security Notes:")
        print("- You can search all public knowledge")
        print("- You can add new patterns (reviewed for quality)")
        print("- You cannot modify or delete existing content")
        print("- All contributions are immutable and attributed to your ID")
        print("\n📚 Documentation: https://docs.anteacore.com/client")
        
        return True

def main():
    """Main entry point for setup command."""
    setup = AnteaCoreSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()