# Spec first

Each project keeps its decisions, including product decisions, in one root contract. Supporting specifications link to it.

- Edit the contract before changing a decision. Update implementation and supporting documents in the same deliverable.
- A conflicting task becomes a question with options. Only the owner approves decision changes.
- Verify implemented behavior against the contract. Keep design targets distinct from shipped behavior.
- Project specifications contain project-specific decisions and explicit exceptions; shared rules are linked ([principles](principles.md#rules)).

Product/interface collaboration follows the [design workflow](../design/workflow.md); it connects these ownership rules to use cases, iterations and acceptance.

## Improve shared rules

An agent that sees a better way during any task follows this order: propose, change the specification, then implement.

- When work exposes a reusable gap, propose a change here with the problem, general rule, affected consumers and verification. A project-only improvement is proposed to the project contract the same way.
- Do not implement an improvement that changes a decision before the owning specification changes.
- Discuss the proposal before adoption. Keep unresolved proposals separate from active rules.
- After approval, update the canonical shared rule; remove duplicate wording from project specifications.
- Review consumer compatibility explicitly. A shared edit does not silently change deployed behavior or override a project contract.
- Keep product names, implementation references, dependency versions and project-specific thresholds in consumer specifications.
