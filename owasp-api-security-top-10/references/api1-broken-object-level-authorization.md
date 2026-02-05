# API1:2023 – Broken Object Level Authorization

## Summary

APIs expose endpoints that use object identifiers (e.g. IDs in URL or body). Without proper authorization checks, users can access or modify other users' objects (IDOR). Always verify the authenticated principal is allowed to access the requested object.

## Key CWEs

- CWE-639 Authorization Bypass Through User-Controlled Key
- CWE-284 Improper Access Control

## Root Causes

- Missing or inconsistent authorization checks per object; trusting client-supplied IDs.

## Prevention Checklist

- Enforce authorization on every request that accesses a resource by ID.
- Use server-side authorization logic; never rely on client to enforce access.
- Prefer indirect references or tokens when appropriate to reduce enumeration.

## Secure Patterns

- Before returning or modifying any object, verify: "Does the authenticated user/role have permission for this object and action?"
- Use consistent authorization layer (middleware or service) for all object access.

## Examples

### Wrong - Missing object-level authorization

```python
@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    # Any authenticated user can access any order by ID
    return Order.query.get(order_id)
```

### Right - Verify ownership before access

```python
@app.get("/api/orders/{order_id}")
def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    order = Order.query.get(order_id)
    if order is None:
        raise HTTPException(404, "Order not found")
    
    # Verify this user owns the order
    if order.user_id != current_user.id:
        raise HTTPException(403, "Access denied")
    
    return order
```

### Right - Authorization service pattern

```python
class AuthorizationService:
    def can_access(self, user: User, resource: str, resource_id: int, action: str) -> bool:
        # Centralized authorization logic
        if resource == "order":
            order = Order.query.get(resource_id)
            return order and (order.user_id == user.id or user.is_admin)
        return False

auth_service = AuthorizationService()

@app.get("/api/orders/{order_id}")
def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    if not auth_service.can_access(current_user, "order", order_id, "read"):
        raise HTTPException(403, "Access denied")
    return Order.query.get(order_id)
```

### Wrong - GraphQL without authorization

```graphql
# Anyone can query any user's data
query {
  user(id: "other-user-id") {
    email
    orders { id amount }
  }
}
```

### Right - Authorization in GraphQL resolvers

```python
@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: str, info: Info) -> User:
        current_user = info.context.user
        if id != current_user.id and not current_user.is_admin:
            raise PermissionError("Access denied")
        return User.query.get(id)
```

## Testing

- Test with different users and roles; try accessing other users' object IDs; use SAST/DAST for missing authorization.
