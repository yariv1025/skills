# A10:2021 – Server-Side Request Forgery (SSRF)

## Summary

SSRF flaws occur when the server is induced to send a request to an unintended destination, often user-supplied or derived from user input. Attackers can reach internal services, cloud metadata endpoints, or other restricted systems. In OWASP 2025, SSRF is merged into A01 Broken Access Control as an access-control issue.

## Key CWEs

- CWE-918 Server-Side Request Forgery (SSRF)
- CWE-441 Unintended Proxy or Intermediary

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/) for the full list.*

## Root Causes / Triggers

- User-controlled URL or host passed to server-side HTTP client or fetcher.
- No allowlist or validation of scheme/host/port; internal or metadata IPs allowed.
- Blind SSRF (no response to attacker) still dangerous (e.g. scanning, callback to attacker).

## Prevention Checklist

- Avoid forwarding raw user-supplied URLs to server-side requests when possible.
- If needed, use a strict allowlist of schemes (e.g. https only) and hosts/ports; block internal IP ranges and metadata (e.g. 169.254.169.254).
- Use URL parsing and validation; reject malformed or unexpected URLs.
- Segment network so app cannot reach sensitive internal services; use firewall/egress rules.
- Disable unnecessary URL-fetch features; use outbound proxy with filtering if appropriate.

## Secure Patterns

- **Allowlist:** Only allow specific hostnames or patterns needed for the feature (e.g. known CDN domains).
- **Blocklist (supplement):** Block localhost, private IP ranges, link-local, and cloud metadata IPs.
- **Design:** Prefer server-defined endpoints or indirect reference (e.g. "fetch preset 1") instead of free-form URL from client.

## Testing / Detection

- Test with internal IPs, localhost, and cloud metadata URLs; try different schemes (file, gopher, etc.).
- DAST/SSRF-specific checks; review all server-side HTTP clients for user input.
- See also A01 for access control and 2025 placement of SSRF.
