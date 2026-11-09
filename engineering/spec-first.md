# Spec first

Each project keeps its decisions, including product decisions, in one root contract, shaped and budgeted by [project contracts](contracts.md). Supporting specifications link to it; shared rules have their home in [principles](principles.md#rules).

- Edit the contract before changing a decision. Update implementation and supporting documents in the same deliverable.
- A conflicting task becomes a question with options. Only the owner approves decision changes.
- Verify implemented behavior against the contract. Keep design targets distinct from shipped behavior.

## Keep the owner's request

A spec rewords an owner request without dropping anything the owner asked for.

- A spec change made for an owner request quotes the owner's original text verbatim or links it, in the task, pull request or commit that makes the change. The contract itself stays free of history and attributions ([rule homes](principles.md#rule-homes)).
- Dropping a case, path, condition or quality of the owner text narrows it. Narrowing is a decision change that only the owner approves, as a [decision question](../caveman/rules/core.md#decision-questions).
- A user-visible requirement is an invariant over every path that produces that output: each entry point, mode, channel, fallback and error path, not one path such as the final answer. Acceptance enumerates those paths with the evidence for each; a path left out is an open gap, never assumed covered.

Example (invented): the owner asks for "readable help". A spec line "help lists every command" keeps the paths but drops readability, so it narrows the request.

Product and interface work follows the [design workflow](../design/workflow.md).

## Improve shared rules

An agent that sees a better way during any task follows this order: propose, change the specification, then implement.

- A reusable gap becomes a proposal here with the problem, general rule, affected consumers and verification; a project-only gap is proposed to the project contract the same way.
- The proposing task closes with options and a recommendation; the owner decides it as a decision question ([experiment tasks](task-planning.md#experiment-tasks)). Unresolved proposals stay separate from active rules.
- After approval, update the canonical shared rule; remove duplicate wording from project specifications.
- Review consumer compatibility explicitly: a shared edit changes no deployed behavior and overrides no project contract by itself.
- Product names, implementation references, dependency versions and project thresholds stay in consumer specifications ([rule homes](principles.md#rule-homes)).
