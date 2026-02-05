# SL1 – Injection (Serverless)

## Summary

Event data (e.g. API body, queue message) used unsafely in queries, commands, or downstream services. Validate and sanitize all event input.

## Prevention

Use parameterized queries; validate event schema; allowlist inputs. Never concatenate event data into commands or queries.

## Testing

Fuzz event payloads; test for injection into DB, OS, or downstream APIs.
