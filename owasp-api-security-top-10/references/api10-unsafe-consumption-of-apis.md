# API10:2023 – Unsafe Consumption of APIs

## Summary

Developers often trust third-party API data more than user input and adopt weaker security standards. Data from external APIs can be malicious or spoofed; treat it as untrusted and validate/sanitize.

## Key CWEs

- CWE-20 Improper Input Validation
- CWE-829 Inclusion of Functionality from Untrusted Control Sphere

## Root Causes

- Trusting third-party API responses without validation; passing API data to sensitive sinks (e.g. eval, redirect, SQL).
- No integrity or authenticity checks on consumed APIs.

## Prevention Checklist

- Validate and sanitize all data from third-party APIs; apply same rigor as user input.
- Use allowlists and schema validation; do not pass API response data directly to sensitive operations.
- Verify TLS and authenticity of consumed APIs; prefer signed or verified data when available.

## Secure Patterns

- Define schemas for consumed API responses; validate before use; map to internal types.
- Never use third-party response data in redirects, SQL, or HTML without encoding/validation.

## Examples

### Wrong - Trusting third-party API response

```python
import requests

def get_weather(city: str):
    # Third-party API response used directly
    response = requests.get(f"https://weather-api.com/v1/{city}")
    data = response.json()
    
    # DANGER: API response used in SQL
    cursor.execute(f"INSERT INTO weather_cache (city, temp) VALUES ('{data['city']}', {data['temp']})")
    
    # DANGER: API response rendered in HTML
    return f"<h1>Weather for {data['city']}</h1>"
```

### Right - Validate and sanitize third-party data

```python
import requests
from pydantic import BaseModel, validator
import html

class WeatherResponse(BaseModel):
    city: str
    temp: float
    humidity: int
    
    @validator("city")
    def validate_city(cls, v):
        if not v.isalnum() or len(v) > 100:
            raise ValueError("Invalid city name")
        return v
    
    @validator("temp")
    def validate_temp(cls, v):
        if not -100 <= v <= 60:
            raise ValueError("Invalid temperature")
        return v

def get_weather(city: str):
    response = requests.get(
        f"https://weather-api.com/v1/{city}",
        timeout=5
    )
    response.raise_for_status()
    
    # Validate against schema
    try:
        data = WeatherResponse(**response.json())
    except Exception as e:
        logger.error(f"Invalid weather API response: {e}")
        raise HTTPException(502, "Weather service error")
    
    # Safe SQL with parameters
    cursor.execute(
        "INSERT INTO weather_cache (city, temp) VALUES (?, ?)",
        (data.city, data.temp)
    )
    
    # Safe HTML with encoding
    return f"<h1>Weather for {html.escape(data.city)}</h1>"
```

### Wrong - Following redirects from API response

```python
def fetch_document(doc_url: str):
    # Third-party API returns redirect URL
    api_response = requests.get(f"https://api.example.com/docs/{doc_url}")
    redirect_url = api_response.json()["download_url"]
    
    # DANGER: Open redirect - attacker can point to malicious site
    return redirect(redirect_url)
```

### Right - Validate redirect URLs

```python
from urllib.parse import urlparse

ALLOWED_DOWNLOAD_HOSTS = {"cdn.trusted.com", "storage.example.com"}

def fetch_document(doc_url: str):
    api_response = requests.get(f"https://api.example.com/docs/{doc_url}")
    redirect_url = api_response.json().get("download_url", "")
    
    # Validate URL before redirect
    parsed = urlparse(redirect_url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_DOWNLOAD_HOSTS:
        raise HTTPException(400, "Invalid download URL")
    
    return redirect(redirect_url)
```

### Right - Verify API authenticity

```python
import hmac
import hashlib

def consume_webhook(payload: bytes, signature: str):
    # Verify webhook signature from third-party
    expected_sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_sig):
        raise HTTPException(401, "Invalid signature")
    
    # Now safe to process
    data = json.loads(payload)
    process_webhook(data)
```

### Right - Timeout and error handling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_api_client():
    session = requests.Session()
    
    # Retry strategy
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    
    return session

def call_third_party_api(endpoint: str):
    client = create_api_client()
    try:
        response = client.get(
            f"https://api.third-party.com/{endpoint}",
            timeout=(5, 30),  # (connect, read) timeouts
            verify=True  # Verify TLS
        )
        response.raise_for_status()
        return validate_response(response.json())
    except requests.RequestException as e:
        logger.error(f"Third-party API error: {e}")
        raise HTTPException(502, "External service unavailable")
```

### Third-party API security checklist

| Check | Action |
|-------|--------|
| TLS | Always use HTTPS, verify certificates |
| Timeout | Set connect and read timeouts |
| Validation | Schema validate all responses |
| Encoding | Escape before SQL, HTML, commands |
| Redirects | Allowlist redirect destinations |
| Authentication | Verify signatures/tokens when available |
| Error handling | Don't expose third-party errors to users |

## Testing

- Fuzz or mock malicious third-party responses; verify validation and encoding; test for injection and open redirect.
