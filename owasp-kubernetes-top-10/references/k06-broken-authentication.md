# K06 – Broken Authentication Mechanisms

## Summary

Weak or misconfigured authentication for API server, dashboard, or workloads. Anonymous access or default credentials enable unauthorized access.

## Prevention

- Enforce strong auth for API and dashboard (e.g. OIDC, RBAC); disable anonymous auth where not required. Use short-lived tokens; protect kubeconfig and service account tokens.

## Testing

- Test anonymous and default access; verify token lifecycle and revocation; check dashboard and API auth.
