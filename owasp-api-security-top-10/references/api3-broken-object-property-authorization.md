# API3:2023 – Broken Object Property Level Authorization

## Summary

Lack of authorization validation at the property level leads to mass assignment, overposting, or information disclosure. APIs may expose or accept more properties than intended (e.g. role, balance, internal IDs).

## Key CWEs

- CWE-915 Improperly Controlled Modification of Object Attributes
- CWE-200 Exposure of Sensitive Information

## Root Causes

- Accepting all client-supplied fields; returning full internal objects; no allowlist for request/response.

## Prevention Checklist

- Allowlist request body properties; reject unknown or sensitive fields.
- Allowlist response properties; never expose internal or sensitive fields by default.
- Validate and sanitize property values; apply schema validation.

## Secure Patterns

- Define explicit DTOs/schemas for request and response; map only allowed fields.
- Use serialization filters or views to control what is returned per role/context.

## Testing

- Send extra properties in requests (overposting); check responses for PII or internal fields; test role-based visibility.
