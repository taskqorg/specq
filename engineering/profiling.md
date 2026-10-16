# Built-in profiling

Every product measures its own operations, so optimization starts from evidence, not guesses. Product contracts name their operations, budgets, store path, bounds and export retention; this page defines the method.

## Coverage by construction

- Coverage includes every product action and execution path: user input, window creation/show/hide, layout, resize, render submission and observed paint, command dispatch, service work, board calls, agent/model/tool calls, context loading and compression. A short operation catalog is not an exemption for other paths.
- Use the shared implementation and automatic instrumentation at execution boundaries. Handlers and dependency clients inherit operation capture from their execution boundary. Owned methods inherit the ability to enable detailed diagnostics; this does not require timing or recording every invocation in normal operation. A manual list that silently omits new handlers or external calls does not satisfy coverage. The collector's own internals exclude recursive self-observation and expose collection health separately.
- Link input, dispatch, execution and observed result with one operation identity and parent spans. Record failures, refusals, cancellation and unknown results as well as success. A submitted render is not proof of paint; an accepted command is not proof of its effective state.
- Record model, input/output/cache tokens, context size and compression before/after when the runtime exposes them. Missing observations carry a reason; never infer them from elapsed time or report them as zero.
- Collection is built in and local first, with no enrollment, credentials, extra service or per-feature setup required. Products share the implementation rather than copying collectors. Optional synchronization reads committed local observations and advances only on verified durable acceptance; disconnection never disables local analysis.
- Acceptance checks coverage against the full handler/method inventory and exercises an input-to-observed-result trace, including failure and newly added code. Passing tests for the instrumented subset is not proof of complete coverage.

## Collection modes

- Keep compact causal records of meaningful actions, decisions and external operations. Record accepted input and observed effect separately; acceptance alone is not completion.
- Keep low-cardinality operation counters and duration distributions continuously. Do not put request, task or trace ids in metric dimensions. Frequent UI events may coalesce with counts and explicit interval boundaries.
- Internal call detail is off by default. Enable selected owned methods for a bounded duration and volume; filter before creating spans, allocating payloads or reading a clock. Record selector, limits, expiry and truncation. Profiling estimates are not exact invocation history.
- Every background activity has an owner that observes completion, failure, cancellation or timeout. Dependency adapters classify expected outcomes, retries and terminal failure without raw payloads. Tests reject silent result disposal and unowned execution at these boundaries.
- Bound memory, storage, export work and application overhead before implementation acceptance. Under pressure, shed optional detail before required operation evidence and expose the gap. Remote export failure must not block local work. Required command receipts are product behavior with an explicit failure policy, not best-effort diagnostics.
- A crash may lose unacknowledged observations. Missing terminal evidence, collection loss, unsupported capture and pruned intervals remain unknown. No promise of complete history under arbitrary failure.

References: [OpenTelemetry instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/libraries/), [sampling](https://opentelemetry.io/docs/concepts/sampling/), [SDK failure isolation](https://opentelemetry.io/docs/specs/otel/error-handling/) and [Prometheus inner loops](https://prometheus.io/docs/practices/instrumentation/#inner-loops). Product budgets require product measurements; these sources supply no universal overhead guarantee.

## Counters

- Name each measured operation once, in the product spec, for example `sync.board` or `render.menu` (invented). A name is stable; a renamed operation starts a new series.
- Counters are always on and cheap: per semantic operation, keep the count, p50, p95 and max duration, the outcome (`ok`, `failed`, `cancelled`, `retried`) and the error class.
- An error class is a short stable code, such as `timeout` or `auth`, never a raw message.
- Retries and instability count separately from failures: an operation that succeeds after retries is unstable, not healthy.
- A switch turns on detailed traces (per-call spans and step timings) for a bounded period or run. It is off by default and reports its own state.

## Store

- Keep profiles in a bounded local store with a pruner in the same service ([data](data.md#files)). The product spec names the bound.
- Store no secrets, user content or host paths: operation names, numbers, outcomes, error classes and run identity (stable ids, runtime name and version, host name) only. Traces follow the same rule.
- Reuse the product's existing telemetry, log or metrics path. Never add a second collector, agent or service for profiling.

## Report

- A profile report ranks operations by slowness against budget, failure rate and instability, worst first, with the measured window and sample count.
- An incident links to the profile report of its window.
- An optimization task cites the report before the change and the same report after it, in the same environment ([performance](performance.md#target)). A change without a before and after comparison is not an optimization result.

## Agent work

Agent work is an operation like any other: every task attempt is measured by design, always on, by the service that runs it.

- Per attempt, record each stage that occurred: `claim`, `start`, `build`, `checks`, `review`, `ask`, `close`. Per stage keep the duration, outcome and error class, with the counters above.
- Every attempt ends with a terminal stage record: `ok`, `failed` or `cancelled`, with a stable error class (`none` when no error occurred). The product contract bounds how long a stage may remain open; past that window, the service closes it as `failed` with an error class, never leaves it open silently or reports it as `ok`.
- Children and background jobs follow the same rule. A child or job that reports `failed` or `stopped`, or vanishes, makes the service close its open stage as `failed` with the corresponding error class within one service pass.
- The service itself detects attempts without a terminal stage record and reports them as defects in its profile report and self-check; this check must not depend on a person reading logs. A missing record reads [unknown, never healthy](verification.md#unknown-is-never-healthy); it is not evidence of a successful attempt.
- Record model calls and context tokens per stage when the client reports them. A client that reports none reads unknown, never zero.
- Identify an attempt by its task and attempt ids, runtime and host name, as [run identity](#store) allows. Store no secrets, task text, prompts, model output or paths.
- Write these records to the existing attempt log or profile store under its bound. Agent work adds no collector, hook service or second store.
- A profile report for agent work ranks stages and runtimes by slowness, failure rate and retries, like any operation report.

## System operations

A service that runs work measures each of its own actions, not only attempts, with the counters, [store](#store) and run identity above.

- Board operations: name each board or forge call by its kind, for example `board.issue.read` or `board.label.set` (invented). Keep the API rate-limit cost when the API reports it; none reported reads unknown.
- Queue transitions: each change of a task's queue state is one record with the task id, from state, to state, time in the previous state, runtime and host. A missing entry time reads unknown, never zero.
- Service passes: each pass of a scheduler, poller or pruner is one operation with its duration, outcome and count of items handled.

## Analysis export

- The export holds one record per observation: an operation call, an agent stage, a queue transition or a service pass.
- Format: JSON lines or CSV with a header, one schema version per file. Each record carries its kind, operation name, UTC start time, duration, outcome, error class, run identity and the fields of its kind.
- Store no secrets, task text, prompts, model output or paths, as in [store](#store).
- The export is a plain file in the bounded store, or one command writes it. Reading it needs no board access.
- The product spec names the retention window and a size bound, for example 90 days and 50 MB (invented). The pruner removes the oldest whole records; the export states the window it covers.
- Reports and dashboards read these same records; no derived copy is a source of truth. Efficiency and cost questions, such as time per stage, board calls per task or wait time per queue state, are answered from them.

## Budgets and unknowns

- Each product spec lists its measured operations with a time budget, such as p95, and an error budget.
- An operation with no samples, a failed collection or a pruned window reads unknown with a reason, never zero or ok ([unknown is never healthy](verification.md#unknown-is-never-healthy)).
