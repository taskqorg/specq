# Behavioral models

How state-driven systems keep their transitions checkable. [Verification](verification.md) owns the evidence rules these checks report under.

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
