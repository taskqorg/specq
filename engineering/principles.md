# Working principles

specq owns the rules every taskqorg project shares. A project repository keeps only what is specific to that project.

## Rules

- Shared rules live in specq: texts, notifications, design and engineering practice. The [spec area index](../README.md#spec-areas) names the owner page of each area.
- Each project's `AGENTS.md` and other agent entrypoints stay thin and discoverable: they name specq as binding for every task and link the project contract and the owner pages it uses. Example line (invented): `Shared rules: https://github.com/taskqorg/specq (binding for every task).`
- A project links to specq, never copies it. A rule that two projects need moves here; a rule only one project needs stays in that project's spec ([spec first](spec-first.md)).
- Effort follows result: pick the measure that removes most of the risk or work for the least effort, do it fully, and name what it leaves open. A heavier process waits for evidence that the light one failed.
- Measure before optimizing: each product profiles its own operations by [built-in profiling](profiling.md), and optimization work cites that evidence before and after the change.
- Owner pages keep their URLs. A move leaves the old path resolving, or updates every link from taskqorg projects in the same deliverable.

## Rule homes

| Content | Canonical home |
|---|---|
| Reusable design, writing, workflow or verification principle | Applicable shared specification |
| Product entities, state meanings, operations and authority | Project root contract and linked specifications |
| Dimensions, assets, platform policies and acceptance fixtures | Project design package |
| Scenarios and product-specific exceptions | Project use cases / contract |
| Observations, screenshots and test results | Revision-specific evidence |

Shared rules contain no consumer names, paths, catalogs or product-specific thresholds. A local shared edit does not prove publication, consumer adoption or deployment.

## Project docs cleanup

Check each page of the project, one item at a time.

- Moves to specq: a style, notification, design or engineering rule that is not about this project alone. Move it to the area's owner page, then link it from the project.
- Stays in the project: the project spec (`<project>.md`) with its decisions, thresholds and names; README usage; project-only examples and golden traces.
- Deleted: a copy or paraphrase of a specq rule; a page that only restates the spec or another page; instructions for a removed feature.
- After the cleanup: `AGENTS.md` names specq as binding; no project page repeats a specq rule; every changed link resolves.
