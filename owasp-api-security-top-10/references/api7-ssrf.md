# API7:2023 – Server Side Request Forgery (SSRF)

## Summary

APIs that fetch remote resources based on user-supplied URIs can be abused to make the server send requests to internal services, cloud metadata, or attacker-controlled hosts. Validate and restrict all user-supplied URLs.

## Key CWEs

- CWE-918 Server-Side Request Forgery (SSRF)

## Root Causes

- User-controlled URL or host passed to server-side HTTP client without validation; internal IPs or metadata endpoints not blocked.

## Prevention Checklist

- Allowlist allowed schemes (e.g. https only) and hostnames/ports; block internal IP ranges and cloud metadata (e.g. 169.254.169.254).
- Use URL parsing and validation; reject malformed or unexpected URLs.
- Segment network so API cannot reach sensitive internal services.

## Secure Patterns

- Prefer server-defined endpoints or indirect reference (e.g. "fetch from CDN 1") instead of free-form URL.
- If user URL is required, validate scheme and host against allowlist; block private/metadata ranges.

## Testing

- Supply internal IPs, localhost, cloud metadata URLs; try different schemes; verify outbound requests are restricted.
