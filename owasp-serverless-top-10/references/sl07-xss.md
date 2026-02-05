# SL7 – XSS (Serverless)

## Summary

User input reflected in responses without encoding. If function returns HTML or feeds a front end, XSS can occur. Encode output for context.

## Prevention

Encode all user-controlled data in output (HTML, JSON, etc.). Use framework escaping; set Content-Type and CSP headers; avoid raw reflection.

## Testing

Inject script payloads in input; verify encoding and CSP in response.
