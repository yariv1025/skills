# API5:2023 – Broken Function Level Authorization

## Summary

Complex access control policies and unclear separation between administrative and regular functions allow attackers to access unauthorized endpoints (e.g. calling admin APIs as a regular user).

## Key CWEs

- CWE-284 Improper Access Control
- CWE-285 Improper Authorization

## Root Causes

- Missing role/scope checks on sensitive endpoints; admin endpoints reachable without proper authorization.
- Relying on client to hide or disable admin UI without server-side enforcement.

## Prevention Checklist

- Enforce function-level (endpoint-level) authorization; deny by default.
- Clearly separate admin and user endpoints; require elevated role/scope for admin operations.
- Apply consistent authorization middleware; audit all routes for required permissions.

## Secure Patterns

- Decorate or annotate routes with required roles/scopes; enforce in middleware before handler.
- Prefer explicit deny for sensitive operations unless principal has required permission.

## Testing

- Call admin or privileged endpoints with regular user tokens; test horizontal/vertical escalation; verify role checks.
