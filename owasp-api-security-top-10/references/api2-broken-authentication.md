# API2:2023 – Broken Authentication

## Summary

Incorrectly implemented authentication allows attackers to compromise tokens or assume other users' identities. Covers token handling, JWT validation, API keys, and OAuth misconfigurations.

## Key CWEs

- CWE-287 Improper Authentication
- CWE-384 Session Fixation
- CWE-306 Missing Authentication for Critical Function

## Root Causes

- Weak or default credentials; insecure token storage or transmission; missing token validation.

## Prevention Checklist

- Validate all tokens (signature, expiry, issuer); use standard libraries; secure storage and transmission.
- Rotate and scope API keys; never in URLs or logs.
- Enforce MFA for sensitive operations; rate limit authentication attempts.

## Secure Patterns

- Validate JWT signature and claims (exp, iss, aud); use HTTPS; store tokens securely (e.g. httpOnly cookie or secure storage).
- Prefer short-lived tokens and refresh flow; invalidate on logout.

## Examples

### Wrong - No JWT validation

```python
import jwt

@app.get("/api/profile")
def get_profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    # DANGER: No signature verification!
    payload = jwt.decode(token, options={"verify_signature": False})
    return User.query.get(payload["sub"])
```

### Right - Full JWT validation

```python
import jwt
from jwt import InvalidTokenError

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"

@app.get("/api/profile")
def get_profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={
                "require": ["exp", "iss", "sub"],
                "verify_exp": True,
                "verify_iss": True,
            },
            issuer="https://auth.example.com"
        )
    except InvalidTokenError as e:
        raise HTTPException(401, "Invalid token")
    
    return User.query.get(payload["sub"])
```

### Wrong - API key in URL

```python
# API key exposed in logs, browser history, referer
@app.get("/api/data")
def get_data():
    api_key = request.args.get("api_key")  # ?api_key=secret123
    if api_key != VALID_KEY:
        raise HTTPException(401)
```

### Right - API key in header

```python
@app.get("/api/data")
def get_data():
    api_key = request.headers.get("X-API-Key")
    if not api_key or not verify_api_key(api_key):
        raise HTTPException(401, "Invalid API key")
    # Rate limit per API key
    check_rate_limit(api_key)
```

### Wrong - Long-lived tokens, no rotation

```python
def create_token(user):
    return jwt.encode(
        {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=365)},
        SECRET
    )  # Token valid for a year!
```

### Right - Short-lived access token with refresh

```python
def create_tokens(user):
    access_token = jwt.encode(
        {"sub": user.id, "exp": datetime.utcnow() + timedelta(minutes=15)},
        SECRET
    )
    refresh_token = secrets.token_urlsafe(32)
    store_refresh_token(refresh_token, user.id, expires=timedelta(days=7))
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/api/refresh")
def refresh():
    refresh_token = request.json.get("refresh_token")
    user_id = validate_and_consume_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(401, "Invalid refresh token")
    return create_tokens(User.query.get(user_id))
```

### JWT validation checklist

| Check | Why |
|-------|-----|
| Signature | Prevent token forgery |
| `exp` (expiration) | Limit token lifetime |
| `iss` (issuer) | Ensure token from trusted source |
| `aud` (audience) | Ensure token intended for this API |
| Algorithm allowlist | Prevent algorithm confusion attacks |

## Testing

- Test token validation (expired, tampered, wrong issuer); check for credential leakage; test rate limiting.
