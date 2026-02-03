# Python Observability & Operational Visibility

Patterns drawn from exemplar projects (e.g. distributed task queues, web APIs): logging, metrics, errors, tracing, health. Apply with any stack.

## Table of Contents

1. [Logging](#logging)
2. [Metrics](#metrics)
3. [Error Taxonomy & Handling](#error-taxonomy--handling)
4. [Tracing & Instrumentation](#tracing--instrumentation)
5. [Health & Readiness](#health--readiness)
6. [Distributed Task Systems](#distributed-task-systems)

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
