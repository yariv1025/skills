# SL8 – Insecure Deserialization (Serverless)

## Summary

Deserializing event or queue data without validation. Can lead to RCE or abuse if format allows object injection. Validate and use safe formats.

## Prevention

Prefer JSON with schema validation; avoid deserializing to executable types. If deserialization required, use allowlists and minimal types; never from untrusted source without validation.

## Testing

Send malicious serialized payloads in event; verify validation and safe parsing.
