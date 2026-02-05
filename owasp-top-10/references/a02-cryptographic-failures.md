# A02:2021 – Cryptographic Failures

## Summary

Failures related to cryptography (and exposure of sensitive data) include weak or missing encryption in transit or at rest, poor key management, weak hashing for passwords, and use of deprecated algorithms or modes. Focus on protecting sensitive data and using crypto correctly.

## Key CWEs

- CWE-327 Use of a Broken or Risky Cryptographic Algorithm
- CWE-328 Use of Weak Hash
- CWE-330 Use of Insufficiently Random Values
- CWE-311 Missing Encryption of Sensitive Data
- CWE-312 Cleartext Storage of Sensitive Information

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/) for the full list.*

## Root Causes / Triggers

- Transmitting or storing sensitive data without encryption or with weak crypto.
- Hardcoded or poorly managed keys; keys in source control or logs.
- Using MD5/SHA1 for security-sensitive purposes; weak password hashing (no salt, low cost).
- Default or weak TLS configuration.

## Prevention Checklist

- Encrypt sensitive data in transit (TLS 1.2+) and at rest; classify data and protect accordingly.
- Use strong, up-to-date algorithms and modes (e.g. AES-GCM, modern KDFs).
- Store keys in a dedicated secret manager; rotate keys; never commit secrets.
- Hash passwords with a modern adaptive function (e.g. Argon2, bcrypt) with salt and appropriate cost.
- Disable legacy protocols and weak ciphers; use secure TLS config.

## Secure Patterns

- **Password hashing:** Use a dedicated password-hashing API with salt and cost factor; never raw MD5/SHA for passwords.
- **Secrets:** Load from environment or secret manager at runtime; restrict access by role.
- **TLS:** Enforce TLS for all sensitive endpoints; use HSTS and secure cookie flags.

## Testing / Detection

- Scan for hardcoded secrets and weak crypto (SAST/secret scanners).
- Verify TLS configuration (e.g. SSL Labs); check for cleartext sensitive data.
- Confirm password storage uses strong hashing and salt.
