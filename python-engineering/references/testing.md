# Python Testing & Quality Assurance

Patterns drawn from exemplar projects: test pyramid, fixtures, CI, async/sync. Apply with any testing stack.

## Table of Contents

1. [Test Pyramid](#test-pyramid)
2. [Structure & Fixtures](#structure--fixtures)
3. [Mocks, Fakes, Real Dependencies](#mocks-fakes-real-dependencies)
4. [Parametrization & Edge Cases](#parametrization--edge-cases)
5. [CI & Quality Gates](#ci--quality-gates)
6. [Async & Sync Testing](#async--sync-testing)
7. [Examples](#examples)

---

## Test Pyramid

- **Unit**: Fast, isolated, many. Test one unit (function, class) with dependencies mocked or faked.
- **Integration**: Fewer; test several components together (e.g. API + DB, or client + server stub). Use real DB or in-memory equivalents where practical.
- **E2E**: Few; cover critical paths against a real or near-real environment. Keep stable and quick to run (or run in CI only on main).

Balance so most feedback comes from units; integration catches interface issues; e2e catches environment issues.

---

## Structure & Fixtures

- **Location**: Mirror source layout (e.g. `tests/unit/`, `tests/integration/`) or colocate `tests/` next to `src/` or `app/`. Be consistent.
- **Fixtures**: Use pytest fixtures for setup/teardown. Scope (function, module, session) to avoid unnecessary work. Share common setup (DB, client) via fixtures.
- **Isolation**: Each test independent; no shared mutable state. Use transactions that roll back, or fresh DB per test, so order doesn’t matter.
- **Determinism**: No hidden network, time, or randomness. Patch time and external HTTP/DB in unit tests; use test doubles or test containers in integration.

---

## Mocks, Fakes, Real Dependencies

- **Mocks**: When you need to assert calls or simulate failure. Use sparingly; over-mocking couples tests to implementation.
- **Fakes**: In-memory or minimal implementations (e.g. fake repo, in-memory broker). Good for integration tests without full infrastructure.
- **Real**: Use real DB or HTTP in integration tests when cost is low (e.g. SQLite, testcontainers). Prefer real for contract and behavior.

**Web/API apps**: Override the app’s dependency or factory to inject test doubles (fake DB, auth) so handlers are tested with real request handling.

---

## Parametrization & Edge Cases

- **pytest.mark.parametrize**: One test, many inputs (e.g. valid/invalid payloads, boundary values). Covers edge cases without duplicating test code.
- **Property-based**: Consider Hypothesis for generated inputs where invariants (e.g. “decode(encode(x)) == x”) matter.
- **Edge cases**: Empty input, large input, unicode, None, zero, negative; permission denied; timeout. Explicit tests or parametrized cases.

---

## CI & Quality Gates

- **Lint**: Ruff, flake8, or similar. Fail on style and obvious bugs.
- **Type check**: mypy (or pyright). Enforce on CI.
- **Tests**: Run full suite. Parallelize (e.g. pytest-xdist) to keep feedback fast.
- **Coverage**: Enforce a minimum (e.g. 80%). Fail if uncovered lines increase on critical paths. Don’t chase 100% blindly.
- **Format**: Use one formatter and one linter. Either fix in CI or block merge on clean run.

---

## Async & Sync Testing

- **Async tests**: Use pytest-asyncio (or your test runner’s async support). Mark async tests appropriately and use an async client against the app when testing HTTP.
- **Sync tests**: Use a sync HTTP client or test client for sync request/response tests.
- **Interface wrappers**: For HTTP, consider a thin interface (e.g. method per endpoint) with type-annotated requests/responses. Test the interface with a real or fake backend; keeps tests stable when URLs or internals change.
- **Connection reuse**: In tests, use one client per test or per module (fixture) to avoid flaky “too many connections” in parallel runs.

---

## Examples

### Wrong — Test creates DB connection and leaves it open

```python
def test_create_user():
    conn = create_engine("sqlite:///test.db").connect()
    repo = UserRepository(conn)
    repo.add(User(name="alice"))
    assert repo.get_by_name("alice") is not None
    # Connection never closed; no rollback — state leaks to next test
```

### Right — Fixture with yield for setup/teardown and isolation

```python
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        conn.begin()
        yield conn
        conn.rollback()

def test_create_user(db_session):
    repo = UserRepository(db_session)
    repo.add(User(name="alice"))
    assert repo.get_by_name("alice") is not None
```

### Wrong — Copy-pasted test for each input

```python
def test_validate_empty():
    assert validate("") is False

def test_validate_negative():
    assert validate(-1) is False

def test_validate_too_long():
    assert validate("x" * 1000) is False
# ... many more
```

### Right — Parametrize valid/invalid/boundary inputs

```python
@pytest.mark.parametrize("value,expected", [
    ("", False),
    (-1, False),
    ("x" * 1000, False),
    (0, True),
    (100, True),
])
def test_validate(value, expected):
    assert validate(value) is expected
```

### Wrong — Unit test calls real API

```python
def test_fetch_user():
    response = requests.get("https://api.example.com/users/1")  # Network; slow; flaky
    assert response.json()["name"] == "Alice"
```

### Right — Patch or inject fake client; fast and deterministic

```python
def test_fetch_user(monkeypatch):
    def fake_get(*args, **kwargs):
        return type("R", (), {"json": lambda: {"name": "Alice"}, "status_code": 200})()

    monkeypatch.setattr(requests, "get", fake_get)
    user = fetch_user(1)
    assert user["name"] == "Alice"
```
