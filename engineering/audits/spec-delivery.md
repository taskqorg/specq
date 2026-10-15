# Spec delivery to agents: full injection versus on-demand rules

Question ([#36](https://github.com/taskqorg/specq/issues/36)): should each attempt start with the whole contract and every shared rule in context ([#33](https://github.com/taskqorg/specq/issues/33)), or with an obligation, an index and rules loaded on demand through a mandatory skill?

Status: approved on 2026-10-15 ([#56](https://github.com/taskqorg/specq/issues/56)). [Attempt context](../agent-workflow.md#attempt-context), as amended by [#52](https://github.com/taskqorg/specq/pull/52), now holds the [rule text](#proposal): the whole project contract and the shared core are injected at attempt start, every other rule file is indexed, a resume repeats only the header and the index, and no native skill is required.

Short answer: keep the #52 hybrid and amend it for resume, the index and skills ([proposal](#proposal)). On three real taskq tasks, spec-first and ask-before-code compliance was 40 of 40 in every mode, from full injection down to skill-only; card format held in 59 of 60 final calls (one Claude `proposal` ask exceeded the option limit by 2 characters). Only the defect task separated the modes: full injection kept its rules in 4 of 4 runs, #52 in 2 of 4, and every smaller mode in at most 2 of 4. Full injection costs 26,000 Claude and 16,000 Codex start tokens more than #52; skill-only saves 46,000 and 30,000 tokens but loses on the defect task.

Measured on 2026-10-15 with Claude Code 2.1.299 (`claude-opus-5-5`, default effort) and codex-cli 0.159.3 (`gpt-6.1-sol`, effort `low`, the host default), on macOS (macbook-m2). Real-task runs use specq `317ea57c97f809bd65fc08ff80383147561df642`.

## How the runtimes load instructions

| Mechanism | Claude Code | Codex CLI |
|---|---|---|
| Project instruction file | `CLAUDE.md` from the working directory up to the root, loaded in full at launch as a user message. `@imports` load at launch too (at most 4 hops), so they save no context. A subdirectory `CLAUDE.md` loads when a file there is touched. Target under 200 lines. [memory](https://code.claude.com/docs/en/memory) | `AGENTS.md` (or `AGENTS.override.md`) from the project root (`.git` marker) down to the working directory, joined root first as a user-context message. Cap `project_doc_max_bytes`, default 32 KiB. A worktree has its own `.git`, so the main checkout's files above it are not read. [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Skills at start | Name and description only. Listing budget is 1% of the context window; each description is at most 1,536 characters. [skills](https://code.claude.com/docs/en/skills) | Name, description and path only. Listing budget is 2% of the context window (8,000 characters when unknown). [skills](https://learn.chatgpt.com/docs/build-skills) |
| Skill body | Loaded by the `Skill` tool when the model invokes it, or by `/name` at the start of a prompt (also in `-p`). After compaction, the first 5,000 tokens of each invoked skill are reattached. | The model reads `SKILL.md` with a shell command, or the user names `$name`. Resolution of `$name` inside a `codex exec` prompt is not documented: unknown. |
| Skill locations | `~/.claude/skills`, `.claude/skills` up to the repository root, `--add-dir`, plugins (`--plugin-dir` per session). | `.agents/skills` from the working directory up to the repository root, `~/.agents/skills`; `~/.codex/skills` is deprecated. |
| What a runner passes per attempt | The brief on stdin; `--append-system-prompt[-file]`, `--system-prompt[-file]`, `--plugin-dir`, `--settings`, `--setting-sources`, `--add-dir`. [CLI](https://code.claude.com/docs/en/cli-reference) | The brief on stdin; `-c developer_instructions=...`, `-c model_instructions_file=...` (replaces the built-in instructions), `-c project_doc_max_bytes=...`, `--add-dir`, `-p` profile. [config](https://learn.chatgpt.com/docs/config-file/config-reference) |
| Prompt cache | Prefix order is tools, system, messages; any change invalidates everything after it. [caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Cache reuse needs the whole rendered prefix to match. [caching](https://developers.openai.com/api/docs/guides/prompt-caching) |

Consequences for the runner:

- Every mechanism that loads at start (brief, `CLAUDE.md`, `AGENTS.md`, imports) costs its full size on every start. Only skills and plain file reads defer cost until use.
- `AGENTS.md` is capped at 32 KiB by default, so it cannot carry the whole contract anyway.
- The brief is the only channel that is identical for Claude, Codex and the codex-app turn. Skill directories differ per runtime, and Codex finds `.agents/skills` only inside the worktree or the user home.
- Resume sends a new brief into the same conversation. Re-injecting file bodies on resume adds them again to the context.

## Experiment on real tasks

Three closed taskq issues, replayed offline on a clone of `taskqorg/taskq` at the main commit their first attempt started from. Each run gets a taskq worker brief of the live shape (delivery commands and limits) with these changes: no fetch, push or PR (offline replay); the task text comes from a stub `inbox`; `taskq` is a stub ([taskq-stub](spec-delivery/taskq-stub)) that checks the result and ask format and logs each call; the live line "Do not wait for CI: `close` checks it" is missing. The permissions are the taskq worker defaults (Claude `dontAsk`, Codex `danger-full-access`).

| Task | Issue and base | What a compliant run does |
|---|---|---|
| RT1 | [taskq#1039](https://github.com/taskqorg/taskq/issues/1039) close tasks whose PR targets a release branch, `f1496cc` | Spec first (R13): edits `taskq.md` before `src/`, or asks before any edit when the task conflicts with the contract. |
| RT2 | [taskq#1096](https://github.com/taskqorg/taskq/issues/1096) flaky `retained_profile_report`, `9554bea` | `result`; [run policy](../verification.md#run-policy-by-stage): before/after evidence or the reason it is missing; the change names its contract rule as `R<n>` or `§`. |
| RT3 | [taskq#1125](https://github.com/taskqorg/taskq/issues/1125) hold a task for an owner action, `5541cc1` | `ask` before any edit: A2 conflicts with § 2 (every move to ready clears the attempt). The live worker asked the same. |

Modes, largest first:

- `full`: the #33 payload. The brief holds `taskq.md` (88-94 KB), every specq Markdown file (109 KB) and a `docs/` index: 204-211 KB.
- `core`: the active #52 rule. The brief holds the whole `taskq.md`, the ten shared-core files (33 KB) and an index of the other specq rule files and `docs/`: about 131 KB.
- `proposal`: like `core`, but of `taskq.md` only the preamble, R1-R13 and § 7 are injected; the other sections join the index; the header states a read obligation (read the indexed rules for the step before the first edit and before `result` or `ask`): about 59 KB.
- `hybrid`: like `proposal` without the shared core; a step guide names the rule files to read: about 27 KB.
- `skill`: the brief holds only a header with the obligation to load the `specq` skill before the first edit and before `result` or `ask` (under 3 KB). A native skill (`.claude/skills/specq` or `.agents/skills/specq`) holds the step guide and the index of `taskq.md` sections, specq rule files and `docs/`.

On-demand files are a local copy under `.taskq/specq/`. Indexes leave out specq contributor files (`README.md`, `AGENTS.md`, `SECURITY.md`, `scripts/`, `vendor/`, `audits/`, `docs/`).

Each of 30 combinations (3 tasks, 5 modes, 2 runtimes) ran twice: 60 runs. Builder: [real.py](spec-delivery/real.py); runner: [run-real.sh](spec-delivery/run-real.sh); metrics: [analyze-real.py](spec-delivery/analyze-real.py). Full per-run evidence: [real-runs.jsonl](spec-delivery/real-runs.jsonl) holds the metrics, every `result`, `ask` and `requeue` call with its complete arguments, the stub verdict and the taskq.md limit recheck, and the token usage of every model request (Claude: one entry per message; Codex: every `token_count` event of the session log, which may repeat an event, so two Codex runs sum above their `turn.completed` total). Excerpts, not evidence: [real-traces.jsonl](spec-delivery/real-traces.jsonl) holds the ordered trace of reads, edits and commands, each entry cut at 200 characters. Run and home paths are removed from both.

Metrics: start tokens are the input of the first model request (Claude: input plus cache write plus cache read; Codex: the first `token_count` event). Total input sums every request, cached reads included. `contract_read` and `rules_read`: the run opened `taskq.md` or an on-demand rule (the skill or a `.taskq/specq/` file) before its first edit and before its taskq command; `late` means after. In `core` and `proposal` the shared core is injected, so `rules_read` counts only further files. Valid first: the stub accepted the first `result`, `ask` or `requeue`. Limits first and final: the first and the accepted call keep every § 2 ask card and § 7 result limit, counted strictly (the R7 exemption for exact commands is not applied). Outside: commands that touched paths outside the run directory.

### Summary

| Runtime | Mode | Runs | Start tokens (mean) | Total input (mean) | Time s (mean) | Expected command | Valid first try | Limits kept (first / final call) | Task rule kept | Outside |
|---|---|---|---|---|---|---|---|---|---|---|
| claude | full | 6 | 108,307 | 765,654 | 75 | 6/6 | 6/6 | 6/6 / 6/6 | 6/6 | 0/6 |
| claude | core | 6 | 81,980 | 617,217 | 72 | 6/6 | 4/6 | 4/6 / 6/6 | 6/6 | 0/6 |
| claude | proposal | 6 | 55,489 | 471,001 | 74 | 6/6 | 6/6 | 5/6 / 5/6 | 4/6 | 0/6 |
| claude | hybrid | 6 | 45,078 | 571,009 | 115 | 6/6 | 5/6 | 5/6 / 6/6 | 5/6 | 0/6 |
| claude | skill | 6 | 35,768 | 601,058 | 87 | 6/6 | 6/6 | 6/6 / 6/6 | 5/6 | 0/6 |
| codex | full | 6 | 66,058 | 605,475 | 55 | 6/6 | 6/6 | 6/6 / 6/6 | 6/6 | 0/6 |
| codex | core | 6 | 50,340 | 554,091 | 66 | 6/6 | 6/6 | 6/6 / 6/6 | 4/6 | 0/6 |
| codex | proposal | 6 | 32,210 | 245,170 | 37 | 4/6 | 6/6 | 6/6 / 6/6 | 4/6 | 0/6 |
| codex | hybrid | 6 | 26,541 | 235,247 | 40 | 4/6 | 6/6 | 6/6 / 6/6 | 4/6 | 0/6 |
| codex | skill | 6 | 20,293 | 520,162 | 69 | 4/6 | 6/6 | 6/6 / 6/6 | 4/6 | 0/6 |

Findings:

- Start cost: the skill brief is under 3 KB, so about 34,000 Claude and 19,000 Codex start tokens are the runtime's own prompt, tools and this host's user instructions, present in every mode. Above that baseline, `full` injects about 74,000 Claude and 47,000 Codex tokens, `core` 48,000 and 31,000, `proposal` 21,000 and 13,000. Only `core` and smaller fit the #33 budget of about 50,000 tokens.
- Total cost: the on-demand runs still read the rules for their step (usually 3 to 6 files). Total input against `full` fell 19-38 % on Claude and 8-61 % on Codex. Time did not fall.
- Spec first and ask: all 40 RT1 and RT3 runs kept the rule. All 20 RT1 runs asked before any edit: at that base § 2 allows close only from review, later and failed, and § 7 publishes into main only, so A2 and A3 need an owner decision (the live worker produced a result instead). All 20 RT3 runs found the § 2 conflict and asked before any edit.
- Rule loading: every `skill` and `hybrid` run read the skill or the named rule files before its first edit and before its taskq command. In `proposal`, Codex read further rule files first in 6 of 6 runs and Claude in none, but Claude read the indexed `taskq.md` sections first in 5 of 6. `core` Claude runs opened `taskq.md` only after acting or never: it was already in context. No run touched paths outside its directory; the toy finding below (Codex running the specq gate under full injection) did not recur.
- Defect task (RT2), the only task that separated the modes. Kept: `full` 4/4, `core` 2/4, `hybrid` 2/4, `skill` 2/4, `proposal` 0/4. The misses:
  - Codex asked before any code in all 4 `hybrid` and `proposal` runs: A2 requires green CI and the replay forbids a push. With the live CI line missing from the brief, this is a defensible reading; Codex `full` and `core` reported `result` with CI listed as open.
  - Codex `skill` committed a fix and then sent `requeue` twice, because `cargo test --locked` failed one sandbox test (`seatbelt_keeps_workers_out_of_the_policy_store`) that also fails on the unchanged base on this host. Every Claude run and Codex `full` and `core` reported it as pre-existing.
  - Codex `core` sent `result` twice with neither a reproduction nor a reason.
  - Claude reproduced the race (forcing the trimmer to lose) in 8 of 10 runs, at least once in every mode. Four Claude runs (`proposal` 2, `hybrid` 1, `skill` 1) named the enforced rule only in prose ("every retained record is a successful append", "taskq.md profiling rule") instead of `§ 4` or an R-number.
- Format: the stub accepted 57 of 60 first taskq calls. A recheck of the full saved calls against every taskq.md card limit (R7 counting, numbering and `★` included) finds 56 of 60 first calls and 59 of 60 final calls within limits. Misses, all Claude: `core` sent a check without `command -- outcome` and a 264-character result line, `hybrid` a 166-character option, each fixed on the second try; `proposal` sent a 162-character option (157 characters plus `1. ` and ` ★`) as its final ask, which the stub accepted because it did not count numbering. No Codex call missed a limit. The commands and limits sit in the brief in every mode.

Limits:

- Two runs per cell on three tasks: a difference of one or two runs is not significant. The RT2 misses have causes tied to the replay (no CI, the missing CI line, one host-specific failing test) and to a strict naming criterion; missing rule text is not proven to cause them.
- Offline replay: no board, no push, no CI, no review round and no resume. Live qualification remains after the consumer change.
- The user-level instructions and plugins of this host loaded in every run and are part of each baseline. Each runtime used its host default model and effort.

### Per run

| rep | run | start | total | out | secs | contract_read | rules_read | command | repro | valid_first | limits_first | limits_final | task_rule | commit | outside |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RT1 core claude | 80920 | 496706 | 2125 | 32 | late | no | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT1 core codex | 48862 | 226306 | 847 | 33 | yes | no | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT1 full claude | 107152 | 440519 | 2310 | 36 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT1 full codex | 65295 | 215930 | 699 | 26 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT1 hybrid claude | 44946 | 430498 | 4220 | 51 | yes | yes | ask |  | no | no | yes | yes |  | 0 |
| 1 | RT1 hybrid codex | 27405 | 153622 | 1068 | 33 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT1 proposal claude | 55136 | 366066 | 3422 | 48 | yes | no | ask |  | yes | no | no | yes |  | 0 |
| 1 | RT1 proposal codex | 31644 | 230681 | 1083 | 33 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT1 skill claude | 35691 | 506394 | 3311 | 51 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT1 skill codex | 21712 | 185002 | 1059 | 35 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT2 core claude | 81699 | 983533 | 4760 | 143 | no | no | result | recorded why | no | no | yes | yes | yes | 0 |
| 1 | RT2 core codex | 49399 | 1296716 | 2972 | 131 | yes | yes | result | none | yes | yes | yes | no | yes | 0 |
| 1 | RT2 full claude | 107931 | 1411380 | 4736 | 143 | n/a (full) | n/a (full) | result | recorded why | yes | yes | yes | yes | yes | 0 |
| 1 | RT2 full codex | 65832 | 1376318 | 2797 | 117 | n/a (full) | n/a (full) | result | recorded why | yes | yes | yes | yes | yes | 0 |
| 1 | RT2 hybrid claude | 44922 | 817682 | 7295 | 215 | no | yes | result | reproduced | yes | yes | yes | no | yes | 0 |
| 1 | RT2 hybrid codex | 25467 | 408415 | 1805 | 66 | yes | yes | ask (want result) | none | yes | yes | yes | no |  | 0 |
| 1 | RT2 proposal claude | 55395 | 725969 | 5119 | 129 | no | no | result | reproduced | yes | yes | yes | no | yes | 0 |
| 1 | RT2 proposal codex | 31851 | 239091 | 1009 | 52 | yes | yes | ask (want result) | none | yes | yes | yes | no |  | 0 |
| 1 | RT2 skill claude | 35761 | 890808 | 5990 | 187 | yes | yes | result | reproduced | yes | yes | yes | yes | yes | 0 |
| 1 | RT2 skill codex | 19575 | 1597393 | 5048 | 168 | yes | yes | requeue (want result) | none | yes | yes | yes | no |  | 0 |
| 1 | RT3 core claude | 83398 | 253585 | 1797 | 32 | late | no | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 core codex | 52745 | 246986 | 664 | 19 | yes | no | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 full claude | 109820 | 445336 | 2437 | 35 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 full codex | 67033 | 221017 | 606 | 22 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 hybrid claude | 45539 | 449293 | 3868 | 54 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 hybrid codex | 25662 | 206279 | 953 | 32 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 proposal claude | 55729 | 357287 | 2631 | 38 | yes | no | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 proposal codex | 32046 | 292618 | 1024 | 37 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 skill claude | 35786 | 356241 | 3478 | 53 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 1 | RT3 skill codex | 19576 | 176604 | 998 | 28 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 core claude | 80933 | 416026 | 2377 | 34 | late | no | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 core codex | 48873 | 166672 | 702 | 21 | yes | no | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 full claude | 107165 | 440438 | 1966 | 38 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 full codex | 65306 | 215969 | 692 | 22 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 hybrid claude | 44769 | 448037 | 3876 | 65 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 hybrid codex | 27416 | 205540 | 1145 | 44 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 proposal claude | 55339 | 289782 | 2381 | 39 | yes | no | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 proposal codex | 31655 | 228373 | 915 | 30 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 skill claude | 35797 | 683294 | 4267 | 58 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT1 skill codex | 19579 | 222895 | 1099 | 40 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT2 core claude | 81522 | 1214062 | 5983 | 161 | no | no | result | reproduced | no | no | yes | yes | yes | 0 |
| 2 | RT2 core codex | 51555 | 1216096 | 4041 | 174 | yes | yes | result | none | yes | yes | yes | no | yes | 0 |
| 2 | RT2 full claude | 107944 | 1411233 | 5105 | 168 | n/a (full) | n/a (full) | result | reproduced | yes | yes | yes | yes | yes | 0 |
| 2 | RT2 full codex | 65843 | 1300902 | 2796 | 114 | n/a (full) | n/a (full) | result | reproduced | yes | yes | yes | yes | yes | 0 |
| 2 | RT2 hybrid claude | 44935 | 1019303 | 7737 | 265 | late | yes | result | reproduced | yes | yes | yes | yes | yes | 0 |
| 2 | RT2 hybrid codex | 25478 | 217171 | 1182 | 32 | yes | yes | ask (want result) | none | yes | yes | yes | no |  | 0 |
| 2 | RT2 proposal claude | 55598 | 733763 | 6004 | 154 | yes | no | result | reproduced | yes | yes | yes | no | yes | 0 |
| 2 | RT2 proposal codex | 31862 | 232111 | 814 | 38 | yes | yes | ask (want result) | none | yes | yes | yes | no |  | 0 |
| 2 | RT2 skill claude | 35774 | 778486 | 5338 | 138 | yes | yes | result | reproduced | yes | yes | yes | no | yes | 0 |
| 2 | RT2 skill codex | 19587 | 707653 | 3387 | 108 | yes | yes | requeue (want result) | none | yes | yes | yes | no |  | 0 |
| 2 | RT3 core claude | 83411 | 339391 | 2218 | 34 | late | no | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 core codex | 50611 | 171774 | 619 | 19 | yes | no | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 full claude | 109833 | 445020 | 1975 | 31 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 full codex | 67044 | 302716 | 813 | 29 | n/a (full) | n/a (full) | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 hybrid claude | 45362 | 261245 | 2932 | 44 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 hybrid codex | 27818 | 220457 | 1083 | 38 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 proposal claude | 55742 | 353144 | 2615 | 38 | yes | no | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 proposal codex | 34202 | 248150 | 1081 | 37 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 skill claude | 35799 | 391129 | 3008 | 40 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |
| 2 | RT3 skill codex | 21733 | 231430 | 1219 | 40 | yes | yes | ask |  | yes | yes | yes | yes |  | 0 |

Rerun: create `$BASES/base-rt1..3` as clones of taskq at the base commits above with `cargo build --tests --locked` done, then `BASES=<dir> SPECQ=<specq checkout> RUNS=<empty dir> engineering/audits/spec-delivery/run-real.sh RT2 core codex` (add `CI_LINE=1` for the live CI line); `RUNS=<dir>[:<dir>] python3 engineering/audits/spec-delivery/analyze-real.py` prints the table. Runs are paid model calls; rerun only when the delivery logic or a runtime version changes.

### RT2 rerun with the live CI line

Question ([#57](https://github.com/taskqorg/specq/issues/57)): was the `core` RT2 result of 2 of 4 a replay confound of the missing line "Do not wait for CI: `close` checks it"? Four new runs on 2026-10-15, same host, runtime versions, base clone and specq `317ea57c97f809bd65fc08ff80383147561df642` as the main table; the only brief change is that line, restored after the commit line (`CI_LINE=1` in [real.py](spec-delivery/real.py)). They are records 61-64 of [real-runs.jsonl](spec-delivery/real-runs.jsonl) and [real-traces.jsonl](spec-delivery/real-traces.jsonl), `rep` 3 and 4, `ci_line: true`; the first 60 records have no `ci_line` field and ran without the line.

| rep | run | start | total | out | secs | contract_read | rules_read | command | repro | valid_first | limits_first | limits_final | task_rule | commit | outside |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | RT2 core claude | 81742 | 1071210 | 5365 | 125 | no | no | result | reproduced | yes | yes | yes | yes | yes | 0 |
| 3 | RT2 core codex | 51608 | 1158576 | 2674 | 107 | yes | yes | result | none | yes | yes | yes | no | yes | 0 |
| 4 | RT2 core claude | 81742 | 1005548 | 5642 | 113 | no | no | result | none | no | no | yes | no | yes | 0 |
| 4 | RT2 core codex | 49463 | 246171 | 1050 | 40 | yes | yes | ask (want result) | none | yes | yes | yes | no |  | 0 |

Result: RT2 task rule kept in 1 of 4 `core` runs with the CI line present (Claude 1 of 2, Codex 0 of 2), against 2 of 4 without it. The earlier 2 of 4 was not a CI-line confound:

- No run asked about CI or waited for it. All three results listed CI as unknown under `Open:`, as the line intends. In the first round, too, both `core` Codex runs had already sent `result`; the line changes only the CI-driven asks seen in `hybrid` and `proposal`.
- The misses have other causes. Codex rep 3 forced the lock contention before and after the fix ("before: count 1 != 0; after: pass") but named the rule as "section 4", so the strict criterion (`R<n>` or `§`, and "fail" or "reproduced" in the evidence) scores it as missed. Claude rep 4 did not force the race, gave the cause from code ("race not forced") and named the rule only in prose. Codex rep 4 asked before any code: taskq.md § 7 rule 4 at that base requires a changed rule for any changed existing test, a defensible reading of the contract that the CI line does not touch.
- Read leniently (rule named in words, evidence in any wording), `core` keeps the rule in 2 of 4 runs again: Claude rep 3 and Codex rep 3.

Limits: two runs per runtime; a difference of one run is not significant. The strict criterion is unchanged from the main table so that the counts compare.

## Supplement: toy project

The first round used an invented toy project (a contract `toyq.md` with three rules, a Python module with a defect, one test) and specq `a4da8c62ea50fe141e01527ed16ca9a8f580b99e`; harness [build.py](spec-delivery/build.py), [run.sh](spec-delivery/run.sh), [analyze.py](spec-delivery/analyze.py). Its raw transcripts were not retained. `index` there is the hybrid without the injected core.

| Runtime | Mode | Runs | Start tokens (mean) | Total input (mean) | Time s (mean) | Right command, valid on first try | Task rule kept | Commands outside the project |
|---|---|---|---|---|---|---|---|---|
| claude | full | 6 | 65,919 | 361,238 | 57 | 6/6 | 6/6 | 6/6 / 6/6 | 0/6 |
| claude | skill | 6 | 34,602 | 395,675 | 73 | 6/6 | 6/6 | 6/6 / 6/6 | 0/6 |
| claude | index | 6 | 35,613 | 302,231 | 66 | 6/6 | 6/6 | 0/6 |
| codex | full | 6 | 38,866 | 203,095 | 28 | 6/6 | 4/6 | 6/6 / 6/6 | 4/6 |
| codex | skill | 6 | 19,934 | 180,383 | 33 | 6/6 | 5/6 | 6/6 / 6/6 | 0/6 |
| codex | index | 6 | 19,379 | 165,245 | 35 | 6/6 | 6/6 | 0/6 |

In 4 of 6 Codex `full` toy runs Codex ran `python3 caveman/scripts/check.py` in the local specq checkout and listed it as a project check: specq's own `README.md` and `AGENTS.md`, injected as "every specq file", direct work in the rule repository. Codex `full` also omitted before/after evidence on the toy defect in both runs.

## Proposal

Problem: the owner asked whether full injection (#33) or a mandatory skill should deliver the rules. #52 already moved to a hybrid. Three points remain open: the active rule re-injects on every resume, indexes every other shared file (including specq contributor files, which misdirected a Codex worker in the toy runs) and does not say whether a native skill is required.

Recommendation: keep the #52 hybrid, `core` in the table. Do not return to full injection: it adds 26,000 Claude and 16,000 Codex start tokens, exceeds the budget, and its RT2 lead is within the replay confounds. Do not adopt skill-only or a smaller contract core: they kept spec-first and ask compliance but did not beat `core` on the defect task, and a native skill needs per-runtime installation and does not reach every client the same way. Amend three points:

- A resume repeats the header and index, not file bodies already in the conversation (survey: resume continues the same conversation; not measured here).
- The index leaves out rule-repository contributor files.
- No native skill: the brief is the one channel every runtime and client receives.

Rule text, replacing the bullets of Attempt context in `engineering/agent-workflow.md` after approval (links as in the current section):

```text
- The runner injects the project contract and the shared core at each attempt start. The shared core applies to every attempt: principles, spec first, Ponytail, this file, use cases, verification, security, Caveman core, documentation and change communication.
- Every other shared file is linked from the injected index and is not injected. The agent loads it on demand when the task touches its area. Rule-repository contributor files (its README.md, AGENTS.md, SECURITY.md, scripts, vendor snapshots and audits) are neither injected nor indexed.
- A header names the injected revisions and states precedence: the project contract overrides shared rules where they conflict.
- Project docs/ are not injected. The index lists them too: one line per file, path plus a one-line summary.
- A resume repeats the header and the index, not file bodies already in the conversation.
- Delivery uses the attempt brief only; no runtime-specific skill is required.
- Acknowledging the injected rules is not evidence. Apply them to the work; evidence follows verification.
```

Affected consumers: taskq (worker, reviewer and operator briefs). Other consumers keep their delivery until they adopt it.

Verification after approval: one live taskq attempt and one resume per runtime on a real task, whose log shows the header, the core and the index at start and only the header and index at resume; then the RT2 cell of this experiment rerun in `core` mode with the live CI line restored, both runtimes.

### Consumer change for taskq#1156

Replaces the #1156 Goal ("inject the whole project contract, every specq .md and a docs index"):

- `turn_text` emits, before the task text: the header (specq revision, source path, precedence line), the whole `taskq.md`, the ten shared-core files at the pin (`engineering/principles.md`, `spec-first.md`, `ponytail.md`, `agent-workflow.md`, `use-cases.md`, `verification.md`, `security.md`, `caveman/rules/core.md`, `documentation.md`, `changes.md`) and one index. Index lines: each other specq rule file at the pin (path, first heading; excluding `README.md`, `AGENTS.md`, `SECURITY.md`, `scripts/`, `vendor/`, `audits/`, `docs/`) and each `docs/` file (path, first heading).
- The service materializes the pinned specq files once per pin under `<root>/.taskq/specq/<revision>/` (a cache that a restart rebuilds, R1), and the header names that path. Workers read indexed rules there and project docs in their worktree.
- Resume: header and index only, no file bodies.
- `taskq.md` § 8 Rule delivery and R13 change in the same PR: one total cap for the injected contract, core and index replaces the 64 KiB per-file cap.
- Tests: `turn_text` holds the header, the contract, the core and one index line per listed file; a missing or unreadable pinned file is a `StartError`, never a silent skip.
