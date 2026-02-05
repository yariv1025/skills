# API4:2023 – Unrestricted Resource Consumption

## Summary

APIs can be exploited to consume excessive resources (bandwidth, CPU, memory, storage), leading to DoS or increased cost. Lack of rate limiting, quotas, or payload size limits enables abuse.

## Key CWEs

- CWE-400 Uncontrolled Resource Consumption
- CWE-799 Improper Control of Interaction Frequency

## Root Causes

- No rate limiting, quotas, or max payload size; expensive operations not throttled.

## Prevention Checklist

- Apply rate limiting per client/user and per endpoint; set quotas for expensive operations.
- Limit request/response size; limit array length and depth; timeout long-running operations.
- Monitor and alert on unusual consumption; use cost controls in serverless/cloud.

## Secure Patterns

- Implement rate limiting at API gateway or app layer (e.g. token bucket, per-user limits).
- Define max payload size and validate before processing; use streaming for large bodies where appropriate.

## Testing

- Test rate limits and quotas; send oversized or deeply nested payloads; verify timeouts and cost controls.
