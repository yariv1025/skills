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

## Examples

### Wrong - Unvalidated URL fetch

```python
import requests

@app.post("/fetch")
def fetch_url():
    url = request.json.get("url")
    # Attacker can reach internal services or cloud metadata
    # url = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    response = requests.get(url)
    return response.text
```

### Right - Allowlist and validation

```python
import requests
from urllib.parse import urlparse
import ipaddress

ALLOWED_HOSTS = {"cdn.example.com", "api.trusted.com"}

def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        
        # Only allow HTTPS
        if parsed.scheme != "https":
            return False
        
        # Check against allowlist
        if parsed.hostname not in ALLOWED_HOSTS:
            return False
        
        # Additional: resolve and check IP is not internal
        # (handles DNS rebinding partially)
        return True
    except Exception:
        return False

@app.post("/fetch")
def fetch_url():
    url = request.json.get("url")
    if not is_safe_url(url):
        return {"error": "URL not allowed"}, 400
    response = requests.get(url, timeout=5)
    return response.text
```

### Right - Block internal IP ranges

```python
import socket
import ipaddress

BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # Link-local / cloud metadata
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]

def is_internal_ip(hostname: str) -> bool:
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(hostname))
        return any(ip in network for network in BLOCKED_NETWORKS)
    except Exception:
        return True  # Fail closed

@app.post("/fetch")
def fetch_url():
    url = request.json.get("url")
    parsed = urlparse(url)
    
    if is_internal_ip(parsed.hostname):
        return {"error": "Internal URLs not allowed"}, 400
    
    # Proceed with request
```

### Right - Indirect reference pattern

```python
# Instead of accepting arbitrary URLs, use predefined options
WEBHOOK_ENDPOINTS = {
    "slack": "https://hooks.slack.com/services/xxx",
    "teams": "https://outlook.office.com/webhook/xxx",
    "discord": "https://discord.com/api/webhooks/xxx",
}

@app.post("/notify")
def send_notification():
    endpoint_key = request.json.get("endpoint")  # "slack", "teams", etc.
    message = request.json.get("message")
    
    if endpoint_key not in WEBHOOK_ENDPOINTS:
        return {"error": "Unknown endpoint"}, 400
    
    # Server controls the actual URL
    url = WEBHOOK_ENDPOINTS[endpoint_key]
    requests.post(url, json={"text": message})
    return {"status": "sent"}
```

### Blocked IP ranges reference

| Range | Description |
|-------|-------------|
| `10.0.0.0/8` | Private (RFC 1918) |
| `172.16.0.0/12` | Private (RFC 1918) |
| `192.168.0.0/16` | Private (RFC 1918) |
| `127.0.0.0/8` | Loopback |
| `169.254.169.254/32` | Cloud metadata (AWS, GCP, Azure) |
| `169.254.0.0/16` | Link-local |
| `0.0.0.0/8` | "This" network |
| `::1/128` | IPv6 loopback |
| `fc00::/7` | IPv6 private |

## Testing / Detection

- Test with internal IPs, localhost, and cloud metadata URLs; try different schemes (file, gopher, etc.).
- DAST/SSRF-specific checks; review all server-side HTTP clients for user input.
- See also A01 for access control and 2025 placement of SSRF.
