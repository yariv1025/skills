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

## Testing / Detection

- Design and architecture reviews; check for missing security controls.
- Abuse-case testing (e.g. repeated actions, boundary values).
- Verify error handling does not leak sensitive data (see also A09).
