# Working principles

specq owns the rules every taskqorg project shares. A project repository keeps only what is specific to that project.

## Rules

- Shared rules live in specq: texts, notifications, design and engineering practice. The [spec area index](../README.md#spec-areas) names the owner page of each area.
- Each project's `AGENTS.md` and other agent entrypoints stay thin and discoverable: they name specq as binding for every task and link the project contract and the owner pages it uses. Example line (invented): `Shared rules: https://github.com/taskqorg/specq (binding for every task).`
- A project links to specq, never copies it. A rule that two projects need moves here; a rule only one project needs stays in that project's spec ([spec first](spec-first.md)).
- Before creating, changing, reviewing, deleting or running tests, changing CI gates, or working on releases or deployments, agents must read and follow [Testing](testing.md).
- Effort follows result: pick the measure that removes most of the risk or work for the least effort, do it fully, and name what it leaves open. A heavier process waits for evidence that the light one failed.
- Best fit for our conditions: we control the servers and design the services, so a design may change anything; language, tools and hosting are chosen for the most stable and fastest result, not to fit the current setup. Stability first; speed is continuous optimization from telemetry. A plan, report or proposal sets no pass threshold, ceiling or limit on speed, overhead or resource use as a condition to build or adopt: what the system's logic requires ships even when slower; measurement shows what to optimize next ([observe, do not gate](performance.md#observe-do-not-gate)).
- Make it work first: add a limit, timeout, cap, budget or cache only when telemetry shows a real problem. Display limits and contract size budgets retain their [existing rules](contracts.md#size-budgets).
- Measure before optimizing: each product profiles its own operations by [built-in profiling](profiling.md); optimization cites that evidence per its [report](profiling.md#report).
- Owner pages keep their URLs. A move leaves the old path resolving, or updates every link from taskqorg projects in the same deliverable.

## Rule homes

| Content | Canonical home |
|---|---|
| Reusable design, writing, workflow or verification principle | Applicable shared specification |
| Product entities, state meanings, operations and authority | Project root contract and linked specifications |
| Dimensions, assets, platform policies and acceptance fixtures | Project design package |
| Scenarios and product-specific exceptions | Project use cases / contract |
| Observations and test results | [Project documents](#project-documents): cited evidence records; other findings go into specifications |
| Screenshots and other working papers | Pull requests, tasks or ignored local scratch |
| Decision history, dates and owner or task attributions | Tasks, pull requests and git history |

Shared rules contain no consumer names, paths, catalogs or product-specific thresholds. A local shared edit does not prove publication, consumer adoption or deployment.

## Project docs cleanup

Check each page of the project, one item at a time.

- Moves to specq: a style, notification, design or engineering rule that is not about this project alone. Move it to the area's owner page, then link it from the project.
- Stays in the project: the project spec (`<project>.md`) with its decisions, thresholds and names, in the [contract shape](contracts.md); README usage; project-only examples and golden traces.
- Deleted: a copy or paraphrase of a specq rule; a page that only restates the spec or another page; instructions for a removed feature.
- After the cleanup: `AGENTS.md` names specq as binding; no project page repeats a specq rule; every changed link resolves.

## Project documents

Each project file has one kind, decided by its path. The project contract names or links the path rules.

- Contract: the one root file of decisions ([contracts](contracts.md)).
- Index: one row per specification: topic, file, one-line summary. The attempt index lists the same files.
- Specification: the current target of one topic. One file per topic, rewritten in place; no history and no dated sections. A part not yet built says so in one line.
- Evidence record: a measurement that a specification or code cites for its exact numbers. Unchanged after merge except link fixes; deleted when nothing cites it.
- Working paper: brief, draft, review, drift report, handoff, screenshot, rejected option. Never committed; it lives in the pull request, the task or ignored local scratch. A finding that must survive goes into the specification it changes.

Before adding a file, find the topic's index row and edit that file. Add a specification only with its new row, and say in the pull request why no row fits. File names carry no dates.

A project check reports, without failing the build: specifications the index does not list, links and cited paths that do not resolve, working papers and uncited evidence in the tree, and the size and file change of each pull request. On the main branch the findings keep one open work item, updated on each run and closed when none remain.
