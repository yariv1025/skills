# API8:2023 – Security Misconfiguration

## Summary

Complex API configurations often have security gaps: unnecessary HTTP methods, permissive CORS, default credentials, verbose errors, or exposed debug endpoints. Harden all environments and follow secure baseline.

## Key CWEs

- CWE-16 Configuration
- CWE-756 Missing Custom Error Page

## Root Causes

- Default or permissive config; debug or admin endpoints enabled in production; missing security headers.

## Prevention Checklist

- Disable unnecessary HTTP methods; restrict CORS to needed origins.
- Remove or protect debug and admin endpoints; use strong credentials.
- Set security headers (e.g. CSP, HSTS); return generic errors to clients; log details server-side.
- Maintain secure baseline (checklist or IaC); automate config checks.

## Secure Patterns

- Explicitly allow only required methods per route; deny by default.
- Separate config per environment; no debug or samples in production.

## Examples

### Wrong - Permissive CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Any origin!
    allow_credentials=True,  # With cookies!
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Right - Restrictive CORS

```python
ALLOWED_ORIGINS = [
    "https://app.example.com",
    "https://admin.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Wrong - Debug enabled in production

```python
# FastAPI
app = FastAPI(debug=True)  # Exposes stack traces

# Django
DEBUG = True  # Shows detailed errors

# Flask
app.run(debug=True)  # Enables debugger
```

### Right - Environment-based configuration

```python
import os

DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

app = FastAPI(
    debug=DEBUG,
    docs_url="/docs" if ENVIRONMENT != "production" else None,  # Disable Swagger in prod
    redoc_url=None,
)

# Custom error handler for production
if not DEBUG:
    @app.exception_handler(Exception)
    async def generic_error_handler(request, exc):
        logger.error(f"Unhandled error: {exc}", exc_info=True)
        return JSONResponse(
            {"error": "Internal server error"},
            status_code=500
        )
```

### Wrong - Unnecessary HTTP methods

```python
# All methods enabled by default - allows PUT/DELETE on read-only endpoint
@app.route("/api/reports/{report_id}")
def get_report(report_id: int):
    return Report.query.get(report_id)
```

### Right - Explicit method restriction

```python
@app.get("/api/reports/{report_id}")  # Only GET allowed
def get_report(report_id: int):
    return Report.query.get(report_id)

# Or with method list
@app.api_route("/api/data", methods=["GET", "HEAD"])
def get_data():
    return {"data": "value"}
```

### API security headers

```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    # Remove server version
    response.headers.pop("Server", None)
    return response
```

### API hardening checklist

| Check | Action |
|-------|--------|
| CORS | Allowlist specific origins |
| Debug mode | Disable in production |
| API docs | Disable or protect in production |
| HTTP methods | Restrict to needed methods per route |
| Error messages | Generic to client, detailed in logs |
| Security headers | Add X-Content-Type-Options, etc. |
| Server header | Remove or obscure version info |
| Default credentials | Change all defaults |

## Testing

- Scan for open methods, permissive CORS, default credentials; check security headers and error responses.
