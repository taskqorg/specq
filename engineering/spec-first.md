# Spec first

One file per project holds every decision, product ones included: `<project>.md` at the repository root (taskq: `taskq.md`).

- A change that alters a decision edits the spec first; code, README and pages follow in the same deliverable.
- A task that conflicts with a decision is a question to the owner with options, not an edit. Only the owner accepts a decision change.
- Every agent reads the spec before work. `AGENTS.md` and `CLAUDE.md` point to it and stay thin.
- The spec is the source of truth and matches the code: tests check it (behavior tables have golden traces; the spec fits a line limit) and code and spec ship in the same release.
- Briefs and docs link to the spec, never copy it.

Reference: [taskq.md](https://github.com/taskqorg/taskq/blob/main/taskq.md) R8 and R13.
