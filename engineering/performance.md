# Performance and capacity

Rules for tools that must stay responsive within fixed resources. Performance is observed in the product's own telemetry ([profiling](profiling.md)), not gated.

## Observe, do not gate

- A budget or ceiling is a reference value taken from the product's own telemetry history. It is never task acceptance, a merge gate or a reason to ask the owner for numbers.
- A task adds no benchmark harness or performance test. Its effect shows in the always-on profile report ([report](profiling.md#report)).
- A degradation the report flags becomes its own task. It never blocks the task that caused it.

## Load and optimization tasks

A dedicated load or optimization task is the only place a performance target applies. It follows [Report](profiling.md#report): the same report before and after the change.

- The task states its load: concurrent users or requests per second, error rate and hold duration. A burst is not a result; a sustained hold is.
- Name the environment limits with the result: CPU, memory, file descriptors, connection tracking, load generator. A limit of the environment is not a limit of the implementation, and results are comparable only within one environment.
- Its target is at or below 70% sustained CPU on the hold. p99 rises first; treat it as the early signal.

## Order of work

1. Remove a layer: a proxy, a framework middleware, an object-to-JSON pass. Most of the gain is here.
2. Reuse: prepared statements, one database connection, response built by the store ([data](data.md#store)), group commit.
3. Only then tune: event loop, allocation on the request path, runtime settings.

A hand-written parser, `unsafe` code or a kernel-specific interface is a deliberate simplification: mark it with a `ponytail:` comment ([Ponytail](ponytail.md)) and keep a differential test against a reference implementation.

## Budget

- Every service defines its behavior when CPU, memory, descriptors or disk run out: pause accepting, retire idle connections, shed load. Running out of memory is a failure of the design, not of the host. The reference value for each resource follows [observe, do not gate](#observe-do-not-gate).
- Queues, retries, timeouts, batch sizes and log sizes are bounded ([data](data.md#files)); the contract names the bound.
- One shared lock or single writer serializes everyone behind the slowest operation. Keep long work off that path.
