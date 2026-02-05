# API3:2023 – Broken Object Property Level Authorization

## Summary

Lack of authorization validation at the property level leads to mass assignment, overposting, or information disclosure. APIs may expose or accept more properties than intended (e.g. role, balance, internal IDs).

## Key CWEs

- CWE-915 Improperly Controlled Modification of Object Attributes
- CWE-200 Exposure of Sensitive Information

## Root Causes

- Accepting all client-supplied fields; returning full internal objects; no allowlist for request/response.

## Prevention Checklist

- Allowlist request body properties; reject unknown or sensitive fields.
- Allowlist response properties; never expose internal or sensitive fields by default.
- Validate and sanitize property values; apply schema validation.

## Secure Patterns

- Define explicit DTOs/schemas for request and response; map only allowed fields.
- Use serialization filters or views to control what is returned per role/context.

## Examples

### Wrong - Mass assignment / overposting

```python
@app.put("/api/users/{user_id}")
def update_user(user_id: int, current_user: User = Depends(get_current_user)):
    user = User.query.get(user_id)
    # DANGER: Accepts ANY field from request body
    for key, value in request.json.items():
        setattr(user, key, value)  # Attacker can set is_admin=True, balance=1000000
    db.session.commit()
    return user
```

### Right - Explicit allowlist for updates

```python
from pydantic import BaseModel

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    # is_admin, balance, etc. NOT included - cannot be set

@app.put("/api/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, current_user: User = Depends(get_current_user)):
    user = User.query.get(user_id)
    
    # Only update allowed fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.session.commit()
    return user
```

### Wrong - Exposing internal fields in response

```python
@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = User.query.get(user_id)
    # Returns ALL fields including sensitive ones
    return user.__dict__  # password_hash, internal_notes, ssn, etc.
```

### Right - Response schema with allowed fields

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    # Excludes: password_hash, ssn, internal_notes, is_admin

    class Config:
        from_attributes = True

@app.get("/api/users/{user_id}")
def get_user(user_id: int) -> UserResponse:
    user = User.query.get(user_id)
    return UserResponse.from_orm(user)
```

### Right - Role-based response filtering

```python
class UserPublicResponse(BaseModel):
    id: int
    name: str

class UserFullResponse(UserPublicResponse):
    email: str
    phone: str
    address: str

class UserAdminResponse(UserFullResponse):
    is_admin: bool
    last_login: datetime
    login_count: int

@app.get("/api/users/{user_id}")
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    user = User.query.get(user_id)
    
    if current_user.is_admin:
        return UserAdminResponse.from_orm(user)
    elif current_user.id == user_id:
        return UserFullResponse.from_orm(user)
    else:
        return UserPublicResponse.from_orm(user)
```

## Testing

- Send extra properties in requests (overposting); check responses for PII or internal fields; test role-based visibility.
