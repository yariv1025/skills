# A01:2021 – Broken Access Control

## Summary

Access control enforces policy so users cannot act outside their intended permissions. Failures lead to vertical or horizontal privilege escalation, path traversal, IDOR, CORS misuse, or force browsing. SSRF is also an access-control concern (OWASP 2025 merges SSRF into this category).

## Key CWEs

- CWE-284 Improper Access Control
- CWE-285 Improper Authorization
- CWE-639 Authorization Bypass Through User-Controlled Key
- CWE-22 Path Traversal
- CWE-918 SSRF (see also [a10-ssrf.md](a10-ssrf.md))

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) for the full list.*

## Root Causes / Triggers

- Missing or inconsistent authorization checks (e.g. per object or per action).
- Trusting client-supplied identifiers (IDs, paths) without server-side verification.
- Default allow or overly broad CORS/headers.
- Forced browsing to URLs that are not linked but are reachable.

## Prevention Checklist

- Deny by default; enforce authorization on every request for the resource and action.
- Check object-level access (user owns or is allowed the resource) using server-side state.
- Avoid exposing internal IDs or paths in URLs when possible; use indirect references or tokens.
- Validate and sanitize path inputs; use allowlists for file operations.
- Configure CORS and security headers restrictively.
- Log and monitor access control failures.

## Secure Patterns

- **Authorization check:** Before returning any resource, verify the authenticated principal is allowed for that resource and action (e.g. "can user X read document Y?").
- **Indirect reference:** Map a random token to an internal ID so clients cannot enumerate or guess others’ resources.
- **Path traversal:** Use a safe base directory and resolve paths within it; reject ".." and absolute paths.

## Testing / Detection

- Test with different roles and users (horizontal/vertical escalation).
- Try modifying IDs and path parameters to access others’ data.
- Use SAST/DAST rules for missing authorization and path traversal.
- Review CORS and security headers.
