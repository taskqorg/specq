# Spec enforcement: from linked rules to checked rules

Question ([#93](https://github.com/taskqorg/specq/issues/93)): taskqorg rules are linked from every entry file, but nothing stops a later change from rewriting or dropping them. How do spec-driven teams enforce specs, which formal checks fit our rule kinds, and what should we add?

Status: approved on 2026-10-29. The owner took the full recommendation ([decision](#decision)): option 1 piloted in taskq, then option 2; option 3 only per proven gap. This page changes no rule; implementation is the staged task [taskq#1794](https://github.com/taskqorg/taskq/issues/1794).

Short answer: no popular spec-driven tool checks that a requirement survives a later change; they check that a spec is well formed, and the rest is LLM self-review. Formal languages (Lean, TLA+, Alloy) check a model, not our Markdown rules, and a hand-kept model drifts. Since [#94](https://github.com/taskqorg/specq/pull/94), [decided rules](../agent-workflow.md#decided-rules) forbid changing a rule or its guarding assertion unless the task names it, but only review applies that rule, and review already missed both taskq regressions. A cheap deterministic check would have caught both: a CI gate that lists every changed or removed rule block and guarding assertion and fails unless the linked task names each one. Recommended: that gate first, piloted in taskq; rule-to-check coverage second; a property-based model of `fold` and board-log monitors only where evidence shows a gap.

Revisions read on 2026-10-29: specq `75417548f88706fe1460ae980b2628fc3b1d7eb0` (after #94), taskq `d4ba0706d2b9e3a41dee9bc459202f77aaba0371`. External sources were read on the same day; items not confirmed from a primary page are marked unverified.

## 1. What spec-driven tools enforce

"Enforces" means a deterministic check that fails: a nonzero exit, a blocking hook or a required CI status. Prompt templates, constitutions and LLM-run reviews are "claims".

| Tool | Enforces | Claims only | Detects a dropped or weakened requirement later |
|---|---|---|---|
| [GitHub Spec Kit](https://github.com/github/spec-kit) | A `check-prerequisites` script aborts when `spec.md` or `tasks.md` is missing. | Constitution, "Phase -1 gates", checklists, [`/speckit.analyze`](https://github.com/github/spec-kit/blob/main/templates/commands/analyze.md) (read-only, keys coverage on `FR-`/`SC-` IDs) and `/speckit.converge` are LLM prompts. [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md) calls the gates "compile-time checks"; no compiler runs them. | No. `converge` compares code to requirement IDs through the LLM and says of itself that it "is not a diff tool and does not track changes". |
| [AWS Kiro](https://kiro.dev/docs/specs/feature-specs/) | [Hooks](https://kiro.dev/docs/hooks/types/) with shell commands: exit 2 on pre-tool, prompt-submit or pre-task blocks the action. Optional [property-based tests](https://kiro.dev/docs/specs/correctness/) derived from EARS requirements fail mechanically and link back to their requirement. | EARS wording is not validated; "Analyze Requirements" is undocumented LLM review; task completion is set by the agent. | No. "Sync Files" adds tasks for new requirements; removal or weakening is not detected. |
| [Tessl](https://docs.tessl.io/codifying-and-enforcing-your-skill-standards/verifiers-overview.md) | `tessl change verify` runs "verifiers" on changed files and can block a PR as a [required check](https://docs.tessl.io/codifying-and-enforcing-your-skill-standards/verify-agent-changes-in-ci.md). | The judge is an LLM; Tessl's own docs advise linters or tests where a rule is deterministic. The earlier spec-as-source framework is closed beta (unverified beyond snippets). | Only a scheduled LLM docs audit. |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | `openspec validate --strict` exits 1: each requirement needs `SHALL` or `MUST` and a scenario, each change needs a delta, retiring a capability's last requirement needs an explicit flag ([CLI](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)). The strongest structural validator found. | `/opsx:verify` (code implements spec) is an agent command. | No. A `REMOVED` requirement is deleted on archive without a reason; a weaker `MODIFIED` text passes if it keeps `SHALL` and a scenario. |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | Nothing on spec content found. | Personas, readiness check, Test Architect `trace` gate (PASS/CONCERNS/FAIL/WAIVED) are LLM workflows. | None documented. |
| [AGENTS.md](https://agents.md/) | Nothing: plain Markdown, nearest file wins, chat overrides it. | Everything. | No. |
| [Claude Code hooks](https://code.claude.com/docs/en/hooks) | Exit 2 or `deny` blocks a tool call; a Stop hook can keep the agent working. Deterministic, but the team writes the check. | — | Only what a written hook checks. |

Studies of context files:

- [Gloaguen et al., arXiv:2602.11988](https://arxiv.org/abs/2602.11988): agents do follow `AGENTS.md`-style files, but the files tend to lower task success and raise cost by more than 20%; they help most for unusual conventions.
- [Lulla et al., arXiv:2601.20404](https://arxiv.org/abs/2601.20404): on 124 PRs, a context file cut median runtime by 28.6% and output tokens by 16.6% at comparable completion; it measured efficiency, not rule compliance.
- [dos Santos et al., arXiv:2606.15828](https://arxiv.org/abs/2606.15828): in 100 `AGENTS.md`/`CLAUDE.md` files the most common defect is "lint leakage" (62%): style rules a linter should enforce, written as prose.
- Our own measurement ([spec delivery](spec-delivery.md)): on three real taskq tasks, injecting the whole contract kept the task rule in 4 of 4 defect runs; smaller modes kept it in at most 2 of 4. Delivery raises compliance; it does not make it certain.

Criticism:

- Birgitta Böckeler, [Understanding spec-driven development: Kiro, spec-kit and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) (2025-10-15): the tools are "spec-first", rarely "spec-anchored"; agents often ignored instructions; Markdown is tedious to review ("I'd rather review code than all these markdown files"). [Thoughtworks Radar](https://www.thoughtworks.com/radar/techniques/spec-driven-development) placed SDD in "Assess" (November 2025).
- Hacker News: [The Waterfall Strikes Back](https://news.ycombinator.com/item?id=45935763): specs and code diverge, and agents "change tests to pass". [OpenSpec thread](https://news.ycombinator.com/item?id=49734264): specs "rot" in long-lived repositories; a two-way audit found "huge divergence"; "illusion of control". [What happened to SDD?](https://news.ycombinator.com/item?id=49182353): code stays the source of truth. Reddit was not reachable for this survey: unknown.

What the field leaves open is exactly our failure: no tool refuses a change that deletes or weakens a requirement, keeps a rule bound to a passing check, or flags a rule and its test rewritten in the same change.

## 2. Spec-to-formal checks

Our rule kinds:

- **S, state machine**: the task lifecycle `fold` over the board log (§ 2 table, leases, fencing, duplicates, stale events).
- **U, UI layout**: for example the menu host strip (labels, hidden zero counts, one line at 320 px, both themes).
- **P, process**: for example spec first, research ends with an ask, the third follow-up rule, no rule removed without the owner.

Key risk, already ruled on in [taskq#641](https://github.com/taskqorg/taskq/issues/641): a second hand-synchronized model drifts from the runtime. Only approaches that check the real code or real runs avoid it.

| Approach | What it checks | Cost for us | Tied to real code | S | U | P |
|---|---|---|---|---|---|---|
| Lean 4 | Machine-checked proofs | Highest; LLMs prove rarely: [Verina](https://arxiv.org/abs/2505.23135) 4.9% proofs, [vericoding](https://arxiv.org/abs/2509.22908) Lean 27% | No; [AWS Cedar](https://amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing) needs differential testing to tie Lean to Rust | partial | poor | poor |
| TLA+ with trace validation | Safety and liveness of a model; logged runs against the spec ([arXiv:2404.16075](https://arxiv.org/abs/2404.16075)) | Medium; code instrumentation | With trace validation: Microsoft CCF found 6 bugs in CI ([arXiv:2406.17455](https://arxiv.org/abs/2406.17455)); MongoDB judged trace checking impractical and used model-generated tests instead ([arXiv:2006.00915](https://arxiv.org/abs/2006.00915)) | good | poor | partial |
| Quint + [quint-connect](https://quint-lang.org/posts/quint_connect) | TLA semantics in typed syntax; replays generated traces against Rust | Medium-low | Yes, by replay | good | poor | poor |
| Alloy 6 | Bounded relational and temporal models | Low-medium | No | partial | poor | partial |
| Dafny / Verus | Verified code with pre/postconditions | Medium; Dafny means a second implementation, Verus stays in Rust | Yes for Verus | partial | poor | poor |
| P + PObserve | Communicating state machines; monitors over production or test logs ([CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services)) | Medium | Yes, by log monitors | good | poor | partial |
| Stateful property tests ([proptest-state-machine](https://docs.rs/proptest-state-machine), [Hypothesis](https://hypothesis.readthedocs.io/en/latest/stateful.html)) | A reference model against the implementation over generated event sequences, with shrinking | Low; same language and CI | Yes | good | partial | poor |
| EARS | Sentence templates ("When ..., the system shall ...") | Very low | Checks nothing by itself; removes ambiguity before a check | partial | good front end | good front end |
| Gherkin | Given/When/Then examples bound to step code | Low start; step glue goes stale | Yes, per example | partial | partial | partial |
| Playwright geometry and [screenshots](https://playwright.dev/docs/test-snapshots) | DOM boxes per viewport and theme; pixel diffs | Low; baselines need upkeep | Yes | poor | good | poor |
| LLM autoformalization ([nl2spec](https://arxiv.org/abs/2303.04864), [nl2postcond](https://arxiv.org/abs/2310.01831), [SpecGen](https://arxiv.org/abs/2401.08807), [Clover](https://arxiv.org/abs/2310.17807), [Req2LTL](https://arxiv.org/abs/2512.17334), [TLA+-Bench](https://arxiv.org/abs/2607.23425)) | Drafts formulas from text | Low per draft; every draft needs a human or test oracle | No | helper | helper | helper |

Findings for us:

- LLMs write syntactically valid specs easily and correct ones rarely; [Lahiri, arXiv:2603.17150](https://arxiv.org/abs/2603.17150) names intent formalization an open challenge. An LLM draft is never the authority.
- S is already the best-covered kind in taskq: `fold` is the executable model and `tests/golden/fold.json` holds 99 traces. The cheapest next step is generated event sequences against the same `fold` with invariants, not a new model language. Quint or TLA+ trace checking pays only if cross-host leases become the main defect source.
- U rules become executable as clause-level assertions: a pure-function test of the label rule, DOM geometry at the stated width in both themes. taskq already does this (`tests/menu-host-strip.browser.cjs`).
- P rules are about agent behavior, so only git-diff and board-log checks can enforce them. No logic formula helps; EARS-style wording helps the check author.
- Neither a proof nor a model stops our two regressions: the agent rewrote the rule and the check together. That needs a check on the change itself.

## 3. Gap audit

Control: **none** (nothing checks it), **review** (an agent or the owner reads it), **test** (a deterministic check fails), **model** (an executable model plus traces), **command** (taskq refuses bad input before writing).

| Rule kind | Example | Home | Control today | Gap |
|---|---|---|---|---|
| Lifecycle transitions | § 2 table rows | taskq.md § 2 | model + test: `fold`, 99 golden traces, `every_table_row_has_a_golden_trace` (`src/core.rs`) | Generated sequences (duplicates, reordering) cover only what traces list. |
| Contract size and form | ≤ 300 lines, ≤ 60 KiB, no dates | taskq.md R8, Change rule | test (same function) | The size cap pushes cuts; nothing checks what a cut removes. |
| Card and result limits | Ask card ≤ 160 per option; result lines ≤ 240 | taskq.md § 2, § 7; R7 | command: `taskq ask/result` refuse over-limit text | none |
| Runtime names in adapters only | — | taskq docs/runtime-qualification.md | test: `scripts/check.py` `runtime_names` | none |
| Change rule | Rule changes name the R-number; numbers kept | taskq.md Change rule | review (result text) | Nothing lists removed or changed R-numbers or sections. |
| Spec first | Edit the contract first; conflicts are asks | taskq R13, [spec first](../spec-first.md) | review | Nothing links a changed rule to an authorizing Acceptance item or owner answer. |
| Decided rules | A rule or guarding assertion changes only when the task names it and the owner decision | specq [decided rules](../agent-workflow.md#decided-rules) (#94) | review: reject unnamed rule changes | Review must find every changed rule line by reading the diff; nothing lists them. |
| PM intake triage | Classify each request, one confirm card | taskq.md v3 § 7 "Take requests" (#464) | was test (`tests/test_single.py` asserted `taskq pm` prints it); now none in taskq; since #94 specq [task intake](../agent-workflow.md#task-intake) holds a triage rule (steer, merge, dependency, new, reject; acceptance checked against decided rules), by review | Lost in the v4 rewrite (regression 2); restored as prose, still unchecked. |
| UI layout rules | Menu host strip label rule | taskq docs/design/menu.md M3 "Running agents" | test: `tests/menu-host-strip.browser.cjs` | The test cites issue numbers, not a rule ID; rule and test can change together unnoticed (regression 1). |
| Owner design corrections | R01-R44, D1-D8 | taskq docs/design/review-handoff.md, ai-workspace.md | review: native audit tables | Rules overlap and conflict across pages (R16 vs M3); nothing detects a conflict. |
| Test weakening | "Do not change expected output just to make a failure green" | specq [testing](../testing.md#when-evidence-disagrees) | review | No check flags a changed or deleted assertion. |
| Process rules | Research ends with an ask; third follow-up; one task per outcome | specq [agent workflow](../agent-workflow.md) | review (taskq reviewer brief) + command (new tasks enter held) | No board-log check: a research task closed without an ask is found only by review. |
| Writing style | Core, documentation | specq [caveman](../../caveman/README.md) | review; partly command (taskq limits) | Lint-shaped rules sit in prose (the "lint leakage" smell). |
| Shared-rule hygiene | Local links resolve; upstream snapshot unchanged | specq `caveman/scripts/check.py` | test | Nothing checks that a removed rule or anchor is not linked by a consumer. |
| Security baseline | Branch protection, scanners, permissions | specq [security](../security.md) | test, run by hand: `engineering/scripts/repo-security-check.sh` | Runs only at review time. |

Traceability today in taskq: 409 `// Chain:` comments name their requirement and risk ([testing](../testing.md#before-adding-or-changing-a-test) step 4). Of them, 165 cite a `§`, 111 an issue number and 24 an R-number. Of 1,253 browser and Node assertions, 36 cite an issue number and 27 a design ID in their message. The links exist, but they point at issues more often than at rules, and nothing reads them.

### Regression 1: host strip labels (taskq#1729, then taskq#1775)

- [taskq#1729](https://github.com/taskqorg/taskq/issues/1729), an owner task, set the rule in `docs/design/menu.md` M3 "Running agents": three-letter labels, longer on collision, four hosts on one line. PR [#1731](https://github.com/taskqorg/taskq/pull/1731) (`e83d64f`) added the assertions `['her','mac 1','pil 1','win 1']` and "four hosts fit one line".
- [taskq#1775](https://github.com/taskqorg/taskq/issues/1775) Acceptance A3, filed the next day, listed "hermes-fra1 is clipped to her (R16, R30)" as a known Fail. R16 asks for named hosts; R30 forbids one-letter clipping in Services. The conflict with the newer M3 rule was not named.
- PR [#1776](https://github.com/taskqorg/taskq/pull/1776) (`bf4a2be`) rewrote M3 to full names that wrap, and in the same change rewrote the assertions to full names and relaxed "one line" to "at most two lines". The test message even says "(was #1729 three-letter labels)". The reviewer closed the task.
- How it slipped: the task text contradicted an approved rule, and intake readback did not compare it with the spec; the rule had no ID of its own, only an issue number; A6 required an ask only for a design-versus-contract conflict, not design-versus-design; nothing listed the rule and assertion changes for the reviewer, and the green test proved only the new text.

### Regression 2: PM intake triage (taskq#464, then `ecb1e57d`)

- [taskq#464](https://github.com/taskqorg/taskq/issues/464) restored the intake algorithm as taskq.md § 7 "Take requests" (`eae8ed1`, #468): collect, read the board once, classify (amend, merge, new, dep, reject, ask), name conflicts, one confirm card, apply only rows answered yes. A test asserted that `taskq pm` prints it.
- `ecb1e57d` (2026-10-12, "taskq v4 contract and Rust binary") replaced the 2,845-line v3 contract with a 297-line v4 contract and moved v3 to `docs/legacy/taskq-v3.md`. 60 of 72 v3 headings have no heading of the same name in v4; "Take requests" is one of them. The new test capped the contract at 300 lines.
- How it slipped: the rewrite had no inventory of what each removed section became (moved, merged or dropped); the old guard test stayed with v3 and no v4 test replaced it; the size cap rewarded deletion; the text survived only in a legacy file that no agent must read, which counts as removal. specq #94 restored a shorter triage rule on 2026-10-29, again guarded only by review.

## 4. Options

Each option is judged against the two regressions and the three rule kinds.

1. **Rule-change gate in CI.** A script compares the PR with its base. It lists every changed or removed rule block (taskq.md R-sections and § headings, § 2 rows, ID'd design headings and table rows) and every changed or deleted assertion or `Chain:` line that cites a rule ID or issue. The gate reads the task named by the commit's `Task:` line and fails unless its body names each listed ID; each removal also needs a destination (moved to a path) or a named owner decision. This is the mechanical form of [decided rules](../agent-workflow.md#decided-rules): review then checks a short list instead of the whole diff.
   - Plus: catches both regressions (#1776 changes M3 and two #1729 assertions that #1775 did not name; `ecb1e57d` removes 60 headings); deterministic; one script in the existing gate.
   - Minus: tasks that change rules must name rule IDs; design rules need IDs first; the gate needs a board read in CI.
2. **Rule IDs mapped to checks.** Every rule that a check can test gets a stable ID and at least one `Chain:` citation; a coverage report lists rules without a check or marked `review-only`. Report only at first, then a gate for new rules.
   - Plus: shows which rules are protected at all; uses the existing `Chain:` convention; answers the owner's "rules as entities" ask without a new language.
   - Minus: a citation proves that a test exists, not that it tests the rule; it does not by itself stop a rule and its test from changing together.
3. **Formal model layer.** Generated event sequences with invariants against `fold` (S), clause-level property and geometry tests for UI rules (U), and board-log monitors for process rules (P), for example "a research task closed without an ask".
   - Plus: strongest semantic checks; P monitors check what agents actually did.
   - Minus: highest cost; S is already modeled; a model is rewritten as easily as a test, so neither regression is stopped.
4. **Keep review only (status quo since #94).** [Decided rules](../agent-workflow.md#decided-rules) and the review line that rejects unnamed rule changes stay the only control.
   - Plus: already active; no code.
   - Minus: both regressions passed review; a cut from 2,845 to 297 lines or two changed assertions in a 53-file diff are easy to miss by reading.

Recommended: option 1 now, option 2 as its second stage, option 3 only per proven gap. Option 1 is the only one that targets the failure we observed (a change that rewrites or drops a rule together with its guard), it is deterministic, and it turns the rule #94 just adopted into a check. Option 2 makes the gate precise. Option 3 is justified per rule kind only when a defect escapes 1 and 2.

### Staged plan

1. **Pilot in taskq (one task).** Add the rule-change gate to `scripts/check.py` for `taskq.md`, `docs/design/menu.md` and `tests/`. Give the M3 sub-rules IDs (for example `M3.1` host strip labels; invented). Acceptance: replaying `bf4a2be` and `ecb1e57d` against their parents fails with the changed IDs listed; naming the IDs in the task body makes them pass; a docs-only typo fix outside rule blocks passes untouched. Measure false positives over the next 20 merged PRs.
2. **Shared rule in specq.** Done in [#96](https://github.com/taskqorg/specq/issues/96). After the pilot, add one line to [decided rules](../agent-workflow.md#decided-rules): projects enforce it with a rule-change gate; the script and ID syntax stay in each consumer.
3. **Coverage report.** Rule IDs mapped to `Chain:` citations, report only; gate for new rules once the report is clean.
4. **Per-kind models, on evidence.** Board-log monitors for process rules first (the board log is already folded); generated `fold` sequences when a lifecycle defect escapes the golden traces; no Lean.

## Ask

Rule enforcement: a task can still rewrite or drop a decided rule and its test in one PR; only review checks it, and review missed both taskq cases.

1. Rule-change gate in CI. Plus: catches both regressions, deterministic. Minus: tasks must name rule IDs they change.
2. Rule IDs mapped to checks. Plus: shows unprotected rules. Minus: does not stop a rule and its test changing together.
3. Formal model layer. Plus: strongest semantic checks. Minus: highest cost; a model is rewritten as easily as a test.
4. Keep review only (since #94). Plus: no code. Minus: review already missed both cases.

Recommended: 1, piloted in taskq, then 2; 3 only per proven gap, because 1 is the only option that targets the observed failure.

## Decision

Owner, 2026-10-29: take the full recommendation. Option 1, the rule-change gate, is piloted in taskq; option 2, the rule-ID coverage report, follows; option 3 models are added only per proven gap. Implementation is one staged taskq task: [taskq#1794](https://github.com/taskqorg/taskq/issues/1794). A shared rule in specq follows the pilot ([staged plan](#staged-plan), step 2) as its own change.
