# API1:2023 – Broken Object Level Authorization

## Summary

APIs expose endpoints that use object identifiers (e.g. IDs in URL or body). Without proper authorization checks, users can access or modify other users' objects (IDOR). Always verify the authenticated principal is allowed to access the requested object.

## Key CWEs

- CWE-639 Authorization Bypass Through User-Controlled Key
- CWE-284 Improper Access Control

## Root Causes

- Missing or inconsistent authorization checks per object; trusting client-supplied IDs.

## Prevention Checklist

- Enforce authorization on every request that accesses a resource by ID.
- Use server-side authorization logic; never rely on client to enforce access.
- Prefer indirect references or tokens when appropriate to reduce enumeration.

## Secure Patterns

- Before returning or modifying any object, verify: "Does the authenticated user/role have permission for this object and action?"
- Use consistent authorization layer (middleware or service) for all object access.

## Testing

- Test with different users and roles; try accessing other users' object IDs; use SAST/DAST for missing authorization.
