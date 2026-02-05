# Python Performance & Concurrency

Patterns drawn from exemplar projects: async safety, resource management, validation. Apply with any async/sync or task-queue stack.

## Table of Contents

1. [Concurrency Model Selection](#concurrency-model-selection)
2. [Async Safety](#async-safety)
3. [Threading Practices](#threading-practices)
4. [Multiprocessing Practices](#multiprocessing-practices)
5. [Throughput & Resource Control](#throughput--resource-control)
6. [Performance Validation](#performance-validation)
7. [Examples](#examples)

---

## Concurrency Model Selection

- **Async (asyncio)**: I/O-bound work (HTTP, DB, queues). Use one event loop; avoid blocking calls. Use async clients and async endpoints where your stack supports them.
- **Threads**: When a library is blocking (e.g. sync DB driver, legacy API). Use a bounded thread pool; avoid unbounded thread creation.
- **Processes**: CPU-bound work (GIL). Use multiprocessing or task-queue workers. Explicit serialization boundaries; higher overhead than threads.

Match the model to the bottleneck. Mix with care: run blocking code in thread pool from async code (e.g. `run_in_executor`); don’t block the event loop.

---

## Async Safety

- **No blocking in async path**: Never use blocking I/O (e.g. sync `requests`, sync DB calls) in async handlers. Use async clients and drivers, or offload to thread pool.
- **One long-lived client**: Reuse a single async HTTP client (or similar) per process/app for connection pooling and TLS reuse. Create at startup; close at shutdown.
- **Timeouts**: Set connect and read (and write) timeouts on every external call (e.g. connect=3s, read=5s). Prefer library-level defaults plus per-call overrides.
- **Cancellation**: Propagate cancellation (e.g. `asyncio.CancelledError`). Use `try/finally` or context managers to release resources on cancel.
- **Backpressure**: Limit concurrency with semaphores or bounded queues. Reject or queue excess work so one slow dependency doesn’t exhaust resources.

**Async HTTP client patterns**: Single long-lived client; configured timeouts; context managers for cleanup; retries with backoff; connection limits; streaming for large bodies; structured tests around the client interface.

---

## Threading Practices

- **Bounded pool**: Use `concurrent.futures.ThreadPoolExecutor` with a fixed max_workers. Size for I/O concurrency, not CPU.
- **Shared state**: Prefer immutability and queues over shared mutable state. If you need locks, hold them briefly and document why.
- **No blocking from async**: Offload blocking calls to the pool via `run_in_executor`; don’t call them directly from async code.

---

## Multiprocessing Practices

- **Serialization**: Only pickle-safe or explicitly serialized data crosses process boundaries. Avoid large or complex objects if not needed.
- **Worker lifecycle**: Start workers explicitly; shut down gracefully (drain queue, then stop). Use your task system’s signals and late-ack/reject options where appropriate.
- **Batching**: Batch work to reduce IPC and broker overhead. Group or chunk tasks; avoid one message per tiny unit of work when possible.

---

## Throughput & Resource Control

- **Connection pooling**: Reuse connections (DB, HTTP). Configure pool size per service; align with server limits and expected concurrency.
- **Per-dependency limits**: Cap concurrent requests per downstream (e.g. semaphore per client). Prevents one dependency from starving others.
- **Bulk operations**: Use batch APIs (e.g. bulk insert, batch HTTP) where available to reduce round-trips and improve throughput.

---

## Performance Validation

- **Profiling**: Use profilers (cProfile, py-spy, etc.) on realistic workloads. Focus on hot paths and unexpected blocking.
- **Benchmarks**: Add benchmarks for critical paths (e.g. request handling, task execution). Run in CI or nightly; track regressions.
- **Load testing**: Simulate production load and validate SLOs (latency, error rate, throughput). Run against staging or a copy of production config.

---

## Examples

### Wrong — New async client per request

```python
@app.get("/proxy")
async def proxy(url: str):
    async with httpx.AsyncClient() as client:  # New connection every request
        response = await client.get(url)
    return response.text
```

### Right — One long-lived client; create at startup, close at shutdown

```python
async def lifespan(app):
    app.state.http_client = httpx.AsyncClient(timeout=httpx.Timeout(5.0))
    yield
    await app.state.http_client.aclose()

@app.get("/proxy")
async def proxy(url: str, request: Request):
    response = await request.app.state.http_client.get(url)
    return response.text
```

### Wrong — External call with no timeout

```python
response = await client.get(url)  # Can hang forever
```

### Right — Timeout on every external call

```python
client = httpx.AsyncClient(timeout=httpx.Timeout(connect=3.0, read=10.0))
response = await client.get(url)
# or per-call: await client.get(url, timeout=5.0)
```

### Wrong — Blocking call in async handler

```python
@app.get("/data")
async def get_data():
    data = requests.get("https://api.example.com/data").json()  # Blocks event loop
    return data
```

### Right — Async client or run_in_executor for blocking lib

```python
@app.get("/data")
async def get_data(request: Request):
    response = await request.app.state.http_client.get("https://api.example.com/data")
    return response.json()
# If you must use sync requests: await asyncio.get_event_loop().run_in_executor(None, sync_fetch)
```

### Wrong — Unbounded asyncio.gather on many tasks

```python
results = await asyncio.gather(*[fetch(url) for url in urls])  # 10_000 URLs = 10_000 connections
```

### Right — Semaphore to bound concurrency

```python
sem = asyncio.Semaphore(20)

async def fetch_bounded(url):
    async with sem:
        return await client.get(url)

results = await asyncio.gather(*[fetch_bounded(url) for url in urls])
```
