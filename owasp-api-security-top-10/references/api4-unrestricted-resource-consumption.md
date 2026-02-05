# API4:2023 – Unrestricted Resource Consumption

## Summary

APIs can be exploited to consume excessive resources (bandwidth, CPU, memory, storage), leading to DoS or increased cost. Lack of rate limiting, quotas, or payload size limits enables abuse.

## Key CWEs

- CWE-400 Uncontrolled Resource Consumption
- CWE-799 Improper Control of Interaction Frequency

## Root Causes

- No rate limiting, quotas, or max payload size; expensive operations not throttled.

## Prevention Checklist

- Apply rate limiting per client/user and per endpoint; set quotas for expensive operations.
- Limit request/response size; limit array length and depth; timeout long-running operations.
- Monitor and alert on unusual consumption; use cost controls in serverless/cloud.

## Secure Patterns

- Implement rate limiting at API gateway or app layer (e.g. token bucket, per-user limits).
- Define max payload size and validate before processing; use streaming for large bodies where appropriate.

## Examples

### Wrong - No rate limiting

```python
@app.post("/api/search")
def search():
    # Unlimited requests - can be abused for DoS or scraping
    query = request.json.get("query")
    return expensive_search(query)
```

### Right - Rate limiting with slowapi

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/search")
@limiter.limit("30/minute")
def search():
    query = request.json.get("query")
    return expensive_search(query)

# Per-user rate limiting for authenticated endpoints
def get_user_id(request):
    return request.state.user.id if hasattr(request.state, "user") else get_remote_address(request)

@app.post("/api/export")
@limiter.limit("5/hour", key_func=get_user_id)
def export_data():
    return generate_export(request.state.user.id)
```

### Wrong - No payload size limit

```python
@app.post("/api/upload")
def upload():
    # No size limit - attacker can send 10GB payload
    data = request.json
    process(data)
```

### Right - Payload size limits

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

MAX_BODY_SIZE = 1 * 1024 * 1024  # 1MB

class LimitBodySizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_BODY_SIZE:
            return JSONResponse({"error": "Payload too large"}, status_code=413)
        return await call_next(request)

app.add_middleware(LimitBodySizeMiddleware)
```

### Wrong - Unbounded array/depth

```python
@app.post("/api/process")
def process():
    data = request.json
    # data["items"] could contain millions of items
    for item in data.get("items", []):
        expensive_operation(item)
```

### Right - Limit array size and nesting

```python
from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    id: str
    value: int

class ProcessRequest(BaseModel):
    items: List[Item] = Field(..., max_length=100)  # Max 100 items

@app.post("/api/process")
def process(data: ProcessRequest):
    for item in data.items:
        expensive_operation(item)
```

### Rate limiting strategies

| Strategy | Use Case | Example |
|----------|----------|---------|
| Per-IP | Anonymous endpoints | 100 req/min per IP |
| Per-user | Authenticated endpoints | 1000 req/min per user |
| Per-endpoint | Expensive operations | 10 exports/hour |
| Sliding window | Smooth distribution | No burst spikes |
| Token bucket | Allow short bursts | Burst of 20, then 5/sec |

### Resource limits checklist

- [ ] Rate limiting on all endpoints
- [ ] Request body size limit (e.g., 1-10MB)
- [ ] Array length limits in schemas
- [ ] Query timeout for database operations
- [ ] Pagination with max page size
- [ ] File upload size limits
- [ ] Cost monitoring and alerts

## Testing

- Test rate limits and quotas; send oversized or deeply nested payloads; verify timeouts and cost controls.
