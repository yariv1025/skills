# Python Observability & Operational Visibility

Patterns drawn from exemplar projects (e.g. distributed task queues, web APIs): logging, metrics, errors, tracing, health. Apply with any stack.

## Table of Contents

1. [Logging](#logging)
2. [Metrics](#metrics)
3. [Error Taxonomy & Handling](#error-taxonomy--handling)
4. [Tracing & Instrumentation](#tracing--instrumentation)
5. [Health & Readiness](#health--readiness)
6. [Distributed Task Systems](#distributed-task-systems)
7. [Examples](#examples)

---

## Logging

- **Structured logs**: JSON or key-value pairs (e.g. `logger.info("request", extra={"request_id": id, "path": path})`). Avoid free-form prose for production.
- **Levels**: Use consistently—DEBUG for development, INFO for normal flow, WARNING for recoverable issues, ERROR for failures that need attention.
- **Correlation IDs**: Attach a request/task ID to every log line in a request or task scope. Propagate to downstream services where possible.
- **No sensitive data**: Never log passwords, tokens, or PII in plain text.

---

## Metrics

- **Expose metrics**: Use Prometheus, StatsD, or similar. Counters for requests/tasks/errors; histograms for latency; gauges for queue depth or active workers.
- **Labels**: Use stable, bounded labels (e.g. `method`, `status`, `handler`). Avoid high-cardinality values (user IDs, raw URLs) unless aggregated.
- **Aggregation**: Prefer application-level metrics that align with SLOs (e.g. p99 latency per endpoint or task type).

---

## Error Taxonomy & Handling

- **Operational errors**: Expected in production (e.g. network timeout, validation failure). Log, metric, optionally retry; return clear responses.
- **Programmer errors**: Bugs (e.g. KeyError, NoneType). Log with stack trace; metric; do not retry indefinitely. Fix the code.
- **Strategy**: Propagate when the caller can handle; translate at boundaries (e.g. DB exception → domain exception); always log at the point of handling with context.

---

## Tracing & Instrumentation

- **OpenTelemetry**: Use for distributed tracing. Instrument HTTP clients, DB drivers, and task queues so spans show full request/task flow.
- **Middleware**: Add tracing at the edge (web or worker entrypoint). Propagate trace context in headers and to async tasks.
- **Task systems**: Instrument task execution (start/end/retry), broker publish/consume, and worker lifecycle so latency and failures are visible per task and per worker.

---

## Health & Readiness

- **Liveness**: “Process is running.” Simple endpoint that returns 200. Use for restarts.
- **Readiness**: “Ready to accept work.” Check DB connectivity, dependency health, and optionally queue depth. Return 503 until ready.
- **Single endpoint**: Often `/health` with a query or body to distinguish liveness vs readiness, or two paths: `/live` and `/ready`.

---

## Distributed Task Systems

- **Inspect/control**: Use your task system’s CLI or API for worker status, active/scheduled/reserved tasks, and stats. Integrate with runbooks and alerting.
- **Silent failures**: Some brokers ack tasks even when the worker crashes or is OOM-killed. Use result backends and monitor for “acknowledged but never completed” patterns; consider late-ack and task tracking for critical tasks.
- **Four layers to monitor**: (1) Task execution (latency, success/retry/failure), (2) Worker health (CPU, memory, concurrency), (3) Queue health (depth, consumer lag), (4) Schedule execution (if you use a scheduler). Combine tooling (dashboards, OpenTelemetry, custom metrics) as needed.
- **Scheduler**: If you have a single scheduler process, it’s a single point of failure. Monitor it and consider redundancy or external schedulers for critical schedules.

---

## Examples

### Wrong — Unstructured or prose logging

```python
print(f"User {user_id} did something")
logger.info(f"User {user_id} did X")  # Not machine-parseable; no correlation
```

### Right — Structured log with correlation ID

```python
logger.info(
    "request_handled",
    extra={
        "request_id": request_id,
        "user_id": user_id,
        "path": path,
        "status": 200,
        "duration_ms": elapsed,
    },
)
```

### Wrong — Single health endpoint that only returns 200

```python
@app.get("/health")
def health():
    return {"status": "ok"}  # Always 200; orchestrator can't tell if DB is down
```

### Right — Liveness vs readiness; 503 when not ready

```python
@app.get("/live")
def liveness():
    return {"status": "ok"}  # Process is running

@app.get("/ready")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"status": "ready"}
```

### Wrong — Treating programmer error as operational

```python
try:
    result = data["key"]["nested"]
except Exception as e:
    retry()  # KeyError is a bug; retrying won't help
```

### Right — Operational error: handle and return; programmer error: log and surface

```python
# Operational: timeout, validation, dependency down — return clear response
try:
    response = await client.get(url, timeout=5)
except asyncio.TimeoutError:
    logger.warning("dependency_timeout", extra={"url": url})
    raise HTTPException(502, "Upstream timeout")

# Programmer error: log with stack trace, don't retry
except KeyError as e:
    logger.exception("missing_key")
    raise
```
