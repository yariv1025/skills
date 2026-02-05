# API5:2023 – Broken Function Level Authorization

## Summary

Complex access control policies and unclear separation between administrative and regular functions allow attackers to access unauthorized endpoints (e.g. calling admin APIs as a regular user).

## Key CWEs

- CWE-284 Improper Access Control
- CWE-285 Improper Authorization

## Root Causes

- Missing role/scope checks on sensitive endpoints; admin endpoints reachable without proper authorization.
- Relying on client to hide or disable admin UI without server-side enforcement.

## Prevention Checklist

- Enforce function-level (endpoint-level) authorization; deny by default.
- Clearly separate admin and user endpoints; require elevated role/scope for admin operations.
- Apply consistent authorization middleware; audit all routes for required permissions.

## Secure Patterns

- Decorate or annotate routes with required roles/scopes; enforce in middleware before handler.
- Prefer explicit deny for sensitive operations unless principal has required permission.

## Examples

### Wrong - No role check on admin endpoint

```python
@app.delete("/api/admin/users/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    # Any authenticated user can delete users!
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return {"status": "deleted"}
```

### Right - Role-based authorization decorator

```python
from functools import wraps

def require_role(role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if role not in current_user.roles:
                raise HTTPException(403, f"Requires {role} role")
            return func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

@app.delete("/api/admin/users/{user_id}")
@require_role("admin")
def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return {"status": "deleted"}
```

### Right - Centralized authorization middleware

```python
# Define permissions per route
ROUTE_PERMISSIONS = {
    ("DELETE", "/api/admin/users/{user_id}"): ["admin"],
    ("POST", "/api/admin/config"): ["admin"],
    ("GET", "/api/reports"): ["admin", "analyst"],
}

@app.middleware("http")
async def check_function_authorization(request: Request, call_next):
    # Get route pattern and method
    route_key = (request.method, get_route_pattern(request))
    required_roles = ROUTE_PERMISSIONS.get(route_key)
    
    if required_roles:
        user = request.state.user
        if not any(role in user.roles for role in required_roles):
            return JSONResponse({"error": "Forbidden"}, status_code=403)
    
    return await call_next(request)
```

### Wrong - Security by obscurity

```python
# "Hidden" admin endpoint - no auth, just hard to guess
@app.post("/api/internal-admin-xyz123/reset-db")
def reset_database():
    # Attacker can find this via fuzzing or leaked docs
    db.drop_all()
    db.create_all()
```

### Right - Explicit admin route group with auth

```python
from fastapi import APIRouter

admin_router = APIRouter(
    prefix="/api/admin",
    dependencies=[Depends(require_admin)],  # All routes require admin
    tags=["admin"]
)

@admin_router.post("/reset-db")
def reset_database():
    # Protected by router-level dependency
    db.drop_all()
    db.create_all()

app.include_router(admin_router)
```

## Testing

- Call admin or privileged endpoints with regular user tokens; test horizontal/vertical escalation; verify role checks.
