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

## Testing

- Test token validation (expired, tampered, wrong issuer); check for credential leakage; test rate limiting.
