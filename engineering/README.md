# Engineering rules

Reusable engineering rules. Projects link to the applicable rule and define their own implementation details.

- [Working principles](principles.md): shared-rule ownership and project boundaries.
- [Spec first](spec-first.md): canonical decisions, project boundaries and the improvement route.
- [Ponytail](ponytail.md): the smallest change that fully solves the task.
- [Agent workflow](agent-workflow.md): ownership, work cycle, approval boundaries and completion.
- [Use cases](use-cases.md): scenario structure, overlap and requirement coverage.
- [Verification](verification.md): evidence boundaries, unknown health, scoped remediation and behavioral models.
- [Testing](testing.md): test decisions, risk coverage, run selection, time budgets and disagreements.
- [Data and storage](data.md): store, durability, atomic files, bounds and crash checks.
- [Performance and capacity](performance.md): observe-not-gate rule, load tasks, order of work and resource budgets.
- [Built-in profiling](profiling.md): operation counters, agent work stages, system operations, traces, bounded store, analysis export and profile reports.
- [Release, update, service](release-contract.md): verifiable releases, safe updates, self-maintenance and service ownership.
- [Permission authority](permission-authority.md): trust boundaries for agent access.
- [Independent product connections](product-connections.md): consent, isolation, delivery, recovery and end-to-end evidence.
- [Security baseline](security.md): repository protection, secrets, [one durable GitHub token per host](security.md#one-durable-github-token-per-host), dependencies, releases and the review routine.
