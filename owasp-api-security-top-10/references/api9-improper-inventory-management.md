# API9:2023 – Improper Inventory Management

## Summary

Poor documentation and tracking of API endpoints and versions expose deprecated or debug endpoints, undocumented parameters, or old API versions that lack security updates. Maintain an accurate API inventory.

## Key CWEs

- CWE-1059 Insufficient Technical Documentation
- CWE-1102 Reliance on Machine Readable Data or Metadata

## Root Causes

- No inventory of endpoints; deprecated or debug endpoints still reachable; documentation out of date.
- Old API versions not retired or protected.

## Prevention Checklist

- Maintain and publish accurate API inventory (OpenAPI/Swagger); document all endpoints and versions.
- Retire or protect deprecated endpoints; disable debug endpoints in production.
- Version APIs explicitly; plan deprecation and sunset; monitor usage of old versions.

## Secure Patterns

- Use API gateway or routing to expose only documented, supported versions.
- Regular audits: compare deployed routes to inventory; remove or protect undocumented endpoints.

## Testing

- Enumerate endpoints (e.g. common paths, version suffixes); check for undocumented or deprecated endpoints; verify documentation matches implementation.
