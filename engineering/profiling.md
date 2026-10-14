# Built-in profiling

Every product measures its own operations, so optimization starts from evidence, not guesses. Product contracts name their operations, budgets, store path and bounds; this page defines the method.

## Counters

- Name each measured operation once, in the product spec, for example `sync.board` or `render.menu` (invented). A name is stable; a renamed operation starts a new series.
- Counters are always on and cheap: per operation, keep the count, p50, p95 and max duration, the outcome (`ok`, `failed`, `cancelled`, `retried`) and the error class.
- An error class is a short stable code, such as `timeout` or `auth`, never a raw message.
- Retries and instability count separately from failures: an operation that succeeds after retries is unstable, not healthy.
- A switch turns on detailed traces (per-call spans and step timings) for a bounded period or run. It is off by default and reports its own state.

## Store

- Keep profiles in a bounded local store with a pruner in the same service ([data](data.md#files)). The product spec names the bound.
- Store no secrets, user content or host paths: operation names, numbers, outcomes and error classes only. Traces follow the same rule.
- Reuse the product's existing telemetry, log or metrics path. Never add a second collector, agent or service for profiling.

## Report

- A profile report ranks operations by slowness against budget, failure rate and instability, worst first, with the measured window and sample count.
- An incident links to the profile report of its window.
- An optimization task cites the report before the change and the same report after it, in the same environment ([performance](performance.md#target)). A change without a before and after comparison is not an optimization result.

## Budgets and unknowns

- Each product spec lists its measured operations with a time budget, such as p95, and an error budget.
- An operation with no samples, a failed collection or a pruned window reads unknown with a reason, never zero or ok ([unknown is never healthy](verification.md#unknown-is-never-healthy)).
