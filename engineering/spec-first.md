# Spec first

Each project keeps its decisions, including product decisions, in one root contract, shaped and budgeted by [project contracts](contracts.md). Supporting specifications link to it; shared rules have their home in [principles](principles.md#rules).

- Edit the contract before changing a decision. Update implementation and supporting documents in the same deliverable.
- A conflicting task becomes a question with options. Only the owner approves decision changes.
- Verify implemented behavior against the contract. Keep design targets distinct from shipped behavior.

## Keep the owner's request

A spec rewords an owner request. The rewording keeps everything the owner asked for.

- A spec change made for an owner request quotes the owner's original text verbatim or links it, in the task, pull request or commit that makes the change. The contract itself stays free of history and attributions ([rule homes](principles.md#rule-homes)).
- A rewording that drops a case, path, condition or quality of the owner text narrows it. Narrowing is a decision change: only the owner approves it, as a [decision question](../caveman/rules/core.md#decision-questions).
- A user-visible requirement is an invariant over every path that produces that output: each entry point, mode, channel, fallback and error path. It is not a rule for one path, such as the final answer only.
- Its acceptance enumerates those paths and names the evidence for each one. A path left out is reported as an open gap, never assumed covered.

Example (invented): the owner asks for "readable help". A spec line "help lists every command" keeps the paths but drops readability, so it narrows the request.

Product/interface collaboration follows the [design workflow](../design/workflow.md); it connects these ownership rules to use cases, iterations and acceptance.

## Improve shared rules

An agent that sees a better way during any task follows this order: propose, change the specification, then implement.

- When work exposes a reusable gap, propose a change here with the problem, general rule, affected consumers and verification. A project-only improvement is proposed to the project contract the same way.
- Do not implement an improvement that changes a decision before the owning specification changes.
- Discuss the proposal before adoption: the proposing task closes with its options and a recommendation, and the owner decides it as a decision question ([experiment tasks](task-planning.md#experiment-tasks)). Keep unresolved proposals separate from active rules.
- After approval, update the canonical shared rule; remove duplicate wording from project specifications.
- Review consumer compatibility explicitly. A shared edit does not silently change deployed behavior or override a project contract.
- Keep product names, implementation references, dependency versions and project-specific thresholds in consumer specifications.
