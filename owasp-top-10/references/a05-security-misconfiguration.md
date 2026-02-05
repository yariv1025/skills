# A05:2021 – Security Misconfiguration

## Summary

Security misconfiguration includes insecure default configs, unnecessary features enabled, default credentials, verbose errors, and missing security headers. Very common; often the result of incomplete hardening or copy-paste deployment.

## Key CWEs

- CWE-16 Configuration
- CWE-611 XML External Entity (XXE)
- CWE-756 Missing Custom Error Page
- CWE-209 Generation of Error Message Containing Sensitive Information

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/) for the full list.*

## Root Causes / Triggers

- Default credentials or default config left in place.
- Unnecessary features, debug endpoints, or sample apps enabled in production.
- Missing or weak security headers (CSP, HSTS, X-Frame-Options, etc.).
- Verbose error messages or stack traces exposed to users.
- Outdated or unpatched frameworks and servers.

## Prevention Checklist

- Harden all environments; remove or disable unneeded features and accounts.
- Change default credentials; use strong, unique credentials per environment.
- Set secure headers (CSP, HSTS, X-Content-Type-Options, etc.) and restrict CORS.
- Use generic error pages in production; log details server-side only.
- Maintain a secure baseline (e.g. checklist or IaC) and automate checks.

## Secure Patterns

- **Headers:** Configure Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options; avoid exposing server version.
- **Errors:** Catch exceptions at boundary; return generic message to client; log full detail securely.
- **Separation:** Different config for dev/staging/prod; no debug or samples in prod.

## Examples

### Wrong - Missing security headers

```python
# Default response with no security headers
@app.get("/")
def home():
    return {"message": "Welcome"}
# Response lacks CSP, HSTS, X-Frame-Options, etc.
```

### Right - Security headers middleware

```python
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app = FastAPI(middleware=[Middleware(SecurityHeadersMiddleware)])
```

### Wrong - Debug mode in production

```python
# Flask
app.run(debug=True)  # Exposes debugger, allows code execution

# Django settings.py
DEBUG = True  # Shows detailed errors, template paths, SQL queries
```

### Right - Production configuration

```python
# Flask
app.run(debug=False)

# Django settings.py (use environment variable)
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
# In production: DEBUG=False
```

### Wrong - Default credentials

```yaml
# docker-compose.yml
services:
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: postgres  # Default/weak password
```

### Right - Strong, unique credentials

```yaml
# docker-compose.yml
services:
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    external: true  # Managed outside of compose file
```

### Security headers reference

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| `Strict-Transport-Security` | Force HTTPS | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | Prevent XSS, injection | `default-src 'self'` (customize per app) |
| `X-Content-Type-Options` | Prevent MIME sniffing | `nosniff` |
| `X-Frame-Options` | Prevent clickjacking | `DENY` or `SAMEORIGIN` |
| `Referrer-Policy` | Control referrer leakage | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Restrict browser features | `geolocation=(), camera=()` |

### Hardening checklist

- [ ] Change all default credentials
- [ ] Disable debug mode and verbose errors
- [ ] Remove sample/test applications
- [ ] Set security headers on all responses
- [ ] Disable directory listing
- [ ] Remove server version headers
- [ ] Review and restrict CORS policy
- [ ] Disable unused HTTP methods

## Testing / Detection

- Scan for default credentials and known weak configs.
- Check security headers (e.g. securityheaders.com); verify error pages.
- Automated config review and compliance (e.g. CIS benchmarks, custom checks).
