# URGENT: Privacy Update Required

## Critical Issue
The current `identity.py` module collects extensive machine identification data including:
- MAC addresses
- CPU information  
- Home directory paths
- Network names
- Hardware identifiers

This is **NOT anonymous** and poses serious privacy/legal risks.

## Immediate Actions Required

### 1. Replace identity.py imports
```python
# OLD - REMOVE
from anteacore_client.identity import get_machine_id

# NEW - USE
from anteacore_client.anonymous_identity import get_anonymous_headers
```

### 2. Update API calls
```python
# OLD - REMOVE
headers = {
    "X-Machine-ID": get_machine_id(),
    "X-API-Key": hash(machine_id)
}

# NEW - USE  
headers = get_anonymous_headers()
```

### 3. Update server-side handling
- Remove any machine ID validation
- Use session IDs for rate limiting
- Don't store any hardware identifiers

## Benefits of Anonymous Approach
1. **Legal Compliance**: GDPR/CCPA compliant by default
2. **User Trust**: No privacy concerns
3. **Simpler**: No complex hardware detection
4. **Portable**: Works everywhere consistently

## Migration Path
1. Release update that supports both (with deprecation warning)
2. Stop accepting machine IDs server-side
3. Remove identity.py in next major version

## User Communication
```
"AnteaCore now uses privacy-preserving anonymous sessions. 
Your contributions remain valuable while protecting your privacy.
No hardware or personal information is collected."
```