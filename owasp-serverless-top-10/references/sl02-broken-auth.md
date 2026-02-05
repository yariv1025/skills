# SL2 – Broken Authentication (Serverless)

## Summary

Weak or missing auth for function invocation (e.g. API Gateway, event source). Unauthorized callers can invoke functions or access data.

## Prevention

Enforce auth at API Gateway and event sources; validate tokens and signatures. Use IAM and resource policies; avoid public invoke where not required.

## Testing

Attempt unauthenticated or cross-tenant invocation; verify token and IAM checks.
