# M4 – Insufficient Input/Output Validation

## Summary

Unvalidated input leads to injection, XSS, or crashes; insufficient output encoding or validation exposes the app to downstream attacks.

## Prevention

- Validate and sanitize all input (user, clipboard, deep links, files); use allowlists.
- Encode output for the correct context (WebView, logs, IPC); avoid passing raw input to sensitive sinks.
- Validate data from other apps and the backend.

## Testing

- Fuzz inputs; test WebView and IPC; check for injection and XSS.
