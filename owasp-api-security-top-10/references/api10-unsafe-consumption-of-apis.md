# API10:2023 – Unsafe Consumption of APIs

## Summary

Developers often trust third-party API data more than user input and adopt weaker security standards. Data from external APIs can be malicious or spoofed; treat it as untrusted and validate/sanitize.

## Key CWEs

- CWE-20 Improper Input Validation
- CWE-829 Inclusion of Functionality from Untrusted Control Sphere

## Root Causes

- Trusting third-party API responses without validation; passing API data to sensitive sinks (e.g. eval, redirect, SQL).
- No integrity or authenticity checks on consumed APIs.

## Prevention Checklist

- Validate and sanitize all data from third-party APIs; apply same rigor as user input.
- Use allowlists and schema validation; do not pass API response data directly to sensitive operations.
- Verify TLS and authenticity of consumed APIs; prefer signed or verified data when available.

## Secure Patterns

- Define schemas for consumed API responses; validate before use; map to internal types.
- Never use third-party response data in redirects, SQL, or HTML without encoding/validation.

## Testing

- Fuzz or mock malicious third-party responses; verify validation and encoding; test for injection and open redirect.
