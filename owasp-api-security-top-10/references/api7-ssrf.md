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

## Examples

### Wrong - Direct URL fetch from user input

```python
import requests

@app.post("/api/fetch-preview")
def fetch_preview():
    url = request.json.get("url")
    # Attacker can reach internal services: http://internal-admin:8080/delete-all
    # Or cloud metadata: http://169.254.169.254/latest/meta-data/
    response = requests.get(url, timeout=5)
    return {"preview": response.text[:500]}
```

### Right - URL validation with allowlist

```python
from urllib.parse import urlparse
import ipaddress
import socket

ALLOWED_HOSTS = {"images.example.com", "cdn.trusted.com"}
BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def validate_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        
        # Only allow HTTPS
        if parsed.scheme != "https":
            return False
        
        # Check against allowlist
        if parsed.hostname not in ALLOWED_HOSTS:
            return False
        
        # Resolve and check IP is not internal
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
        if any(ip in network for network in BLOCKED_NETWORKS):
            return False
        
        return True
    except Exception:
        return False

@app.post("/api/fetch-preview")
def fetch_preview():
    url = request.json.get("url")
    if not validate_url(url):
        raise HTTPException(400, "URL not allowed")
    
    response = requests.get(url, timeout=5)
    return {"preview": response.text[:500]}
```

### Right - Indirect reference pattern

```python
# User selects from predefined options, not arbitrary URLs
IMAGE_SOURCES = {
    "unsplash": "https://api.unsplash.com/photos/random",
    "placeholder": "https://via.placeholder.com/150",
    "company_cdn": "https://cdn.company.com/images",
}

@app.post("/api/fetch-image")
def fetch_image(source: str, image_id: str):
    if source not in IMAGE_SOURCES:
        raise HTTPException(400, "Invalid source")
    
    # Server controls the base URL
    base_url = IMAGE_SOURCES[source]
    # Validate image_id format
    if not image_id.isalnum():
        raise HTTPException(400, "Invalid image ID")
    
    response = requests.get(f"{base_url}/{image_id}", timeout=5)
    return response.content
```

### Right - Webhook with signature verification

```python
# For webhooks, verify the sender instead of accepting arbitrary URLs
import hmac

@app.post("/api/webhook/stripe")
def handle_stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    
    # Verify webhook is from Stripe, not attacker
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    
    process_event(event)
    return {"status": "ok"}
```

## Testing

- Supply internal IPs, localhost, cloud metadata URLs; try different schemes; verify outbound requests are restricted.
