# M9 – Insecure Data Storage

## Summary

Sensitive data stored in plaintext, in world-readable locations, or in backups without encryption. Leads to data exposure if device is lost or compromised.

## Prevention

- Store sensitive data in platform secure storage (Keychain/Keystore/EncryptedSharedPreferences).
- Encrypt sensitive files and databases; protect backup content; avoid storing secrets in logs or caches.
- Clear sensitive data when no longer needed; sanitize on logout.

## Testing

- Inspect storage and backups for plaintext sensitive data; verify encryption and access control.
