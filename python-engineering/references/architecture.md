# Python Architecture & Design

Patterns drawn from exemplar projects (e.g. FastAPI, Poetry)—package structure, DI, config, plugins. Apply with any framework or plain Python.

## Table of Contents

1. [Package & Module Structure](#package--module-structure)
2. [Separation of Concerns](#separation-of-concerns)
3. [Dependency Injection](#dependency-injection)
4. [Configuration Management](#configuration-management)
5. [Plugin Architecture](#plugin-architecture)
6. [Production Layout](#production-layout)
7. [Examples](#examples)

---

## Package & Module Structure

- **Feature-based vs file-type**: Choose one and stick to it. Feature-based (e.g. `users/`, `orders/`) scales better for large apps; file-type (e.g. `routers/`, `models/`, `services/`) is familiar and works for smaller codebases.
- **Module boundaries**: Each module has a single responsibility. Routers only handle HTTP; domain logic lives in services or domain modules; persistence in repositories or adapters.
- **Dependency direction**: Dependencies point inward: infrastructure → application → domain. Domain has no imports from routers or DB layers.

**API/service layout (pattern from many exemplars):**

```
app/
  main.py          # App factory, lifespan
  config.py        # Settings
  api/
    deps.py        # Shared dependencies
    v1/
      users.py     # Router / handlers
      items.py
  core/            # Domain or shared logic
  db/              # Persistence, sessions
```

**Tooling/packaging**: `pyproject.toml` as single source of truth; build backend via PEP 517/518; plugin entry points for extensibility.

---

## Separation of Concerns

- **Routing**: Thin layer—parse request, call use case, return response. No SQL, no heavy business logic.
- **Domain**: Business rules, entities, value objects. Framework-agnostic.
- **Persistence**: Repositories or adapters that domain depends on via abstractions (interfaces/protocols).
- **Integration**: External APIs, message queues, etc. behind adapters so they can be swapped or mocked.

Clean Architecture for APIs: endpoints orchestrate use cases; use cases depend on abstractions (e.g. `UserRepository`); concrete DB/HTTP implementations live at the edges.

---

## Dependency Injection

- **Typed DI**: Compose dependencies with typed functions (e.g. `get_db` → `get_user_service` → `get_current_user`). Keep functions pure where possible. Use whatever your stack provides (framework DI, factory functions, or manual wiring).
- **Type hints**: Use for DI and validation. Use a validation/settings library if needed; use `typing.Protocol` for abstractions.
- **Lifecycle**: Prefer a single app factory with explicit lifespan (startup/shutdown) for DB pools, HTTP clients, and caches.

Example: Router depends on `UserService`; `UserService` depends on `UserRepository`; `UserRepository` gets a session from `get_db`. Wire via your framework’s DI or explicit factories.

---

## Configuration Management

- **Single source**: Prefer `pyproject.toml` for package metadata and tool config; env vars or a typed settings module for runtime.
- **Validation**: Load and validate at startup. Fail fast on missing or invalid config.
- **Secrets**: Never in code or repo. Use env vars, secret managers, or platform-specific injection.
- **Twelve-factor**: Config in environment; strict separation between code and config.

---

## Plugin Architecture

- **Entry points**: Use `[project.entry-points."group.name"]` in `pyproject.toml` so plugins register without being imported at top level.
- **Pattern**: Plugins receive a core object and I/O handle; they can extend config or add CLI commands. Discovery is optional; core behavior works without plugins. Support a global flag to disable plugins when needed.

---

## Production Layout

- **Three-tier pseudo-architecture**: Presentation (API/routers) → Application (use cases, orchestration) → Data (repositories, external services).
- **Security, testing, async, config**: Design these in from the start so scaling to production and multiple teams doesn’t require a full rewrite.
- **Naming and tooling**: Consistent conventions for modules, migrations, and tooling so the codebase stays navigable as it grows.

---

## Examples

### Wrong — Router instantiates DB/service directly

```python
# Tight coupling; hard to test or swap implementation
from myapp.db import get_engine

@app.get("/users/{user_id}")
def get_user(user_id: int):
    engine = get_engine()
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id}).fetchone()
    return {"id": row[0], "name": row[1]}
```

### Right — Dependencies injected; router receives service

```python
# Router depends on abstraction; service/repo wired via get_db
def get_user_service(db = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

@app.get("/users/{user_id}")
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(404)
    return {"id": user.id, "name": user.name}
```

### Wrong — Config scattered, no validation

```python
# Different modules read env directly; no single place; fails at runtime
# in api/users.py
db_url = os.environ["DATABASE_URL"]
# in worker/tasks.py
redis_url = os.getenv("REDIS_URL", "redis://localhost")  # Default may be wrong for prod
```

### Right — Single settings module, validated at startup

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()  # Raises ValidationError if required fields missing
```

### Wrong — SQL and business logic in route handler

```python
@app.post("/orders")
def create_order(data: dict):
    # Routing, validation, business rules, and persistence mixed together
    if data["amount"] < 0:
        raise HTTPException(400, "Invalid amount")
    with get_engine().connect() as conn:
        conn.execute(text("INSERT INTO orders ..."), data)
        conn.commit()
    return {"status": "created"}
```

### Right — Thin route; use case and repository abstraction

```python
@app.post("/orders")
def create_order(data: OrderCreate, order_service: OrderService = Depends(get_order_service)):
    order = order_service.create(data)  # Use case: validation + business rules
    return {"id": order.id, "status": "created"}

# OrderService uses OrderRepository (interface); repository handles SQL.
```
