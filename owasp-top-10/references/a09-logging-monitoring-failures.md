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

## Testing / Detection

- Verify logs for auth and access control events; confirm no secrets in logs.
- Test log injection; review log storage and access control.
- Validate alerting and response procedures.
