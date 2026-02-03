---
name: python-engineering
description: Production Python engineering patterns covering architecture, observability, testing, performance/concurrency, and core practices. Use when designing Python systems, implementing async/sync APIs, setting up monitoring, structuring tests, optimizing performance, or following Python best practices.
---

# Python Engineering

Production-grade patterns drawn *from* (not requiring) exemplar projects—FastAPI, Poetry, HTTPX, Celery, Black—as reference. Apply the patterns with any stack.

This skill is structured per the skill-creator: essentials and navigation in SKILL.md; detailed patterns in `references/`, loaded only when needed (progressive disclosure).

## When to Read Which Reference

| Need | Read |
|------|------|
| Package layout, DI, config, plugins | [references/architecture.md](references/architecture.md) |
| Logging, metrics, tracing, health | [references/observability.md](references/observability.md) |
| Test structure, fixtures, CI | [references/testing.md](references/testing.md) |
| Async safety, concurrency, throughput | [references/performance-concurrency.md](references/performance-concurrency.md) |
| GIL, packaging, I/O, reliability | [references/core-practices.md](references/core-practices.md) |

## Quick Patterns

- **Structure**: Separate routing, domain, persistence, integration; use dependency injection and typed config (any framework or stdlib).
- **Observability**: Structured logs with correlation IDs; metrics (Prometheus/StatsD); health/readiness endpoints; distinguish operational vs programmer errors.
- **Tests**: Pyramid (unit → integration → e2e); fixtures for isolation; parametrize edge cases; parallel CI; avoid hidden network/time.
- **Concurrency**: Async for I/O; threads for blocking libs; processes for CPU-bound. One long-lived client per dependency; timeouts and backpressure everywhere.
- **Reliability**: Context managers for cleanup; validate at boundaries; no blocking calls in async paths; idempotent retries and circuit breaking for I/O.

## Workflow

1. **Designing a new service** → Read [references/architecture.md](references/architecture.md), then [references/core-practices.md](references/core-practices.md).
2. **Adding monitoring** → Read [references/observability.md](references/observability.md).
3. **Writing or refactoring tests** → Read [references/testing.md](references/testing.md).
4. **Optimizing or introducing async/threads/workers** → Read [references/performance-concurrency.md](references/performance-concurrency.md).

Keep SKILL.md lean; load reference files only when relevant to the task.
