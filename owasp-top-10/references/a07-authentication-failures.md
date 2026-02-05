# A07:2021 – Identification and Authentication Failures

## Summary

Authentication and identification failures allow attackers to compromise passwords, tokens, or session identifiers, or to exploit weak session management. This includes credential stuffing, brute force, weak password policy, and missing MFA.

## Key CWEs

- CWE-287 Improper Authentication
- CWE-384 Session Fixation
- CWE-306 Missing Authentication for Critical Function
- CWE-798 Hard-coded Credentials
- CWE-521 Weak Password Requirements

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) for the full list.*

## Root Causes / Triggers

- Weak or default credentials; no MFA for sensitive actions.
- Credentials or session tokens transmitted or stored insecurely.
- Session fixation, long-lived or improperly invalidated sessions.
- Missing or weak rate limiting on login and password reset.
- Exposing credential or session info in URLs or logs.

## Prevention Checklist

- Require strong password policy and MFA for sensitive accounts and actions.
- Use secure session management: random session IDs, secure cookie flags, timeout and logout.
- Store passwords with strong adaptive hashing (see A02); never in cleartext.
- Rate limit login and password reset; lock or delay after failures.
- Do not expose session IDs in URLs; use HTTPS and Secure/HttpOnly cookies.

## Secure Patterns

- **Sessions:** Generate cryptographically random session ID; bind to user and IP/UA if appropriate; invalidate on logout and timeout.
- **Passwords:** Hash with Argon2/bcrypt; never log or echo; use secure comparison.
- **MFA:** Prefer TOTP or hardware; avoid SMS for high-risk; enforce for admin and sensitive operations.

## Examples

### Wrong - Weak session management

```python
from flask import session

@app.route("/login", methods=["POST"])
def login():
    if check_credentials(request.form["user"], request.form["pass"]):
        # Session ID in cookie is predictable or not regenerated
        session["user"] = request.form["user"]
        return redirect("/dashboard")
```

### Right - Secure session management

```python
from flask import session
import secrets

app.config["SESSION_COOKIE_SECURE"] = True      # HTTPS only
app.config["SESSION_COOKIE_HTTPONLY"] = True    # No JS access
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"   # CSRF protection
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour timeout

@app.route("/login", methods=["POST"])
def login():
    if check_credentials(request.form["user"], request.form["pass"]):
        session.clear()  # Prevent session fixation
        session.regenerate()  # New session ID
        session["user"] = request.form["user"]
        session["csrf_token"] = secrets.token_hex(32)
        return redirect("/dashboard")
```

### Wrong - No rate limiting on login

```python
@app.route("/login", methods=["POST"])
def login():
    # Unlimited attempts - brute force / credential stuffing possible
    if authenticate(request.form["user"], request.form["pass"]):
        return create_session()
    return "Invalid credentials", 401
```

### Right - Rate limiting with account lockout

```python
from flask_limiter import Limiter
import time

limiter = Limiter(app, key_func=get_remote_address)
failed_attempts = {}  # Use Redis in production

@app.route("/login", methods=["POST"])
@limiter.limit("10/minute")
def login():
    username = request.form["user"]
    
    # Check for account lockout
    if is_locked(username):
        return "Account temporarily locked", 429
    
    if authenticate(username, request.form["pass"]):
        clear_failed_attempts(username)
        return create_session()
    
    record_failed_attempt(username)
    # Constant-time response
    time.sleep(0.1)
    return "Invalid credentials", 401

def is_locked(username):
    attempts = failed_attempts.get(username, {"count": 0, "time": 0})
    if attempts["count"] >= 5 and time.time() - attempts["time"] < 900:
        return True
    return False
```

### Wrong - Session token in URL

```python
# Session ID exposed in URL - logged, cached, shared via Referer
@app.route("/dashboard")
def dashboard():
    token = request.args.get("session_token")
    # https://example.com/dashboard?session_token=abc123
```

### Right - Session in secure cookie

```python
# Session ID in cookie with secure flags
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    # Session managed via secure cookie, not URL
```

### Password policy checklist

- [ ] Minimum 12 characters (or 8 with complexity)
- [ ] Check against breached password lists (Have I Been Pwned)
- [ ] No password hints or security questions
- [ ] Secure password reset with time-limited tokens
- [ ] Hash with Argon2id or bcrypt (cost factor 10+)
- [ ] MFA for admin and sensitive operations

## Testing / Detection

- Test for default credentials, weak password rules, and missing MFA.
- Verify session invalidation and timeout; check for fixation and token in URL.
- Brute-force and rate-limiting tests; credential stuffing simulation.
