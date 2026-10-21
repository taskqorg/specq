# Evidence and behavioral models

Report what observations establish. Delivery, exit code and a finished conversation do not prove application or completion.
Use the shared [Core review](../caveman/rules/core.md#review) for reporting; the rules below define engineering evidence.

- Read back changed state before claiming application. Report partial results separately.
- Keep missing, stale or untested observations unknown; name the affected claim or platform.
- Separate model, adapter, process and target-platform checks. Passing one does not qualify the others.
- Verify the exact candidate or artifact being accepted; identify relevant checks and remaining gaps.
- Visual evidence follows the [review set](../design/workflow.md#review-sets) cap.

## Unknown is never healthy

- A collection error, unsupported platform, corrupt state or stale value reads unknown with a reason.
- Never report such a value as ok, zero or success. Health, status and counts follow this rule in every interface.
- For attempts without a terminal stage record, apply the service detection and reporting rule in [Agent work profiling](profiling.md#agent-work).

## Remediation

- Diagnose read-only first.
- Then make only explicitly authorized ([approval boundaries](agent-workflow.md#approval-boundaries)), scoped changes. Each change has ownership proof, a rollback path and a verification step.

## Test classes

Definitions and the decision procedure live in [Testing](testing.md#before-adding-or-changing-a-test). This heading preserves existing links.

## Run policy by stage

The canonical [run policy](testing.md#run-policy-by-stage) lives in Testing. This heading preserves existing links.

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
