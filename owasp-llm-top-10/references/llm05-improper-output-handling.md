# LLM05 – Improper Output Handling

## Summary

Treating LLM output as trusted can lead to XSS, SSRF, or code execution when output is reflected or used in sensitive operations.

## Prevention

- Treat all LLM output as untrusted; validate and encode for context (HTML, URL, code). Use allowlists for actions and data; never pass raw output to eval, redirect, or SQL.

## Testing

- Inject payloads via prompt to generate malicious output; verify output encoding and validation.
