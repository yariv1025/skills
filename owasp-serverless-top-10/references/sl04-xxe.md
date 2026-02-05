# SL4 – XML External Entities (Serverless)

## Summary

XML input processed with external entity resolution enabled. Can lead to SSRF, file disclosure, or DoS. Less common in serverless but still applies if parsing XML.

## Prevention

Disable external entities; use safe XML parser options; validate and limit input size. Prefer JSON or other formats when possible.

## Testing

Send malicious XML payloads; verify parser configuration and entity resolution.
