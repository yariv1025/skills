# CNAS-5 – Insecure secrets storage

## Summary

Unencrypted secrets in orchestrator, hardcoded app secrets, or poorly encrypted credentials. Secrets in env or configMaps are common mistakes.

## Prevention

Use dedicated secret manager or encrypted secrets; inject at runtime; rotate regularly. Never store in plaintext or in source control; restrict access via RBAC.

## Testing

Scan for hardcoded and plaintext secrets; verify use of secret store and encryption; check RBAC.
