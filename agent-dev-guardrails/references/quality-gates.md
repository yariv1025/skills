# Quality Gates

Definition of Done and validation workflows. Use to verify work is complete.

## Table of Contents

1. [Definition of Done](#definition-of-done)
2. [Pre-Work Checklist](#pre-work-checklist)
3. [Post-Work Checklist](#post-work-checklist)
4. [Linting Workflow](#linting-workflow)
5. [Testing Workflow](#testing-workflow)
6. [Language-Specific Gates](#language-specific-gates)
7. [Examples](#examples)

---

## Definition of Done

A slice of work is "done" only when ALL of these pass:

| Gate | Verification |
|------|--------------|
| **Compiles/Imports** | No syntax errors, all imports resolve |
| **Lint passes** | Zero lint errors (warnings reviewed) |
| **Type checks pass** | No type errors (if using typed language) |
| **Tests pass** | All existing tests still pass |
| **New tests added** | New functionality has test coverage |
| **Edge cases handled** | Boundary conditions considered |
| **No secrets** | No hardcoded credentials or API keys |
| **Self-reviewed** | Applied relevant reviewer roles |
| **Docs updated** | Task docs reflect current state |

**Quick check command pattern:**
```bash
# Python
ruff check . && mypy . && pytest

# Node.js
npm run lint && npm run typecheck && npm test

# Go
golangci-lint run && go test ./...

# Rust
cargo clippy && cargo test
```

---

## Pre-Work Checklist

Before starting any code change:

```markdown
## Pre-Work Checklist
- [ ] **Understand**: What exactly needs to be done?
- [ ] **Scope**: Is this small (<10 min) or needs planning?
- [ ] **Context**: What files are affected?
- [ ] **Patterns**: Are there existing patterns to follow?
- [ ] **Dependencies**: Any blockers or prerequisites?
- [ ] **Skills**: Which skill docs apply?
```

For non-trivial work, also:
- [ ] Produce a plan with tasks and risks
- [ ] Create dev docs folder if >30 min expected
- [ ] Get plan approval before implementation

---

## Post-Work Checklist

After every code edit, run through this checklist:

```markdown
## Post-Work Checklist

### Validation
- [ ] **Lint**: Run linter, fix any errors introduced
- [ ] **Types**: Run type checker (if applicable)
- [ ] **Tests**: Run relevant tests, ensure they pass
- [ ] **Imports**: Verify all imports resolve

### Self-Review
- [ ] **Correctness**: Does the code do what was asked?
- [ ] **Edge cases**: Are boundary conditions handled?
- [ ] **Errors**: Are exceptions handled appropriately?
- [ ] **Security**: Any input validation or secrets issues?

### Documentation
- [ ] **Dev docs**: Update task docs if applicable
- [ ] **Comments**: Add comments for non-obvious logic
- [ ] **Summary**: Report what changed and how validated

### Output Format
Files changed: [list paths]
Commands run: [lint, test commands + results]
Self-review: [findings from reviewer roles]
Next: [next slice or "complete"]
```

---

## Linting Workflow

### Using ReadLints Tool

After editing files, check for lint errors:

1. **Run ReadLints** on edited files
2. **Review errors** — Focus on errors you introduced
3. **Fix errors** — Don't leave new errors behind
4. **Re-run** — Verify fixes worked

**Important:** Pre-existing lint errors are not your responsibility unless fixing them is part of the task. Focus on not introducing new ones.

### Common Lint Error Patterns

| Error Type | Common Fix |
|------------|------------|
| Unused import | Remove the import |
| Unused variable | Remove or prefix with `_` |
| Line too long | Break into multiple lines |
| Missing type hint | Add type annotation |
| Undefined name | Import or define the name |
| Trailing whitespace | Remove trailing spaces |
| Missing newline at EOF | Add blank line at end |

### Fixing Lint Errors

**Process:**
1. Read the error message carefully
2. Identify the root cause (not just the symptom)
3. Make the minimal fix
4. Re-run lint to verify

**Don't:**
- Disable lint rules without good reason
- Make unrelated changes while fixing lint
- Ignore errors and mark work as done

---

## Testing Workflow

### When to Run Tests

| Situation | Run What |
|-----------|----------|
| After any code edit | Related tests (`pytest tests/test_affected.py`) |
| Before marking done | Full test suite (`pytest`) |
| After refactoring | Full test suite |
| CI/pre-commit | Full test suite |

### Test Verification Steps

1. **Run related tests first** — Fast feedback
2. **Run full suite before done** — Catch regressions
3. **Check coverage** — New code should have tests
4. **Review failures** — Don't ignore or skip

### Handling Test Failures

**If tests fail after your changes:**

1. **Read the failure** — What test, what assertion?
2. **Determine cause:**
   - Did you break existing behavior? → Fix your code
   - Is the test outdated? → Update the test (with justification)
   - Is it a flaky test? → Fix the flakiness or mark for follow-up
3. **Never skip tests** to make CI pass

**Test failure checklist:**
- [ ] Read the full error message
- [ ] Identify which change caused it
- [ ] Determine if code or test needs fixing
- [ ] Make the fix
- [ ] Re-run to verify
- [ ] Run full suite to check for other regressions

---

## Language-Specific Gates

### Python

```bash
# Lint + format
ruff check . --fix
ruff format .

# Type check
mypy src/ --strict

# Tests
pytest -v --tb=short

# All in one
ruff check . && mypy src/ && pytest
```

**Key checks:**
- [ ] No ruff errors
- [ ] mypy passes (or type: ignore with reason)
- [ ] pytest passes
- [ ] No print() statements left (use logging)

### Node.js / TypeScript

```bash
# Lint + format
npm run lint
npm run format

# Type check
npm run typecheck  # or: tsc --noEmit

# Tests
npm test

# All in one
npm run lint && npm run typecheck && npm test
```

**Key checks:**
- [ ] No ESLint errors
- [ ] No TypeScript errors
- [ ] Tests pass
- [ ] No console.log() left (use proper logging)

### Go

```bash
# Lint
golangci-lint run

# Vet (built-in checks)
go vet ./...

# Tests
go test ./... -v

# All in one
golangci-lint run && go test ./...
```

**Key checks:**
- [ ] No golangci-lint errors
- [ ] go vet passes
- [ ] go test passes
- [ ] No fmt.Println() left (use proper logging)

### Rust

```bash
# Lint
cargo clippy -- -D warnings

# Format check
cargo fmt -- --check

# Tests
cargo test

# All in one
cargo clippy && cargo test
```

**Key checks:**
- [ ] No clippy warnings
- [ ] cargo fmt passes
- [ ] cargo test passes
- [ ] No println!() left (use proper logging)

### Java

```bash
# Lint (Checkstyle)
mvn checkstyle:check

# Format
google-java-format -i $(find . -name "*.java")

# Tests
mvn test

# All in one
mvn checkstyle:check && mvn test
```

**Key checks:**
- [ ] No checkstyle violations
- [ ] mvn compile succeeds
- [ ] mvn test passes
- [ ] No System.out.println() left (use proper logging)

### C# / .NET

```bash
# Format
dotnet format

# Build (warnings as errors)
dotnet build --warnaserror

# Tests
dotnet test

# All in one
dotnet format && dotnet build && dotnet test
```

**Key checks:**
- [ ] No build warnings
- [ ] dotnet test passes
- [ ] No Console.WriteLine() left (use ILogger or similar)

### Ruby

```bash
# Lint + format
bundle exec rubocop -a

# Type check (optional)
bundle exec srb typecheck

# Tests
bundle exec rspec

# All in one
bundle exec rubocop && bundle exec rspec
```

**Key checks:**
- [ ] No RuboCop offenses
- [ ] RSpec passes
- [ ] No puts left in production code (use logger)

### PHP

```bash
# Lint
vendor/bin/phpstan analyse

# Format
vendor/bin/php-cs-fixer fix

# Tests
vendor/bin/phpunit

# All in one
vendor/bin/phpstan analyse && vendor/bin/phpunit
```

**Key checks:**
- [ ] No PHPStan errors
- [ ] PHPUnit passes
- [ ] No var_dump/print_r left (use proper logging)

---

## Examples

### Example: Post-Work Summary (Passing)

```
## Post-Work Summary

### Files Changed
- src/auth/service.py
- tests/auth/test_service.py

### Validation
- Lint: `ruff check src/auth/` → 0 errors ✓
- Types: `mypy src/auth/` → 0 errors ✓
- Tests: `pytest tests/auth/` → 5 passed ✓

### Self-Review (Code Reviewer + Security Reviewer)
- ✓ Single responsibility maintained
- ✓ Input validation on credentials
- ✓ Password hashed before storage
- ⚠ Consider: rate limiting (noted for future)

### Status
Slice complete. All gates passed.

### Next
Slice 3: Implement token refresh endpoint
```

### Example: Post-Work Summary (With Fixes)

```
## Post-Work Summary

### Files Changed
- src/api/routes.py
- src/api/handlers.py

### Validation (Initial)
- Lint: `ruff check src/api/` → 2 errors ✗
  - routes.py:45: F401 unused import 'json'
  - handlers.py:23: E501 line too long (127 > 100)

### Fixes Applied
1. Removed unused import 'json' from routes.py
2. Broke long line in handlers.py into multiple lines

### Validation (After Fix)
- Lint: `ruff check src/api/` → 0 errors ✓
- Tests: `pytest tests/api/` → 12 passed ✓

### Self-Review
- ✓ Changes match requirements
- ✓ Error handling in place
- ✓ No security issues

### Status
Slice complete after lint fixes.
```

### Example: Handling Test Failure

```
## Post-Work Validation

### Initial Test Run
`pytest tests/` → 1 failed, 24 passed

### Failure Analysis
```
FAILED tests/test_user.py::test_user_creation
AssertionError: Expected email 'test@example.com', got 'TEST@EXAMPLE.COM'
```

### Root Cause
My change in `user.py` normalizes email to uppercase, but test expected lowercase.

### Decision
Email normalization is intentional (case-insensitive). Test needs update.

### Fix
Updated test to expect uppercase email:
```python
assert user.email == "TEST@EXAMPLE.COM"  # Normalized to uppercase
```

### Re-validation
`pytest tests/` → 25 passed ✓

### Status
Slice complete. Test updated to reflect new behavior.
```

### Example: Pre-existing Lint Errors

```
## Post-Work Validation

### Lint Run
`ruff check src/` → 5 errors

### Analysis
- 2 errors in files I edited (src/auth/service.py)
- 3 errors in files I didn't touch (src/legacy/old_code.py)

### Actions
- Fixed: 2 errors in src/auth/service.py (my changes)
- Ignored: 3 errors in src/legacy/old_code.py (pre-existing)

### Re-validation
`ruff check src/auth/` → 0 errors ✓

### Note
Pre-existing errors in legacy code noted but not fixed (out of scope).
To fix those, create separate cleanup task.
```
