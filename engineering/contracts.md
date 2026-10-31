# Project contracts

A project contract (`<project>.md`) is the one root file of a project's decisions ([spec first](spec-first.md)). This page sets its shape, writing rules and budget. [`contract_lint.py`](scripts/contract_lint.py) checks the mechanical part.

## Shape

A contract has these parts, in this order:

1. Title (H1) and purpose: one paragraph on what the product does and does not do.
2. `Principles` (or `Rules`): the mandatory rules, most important first. Each one starts with a stable ID, such as `R1`.
3. Product sections, one per area, most important first. Inside a section, mandatory rules come first and detail follows.
4. Linked detail: one line per linked file, its path plus a one-line summary.

Headings alone read as a usable outline ([Documentation review](../caveman/rules/documentation.md#review)). Headings are descriptive and unique, skip no level, and are never generic, such as `Notes` or `Other`.

## Writing

- A contract states current rules only. It has no history, dates, decision logs, changelogs or owner and task attributions; those live in tasks, pull requests and git history ([rule homes](principles.md#rule-homes)).
- Open questions are owner asks, not contract sections ([spec first](spec-first.md#improve-shared-rules)).
- A task or issue number appears only where a rule needs a trace, such as a pilot or a recorded exception.
- One idea per paragraph ([Documentation](../caveman/rules/documentation.md#structure)). A source line holds at most 400 visible characters, about three sentences of 20 words. Link targets and code blocks do not count.

## Budget

- The default cap is 60 KiB (61440 bytes) and 300 lines. A contract may declare its own cap in one comment line, for example (invented values): `<!-- contract-budget: bytes=81920 lines=400 -->`. A declared cap is a decision of that contract.
- A cleaned contract stays at or below 70% of its cap. The rest is headroom for new rules.
- A change that would cross the cap moves the lowest-priority detail to a linked file until the contract is back at or below 70%. Linked files are not injected; the attempt index lists them ([attempt context](rule-delivery.md#attempt-context)).
- Never squeeze wording, drop a condition or merge ideas to fit the cap ([Documentation review](../caveman/rules/documentation.md#review)).

## Lint

`python3 engineering/scripts/contract_lint.py <contract.md>...` uses the Python standard library only. It prints bytes, lines and the longest line per file, then one finding per line. It exits 1 on any error; headroom above 70% is a warning.

- Checks: cap, headroom, line length, ISO dates, decision-log phrases, and the outline: one H1 first, a purpose paragraph, `Principles` or `Rules` as the first section, no skipped level, no duplicate, generic or history heading.
- Not checked: priority order, rule IDs and whether a task number is needed. Review judges these.
- specq runs the lint on [specq.md](../specq.md) inside `caveman/scripts/check.py`, in CI.

A project runs the lint from its own check at a pinned specq commit. Example GitHub Actions steps (invented placeholders):

```yaml
- uses: actions/checkout@v4
  with: {repository: taskqorg/specq, ref: <specq commit SHA>, path: .specq}
- run: python3 .specq/engineering/scripts/contract_lint.py <project>.md
```
