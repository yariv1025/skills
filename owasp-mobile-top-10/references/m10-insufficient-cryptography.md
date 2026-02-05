# M10 – Insufficient Cryptography

## Summary

Use of weak or deprecated algorithms, poor key management, or custom crypto instead of platform APIs. Compromises confidentiality and integrity.

## Prevention

- Use platform crypto APIs and modern algorithms (e.g. AES-GCM, secure random); avoid MD5/SHA1 for security.
- Manage keys in secure storage; derive keys with proper KDFs; do not reuse keys inappropriately.
- Prefer standard, reviewed implementations; avoid custom crypto.

## Testing

- Identify crypto usage; check for weak algorithms and key handling; verify use of secure APIs.
