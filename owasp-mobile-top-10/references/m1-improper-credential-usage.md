# M1 – Improper Credential Usage

## Summary

Security of credentials, API keys, and other secrets in mobile apps. Hardcoded or poorly stored secrets lead to theft and abuse.

## Prevention

- Use platform secure storage (Keychain/Keystore); never hardcode API keys or passwords.
- Prefer short-lived tokens and refresh flows; scope credentials minimally.
- Do not log or expose credentials in UI or backups.

## Testing

- Scan for hardcoded secrets; verify use of secure storage; check backup and sharing behavior.
