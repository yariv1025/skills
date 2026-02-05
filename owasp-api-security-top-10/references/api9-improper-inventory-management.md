# API9:2023 – Improper Inventory Management

## Summary

Poor documentation and tracking of API endpoints and versions expose deprecated or debug endpoints, undocumented parameters, or old API versions that lack security updates. Maintain an accurate API inventory.

## Key CWEs

- CWE-1059 Insufficient Technical Documentation
- CWE-1102 Reliance on Machine Readable Data or Metadata

## Root Causes

- No inventory of endpoints; deprecated or debug endpoints still reachable; documentation out of date.
- Old API versions not retired or protected.

## Prevention Checklist

- Maintain and publish accurate API inventory (OpenAPI/Swagger); document all endpoints and versions.
- Retire or protect deprecated endpoints; disable debug endpoints in production.
- Version APIs explicitly; plan deprecation and sunset; monitor usage of old versions.

## Secure Patterns

- Use API gateway or routing to expose only documented, supported versions.
- Regular audits: compare deployed routes to inventory; remove or protect undocumented endpoints.

## Examples

### Wrong - Forgotten debug endpoints

```python
# Left in production - not in documentation
@app.get("/api/debug/users")
def debug_list_users():
    return [u.__dict__ for u in User.query.all()]

@app.post("/api/debug/reset-db")
def debug_reset():
    db.drop_all()
    db.create_all()

# Old version still accessible
@app.get("/api/v1/users/{user_id}")  # v1 has no auth!
def get_user_v1(user_id: int):
    return User.query.get(user_id)
```

### Right - Explicit route registration with inventory

```python
# Generate OpenAPI from code - single source of truth
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="My API",
    version="2.0.0",
    openapi_tags=[
        {"name": "users", "description": "User operations"},
        {"name": "orders", "description": "Order operations"},
    ]
)

# All routes documented
@app.get("/api/v2/users/{user_id}", tags=["users"])
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    """Get a user by ID. Requires authentication."""
    return User.query.get(user_id)

# No debug routes in production
if os.environ.get("ENVIRONMENT") != "production":
    @app.get("/api/debug/health", include_in_schema=False)
    def debug_health():
        return {"status": "ok"}
```

### Right - API versioning with deprecation

```python
from fastapi import APIRouter, Header
from datetime import datetime

v2_router = APIRouter(prefix="/api/v2")
v3_router = APIRouter(prefix="/api/v3")

# Deprecated version with warning header
@v2_router.get("/users/{user_id}")
def get_user_v2(user_id: int):
    response = User.query.get(user_id)
    headers = {
        "Deprecation": "true",
        "Sunset": "2024-12-31",
        "Link": '</api/v3/users>; rel="successor-version"'
    }
    return JSONResponse(content=response, headers=headers)

# Current version
@v3_router.get("/users/{user_id}")
def get_user_v3(user_id: int, current_user: User = Depends(get_current_user)):
    return User.query.get(user_id)

app.include_router(v2_router)
app.include_router(v3_router)
```

### Right - Route audit script

```python
# Script to compare deployed routes to OpenAPI spec
import requests
from fastapi.openapi.utils import get_openapi

def audit_routes():
    # Get documented routes from OpenAPI
    openapi = get_openapi(app=app, title="API", version="1.0")
    documented = set()
    for path, methods in openapi["paths"].items():
        for method in methods:
            documented.add((method.upper(), path))
    
    # Get actual deployed routes
    deployed = set()
    for route in app.routes:
        if hasattr(route, "methods"):
            for method in route.methods:
                deployed.add((method, route.path))
    
    # Find undocumented routes
    undocumented = deployed - documented
    if undocumented:
        print("WARNING: Undocumented routes found:")
        for method, path in undocumented:
            print(f"  {method} {path}")
    
    return len(undocumented) == 0

# Run in CI/CD
assert audit_routes(), "Undocumented routes detected"
```

### API inventory checklist

| Item | Action |
|------|--------|
| OpenAPI spec | Keep in sync with code |
| Version policy | Document supported versions |
| Deprecation | Add headers, set sunset date |
| Debug endpoints | Remove or protect in prod |
| Old versions | Retire or add auth if missing |
| Audit | Compare spec to deployed routes |

## Testing

- Enumerate endpoints (e.g. common paths, version suffixes); check for undocumented or deprecated endpoints; verify documentation matches implementation.
