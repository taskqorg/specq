# Project contracts

A project contract (`<project>.md`) is the one root file of a project's decisions ([spec first](spec-first.md)). This page sets its shape, writing rules and budget. [`contract_lint.py`](scripts/contract_lint.py) checks the mechanical part.

## Shape

A contract has these parts, in this order:

1. Title (H1) and purpose: one paragraph on what the product does and does not do.
2. `Principles` (or `Rules`): the mandatory rules, most important first. Each one starts with a stable [rule ID](#rule-ids).
3. Product sections, one per area, most important first. Inside a section, mandatory rules come first and detail follows.
4. Linked detail: one line per linked file, its path plus a one-line summary.

Headings alone read as a usable outline ([Documentation review](../caveman/rules/documentation.md#review)). Headings are descriptive and unique, skip no level, and are never generic, such as `Notes` or `Other`.

## Rule IDs

Every mandatory rule starts with a stable ID of the form `<SCOPE>-<prefix><n>`, for example `SPECQ-D7` or `TASKQ-R12` (invented). The ID says where the rule lives before anyone reads it.

- Scope is the repository name in capitals that owns the rule: `SPECQ` for a shared rule, the project name for its contract and linked pages. `SPECQ-` is shared and binding everywhere; any other scope is one project's decision ([rule homes](principles.md#rule-homes)).
- Prefix is one or two capital letters for the page or area. A scope lists its prefixes in its index ([specq prefixes](../specq.md#rule-prefixes)); one prefix has one page. The number is sequential within a prefix and never reused; a deleted rule leaves a gap. A sub-rule appends `.<n>`, for example `SPECQ-M3.1` (invented).
- Hyphen is the only separator. It survives Markdown anchors, grep, file names and issue titles; a dot would collide with sub-rule numbering and sentence ends.
- The full form appears at the definition and in every reference, including inside the owning repository. An attempt reads injected shared files and the project contract in one conversation, so a bare `D1` is ambiguous. A range names the scope once: `SPECQ-D1–D14`.
- A bare ID without scope refers to nothing; review rejects it. [`check.py`](../caveman/scripts/check.py) fails a specq rule defined without `SPECQ-`.

## Writing

- A contract states current rules only. It has no history, dates, decision logs, changelogs or owner and task attributions; those live in tasks, pull requests and git history ([rule homes](principles.md#rule-homes)).
- Open questions are owner asks, not contract sections ([spec first](spec-first.md#improve-shared-rules)).
- A task or issue number appears only where a rule needs a trace, such as a pilot or a recorded exception.
- One idea per paragraph ([Documentation](../caveman/rules/documentation.md#structure)). A source line holds at most 400 visible characters, about three sentences of 20 words. Link targets and code blocks do not count.

## Size budgets

A size budget limits how much content a file or bundle may hold, so that it stays cheap to inject and read. Every budget keeps a buffer.

- Each byte, line or count budget has a cap and a target of 70% of the cap. The target is the working limit, never the cap.
- Content above the target creates one compaction task at once. The project files it from its check output and does not file a second one while the first is open.
- CI fails only above the cap. Above the target and at or below the cap, CI passes and the compaction task carries the work.

Compaction restores content to at or below the target in this order ([Documentation](../caveman/rules/documentation.md#density-without-ambiguity)):

1. Make wording dense: every word carries meaning, and removing one changes it. Replace a phrase with one exact term where possible.
2. Keep one source of truth: a repeated idea lives once; other mentions link to it.
3. Only then move the lowest-priority detail to linked files.

Never drop a condition during compaction.

This rule covers these budgets:

- Contract size in bytes and contract length in lines, defined below.
- Injected rule size: the total of the contract, shared core and index that one attempt receives ([attempt context](rule-delivery.md#attempt-context)). The consumer that injects the rules states its cap.

Display limits are format rules, not budgets: for example, title length, line length and the field limits of an ask card or a notification. Content at a display limit is valid; text over it is rejected or shortened at once, with no target and no compaction task.

## Budget

- The default cap is 60 KiB (61440 bytes) and 300 lines. A contract may declare its own cap in one comment line, for example (invented values): `<!-- contract-budget: bytes=81920 lines=400 -->`. A declared cap is a decision of that contract.
- Linked files are not injected; the attempt index lists them ([attempt context](rule-delivery.md#attempt-context)).

## Lint

`python3 engineering/scripts/contract_lint.py <contract.md>...` uses the Python standard library only. It prints bytes, lines and the longest line per file, then one finding per line. It exits 1 on any error, including a file above its cap.

- A file above the target and at or below its cap gets one marker line, `COMPACT: <path>: <value> <bytes|lines> > target <target> (cap <cap>)`, and passes. A project check turns each marker into the compaction task of [size budgets](#size-budgets).
- Checks: cap, headroom, line length, ISO dates, decision-log phrases, and the outline: one H1 first, a purpose paragraph, `Principles` or `Rules` as the first section, no skipped level, no duplicate, generic or history heading.
- Not checked: priority order, rule ID numbering and whether a task number is needed. Review judges these.
- specq runs the lint on [specq.md](../specq.md) inside `caveman/scripts/check.py`, in CI.

A project runs the lint from its own check at a pinned specq commit. Example GitHub Actions steps (invented placeholders):

```yaml
- uses: actions/checkout@v4
  with: {repository: taskqorg/specq, ref: <specq commit SHA>, path: .specq}
- run: python3 .specq/engineering/scripts/contract_lint.py <project>.md
```
