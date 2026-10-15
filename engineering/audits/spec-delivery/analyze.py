#!/usr/bin/env python3
# Summarize runs: start/total tokens, time, compliance checks.
import glob, json, os, re, subprocess
R = os.environ["RUNS"]
rows = []
def shell_edits(c):
    # Files changed by a shell command, in order of appearance (sed -i, perl -pi, apply_patch, redirects, python heredoc).
    if not re.search(r"sed -i|perl -[a-z]*i|apply_patch|\*\*\* (Update|Add) File|> ?\S*toyq|write_text|open\(", c): return []
    return [("edit", f) for f in re.findall(r"(?<![\w/])(?:test_toyq\.py|toyq\.py|toyq\.md)", c)]
def outside(c, d):
    # A command that runs or inspects the rule repository's own gate outside the run directory.
    here = os.path.realpath(d)
    return any(not p.startswith((d, here)) for p in re.findall(r"/[^\s'\"]*caveman/scripts/check\.py", c))
def base(p): return os.path.basename(p)
for d in sorted(x for x in glob.glob(R + "/T*") if os.path.exists(x + "/exit")):
    task, mode, rt = os.path.basename(d).split("-")
    ev = [json.loads(l) for l in open(d + "/out.jsonl") if l.strip().startswith("{")]
    actions = []  # ordered: ("edit", path) | ("cmd", text) | ("skill", name)
    start = total = out = None
    if rt == "claude":
        for e in ev:
            if e.get("type") == "assistant":
                u = e["message"]["usage"]
                if start is None:
                    start = u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]
                for c in e["message"]["content"]:
                    if c["type"] != "tool_use": continue
                    i = c["input"]
                    if c["name"] in ("Edit", "Write", "MultiEdit"): actions.append(("edit", i.get("file_path", "")))
                    elif c["name"] == "Skill": actions.append(("skill", i.get("skill")))
                    elif c["name"] == "Read": actions.append(("cmd", "read " + i.get("file_path", "")))
                    elif c["name"] == "Bash":
                        actions.append(("cmd", i.get("command", ""))); actions += shell_edits(i.get("command", ""))
            if e.get("type") == "result":
                u = e["usage"]; total = u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]; out = u["output_tokens"]
    else:
        tid = next(e["thread_id"] for e in ev if e["type"] == "thread.started")
        roll = glob.glob(os.path.expanduser(f"~/.codex/sessions/*/*/*/rollout-*-{tid}.jsonl"))
        for l in open(roll[0]):
            j = json.loads(l); p = j.get("payload", {})
            if p.get("type") == "token_count" and p.get("info") and start is None:
                start = p["info"]["last_token_usage"]["input_tokens"]
        for e in ev:
            if e["type"] == "item.completed":
                it = e["item"]
                if it["type"] == "command_execution":
                    c = it["command"]
                    if "SKILL.md" in c and "specq" in c: actions.append(("skill", "specq"))
                    actions.append(("cmd", c))
                    actions += shell_edits(c)
                elif it["type"] == "file_change":
                    for ch in it.get("changes", []): actions.append(("edit", ch.get("path", "")))
            if e["type"] == "turn.completed":
                total = e["usage"]["input_tokens"]; out = e["usage"]["output_tokens"]
    calls = [json.loads(l) for l in open(d + "/taskq.log")] if os.path.exists(d + "/taskq.log") else []
    term = [c for c in calls if c["argv"][0] in ("result", "ask", "requeue")]
    final = next((c for c in term if not c["errors"]), None)
    first_ok = bool(term) and not term[0]["errors"]
    edits = [p for k, p in actions if k.startswith("edit")]
    def first(pred):
        return next((i for i, a in enumerate(actions) if pred(a)), None)
    i_md = first(lambda a: a[0].startswith("edit") and base(a[1]) == "toyq.md")
    i_py = first(lambda a: a[0].startswith("edit") and base(a[1]) == "toyq.py")
    i_test = first(lambda a: a[0].startswith("edit") and base(a[1]) == "test_toyq.py")
    i_skill = first(lambda a: a[0] == "skill" or (a[0] == "cmd" and re.search(r"specq/(engineering|caveman|design)/", a[1])))
    first_edit = min([i for i in (i_md, i_py, i_test) if i is not None], default=None)
    i_run = first(lambda a: a[0] == "cmd" and ("unittest" in a[1] or "parse_size" in a[1]))
    expect = "ask" if task == "T2" else "result"
    got = final["argv"][0] if final else "none"
    ok = got == expect
    if task == "T1":
        rule = i_md is not None and (i_py is None or i_md < i_py)
        if final:
            t = " ".join(final["argv"])
            rule = rule and "R2" in t
    elif task == "T2":
        rule = not edits
    else:
        before = i_run is not None and (i_py is None or i_run < i_py)
        chk = " ".join(final["argv"]) if final else ""
        rule = before and bool(re.search(r"(before|fail|ValueError|repro)", chk, re.I))
    sha_ok = None
    if final and got == "result":
        sha = final["argv"][final["argv"].index("--sha") + 1]
        head = open(d + "/gitlog").readline().split()
        log = subprocess.run(["git", "-C", d + "/repo", "log", "-1", "--format=%B"], capture_output=True, text=True).stdout
        sha_ok = bool(head) and head[0] == sha and "Task: #7" in log
    loaded = "yes" if mode == "full" else ("before edit" if i_skill is not None and (first_edit is None or i_skill < first_edit) else ("late" if i_skill is not None else "no"))
    rows.append(dict(run=f"{task} {mode} {rt}", start=start, total=total, out=out, secs=int(open(d + "/secs").read()),
                     rules=loaded, command=f"{got}{'' if ok else ' (want ' + expect + ')'}", first_try=first_ok,
                     rule=rule, commit=sha_ok, outside=sum(outside(a[1], d) for a in actions if a[0] == "cmd")))
keys = list(rows[0])
print("| " + " | ".join(keys) + " |"); print("|" + "---|" * len(keys))
for r in rows: print("| " + " | ".join("" if r[k] is None else str(r[k]) for k in keys) + " |")
