# Rule delivery

How a runner gives shared rules to an agent attempt, and how an agent integration is qualified. Consumer runners keep their file lists, caps and commands in their own contract.

## Attempt context

- The runner injects the project contract and the shared core at each attempt start. The shared core applies to every attempt: [principles](principles.md), [spec first](spec-first.md), [Ponytail](ponytail.md), [agent workflow](agent-workflow.md), [use cases](use-cases.md), [verification](verification.md), [security](security.md), [Caveman core](../caveman/rules/core.md), [documentation](../caveman/rules/documentation.md) and [change communication](../caveman/rules/changes.md).
- Every other shared file is linked from the injected index and is not injected. The agent loads it on demand when the task touches its area. Rule-repository contributor files (its `README.md`, `AGENTS.md`, `SECURITY.md`, scripts, vendor snapshots and audits) are neither injected nor indexed.
- A core file keeps only rules that apply to every attempt. A section that applies only to some attempts lives in a linked-only file; the core file keeps a one-line link under the old heading, so existing links resolve.
- A header names the injected revisions and states precedence: the project contract overrides shared rules where they conflict.
- Project `docs/` are not injected. The index lists them too: one line per file, path plus a one-line summary.
- A resume repeats the header and the index, not file bodies already in the conversation.
- Delivery uses the attempt brief only; no runtime-specific skill is required.

## Agent integration

The entry stays thin ([principles](principles.md#rules)) and loads the compatible installed contract. Qualify integration presence, actual instruction loading and the complete user flow separately. Report unavailable capabilities explicitly. Keep provider-specific commands, versions and qualification fixtures in the consumer project. A second supported client must be able to continue from authoritative project state without the original chat.
