"""
Machine Identity Management for AnteaCore Client
Generates and manages unique machine identifiers
"""

import uuid
import hashlib
import platform
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

def get_machine_factors() -> Dict[str, str]:
    """Get machine-specific factors for ID generation."""
    factors = {
        "node": platform.node(),  # Network name
        "machine": platform.machine(),  # Machine type (x86_64, etc)
        "processor": platform.processor(),  # Processor info
        "system": platform.system(),  # OS type
        "release": platform.release(),  # OS release
        "home": str(Path.home()),  # Home directory path
    }
    
    # Add MAC address if available (more stable)
    try:
        import getmac
        mac = getmac.get_mac_address()
        if mac:
            factors["mac"] = mac
    except:
        pass
    
    # Add CPU info if available
    try:
        import cpuinfo
        cpu = cpuinfo.get_cpu_info()
        factors["cpu_brand"] = cpu.get('brand_raw', '')
    except:
        pass
    
    return factors

def generate_machine_id() -> str:
    """Generate a unique, stable machine identifier."""
    factors = get_machine_factors()
    
    # Create a stable string from factors
    # Sort keys to ensure consistency
    factor_string = '|'.join([
        f"{k}:{v}" for k, v in sorted(factors.items())
    ])
    
    # Generate SHA256 hash
    machine_hash = hashlib.sha256(factor_string.encode()).hexdigest()
    
    # Convert to UUID format for consistency
    # Use first 32 chars of hash to create UUID
    machine_uuid = str(uuid.UUID(machine_hash[:32]))
    
    return machine_uuid

def load_identity() -> Optional[Dict[str, any]]:
    """Load existing machine identity."""
    identity_file = Path.home() / ".anteacore" / "identity.json"
    
    if not identity_file.exists():
        return None
    
    try:
        with open(identity_file, 'r') as f:
            return json.load(f)
    except Exception:
        return None

def save_identity(identity: Dict[str, any]) -> None:
    """Save machine identity securely."""
    identity_dir = Path.home() / ".anteacore"
    identity_dir.mkdir(exist_ok=True)
    
    identity_file = identity_dir / "identity.json"
    
    # Write with secure permissions
    with open(identity_file, 'w') as f:
        json.dump(identity, f, indent=2)
    
    # Set file permissions (Unix-like systems)
    if platform.system() != "Windows":
        os.chmod(identity_file, 0o600)

def ensure_machine_identity() -> Dict[str, any]:
    """Ensure machine has an identity, create if needed."""
    # Try to load existing
    identity = load_identity()
    
    if identity and 'machine_id' in identity:
        # Validate it's still correct for this machine
        current_id = generate_machine_id()
        if identity['machine_id'] == current_id:
            return identity
        
        # Machine has changed significantly, create new
        print("⚠️  Machine configuration changed, generating new identity")
    
    # Generate new identity
    machine_id = generate_machine_id()
    
    identity = {
        "machine_id": machine_id,
        "created_at": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "factors": get_machine_factors(),  # Store for debugging
        "anonymous": True,  # No personal data collected
    }
    
    save_identity(identity)
    
    return identity

def get_machine_id() -> str:
    """Get the current machine ID, creating if necessary."""
    identity = ensure_machine_identity()
    return identity['machine_id']

def get_anonymous_display_id() -> str:
    """Get a short, anonymous display ID for the user."""
    machine_id = get_machine_id()
    # Use first 8 chars for display
    return f"User-{machine_id[:8]}"

# Command-line utility
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--show":
        identity = ensure_machine_identity()
        print(f"Machine ID: {identity['machine_id']}")
        print(f"Display ID: {get_anonymous_display_id()}")
        print(f"Created: {identity['created_at']}")
    else:
        # Just ensure identity exists
        identity = ensure_machine_identity()
        print(f"✅ Machine identity: {get_anonymous_display_id()}")