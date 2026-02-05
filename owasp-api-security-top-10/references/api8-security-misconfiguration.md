# API8:2023 – Security Misconfiguration

## Summary

Complex API configurations often have security gaps: unnecessary HTTP methods, permissive CORS, default credentials, verbose errors, or exposed debug endpoints. Harden all environments and follow secure baseline.

## Key CWEs

- CWE-16 Configuration
- CWE-756 Missing Custom Error Page

## Root Causes

- Default or permissive config; debug or admin endpoints enabled in production; missing security headers.

## Prevention Checklist

- Disable unnecessary HTTP methods; restrict CORS to needed origins.
- Remove or protect debug and admin endpoints; use strong credentials.
- Set security headers (e.g. CSP, HSTS); return generic errors to clients; log details server-side.
- Maintain secure baseline (checklist or IaC); automate config checks.

## Secure Patterns

- Explicitly allow only required methods per route; deny by default.
- Separate config per environment; no debug or samples in production.

## Testing

- Scan for open methods, permissive CORS, default credentials; check security headers and error responses.
