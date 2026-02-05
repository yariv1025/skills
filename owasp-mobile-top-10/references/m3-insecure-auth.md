# M3 – Insecure Authentication/Authorization

## Summary

Weak or missing authentication and authorization in the app or backend allow impersonation and unauthorized access.

## Prevention

- Use strong auth (biometrics, device binding where appropriate); enforce server-side session validation.
- Apply proper authorization checks for all sensitive operations and data.
- Implement secure logout and session invalidation; avoid storing tokens insecurely.

## Testing

- Test auth bypass, session handling, and role escalation; verify server-side checks.
