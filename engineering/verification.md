# Evidence and behavioral models

Report what observations establish. Delivery, exit code and a finished conversation do not prove application or completion.
Use the shared [Core review](../caveman/rules/core.md#review) for reporting; the rules below define engineering evidence.

- Read back changed state before claiming application. Report partial results separately.
- Keep missing, stale or untested observations unknown; name the affected claim or platform.
- Separate model, adapter, process and target-platform checks. Passing one does not qualify the others.
- Verify the exact candidate or artifact being accepted; identify relevant checks and remaining gaps.

## State-driven systems

- Keep transitions in an explicit behavioral model; adapters handle external effects.
- Change the transition specification, executable traces, model and adapters in that order.
- Trace initial state and events to expected state, including ignored events.
- Cover duplicates, stale events, ordering and human-authored input where supported.
- Keep product states, commands, fixture paths and acceptance thresholds in the consumer contract.
