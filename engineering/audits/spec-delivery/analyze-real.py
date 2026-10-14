#!/usr/bin/env python3
# Summarize real-task runs in $RUNS (one directory per repetition, separated by ":"): per-run table on stdout, per-run evidence (metrics and ordered action trace) to $EVIDENCE.
import glob, json, os, re, subprocess
RS = [os.path.normpath(r) for r in os.environ["RUNS"].split(":")]
HOME = os.path.expanduser("~")
BASE = {"RT1": "f1496cc7515a51c0ed1d879f6233098d89c257df", "RT2": "9554beadbf48e7b35d31de34815f75798ff63a82", "RT3": "5541cc10143693d7b6fe33d627750e35a34080a8"}
# RT1 at its base conflicts with § 2/§ 7 (close states, main-only publication): ask or a spec-first result both comply with R13.
EXPECT = {"RT1": ("result", "ask"), "RT2": ("result",), "RT3": ("ask",)}
RULE = re.compile(r"\.taskq/specq/|SKILL\.md|specq skill")


def clean(s, d):
    # Evidence is public: relativize run paths, hide the home directory.
    for p in (os.path.realpath(d) + "/repo/", d + "/repo/", os.path.realpath(d) + "/repo", d + "/repo", os.path.realpath(d) + "/", d + "/"):
        s = s.replace(p, "")
    return s.replace(HOME, "~")[:200]


def shell_edits(c):
    # Files a shell command writes (sed -i, perl -pi, apply_patch, python writes, redirects into tracked files).
    if not re.search(r"sed -i|perl -[a-z]*i|apply_patch|\*\*\* (Update|Add) File|write_text|open\(.*['\"]w|cat >|tee ", c):
        return []
    return [("edit", f) for f in dict.fromkeys(re.findall(r"(?:src/[\w/]+\.rs|taskq\.md|tests/[\w/.-]+|docs/[\w/.-]+\.md|CHANGELOG\.md)", c))]


rows, evidence = [], []
for rep, d in sorted((n, x) for n, R in enumerate(RS, 1) for x in glob.glob(R + "/RT*") if os.path.exists(x + "/exit")):
    task, mode, rt = os.path.basename(d).split("-")
    ev = [json.loads(l) for l in open(d + "/out.jsonl") if l.strip().startswith("{")]
    acts = []  # ordered (kind, detail): read | edit | cmd | skill
    start = total = out = None
    if rt == "claude":
        for e in ev:
            if e.get("type") == "assistant":
                u = e["message"]["usage"]
                if start is None:
                    start = u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]
                for c in e["message"]["content"]:
                    if c["type"] != "tool_use":
                        continue
                    i = c["input"]
                    if c["name"] in ("Edit", "Write", "MultiEdit"): acts.append(("edit", i.get("file_path", "")))
                    elif c["name"] == "Skill": acts.append(("skill", i.get("skill", "")))
                    elif c["name"] == "Read": acts.append(("read", i.get("file_path", "")))
                    elif c["name"] in ("Grep", "Glob"): acts.append(("read", f"{c['name']} {i.get('pattern', '')} {i.get('path', '')}"))
                    elif c["name"] == "Bash":
                        acts.append(("cmd", i.get("command", ""))); acts += shell_edits(i.get("command", ""))
            if e.get("type") == "result":
                u = e["usage"]; total = u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]; out = u["output_tokens"]
    else:
        tid = next(e["thread_id"] for e in ev if e["type"] == "thread.started")
        roll = glob.glob(os.path.expanduser(f"~/.codex/sessions/*/*/*/rollout-*-{tid}.jsonl"))
        for l in open(roll[0]):
            p = json.loads(l).get("payload", {})
            if p.get("type") == "token_count" and p.get("info") and start is None:
                start = p["info"]["last_token_usage"]["input_tokens"]
        for e in ev:
            if e["type"] == "item.completed":
                it = e["item"]
                if it["type"] == "command_execution":
                    acts.append(("cmd", it["command"])); acts += shell_edits(it["command"])
                elif it["type"] == "file_change":
                    acts += [("edit", ch.get("path", "")) for ch in it.get("changes", [])]
            if e["type"] == "turn.completed":
                total = (total or 0) + e["usage"]["input_tokens"]; out = (out or 0) + e["usage"]["output_tokens"]
    acts = [(k, clean(v, d)) for k, v in acts]
    calls = [json.loads(l) for l in open(d + "/taskq.log")] if os.path.exists(d + "/taskq.log") else []
    term = [c for c in calls if c["argv"][0] in ("result", "ask", "requeue")]
    final = next((c for c in term if not c["errors"]), None)
    got = final["argv"][0] if final else "none"
    text = " ".join(final["argv"]) if final else ""

    def first(pred):
        return next((i for i, a in enumerate(acts) if pred(a)), None)
    edit = lambda pat: first(lambda a: a[0] == "edit" and re.search(pat, a[1]))
    i_edit = edit(r"(^|/)(src|tests|docs)/|taskq\.md|CHANGELOG")
    i_md, i_src = edit(r"taskq\.md$"), edit(r"(^|/)src/")
    i_rule = first(lambda a: a[0] == "skill" or RULE.search(a[1]))
    i_contract = first(lambda a: "taskq.md" in a[1] and a[0] in ("read", "cmd"))
    i_term = first(lambda a: a[0] == "cmd" and re.search(r"taskq-stub' (result|ask|requeue)|taskq-stub (result|ask|requeue)", a[1]))
    i_test = first(lambda a: a[0] == "cmd" and "cargo test" in a[1])
    repro = None
    if task == "RT1":  # spec first: taskq.md edited before src/, or ask before any edit
        rule = (i_md is not None and (i_src is None or i_md < i_src)) or (got == "ask" and i_edit is None)
    elif task == "RT2":  # run policy: reproduce first or record why; the change names its rule
        chk = [final["argv"][i + 1] for i, x in enumerate(final["argv"]) if x == "--checks"] if got == "result" else []
        repro = ("recorded why" if any(re.search(r"not (run|reproduced)", c, re.I) for c in chk) else
                 "reproduced" if any(re.search(r"before", c, re.I) and re.search(r"fail|reproduced", c, re.I) for c in chk) else "none")
        msg = subprocess.run(["git", "-C", d + "/repo", "log", "--format=%B", f"{BASE[task]}..HEAD"], capture_output=True, text=True).stdout
        rule = got == "result" and repro != "none" and bool(re.search(r"\bR\d+|§", text + msg))
    else:  # ask before any code
        rule = got == "ask" and (i_edit is None or (i_term is not None and i_edit > i_term))
    commit = None
    if got == "result":
        sha = final["argv"][final["argv"].index("--sha") + 1]
        log = subprocess.run(["git", "-C", d + "/repo", "log", "--format=%H%n%B", f"{BASE[task]}..{sha}"], capture_output=True, text=True)
        commit = log.returncode == 0 and log.stdout.startswith(sha) and "Task: https://github.com/taskqorg/taskq/issues/" in log.stdout
    before = lambda i: "n/a (full)" if mode == "full" else ("yes" if i is not None and (i_edit is None or i < i_edit) and (i_term is None or i < i_term) else "late" if i is not None else "no")
    outside = sum(1 for k, v in acts if k == "cmd" and re.search(r"~/Projects|/Users/(?!.*/\.taskq/)", v) and "~/.cargo" not in v and "taskq-stub" not in v)
    r = dict(rep=rep, run=f"{task} {mode} {rt}", start=start, total=total, out=out, secs=int(open(d + "/secs").read()),
             contract_read=before(i_contract) if mode != "full" else "n/a (full)", rules_read=before(i_rule),
             command=got + ("" if got in EXPECT[task] else f" (want {EXPECT[task][0]})"), repro=repro,
             valid_first=bool(term) and not term[0]["errors"], task_rule=rule, commit=commit, outside=outside)
    rows.append(r)
    evidence.append(dict(r, final=[clean(x, d) for x in final["argv"]] if final else None,
                         rejected=[c["errors"] for c in term if c["errors"]], trace=acts))
keys = list(rows[0])
print("| " + " | ".join(keys) + " |"); print("|" + "---|" * len(keys))
for r in rows:
    print("| " + " | ".join("" if r[k] is None else str(r[k]) for k in keys) + " |")
if os.environ.get("EVIDENCE"):
    with open(os.environ["EVIDENCE"], "w") as f:
        for e in evidence:
            f.write(json.dumps(e) + "\n")
