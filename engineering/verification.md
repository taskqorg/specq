# Evidence and behavioral models

Report what observations establish. Delivery, exit code and a finished conversation do not prove application or completion.
Use the shared [Core review](../caveman/rules/core.md#review) for reporting; the rules below define engineering evidence.

- Read back changed state before claiming application. Report partial results separately.
- Keep missing, stale or untested observations unknown; name the affected claim or platform.
- Separate model, adapter, process and target-platform checks. Passing one does not qualify the others.
- Verify the exact candidate or artifact being accepted; identify relevant checks and remaining gaps.

## Unknown is never healthy

- A collection error, unsupported platform, corrupt state or stale value reads unknown with a reason.
- Never report such a value as ok, zero or success. Health, status and counts follow this rule in every interface.

## Remediation

- Diagnose read-only first.
- Then make only explicitly authorized ([approval boundaries](agent-workflow.md#approval-boundaries)), scoped changes. Each change has ownership proof, a rollback path and a verification step.

## Test classes

- A test is an instrument, never a goal. Two classes exist: development checks and chain checks.
- Write a test only when no existing chain check, trace or readback answers the question. The author names the question and the cheaper proof rejected, with the reason.
- A development check answers one question about one change. Delete it when the question is answered, or promote it to a chain check. Do not keep it because it exists.
- A chain check proves that one named chain works end to end (a requirement, a lifecycle path, a user scenario). It names the chain and the distinct failure risk it catches, and uses the cheapest run that proves the chain.
- Each persistent test names its requirement and its distinct failure risk; one that names no chain is deleted. Remove a redundant test only after another check covers its risk. Prefer executable traces, data cases and generated sequences to authored per-function tests.
- No coverage percentage targets, snapshot churn or tests of trivial helpers.
- The persistent set runs with one command in minutes, in CI on every merge candidate. Nothing in it needs a human, a paid service or hours.
- Looks, sound and feel are accepted by the owner from pictures or video; a numeric gate for them is written only after the owner accepted the result, and encodes what was accepted.
- A test review is a normal task: inventory, name each kept test's chain, delete the rest, make the set run cleanly.

## Run policy by stage

- During development: run only the check the change affects. Do not repeat unrelated checks or suites.
- For a defect fix, first reproduce the failure with the smallest safe check at the affected behavior boundary, then run the same check after the fix. Reuse chain checks where possible. If reproducing is unsafe or unavailable, record why and the alternative evidence; do not claim a before/after proof. This is not mandatory test-first work for trivial or documentation changes.
- Merge candidate: run cheap deterministic core acceptance and the checks the diff affects. Capture seed, version, step events and native logs. A failure names the broken chain before anyone isolates the step.
- Release candidate: run the platform and client matrix, lifecycle and outage cases, and bounded live probes of changed integration paths. Run expensive or paid evaluations only when the logic they measure changed, never for doc edits or unchanged redeploys.

## State-driven systems

- Keep transitions in an explicit behavioral model; adapters handle external effects.
- Change the transition specification, executable traces, model and adapters in that order.
- Trace initial state and events to expected state, including ignored events.
- Cover duplicates, stale events, ordering and human-authored input where supported.
- Keep product states, commands, fixture paths and acceptance thresholds in the consumer contract.

## Formal checks (optional)

- Formalize only risky state transitions, for example mutual exclusion of operations, no activation before verification, drain before switch, no deletion outside owned files, stable IDs against double counting. Tie each invariant to a requirement ID.
- Default: one state model plus generated operation sequences in the project's existing test tools. Adopt a heavier tool (for example P, Quint or TLA+) only after a one-scenario spike finds real defects at lower ongoing cost than targeted checks.
- A model check proves the model within its bounds; a trace check proves observed runs. Neither proves all code.

## Agent integration

The entry stays thin ([principles](principles.md#rules)) and loads the compatible installed contract. Qualify integration presence, actual instruction loading and the complete user flow separately. Report unavailable capabilities explicitly. Keep provider-specific commands, versions and qualification fixtures in the consumer project. A second supported client must be able to continue from authoritative project state without the original chat.
