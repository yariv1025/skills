# Specialized Roles for Self-Review

Role personas for thorough code review. Apply relevant roles after every code edit.

## Table of Contents

1. [Overview](#overview)
2. [Role Definitions](#role-definitions)
3. [When to Apply Each Role](#when-to-apply-each-role)
4. [Output Format](#output-format)
5. [Examples](#examples)

---

## Overview

Instead of generic "review this code," apply specific reviewer personas. Each role has a defined focus and output format.

**Rule:** No response that edits code is valid without listing what changed and how it was verified.

---

## Role Definitions

### 1. Plan Architect

**Focus:** High-level design, task breakdown, risk identification

**Output:**
- Plan with phases and milestones
- Task checklist with dependencies
- Risks and mitigations
- Impacted files list
- Success criteria

**When to use:** Before starting non-trivial work, when scoping a feature, when the approach is unclear.

---

### 2. Code Reviewer (Architecture)

**Focus:** Code quality, design patterns, maintainability

**Output:**
- SOLID principle violations
- Layering/separation of concerns issues
- API design problems
- Edge cases not handled
- Maintainability concerns
- Suggested refactors

**Checklist:**
- [ ] Single Responsibility: Does each unit do one thing?
- [ ] Open/Closed: Can it be extended without modification?
- [ ] Liskov Substitution: Are subtypes substitutable?
- [ ] Interface Segregation: Are interfaces minimal?
- [ ] Dependency Inversion: Are dependencies abstracted?
- [ ] Naming: Are names clear and consistent?
- [ ] Complexity: Is cyclomatic complexity reasonable?
- [ ] Duplication: Is there unnecessary repetition?

**When to use:** After implementing any code, during refactoring, before merging.

---

### 3. Test Engineer

**Focus:** Test coverage, test quality, failure scenarios

**Output:**
- Test plan (what to test)
- Missing tests identified
- Suggested fixtures and mocks
- Failure scenarios to cover
- Edge cases for parametrization
- CI/CD considerations

**Checklist:**
- [ ] Happy path covered?
- [ ] Error cases covered?
- [ ] Edge cases covered (empty, null, max, min)?
- [ ] Boundary conditions tested?
- [ ] Integration points mocked appropriately?
- [ ] Tests isolated (no shared state)?
- [ ] Tests deterministic (no flakiness)?
- [ ] Performance-sensitive paths benchmarked?

**When to use:** After implementing features, before marking work complete, when tests are failing.

---

### 4. Security Reviewer

**Focus:** Security vulnerabilities, attack surfaces, secure coding

**Output:**
- Input validation gaps
- Injection surfaces (SQL, command, XSS, etc.)
- Secrets handling issues
- Authentication/authorization gaps
- SSRF/file handling risks
- Recommended fixes with priority

**Checklist:**
- [ ] Input validated at boundaries?
- [ ] Output encoded/escaped appropriately?
- [ ] SQL uses parameterized queries?
- [ ] No command injection (shell=True, string concat)?
- [ ] No path traversal vulnerabilities?
- [ ] Secrets not in code or logs?
- [ ] Authentication required where needed?
- [ ] Authorization checks in place?
- [ ] HTTPS/TLS for sensitive data?
- [ ] Error messages don't leak info?

**When to use:** For any code handling user input, authentication, file operations, external calls, or sensitive data.

---

### 5. Build/Fail Fixer

**Focus:** Fixing build failures, lint errors, test failures

**Output:**
- Ordered list of failures (by priority)
- Root cause for each failure
- Minimal fix for each
- Verification commands
- Regression prevention notes

**Process:**
1. List all failures
2. Identify root causes
3. Fix in dependency order (if A depends on B, fix B first)
4. Verify each fix before moving on
5. Run full validation at end

**When to use:** When builds fail, tests fail, linting fails, or imports break.

---

## When to Apply Each Role

| Situation | Roles to Apply |
|-----------|---------------|
| Starting new feature | Plan Architect |
| After implementing code | Code Reviewer + Security Reviewer |
| After writing tests | Test Engineer |
| Handling user input | Security Reviewer |
| Build/lint/test failures | Build/Fail Fixer |
| Before marking complete | Code Reviewer + Test Engineer + Security Reviewer |
| Refactoring existing code | Code Reviewer |
| Performance optimization | Code Reviewer (Architecture focus) |

**Typical post-edit sequence:**
1. Build/Fail Fixer (if any errors)
2. Code Reviewer (Architecture)
3. Security Reviewer (if applicable)
4. Test Engineer (if tests involved)

---

## Output Format

### Summary Format

After applying roles, output a summary:

```
## Self-Review Summary

**Roles Applied:** Code Reviewer, Security Reviewer

### Code Reviewer Findings
- ✓ SOLID principles followed
- ✓ Clear separation of concerns
- ⚠ Suggestion: Extract validation logic to separate function
- ✗ Issue: Magic number on line 42 (use named constant)

### Security Reviewer Findings
- ✓ Input validated at boundary
- ✓ Parameterized SQL queries
- ✓ No secrets in code
- ⚠ Consider: Add rate limiting for auth endpoints

### Actions Taken
- Fixed: Magic number → named constant AUTH_MAX_ATTEMPTS
- Noted: Rate limiting for future slice

### Verification
- ReadLints: 0 errors
- pytest: 15 passed, 0 failed
```

### Severity Levels

- **✓ Pass** — No issues found
- **⚠ Suggestion** — Consider improving, not blocking
- **✗ Issue** — Must fix before proceeding
- **🔴 Critical** — Security/data issue, fix immediately

---

## Examples

### Example: Code Review After Implementation

```
## Self-Review: User Authentication Module

**Roles Applied:** Code Reviewer, Security Reviewer

### Code Reviewer (Architecture)
- ✓ Single Responsibility: Auth logic separate from routes
- ✓ Dependency Inversion: Uses abstract UserRepository
- ⚠ Suggestion: LoginService.authenticate() is 45 lines — consider splitting
- ✗ Issue: Hardcoded token expiry (3600) — move to config

### Security Reviewer
- ✓ Password hashed with bcrypt, cost factor 12
- ✓ Tokens signed with HS256, secret from env
- ✓ No plaintext passwords in logs
- ⚠ Consider: Add failed login attempt tracking
- ✗ Issue: Token not invalidated on password change

### Actions Taken
1. Moved token expiry to config.py → AUTH_TOKEN_EXPIRY
2. Added token invalidation on password change
3. Noted: Login attempt tracking for security slice

### Verification
- ReadLints: 0 errors
- pytest tests/auth/: 8 passed
```

### Example: Test Engineer Review

```
## Self-Review: Test Coverage for Auth Module

**Role Applied:** Test Engineer

### Test Plan
| Component | Test Type | Status |
|-----------|-----------|--------|
| LoginService.authenticate | Unit | ✓ Done |
| LoginService.refresh_token | Unit | ✓ Done |
| Auth middleware | Integration | ✓ Done |
| Full login flow | E2E | ○ TODO |

### Missing Tests Identified
- [ ] Test expired token rejection
- [ ] Test invalid signature rejection
- [ ] Test concurrent refresh requests
- [ ] Test password change invalidates tokens

### Edge Cases to Add
```python
@pytest.mark.parametrize("password", [
    "",              # Empty
    "a" * 1000,      # Very long
    "pass word",     # Spaces
    "пароль",        # Unicode
    "pass\x00word",  # Null byte
])
def test_password_edge_cases(password):
    ...
```

### Suggested Fixtures
```python
@pytest.fixture
def expired_token():
    return create_token(user_id=1, expiry=-3600)

@pytest.fixture
def invalid_signature_token():
    return jwt.encode(payload, "wrong_secret", algorithm="HS256")
```
```

### Example: Security Review for User Input

```
## Self-Review: File Upload Endpoint

**Role Applied:** Security Reviewer

### Findings

| Check | Status | Notes |
|-------|--------|-------|
| Input validation | ✗ | File type not validated |
| Path traversal | ✗ | Filename used directly |
| Size limits | ⚠ | 10MB limit, but no streaming |
| Content validation | ✗ | Magic bytes not checked |

### Critical Issues

1. **Path Traversal (Critical)**
   ```python
   # WRONG
   path = f"uploads/{filename}"
   
   # RIGHT
   safe_name = secure_filename(filename)
   path = os.path.join(UPLOAD_DIR, safe_name)
   ```

2. **File Type Validation (Critical)**
   ```python
   # Add
   ALLOWED_EXTENSIONS = {'.jpg', '.png', '.pdf'}
   ALLOWED_MIMES = {'image/jpeg', 'image/png', 'application/pdf'}
   
   if not (ext in ALLOWED_EXTENSIONS and mime in ALLOWED_MIMES):
       raise ValidationError("Invalid file type")
   ```

3. **Magic Bytes Check (Important)**
   ```python
   import magic
   detected = magic.from_buffer(file.read(1024), mime=True)
   if detected not in ALLOWED_MIMES:
       raise ValidationError("File content doesn't match extension")
   ```

### Actions Required
- [ ] Fix path traversal vulnerability
- [ ] Add file type validation
- [ ] Add magic bytes check
- [ ] Add virus scanning (future enhancement)
```
