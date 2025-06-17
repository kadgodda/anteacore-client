"""
Anonymous Session Management for AnteaCore Client
Provides truly anonymous, privacy-respecting session handling
"""

import uuid
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional

class AnonymousSession:
    """Manages anonymous sessions without any machine identification."""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.submission_count = 0
        
    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary for storage."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "submission_count": self.submission_count,
            "anonymous": True,
            "expires_at": (self.created_at + timedelta(hours=24)).isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'AnonymousSession':
        """Create from dictionary."""
        session = cls()
        session.session_id = data["session_id"]
        session.created_at = datetime.fromisoformat(data["created_at"])
        session.submission_count = data.get("submission_count", 0)
        return session
    
    def is_expired(self) -> bool:
        """Check if session has expired (24 hours)."""
        return datetime.utcnow() > self.created_at + timedelta(hours=24)

def get_session_file() -> Path:
    """Get path to session file."""
    session_dir = Path.home() / ".anteacore" / "sessions"
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir / "current_session.json"

def load_or_create_session() -> AnonymousSession:
    """Load existing session or create new one."""
    session_file = get_session_file()
    
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                session = AnonymousSession.from_dict(data)
                
                # Check if expired
                if not session.is_expired():
                    return session
        except Exception:
            pass  # Create new session on any error
    
    # Create new session
    session = AnonymousSession()
    save_session(session)
    return session

def save_session(session: AnonymousSession) -> None:
    """Save session to file."""
    session_file = get_session_file()
    
    with open(session_file, 'w') as f:
        json.dump(session.to_dict(), f, indent=2)
    
    # Set secure permissions on Unix-like systems
    if os.name != 'nt':
        os.chmod(session_file, 0o600)

def get_anonymous_headers() -> Dict[str, str]:
    """Get headers for anonymous API requests."""
    session = load_or_create_session()
    
    return {
        "X-Session-ID": session.session_id,
        "X-Anonymous": "true",
        "X-Client-Version": "0.1.0",
        # NO machine identification
        # NO persistent tracking
    }

def increment_submission_count() -> None:
    """Increment the submission count for rate limiting."""
    session = load_or_create_session()
    session.submission_count += 1
    save_session(session)

def clear_session() -> None:
    """Clear current session (user-initiated)."""
    session_file = get_session_file()
    if session_file.exists():
        session_file.unlink()
    print("✅ Session cleared - new anonymous session will be created")

# Privacy-respecting alternatives to machine ID
def get_display_name() -> str:
    """Get a friendly, non-identifying display name."""
    adjectives = ["Swift", "Bright", "Keen", "Sharp", "Quick", "Wise", "Bold", "Calm"]
    nouns = ["Fox", "Eagle", "Owl", "Wolf", "Bear", "Deer", "Hawk", "Raven"]
    
    # Use session ID to generate consistent name within session
    session = load_or_create_session()
    session_hash = hash(session.session_id)
    
    adj = adjectives[session_hash % len(adjectives)]
    noun = nouns[(session_hash // len(adjectives)) % len(nouns)]
    
    return f"{adj} {noun}"

# Command-line utility
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--show":
            session = load_or_create_session()
            print(f"Session ID: {session.session_id}")
            print(f"Display Name: {get_display_name()}")
            print(f"Created: {session.created_at}")
            print(f"Submissions: {session.submission_count}")
            print(f"Expires: {session.created_at + timedelta(hours=24)}")
        elif sys.argv[1] == "--clear":
            clear_session()
        elif sys.argv[1] == "--privacy":
            print("🔒 Privacy Information:")
            print("- No machine IDs collected")
            print("- No hardware information tracked")
            print("- Sessions expire after 24 hours")
            print("- Completely anonymous contributions")
            print("- You can clear your session anytime with --clear")
    else:
        session = load_or_create_session()
        print(f"✅ Anonymous session: {get_display_name()}")