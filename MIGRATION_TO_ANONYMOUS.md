# Migration Guide: Anonymous Sessions

## What's Changing

AnteaCore is transitioning from machine-based identification to truly anonymous sessions to better protect user privacy.

### Old Approach (Deprecated)
- Used hardware identifiers (MAC address, CPU info, etc.)
- Persistent machine IDs tracked users
- Privacy concerns with hardware fingerprinting

### New Approach (Privacy-First)
- Temporary session IDs (24-hour expiration)
- No hardware information collected
- Truly anonymous contributions
- Fun display names like "Swift Fox" or "Wise Owl"

## For Users

### Immediate Impact
- Your existing machine ID will stop working
- You'll get a new anonymous session automatically
- Your contribution history won't transfer (by design - it's anonymous!)

### What You Need to Do
1. Update to the latest anteacore-client package:
   ```bash
   pip install --upgrade anteacore-client
   ```

2. Clear old identity data (optional but recommended):
   ```bash
   rm -rf ~/.anteacore/identity.json
   ```

3. Test your new anonymous session:
   ```bash
   python -m anteacore_client.anonymous_identity --show
   ```

## For Developers

### Code Changes Required

#### If you're using the client directly:
```python
# OLD CODE - REMOVE
from anteacore_client.identity import get_machine_id
machine_id = get_machine_id()

# NEW CODE - USE
client = AnteaCoreClient()
session_info = client.get_session_info()
print(f"Contributing as: {session_info['display_name']}")
```

#### If you're building on the API:
```python
# OLD HEADERS - REMOVE
headers = {
    "X-Machine-ID": machine_id,
    "X-API-Key": hash(machine_id)
}

# NEW HEADERS - USE
from anteacore_client.anonymous_identity import get_anonymous_headers
headers = get_anonymous_headers()
```

### Server-Side Changes

If you're running a server that accepts AnteaCore contributions:

1. Stop validating machine IDs
2. Use session IDs for rate limiting (they expire after 24 hours)
3. Don't store any persistent user identifiers

## Privacy Benefits

1. **No Tracking**: Sessions expire, no persistent identification
2. **No Hardware Data**: No MAC addresses, CPU info, or system details
3. **User Control**: Users can clear sessions anytime
4. **Legal Compliance**: GDPR/CCPA compliant by default

## FAQ

**Q: What happens to my previous contributions?**
A: They remain in the system but won't be linked to your new sessions. This is intentional for privacy.

**Q: Can I get a permanent account?**
A: We're working on an optional account system for users who want attribution. Stay tuned!

**Q: How do you prevent spam without machine IDs?**
A: We use rate limiting per session, proof-of-work challenges, and content validation.

**Q: Can I opt back into machine IDs?**
A: No. We've removed this functionality entirely for privacy reasons.

## Timeline

- **Phase 1 (Now)**: New client uses anonymous sessions
- **Phase 2 (2 weeks)**: Server stops accepting machine IDs
- **Phase 3 (1 month)**: Old client versions will stop working

## Need Help?

- GitHub Issues: [Report problems](https://github.com/anteacore/client/issues)
- Documentation: [Privacy Policy](https://anteacore.com/privacy)
- Email: privacy@anteacore.com