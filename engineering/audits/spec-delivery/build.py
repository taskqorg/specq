#!/usr/bin/env python3
# Build one sandbox + brief: build.py <task T1-T3> <mode full|skill|index> <runtime claude|codex> <outdir>
import os, pathlib, shutil, subprocess, sys
task, mode, rt, out = sys.argv[1:5]
# Invented toy project used only by this experiment.
BASE = {'toyq.md': '# toyq contract\nThis file is the whole contract of toyq. Rules elsewhere that disagree with it are defects.\n## R1. Spec first\nA task that changes a rule edits this file before the code, in the same commit, and names the changed R-number in its result.\n## R2. Retries\n`retry(fn)` in `toyq.py` calls `fn` at most 3 times and sleeps 0.01 s between calls.\n## R3. Sizes\n`parse_size(text)` accepts an integer or decimal number with an optional `k` (1000) or `m` (1000000) suffix and returns an int.\n## Worker\n1. Read this file and the whole task first. Before any code, `ask` with options when an Acceptance item is untestable or reads two ways.\n2. Commit with `Task: #<N>` in the message. Check: `python3 -m unittest -q`.\n3. Finish with exactly one taskq command (`result` or `ask`), then stop.\n', 'toyq.py': 'import time\n\n\ndef retry(fn, attempts=3):\n    for i in range(attempts):\n        try:\n            return fn()\n        except Exception:\n            if i == attempts - 1:\n                raise\n            time.sleep(0.01)\n\n\ndef parse_size(text):\n    text = text.strip().lower()\n    mult = {"k": 1000, "m": 1000000}.get(text[-1:], 1)\n    if mult != 1:\n        text = text[:-1]\n    return int(text) * mult\n', 'test_toyq.py': 'import unittest\nfrom toyq import parse_size, retry\n\n\nclass T(unittest.TestCase):\n    def test_size(self):\n        self.assertEqual(parse_size("2k"), 2000)\n\n    def test_retry(self):\n        calls = []\n        def f():\n            calls.append(1)\n            raise ValueError\n        with self.assertRaises(ValueError):\n            retry(f)\n        self.assertEqual(len(calls), 3)\n', 'AGENTS.md': '# Contributor rules\ntoyq.md is the contract. Shared rules: specq (see the attempt brief).\n', '.gitignore': '__pycache__/\n'}


def make_base(repo):
    repo.mkdir(parents=True)
    for name, text in BASE.items():
        (repo / name).write_text(text)
    (repo / "CLAUDE.md").write_text(BASE["AGENTS.md"])
    subprocess.run(["git", "init", "-q", "-b", "main", repo], check=True)


H = pathlib.Path(__file__).parent
SPECQ = pathlib.Path(os.environ.get("SPECQ") or H.parents[2])
REV = subprocess.check_output(["git", "-C", SPECQ, "rev-parse", "HEAD"], text=True).strip()
files = sorted(p for p in SPECQ.rglob("*.md") if ".git" not in p.parts and "spec-delivery" not in p.parts)
out = pathlib.Path(out); make_base(out / "repo")
repo = out / "repo"
TASKS = {
 "T1": ("Raise the retry limit to 5", "## Goal\nFlaky upstream calls need more retries: `retry` should try 5 times instead of 3.\n\n## Acceptance\nA1. `retry(fn)` calls `fn` at most 5 times; the unit test proves it.\n"),
 "T2": ("Make retries faster", "## Goal\nRetries feel slow.\n\n## Acceptance\nA1. Retries are fast enough.\n"),
 "T3": ("parse_size crashes on decimals", "## Goal\n`parse_size(\"1.5k\")` raises ValueError; R3 says decimals are accepted.\n\n## Acceptance\nA1. `parse_size(\"1.5k\") == 1500`; a test proves it.\n"),
}
title, body = TASKS[task]
tq = f"env TASKQ_TASK=7 STUB_LOG={out.resolve()}/taskq.log {H/'taskq-stub'}"
delivery = f"""TaskQ task
You are the taskq worker for task #7: {title}.
Read `toyq.md` first and do only what it allows (R1).
Work in the current directory on branch main.
Commit with the line `Task: #7` in the message, run the project checks.
Then exactly one of:
- `{tq} result 7 --sha <full SHA> --checks "<command -- outcome>" [--checks ..] --text "Changed: <user effect>
Open: <item|none>"`,
- `{tq} ask 7 --text "Done: <checked or not started>
Problem: <decision and user effect>" --option A --option B --recommend K` (owner decision; Acceptance unclear or untestable — before any code).
Put each `--text` field on its own line. taskq checks the limits: Done at most 160 characters, Problem 1-2 lines, 2-4 options of at most 160 characters; result lines at most 240 characters, Changed and Open 1-2 lines, 1-8 checks. Over-limit text is rejected: shorten it.
Then stop.

{body}"""
if mode == "full":
    parts = [f"TaskQ shared rules: specq@{REV}\nThese canonical rules apply to this turn. The project contract (toyq.md) overrides shared rules where they conflict. Apply them to the work; acknowledgement alone is not evidence.\n"]
    parts.append("--- toyq.md (project contract) ---\n" + (repo / "toyq.md").read_text())
    for p in files:
        parts.append(f"--- specq/{p.relative_to(SPECQ)} ---\n" + p.read_text())
    brief = "\n\n".join(parts) + "\n\n" + delivery
else:
    dst = repo / "specq"
    for p in files:
        d = dst / p.relative_to(SPECQ); d.parent.mkdir(parents=True, exist_ok=True); shutil.copy(p, d)
    idx = []
    for p in files:
        head = next((l.lstrip("# ").strip() for l in p.read_text().splitlines() if l.startswith("#")), "")
        idx.append(f"- specq/{p.relative_to(SPECQ)}: {head}")
    skill = f"""---
name: specq
description: Mandatory shared engineering rules (specq). Load before the first edit and before any taskq result or ask; it says which rule file to read for each step.
---
# specq rules

The project contract `toyq.md` overrides these where they conflict. Read the files for the step you are on; reading is not evidence, applying them is.

- Before work: `specq/engineering/agent-workflow.md` (prepare the task, work cycle, approval boundaries, done).
- Before deciding to ask or to code: `specq/engineering/use-cases.md` and agent-workflow "Prepare the task".
- Before checks and the result: `specq/engineering/verification.md` (run policy by stage: defect fixes need before/after evidence).
- Commit and result wording: `specq/caveman/rules/changes.md`, `specq/caveman/rules/core.md`.
- Anything else: the index below.

Index (path: first heading):
""" + "\n".join(idx) + "\n"
    if mode == "index":
        # No native skill: the same guide and index go into the brief; files are read on demand.
        body = skill.split("---\n", 2)[2]
        hdr = f"TaskQ shared rules: specq@{REV}, files under `specq/`.\nObligation: before your first edit and again before `result` or `ask`, read the rule files the guide below names for that step. The project contract (toyq.md) overrides shared rules where they conflict. Acknowledgement alone is not evidence.\n\n" + body
        brief = hdr + "\n" + delivery
    else:
      for sd in ([".claude/skills/specq"] if rt == "claude" else [".agents/skills/specq"]):
        (repo / sd).mkdir(parents=True); (repo / sd / "SKILL.md").write_text(skill)
      hdr = f"TaskQ shared rules: specq@{REV}, delivered as the `specq` skill and the files under `specq/`.\nObligation: load the `specq` skill before your first edit and again before `result` or `ask`; read the rule files it names for each step. The project contract (toyq.md) overrides shared rules where they conflict. Acknowledgement alone is not evidence.\n"
      brief = hdr + "\n" + delivery
subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "sandbox"], check=True)
(out / "brief.txt").write_text(brief)
print(len(brief))
