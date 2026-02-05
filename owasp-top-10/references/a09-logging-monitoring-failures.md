# A09:2021 – Security Logging and Monitoring Failures

## Summary

Missing or insufficient logging and monitoring makes detection and response to attacks difficult or impossible. This includes failing to log security-relevant events (auth failures, access control failures, input validation failures), logging sensitive data, or not alerting on suspicious activity.

## Key CWEs

- CWE-223 Omission of Security-Relevant Information
- CWE-778 Insufficient Logging
- CWE-779 Logging of Excessive Data
- CWE-117 Improper Output Neutralization for Logs

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/) for the full list.*

## Root Causes / Triggers

- No logging of authentication or authorization failures.
- Logs that contain secrets, PII, or full payloads (increasing exposure and compliance risk).
- No alerting or correlation; logs not reviewed or retained appropriately.
- Log injection (unvalidated input in log messages) leading to tampering or confusion.

## Prevention Checklist

- Log security-relevant events: login success/failure, access control failures, input validation failures, high-value actions.
- Do not log passwords, tokens, or full PII; redact or omit sensitive fields.
- Use structured logging and correlation IDs for tracing.
- Set up alerting on anomalies and known-bad patterns; define response playbooks.
- Protect and retain logs; ensure they cannot be altered by attackers.

## Secure Patterns

- **What to log:** User ID (not password), timestamp, resource/action, result (success/failure), IP/session if useful; avoid request/response bodies with secrets.
- **Structure:** JSON or similar with consistent fields; include correlation ID for request tracing.
- **Injection:** Sanitize or avoid including unsanitized user input in log messages.

## Examples

### Wrong - No security logging

```python
@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.form["user"], request.form["pass"])
    if user:
        return create_session(user)
    # No logging of failed attempt
    return "Invalid credentials", 401
```

### Right - Log security events

```python
import logging
import structlog

logger = structlog.get_logger()

@app.route("/login", methods=["POST"])
def login():
    username = request.form["user"]
    user = authenticate(username, request.form["pass"])
    
    if user:
        logger.info(
            "login_success",
            user_id=user.id,
            ip=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )
        return create_session(user)
    
    logger.warning(
        "login_failure",
        username=username,  # Log username, not password
        ip=request.remote_addr,
        reason="invalid_credentials"
    )
    return "Invalid credentials", 401
```

### Wrong - Logging sensitive data

```python
logger.info(f"User login: {username}, password: {password}")
logger.debug(f"API response: {response.json()}")  # May contain tokens/PII
logger.info(f"Payment processed: card={card_number}")
```

### Right - Redact sensitive fields

```python
def redact_sensitive(data: dict) -> dict:
    sensitive_keys = {"password", "token", "card_number", "ssn", "api_key"}
    return {
        k: "[REDACTED]" if k.lower() in sensitive_keys else v
        for k, v in data.items()
    }

logger.info("User login", user_id=user.id)  # No password
logger.debug("API response", status=response.status_code)  # No body
logger.info("Payment processed", last_four=card_number[-4:])
```

### Wrong - Log injection vulnerability

```python
# User input: "admin\n2024-01-01 INFO: User admin granted access"
logger.info(f"Login attempt for user: {username}")
# Results in fake log entries
```

### Right - Structured logging prevents injection

```python
import structlog

logger = structlog.get_logger()

# Structured logging - username is a field, not part of message
logger.info("login_attempt", username=username)
# Output: {"event": "login_attempt", "username": "admin\n...", "timestamp": "..."}
# Newline is data, not log structure
```

### Structured log example

```python
import structlog
import uuid

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

@app.before_request
def add_request_id():
    g.request_id = str(uuid.uuid4())

logger.info(
    "request_processed",
    request_id=g.request_id,
    user_id=current_user.id,
    action="view_document",
    resource_id=doc_id,
    result="success",
    duration_ms=elapsed
)
```

### What to log checklist

| Event | Log? | Fields |
|-------|------|--------|
| Login success | Yes | user_id, ip, timestamp |
| Login failure | Yes | username (not password), ip, reason |
| Access denied | Yes | user_id, resource, action |
| Admin action | Yes | user_id, action, target, changes |
| Input validation failure | Yes | endpoint, field, reason (not value) |
| Password | Never | - |
| API tokens | Never | - |
| Full request body | Rarely | Redact sensitive fields |

## Testing / Detection

- Verify logs for auth and access control events; confirm no secrets in logs.
- Test log injection; review log storage and access control.
- Validate alerting and response procedures.
