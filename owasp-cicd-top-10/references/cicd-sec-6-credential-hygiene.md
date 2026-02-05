# CICD-SEC-6 – Insufficient Credential Hygiene

## Summary

Secrets hardcoded, stored insecurely, or exposed in logs. Compromised credentials lead to full pipeline and deployment access.

## Prevention

- Use secret manager or vault; inject at runtime; rotate regularly. Never log secrets; restrict secret access by pipeline; use short-lived, scoped tokens.

## Testing

- Scan for hardcoded secrets and log exposure; verify use of secret store and rotation.
