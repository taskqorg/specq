# Performance and capacity

Rules for tools that must stay responsive within a fixed resource budget. Consumer contracts name the target, the budget and the environment.

## Target

- State the target in the contract: concurrent users or requests per second, p95 and p99 latency, error rate and hold duration. A burst is not a result; a sustained hold is.
- Name the environment limits with the result: CPU, memory, file descriptors, connection tracking, load generator. A limit of the environment is not a limit of the implementation, and results are comparable only within one environment.
- Accept at or below 70% sustained CPU on the hold. p99 rises first; treat it as the early signal.

## Order of work

1. Remove a layer: a proxy, a framework middleware, an object-to-JSON pass. Most of the gain is here.
2. Reuse: prepared statements, one database connection, response built by the store ([data](data.md#store)), group commit.
3. Only then tune: event loop, allocation on the request path, runtime settings.

A hand-written parser, `unsafe` code or a kernel-specific interface is a deliberate simplification: mark it with a `ponytail:` comment ([Ponytail](ponytail.md)) and keep a differential test against a reference implementation.

## Budget

- Every service names its ceiling for CPU, memory, descriptors and disk, and its behavior at the ceiling: pause accepting, retire idle connections, shed load. Running out of memory is a failure of the design, not of the host.
- Queues, retries, timeouts, batch sizes and log sizes are bounded; the contract names the bound.
- One shared lock or single writer serializes everyone behind the slowest operation. Keep long work off that path.
