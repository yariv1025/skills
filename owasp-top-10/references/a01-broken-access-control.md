# A01:2021 – Broken Access Control

## Summary

Access control enforces policy so users cannot act outside their intended permissions. Failures lead to vertical or horizontal privilege escalation, path traversal, IDOR, CORS misuse, or force browsing. SSRF is also an access-control concern (OWASP 2025 merges SSRF into this category).

## Key CWEs

- CWE-284 Improper Access Control
- CWE-285 Improper Authorization
- CWE-639 Authorization Bypass Through User-Controlled Key
- CWE-22 Path Traversal
- CWE-918 SSRF (see also [a10-ssrf.md](a10-ssrf.md))

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) for the full list.*

## Root Causes / Triggers

- Missing or inconsistent authorization checks (e.g. per object or per action).
- Trusting client-supplied identifiers (IDs, paths) without server-side verification.
- Default allow or overly broad CORS/headers.
- Forced browsing to URLs that are not linked but are reachable.

## Prevention Checklist

- Deny by default; enforce authorization on every request for the resource and action.
- Check object-level access (user owns or is allowed the resource) using server-side state.
- Avoid exposing internal IDs or paths in URLs when possible; use indirect references or tokens.
- Validate and sanitize path inputs; use allowlists for file operations.
- Configure CORS and security headers restrictively.
- Log and monitor access control failures.

## Secure Patterns

- **Authorization check:** Before returning any resource, verify the authenticated principal is allowed for that resource and action (e.g. "can user X read document Y?").
- **Indirect reference:** Map a random token to an internal ID so clients cannot enumerate or guess others’ resources.
- **Path traversal:** Use a safe base directory and resolve paths within it; reject ".." and absolute paths.

## Examples

### Wrong - Missing authorization check (IDOR)

```python
@app.get("/api/documents/{doc_id}")
def get_document(doc_id: int):
    # Anyone can access any document by guessing/enumerating IDs
    return Document.query.get(doc_id)
```

### Right - Authorization check before access

```python
@app.get("/api/documents/{doc_id}")
def get_document(doc_id: int, current_user: User = Depends(get_current_user)):
    doc = Document.query.get(doc_id)
    if doc is None:
        raise HTTPException(404, "Not found")
    # Check ownership or permission
    if doc.owner_id != current_user.id and not current_user.has_permission("view_all_docs"):
        raise HTTPException(403, "Access denied")
    return doc
```

### Wrong - Path traversal vulnerability

```python
@app.get("/files/{filename}")
def get_file(filename: str):
    # Attacker can use ../../../etc/passwd
    return FileResponse(f"/var/uploads/{filename}")
```

### Right - Safe path handling

```python
import os
from pathlib import Path

UPLOAD_DIR = Path("/var/uploads").resolve()

@app.get("/files/{filename}")
def get_file(filename: str):
    # Resolve and verify path stays within allowed directory
    safe_path = (UPLOAD_DIR / filename).resolve()
    if not safe_path.is_relative_to(UPLOAD_DIR):
        raise HTTPException(400, "Invalid path")
    if not safe_path.exists():
        raise HTTPException(404, "Not found")
    return FileResponse(safe_path)
```

### Wrong - Overly permissive CORS

```python
# Allows any origin to make credentialed requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)
```

### Right - Restrictive CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Testing / Detection

- Test with different roles and users (horizontal/vertical escalation).
- Try modifying IDs and path parameters to access others’ data.
- Use SAST/DAST rules for missing authorization and path traversal.
- Review CORS and security headers.
