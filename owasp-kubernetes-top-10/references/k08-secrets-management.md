# K08 – Secrets Management Failures

## Summary

Secrets in environment variables, configMaps, or plaintext in repo. Compromised secrets lead to full cluster or external system access.

## Prevention

- Use external secret manager (e.g. CSI driver, Vault); inject at runtime. Avoid encoding secrets in base64 only; rotate regularly; restrict access to Secret objects via RBAC.

## Testing

- Scan for secrets in manifests and env; verify use of secret store; check RBAC on Secrets.
