# SL5 – Broken Access Control (Serverless)

## Summary

Functions or resources accessible to callers who should not have access. Over-permissive IAM or missing authorization checks on event data.

## Prevention

Apply least privilege to function role; authorize per request (e.g. user can access only their resources). Validate resource IDs and scope in event; use IAM and API auth.

## Testing

Attempt cross-tenant or cross-resource access; verify IAM and in-function auth checks.
