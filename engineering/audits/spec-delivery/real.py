#!/usr/bin/env python3
# Replay one real taskq task offline: real.py <task RT1-RT3> <mode full|skill|hybrid|core|proposal> <runtime claude|codex> <outdir>
# Needs $BASES/base-rtN: taskq clones checked out at the base commit below, with `cargo build --tests` done.
import os, pathlib, re, subprocess, sys
task, mode, rt, out = sys.argv[1:5]
out = pathlib.Path(out).resolve()
H = pathlib.Path(__file__).parent
SPECQ = pathlib.Path(os.environ.get("SPECQ") or H.parents[2])
REV = subprocess.check_output(["git", "-C", SPECQ, "rev-parse", "HEAD"], text=True).strip()
# Real taskq issues (text as filed) at the main commit their first attempt started from.
TASKS = {
 "RT1": (1039, "f1496cc7515a51c0ed1d879f6233098d89c257df", "Close tasks whose PR targets a release branch",
  "## Goal\nA task whose PR merges into a release branch (not the default branch) closes through taskq like any other task, without a manual gh issue close.\n\n## Acceptance\nA1. taskq.md states how a task with a release-branch PR closes; spec edited before code (R13).\nA2. A merged PR into a non-default branch that references the task leads to the task closing with the usual close record.\nA3. taskq close works for such a task when the owner or PM closes it after the merge, including from ask or doing if the spec allows it.\nA4. A test covers the release-branch case; cargo test --locked and cargo run -- selftest pass.\n"),
 "RT2": (1096, "9554beadbf48e7b35d31de34815f75798ff63a82", "Flaky test: profile::tests::retained_profile_report",
  "## Goal\nretained_profile_report passes deterministically in CI; push run 38601584294 failed it at src/profile.rs:246 (left 1, right 0) when no concurrent trim_tail won the log lock.\n\n## Acceptance\nA1. The test, or trim_tail locking, is fixed so the concurrent writer/trim race cannot leave a pre-filled record; the change names the rule it enforces.\nA2. cargo test --locked passes repeatedly (e.g. 50 runs of the test) on one host and CI is green.\n\n## Scope\n- src/profile.rs\n- src/data.rs\n"),
 "RT3": (1125, "5541cc10143693d7b6fe33d627750e35a34080a8", "Hold a task for an owner action and resume it on the answer",
  "## Goal\nA task waiting for the owner costs no worker turns and resumes on the answer.\n\n## Acceptance\nA1. A task in wait-owner starts no attempt until a new owner answer exists\nA2. The owner answer moves the task to ready with the same attempt context\nA3. The board shows 'waiting for owner: <action>'\n"),
}
n, base, title, body = TASKS[task]
repo = out / "repo"
bdir = pathlib.Path(os.environ["BASES"]) / f"base-{task.lower()}"
assert subprocess.check_output(["git", "-C", bdir, "rev-parse", "HEAD"], text=True).strip() == base, "base commit"
out.mkdir(parents=True, exist_ok=True)
subprocess.run(["cp", "-cR", bdir, repo], check=True)  # APFS clone keeps the prebuilt target/ cheap
subprocess.run(["git", "-C", repo, "checkout", "-q", "-b", f"taskq-{n}"], check=True)
(repo / ".git/info/exclude").write_text(".taskq/\n.claude/\n.agents/\n")
(out / "task.md").write_text(f"#{n} {title}\n\n{body}")

def head(p):
    return next((l.lstrip("# ").strip() for l in p.read_text().splitlines() if l.startswith("#")), "")
ALL = sorted(p for p in SPECQ.rglob("*.md") if not {".git", ".worktrees", ".claude", "spec-delivery"} & set(p.relative_to(SPECQ).parts))
# Contributor files of the rule repository direct work there, not in a consumer: not indexed.
RULES = [p for p in ALL if not {"vendor", "audits", "scripts", "docs"} & set(p.relative_to(SPECQ).parts)
         and p.relative_to(SPECQ).as_posix() not in ("README.md", "AGENTS.md", "SECURITY.md")]
contract = (repo / "taskq.md").read_text()
secs = re.split(r"(?m)^(?=## )", contract)  # preamble, then one chunk per "## " section
docs = sorted(p for p in (repo / "docs").rglob("*.md"))
docs_idx = "\n".join(f"- {p.relative_to(repo)}: {head(p)}" for p in docs)
tq = f"env TASKQ_TASK={n} STUB_LOG={out}/taskq.log STUB_TASK={out}/task.md {H / 'taskq-stub'}"
delivery = f"""TaskQ task
You are the taskq worker for task #{n}: {title}. Attempt 1.
Read `taskq.md` first and do only what it allows (R13).
Task text, state and your inbox: `{tq} inbox {n}`.
Touch only this repository and the OS temp dir.
Work in the current directory on branch taskq-{n} (checked out). This is an offline replay: do not fetch, push or open a PR.
Commit with the line `Task: https://github.com/taskqorg/taskq/issues/{n}` in the message, run the project checks.
Then exactly one of:
- `{tq} result {n} --sha <full SHA> --checks "<command -- outcome>" [--checks ..] --text "Changed: <user effect>
Open: <item|none>"`,
- `{tq} ask {n} --text "Done: <checked or not started>
Problem: <decision and user effect>" --option A --option B --recommend K [--link URL]` (owner decision; Acceptance unclear or untestable; or a split of work bigger than one reviewable diff — before any code),
- `{tq} requeue {n} --text "<why it cannot be done>"`.
Put each `--text` field on its own line. The commands check the limits: Done at most 160 characters, Problem 1-2 lines, 2-4 options of at most 160 characters, at most 2 links; result lines at most 240 characters, Changed and Open 1-2 lines, 1-8 checks. Over-limit text is rejected: shorten it.
Then stop.
"""
guide = f"""Read the files for the step you are on; reading is not evidence, applying them is. taskq.md overrides shared rules where they conflict.

- Before work: taskq.md R13 and the sections the task touches; `{{S}}/engineering/agent-workflow.md`; `{{S}}/engineering/spec-first.md`.
- Before deciding to ask or to code: taskq.md § 2 (Ask card); `{{S}}/engineering/use-cases.md`.
- Before checks and the result: `{{S}}/engineering/verification.md` (run policy: a defect fix reproduces first and reports before/after); taskq.md § 7.
- Commit and result wording: `{{S}}/caveman/rules/changes.md`, `{{S}}/caveman/rules/core.md`.
- Anything else: the index below.
"""
S = ".taskq/specq"
# Shared core of specq#52: applies to every attempt.
SHARED = ["engineering/principles.md", "engineering/spec-first.md", "engineering/ponytail.md", "engineering/agent-workflow.md", "engineering/use-cases.md",
          "engineering/verification.md", "engineering/security.md", "caveman/rules/core.md", "caveman/rules/documentation.md", "caveman/rules/changes.md"]
def index(skip_core, contract=True, skip_shared=False):
    lines = [f"- taskq.md: {s.splitlines()[0].lstrip('# ')}" for s in secs[1:] if contract and not (skip_core and core_sec(s))]
    lines += [f"- {S}/{p.relative_to(SPECQ)}: {head(p)}" for p in RULES if not (skip_shared and p.relative_to(SPECQ).as_posix() in SHARED)]
    return "Index (path: first heading):\n" + "\n".join(lines) + "\nProject docs (read when the task touches them):\n" + docs_idx + "\n"
def core_sec(s):
    return s.startswith(("## Principles", "## 7."))
if mode == "full":
    # The #33 payload: the whole contract, every specq Markdown file and a docs index.
    parts = [f"TaskQ shared rules: specq@{REV}\nThese canonical rules apply to this turn, including continuations. taskq.md overrides shared rules where they conflict. Apply them to the work; acknowledgement alone is not evidence.\n",
             "--- taskq.md (project contract) ---\n" + contract]
    parts += [f"--- specq/{p.relative_to(SPECQ)} ---\n" + p.read_text() for p in ALL]
    parts.append("Project docs index (read when the task touches them):\n" + docs_idx)
    brief = "\n\n".join(parts) + "\n\n" + delivery
else:
    for p in RULES:
        d = repo / S / p.relative_to(SPECQ); d.parent.mkdir(parents=True, exist_ok=True); d.write_text(p.read_text())
    g = guide.replace("{S}", S)
    shared = "".join(f"--- {S}/{f} ---\n" + (SPECQ / f).read_text() + "\n" for f in SHARED)
    if mode == "core":
        # specq#52: the whole contract and the shared core injected; every other file indexed.
        brief = (f"TaskQ shared rules: specq@{REV}, files under `{S}/`. taskq.md overrides shared rules where they conflict. Every other shared file and project doc is in the index; load it when the task touches its area. Acknowledgement alone is not evidence.\n\n"
                 + "--- taskq.md (project contract) ---\n" + contract + "\n" + shared + "\n" + index(False, contract=False, skip_shared=True) + "\n" + delivery)
    elif mode == "proposal":
        core = secs[0] + "".join(s for s in secs[1:] if core_sec(s))
        brief = (f"TaskQ shared rules: specq@{REV}, files under `{S}/`.\nObligation: before your first edit and again before `result` or `ask`, read the indexed rules for that step. A listed file that is missing is a start failure. taskq.md overrides shared rules where they conflict. Acknowledgement alone is not evidence.\n\n"
                 + "--- taskq.md always-on core (principles and § 7; other sections are in the index) ---\n" + core + "\n" + shared + "\n" + index(True, skip_shared=True) + "\n" + delivery)
    elif mode == "hybrid":
        core = secs[0] + "".join(s for s in secs[1:] if core_sec(s))
        brief = (f"TaskQ shared rules: specq@{REV}, files under `{S}/`.\nObligation: before your first edit and again before `result` or `ask`, read the rule files the guide below names for that step. A listed file that is missing is a start failure. Acknowledgement alone is not evidence.\n\n"
                 + g + "\n--- taskq.md always-on core (principles and § 7; other sections are in the index) ---\n" + core + "\n" + index(True) + "\n" + delivery)
    else:
        sd = repo / (".claude/skills/specq" if rt == "claude" else ".agents/skills/specq"); sd.mkdir(parents=True)
        (sd / "SKILL.md").write_text("---\nname: specq\ndescription: Mandatory taskq contract and shared engineering rules (specq). Load before the first edit and before any taskq result or ask; it says which rule to read for each step.\n---\n# specq rules\n\n" + g + "\n" + index(False))
        brief = (f"TaskQ shared rules: specq@{REV}, delivered as the `specq` skill and the files under `{S}/`.\nObligation: load the `specq` skill before your first edit and again before `result` or `ask`; read the rules it names for each step. Acknowledgement alone is not evidence.\n\n" + delivery)
(out / "brief.txt").write_text(brief)
print(len(brief))
