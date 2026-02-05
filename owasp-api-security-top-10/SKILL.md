---
name: owasp-api-security-top-10
description: "OWASP API Security Top 10 - prevention, detection, and remediation for REST/GraphQL/API security. Use when designing or reviewing APIs - object- and function-level authorization, authentication, rate limiting and resource consumption, sensitive business flows, SSRF, API inventory and versioning, or consumption of third-party APIs."
---

# OWASP API Security Top 10

This skill encodes the OWASP API Security Top 10 for secure API design, code review, and vulnerability prevention. References are loaded per risk (progressive disclosure).

Based on OWASP API Security Top 10:2023.

## When to Read Which Reference

| Risk | Read |
|------|------|
| API1 Broken Object Level Authorization | [references/api1-broken-object-level-authorization.md](references/api1-broken-object-level-authorization.md) |
| API2 Broken Authentication | [references/api2-broken-authentication.md](references/api2-broken-authentication.md) |
| API3 Broken Object Property Level Authorization | [references/api3-broken-object-property-authorization.md](references/api3-broken-object-property-authorization.md) |
| API4 Unrestricted Resource Consumption | [references/api4-unrestricted-resource-consumption.md](references/api4-unrestricted-resource-consumption.md) |
| API5 Broken Function Level Authorization | [references/api5-broken-function-level-authorization.md](references/api5-broken-function-level-authorization.md) |
| API6 Unrestricted Access to Sensitive Business Flows | [references/api6-sensitive-business-flows.md](references/api6-sensitive-business-flows.md) |
| API7 Server Side Request Forgery (SSRF) | [references/api7-ssrf.md](references/api7-ssrf.md) |
| API8 Security Misconfiguration | [references/api8-security-misconfiguration.md](references/api8-security-misconfiguration.md) |
| API9 Improper Inventory Management | [references/api9-improper-inventory-management.md](references/api9-improper-inventory-management.md) |
| API10 Unsafe Consumption of APIs | [references/api10-unsafe-consumption-of-apis.md](references/api10-unsafe-consumption-of-apis.md) |

## Quick Patterns

- Enforce object-level and function-level authorization on every API request; never trust client-supplied IDs without server-side checks.
- Validate and sanitize all inputs; treat third-party API responses as untrusted.
- Apply rate limiting, quotas, and cost controls to prevent abuse and DoS.
- Maintain an API inventory; retire or protect deprecated and debug endpoints.

## Workflow

1. **Object-level authorization (IDOR)** → Read [references/api1-broken-object-level-authorization.md](references/api1-broken-object-level-authorization.md).
2. **Authentication and tokens** → Read [references/api2-broken-authentication.md](references/api2-broken-authentication.md).
3. **Rate limiting / DoS** → Read [references/api4-unrestricted-resource-consumption.md](references/api4-unrestricted-resource-consumption.md).
4. **Admin vs user endpoints** → Read [references/api5-broken-function-level-authorization.md](references/api5-broken-function-level-authorization.md).
5. **User-supplied URLs in API** → Read [references/api7-ssrf.md](references/api7-ssrf.md).
6. **Third-party API consumption** → Read [references/api10-unsafe-consumption-of-apis.md](references/api10-unsafe-consumption-of-apis.md).

Load reference files only when relevant to the task.
