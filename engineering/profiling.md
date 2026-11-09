# Built-in profiling

Every product measures its own operations, so optimization starts from evidence, not guesses. Product contracts name their operations, store path, bounds and export retention; this page defines the method.

## Counters

- Name each measured operation once, in the product spec, for example `sync.board` or `render.menu` (invented). A name is stable; a renamed operation starts a new series. A time or error reference value, if any, comes from the operation's own telemetry history ([observe, do not gate](performance.md#observe-do-not-gate)); a spec never asks for invented numbers.
- Counters are always on and cheap: per operation, keep the count, p50, p95 and max duration, the outcome (`ok`, `failed`, `refused`, `cancelled`, `retried`) and the error class.
- An error class is a short stable code, such as `timeout` or `auth`, never a raw message.
- Retries and instability count separately from failures: an operation that succeeds after retries is unstable, not healthy.
- A switch turns on detailed traces (per-call spans and step timings) for a bounded period or run. It is off by default and reports its own state.

## Store

- Store no secrets, user content, task text, prompts, model output or host paths: operation names, numbers, outcomes, error classes and run identity (stable ids, runtime name and version, host name) only. Traces follow the same rule. Session content has one home outside telemetry: the [agent session archive](#agent-session-archive).
- Never add a second collector, agent, store or service for profiling: observations go to the one [local store](#ship-and-store).

## Report

- A profile report ranks operations by slowness, failure rate and instability, worst first, with the measured window and sample count.
- The always-on report compares each operation with the previous window of the same length and flags the ones that got worse. A large degradation becomes its own task; it never blocks the task that caused it ([performance](performance.md#observe-do-not-gate)).
- An incident links to the profile report of its window.
- Optimization is a dedicated task. It cites the report before the change and the same report after it, in the same environment ([performance](performance.md#load-and-optimization-tasks)). A change without a before and after comparison is not an optimization result.

## Agent work

Agent work is an operation like any other: every task attempt is measured by design, always on, by the service that runs it.

- Per attempt, record each stage that occurred: `claim`, `start`, `build`, `checks`, `review`, `ask`, `close`. Per stage keep the duration, outcome and error class, with the counters above.
- Every attempt ends with a terminal stage record: `ok`, `failed` or `cancelled`, with a stable error class (`none` when no error occurred). The product contract bounds how long a stage may remain open; past that window, the service closes it as `failed` with an error class, never leaves it open silently or reports it as `ok`.
- Children and background jobs follow the same rule. A child or job that reports `failed` or `stopped`, or vanishes, makes the service close its open stage as `failed` with the corresponding error class within one service pass.
- An attempt without a terminal stage record reads [unknown, never healthy](verification.md#unknown-is-never-healthy). The [errors query](#queries) lists it; no person reads logs to find it.
- Each agent run and each model call is an observation of the [telemetry contract](#telemetry-contract). A client that reports no tokens reads unknown, never zero.
- A profile report for agent work ranks stages and runtimes by slowness, failure rate and retries, like any operation report.

## System operations

A service that runs work measures each of its own actions, not only attempts, with the counters, [store](#store) and run identity above.

- Board operations: name each board or forge call by its kind, for example `board.issue.read` or `board.label.set` (invented). Keep the API rate-limit cost when the API reports it; none reported reads unknown.
- Queue transitions: each change of a task's queue state is one record with the task id, from state, to state, time in the previous state, runtime and host. A missing entry time reads unknown, never zero.
- Service passes: each pass of a scheduler, poller or pruner is one operation with its duration, outcome and count of items handled.
- Host and service checks are observations of the same contract, with the check name as the operation.

## Telemetry by design

Telemetry is a development tool, not a report added later. A product is built so that any question about what it did is answered from its records.

- **Context is inherited.** CoreQ carries `project`, `task`, `attempt`, `actor` and the trace from the caller to every nested record and child process. Product code never passes them by hand. A value with no caller reads null with a reason code.
- **Code without telemetry fails the check.** A product's check fails when a command, route, service pass, worker stage or board call has no record, or when a failure path has no error class.
- **A refusal is not an error.** An operation that declines by design, such as a cooldown, a load gate or a focus rule, has the outcome `refused` and its reason as the error class. Refusals are counted apart from failures.
- **A question answered from a log is a defect.** When someone must read a log, a session file or a process list to learn what happened, the missing field or record is filed as a defect.
- **Questions are tests.** The global store's check runs each question below on fixture records. Each returns an answer, or unknown with a reason, from one query:
  - failures and unstable operations in a window, by product, operation and error class;
  - calls, duration and outcome per operation;
  - who worked on a task, with tokens, time and outcome per project, task, attempt and actor;
  - board calls per product, host and task;
  - time per stage and wait per queue state;
  - asset pipelines compared by method, cost, time, retries and outcome.
- **A change cites its query.** A task result that changes runtime behavior cites the query that shows the change working in the real environment, with the result before and after. When no record exists yet, the change adds it.

## Telemetry contract

One observation format, one local store per installation, one shipper and one global store. It applies to taskq, pilotq, assetq, agentq, coreq, dashq and serverq. Every agent run and every model call is visible by architecture, not by a product remembering to log it.

### Observation

- An observation is one CoreQ record. Every kind uses the same record: an operation call, an agent stage, a queue transition, a service pass, a check, `agent.turn` or `agent.call`.
- Shared fields: schema version, kind, operation name, UTC start time, duration, outcome, error class, `project`, `task`, `attempt`, `actor`, `entry` (the board comment id that the record belongs to), `pipeline`, `pipeline_revision`, `step`, `units`, `unit_kind`, `disk_bytes`, runtime name and version, host name.
- A record holds metadata only, as in [store](#store).
- A value that was not collected, has no samples, failed collection or a pruned window is null with a reason code, never zero, ok or a guess ([unknown is never healthy](verification.md#unknown-is-never-healthy)).

Request summaries distinguish observed counts from complete intervals using the [typed request coverage contract](request-coverage.md).

### Capture

- agentq-runtime writes one `agent.turn` per agent run and one `agent.call` per model request. Products that start agents add no capture of their own.
- `agent.call` carries the model, the token buckets the provider reports (input, cached input, cache write, output, reasoning), timing, outcome and error class.
- `agent.turn` also carries the exit code, the session id, user and system CPU time, and the peak RSS of the process tree.
- Peak RSS of the tree is the largest sampled sum of the live processes. Per-process peaks are never summed: they occur at different times.
- Manual and PM sessions write the same records through agentq hooks to CoreQ.

### Ship and store

- Each installation has one CoreQ local store; products write to it and to nothing else.
- One CoreQ shipper sends local records to the global store. It keeps a durable cursor per store, so a restart neither loses nor duplicates a record.
- The local store prunes a record only after the shipper's cursor has passed it.
- DASHQ-D11 on pds18 is the only global store and the only reader. Dashboards, reports and exports read it; no derived copy is a source of truth.
- Langfuse is not part of the contract and is deleted.

### Cost

- Records store a quantity and its unit: `units` with `unit_kind` `tokens` or provider credits.
- An API-equivalent cost estimate is computed at read time from a price table. Prices are never stored in records, so a price change needs no rewrite.
- Telemetry never allocates real spend, such as a subscription fee, to tasks or attempts.

### Board join

- Board lifecycle joins telemetry by `project`, `task` and `attempt` at read time. The board stays the source of truth for lifecycle; board state is never copied into telemetry.
- `agent.turn` totals and `agent.call` records describe the same tokens. Sum one kind, never both.

### Queries

- One query over outcome and error class lists every failure, every unstable operation and every attempt without a terminal record; `refused` records are left out of it. No separate detector or alert service exists.
- Efficiency and cost questions, such as time per stage, board calls per task, wait time per queue state or tokens per attempt, are answered from the same records.
- An export, when needed, is one command against the global store: JSON lines or CSV with a header and one schema version per file, stating the window it covers.

### Retention

- DashQ keeps history with no fixed retention window.
- Pruning starts only when measured volume requires it. The prune removes the oldest whole records and states the window that remains.
- Nobody invents a size or time limit in advance ([performance](performance.md#observe-do-not-gate)).

### Rollout

Each repository changes in this order. A deletion waits until the new path shows parity with the old one for the same window.

1. specq: this contract.
2. coreq: observation schema, inherited context, local store, shipper with durable cursors.
3. agentq: `agent.turn` and `agent.call` capture in agentq-runtime; hooks for manual and PM sessions. Then delete the agentq store and OTLP export.
4. Products (taskq, pilotq, assetq, serverq): write observations to the local CoreQ store; serverq checks become observations. Then delete the PilotQ store, the taskq sync and parser and TASKQ-R46.
5. dashq: DASHQ-D11 as the global store and reader, read-time price table, errors query, question tests. Then delete Langfuse; it needs no parity window, only the new reader showing records.

## Agent session archive

Telemetry never holds content. An agent session archive holds content: the session's native bytes, from which its [step history](agent-runtimes.md#step-history-and-archive) is derived.

- **Separate store.** The archive shares no store, shipper, schema or retention with telemetry. It serves reading and comparing runs, not profiling, so it is not a second store under [store](#store).
- **Explicit grant.** Capture and content reads need the archive's own grant, approved by the owner. Capture is off without that grant. A telemetry or observation grant never implies it.
- **Access audit.** Every content read leaves an audit record with the reader, time, session and outcome. The audit record holds no content.
- **Own retention.** The archive has its own configured and enforced retention, and a deletion can be verified. Telemetry [retention](#retention) does not apply to it.
- **Never reachable from telemetry.** A telemetry record holds no archive content, location, link or credential. No telemetry query, report, export or dashboard returns archive content. The session id in `agent.turn` is an opaque join key and gives no access.
- **One-way join.** A guarded archive reader may join telemetry records by `project`, `task` and `attempt`. Telemetry never joins the archive.
- **Telemetry questions stay in telemetry.** A question about what a product did that only the archive answers is a missing record, the same defect as [a question answered from a log](#telemetry-by-design).
- **Secrets.** Scrub known secret shapes before content leaves the host. Scrubbing is best effort, so treat archive content as possibly holding a secret.

The consumer contract names the grant scope, reader roles, retention values and store location.
