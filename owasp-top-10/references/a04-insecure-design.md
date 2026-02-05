# A04:2021 – Insecure Design

## Summary

Insecure design is the risk of missing or flawed security controls and threat modeling. It covers design-level weaknesses rather than implementation bugs: lack of threat modeling, insecure business logic, or missing security requirements. Shift-left security and secure SDLC address this.

## Key CWEs

- CWE-209 Generation of Error Message Containing Sensitive Information
- CWE-256 Plaintext Storage of a Password
- CWE-501 Trust Boundary Violation
- CWE-522 Insufficiently Protected Credentials

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A04_2021-Insecure_Design/) for the full list.*

## Root Causes / Triggers

- No threat model or security requirements during design.
- Business logic that allows abuse (e.g. unlimited actions, missing rate limits).
- Trust boundaries not identified or enforced.
- OWASP 2025 A10 (Mishandling of Exceptional Conditions) relates to design: safe failure and error handling.

## Prevention Checklist

- Perform threat modeling and define security requirements early.
- Design for denial-of-service and abuse (rate limits, quotas, validation).
- Enforce trust boundaries (user vs system, tiers) in the architecture.
- Use secure design patterns and avoid known anti-patterns.
- Review designs for security before implementation; fail secure on errors.

## Secure Patterns

- **Threat model:** Identify assets, trust boundaries, and threats; document assumptions and mitigations.
- **Rate limiting:** Apply at API and critical operations to limit abuse and DoS.
- **Fail secure:** On exception or unexpected input, deny or fall back to a safe state; avoid leaking internals.

## Examples

### Wrong - No rate limiting on sensitive operation

```python
@app.post("/api/login")
def login(username: str, password: str):
    # Unlimited attempts - brute force possible
    user = authenticate(username, password)
    if user:
        return create_token(user)
    return {"error": "Invalid credentials"}
```

### Right - Rate limiting on authentication

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/login")
@limiter.limit("5/minute")  # Max 5 attempts per minute per IP
def login(username: str, password: str):
    user = authenticate(username, password)
    if user:
        return create_token(user)
    # Constant-time response to prevent timing attacks
    return {"error": "Invalid credentials"}
```

### Wrong - Fail open on error

```python
def check_permission(user, resource):
    try:
        return permission_service.check(user, resource)
    except Exception:
        # Fail open - grants access on any error!
        return True
```

### Right - Fail secure on error

```python
def check_permission(user, resource):
    try:
        return permission_service.check(user, resource)
    except Exception as e:
        logger.error(f"Permission check failed: {e}")
        # Fail closed - deny access on any error
        return False
```

### Wrong - Verbose error messages

```python
@app.exception_handler(Exception)
def handle_error(request, exc):
    # Exposes internal details to attacker
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": traceback.format_exc()}
    )
```

### Right - Generic error to client, detailed logging

```python
import logging
import uuid

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
def handle_error(request, exc):
    error_id = str(uuid.uuid4())
    # Log full details server-side
    logger.error(f"Error {error_id}: {exc}", exc_info=True)
    # Return generic message with reference ID
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "reference": error_id}
    )
```

### Threat modeling checklist

1. **Identify assets**: What data/systems need protection?
2. **Define trust boundaries**: Where does trusted meet untrusted?
3. **Enumerate threats**: Use STRIDE (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation)
4. **Assess risk**: Likelihood x Impact for each threat
5. **Plan mitigations**: Controls to reduce risk to acceptable level
6. **Document and review**: Keep threat model updated as system evolves

## Testing / Detection

- Design and architecture reviews; check for missing security controls.
- Abuse-case testing (e.g. repeated actions, boundary values).
- Verify error handling does not leak sensitive data (see also A09).
