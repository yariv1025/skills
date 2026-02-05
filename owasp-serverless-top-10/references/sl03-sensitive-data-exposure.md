# SL3 – Sensitive Data Exposure (Serverless)

## Summary

Secrets or PII in environment variables, logs, or responses. Cold start and reuse can leak data across invocations if not isolated.

## Prevention

Use secret manager; never log secrets; redact PII in logs. Isolate sensitive data per invocation; encrypt at rest; minimize env vars.

## Testing

Check env, logs, and responses for secrets and PII; verify cold start isolation.
