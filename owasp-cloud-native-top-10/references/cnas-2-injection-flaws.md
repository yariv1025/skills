# CNAS-2 – Injection flaws

## Summary

SQL, NoSQL, OS command, or serverless event data injection. Cloud-native apps still process user and event input; validate and sanitize.

## Prevention

Use parameterized queries and safe APIs; validate and allowlist input; encode output. Apply to app layer, cloud events, and service-to-service input.

## Testing

Fuzz inputs and event data; test for SQLi, command injection, and event injection.
