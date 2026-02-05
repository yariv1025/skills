# Python Core Engineering Practices

Patterns drawn from exemplar projects: runtime, packaging, I/O, reliability. Apply with any stack.

## Table of Contents

1. [Runtime & Language](#runtime--language)
2. [Packaging & Maintainability](#packaging--maintainability)
3. [I/O & Network Correctness](#io--network-correctness)
4. [Reliability & Secure Coding](#reliability--secure-coding)
5. [Tooling & Consistency](#tooling--consistency)
6. [Examples](#examples)

---

## Runtime & Language

- **GIL**: Only one thread runs Python bytecode at a time. Use threads for I/O-bound concurrency; use processes or C extensions for CPU-bound parallelism.
- **Memory**: Be aware of allocation patterns and large structures. Reuse buffers/iterators where it helps; avoid unnecessary copies (e.g. use views when safe).
- **Data model**: Use iterators, context managers, and dunder methods (`__enter__`/`__exit__`, `__iter__`) to make APIs clear and resource-safe.
- **Exceptions**: Use the right exception type; prefer built-in or domain-specific hierarchy. Don’t catch broad `Exception` unless re-raising or logging at a boundary.

---

## Packaging & Maintainability

- **pyproject.toml**: Single source for metadata and tool config. PEP 517 (build), PEP 518 (build deps), PEP 621 (project), PEP 660 (editable installs). Prefer over `setup.py`/`setup.cfg`.
- **Dependencies**: Pin for reproducibility (e.g. lock file). Separate dev and runtime deps. Use virtual envs or containers so system Python isn’t polluted.
- **Type safety**: Use type hints and run mypy (or pyright). Strict mode where practical; gradual typing for legacy code.
- **Lint & format**: Enforce one formatter and one linter. CI fails on violations. Prefer opinionated, minimal-option tools.

---

## I/O & Network Correctness

- **Retries**: Make retries idempotent where possible (e.g. safe to retry on timeout). Use exponential backoff and jitter; cap attempts.
- **Circuit breaking**: After repeated failures to a dependency, stop calling it briefly and fail fast. Recover with a test request or timer.
- **Connection reuse**: Use a single client/session per process with pooling. Don’t open a new connection per request.
- **Streaming**: For large responses, use streaming (iter_content, aiter_bytes) instead of loading into memory. Same for uploads when supported.
- **Cleanup**: Use context managers (`with` or `async with`) so connections and files are closed even on errors or cancellation.

---

## Reliability & Secure Coding

- **Resource cleanup**: Always release handles (files, sockets, DB connections) via context managers or explicit try/finally. Avoid finalizers for critical cleanup.
- **Input validation**: Validate and sanitize at boundaries (API, CLI, file input). Use a validation library or manual checks for structured input; reject invalid data early.
- **Secrets**: No secrets in code or repo. Use env vars or a secret manager; restrict access in production.
- **Subprocess & filesystem**: Validate and sanitize paths and arguments. Prefer allowlists; avoid shell=True with user input. Set timeouts and resource limits.

---

## Tooling & Consistency

- **Opinionated formatter**: One style reduces churn and review noise. Few options; “just run it.”
- **CLI**: Use argparse or Click; support config file + env + flags. Prefer clear subcommands and a way to disable plugins or extensions when needed.
- **Minimal surface**: Keep public API and options small. Few flags; complexity inside the tool, not in configuration.

---

## Examples

### Wrong — Open file/socket without with; manual try/finally error-prone

```python
f = open(path)
data = f.read()
process(data)
f.close()  # Skipped if process() raises
```

### Right — Context manager guarantees cleanup

```python
with open(path) as f:
    data = f.read()
    process(data)
# f closed even if process() raises
```

### Wrong — Bare retry loop with fixed sleep

```python
for _ in range(5):
    try:
        return client.get(url)
    except Exception:
        time.sleep(1)  # No backoff; no jitter; retries on all errors
return None
```

### Right — Exponential backoff, jitter, max attempts, idempotent operation

```python
import random

def fetch_with_retry(url, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return client.get(url, timeout=5)
        except (TimeoutError, ConnectionError):
            if attempt == max_attempts - 1:
                raise
            delay = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### Wrong — Use user input directly in DB or subprocess

```python
user_id = request.args.get("id")
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # Injection
# or: subprocess.run(f"echo {user_input}", shell=True)
```

### Right — Validate at boundary; then pass validated value

```python
from pydantic import BaseModel

class UserQuery(BaseModel):
    id: int  # Validated type

query = UserQuery(id=request.args.get("id"))  # ValidationError if invalid
cursor.execute("SELECT * FROM users WHERE id = ?", (query.id,))
```

### Wrong — Hardcoded secret

```python
API_KEY = "sk-prod-abc123"  # In repo; visible to anyone with access
```

### Right — Env or secret manager

```python
import os

API_KEY = os.environ["API_KEY"]  # Set at runtime; not in code
# Or: load from secret manager in config module, validate at startup
```
