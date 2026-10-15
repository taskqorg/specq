#!/usr/bin/env python3
# Summarize real-task runs in $RUNS (one directory per repetition, separated by ":"): per-run table on stdout;
# full per-run evidence (metrics, every taskq call verbatim with stub and limit verdicts, token usage per request) to $EVIDENCE;
# action-trace excerpts (each entry cut at 200 characters) to $TRACES.
import glob, json, os, re, subprocess
RS = [os.path.normpath(r) for r in os.environ["RUNS"].split(":")]
HOME = os.path.expanduser("~")
BASE = {"RT1": "f1496cc7515a51c0ed1d879f6233098d89c257df", "RT2": "9554beadbf48e7b35d31de34815f75798ff63a82", "RT3": "5541cc10143693d7b6fe33d627750e35a34080a8"}
# RT1 at its base conflicts with § 2/§ 7 (close states, main-only publication): ask or a spec-first result both comply with R13.
EXPECT = {"RT1": ("result", "ask"), "RT2": ("result",), "RT3": ("ask",)}
RULE = re.compile(r"\.taskq/specq/|SKILL\.md|specq skill")


HARNESS = os.path.dirname(os.path.abspath(__file__))


def clean(s, d):
    # Evidence is public: relativize run paths, name the harness, hide the home directory. Never truncates.
    for p in (os.path.realpath(d) + "/repo/", d + "/repo/", os.path.realpath(d) + "/repo", d + "/repo", os.path.realpath(d) + "/", d + "/"):
        s = s.replace(p, "")
    return s.replace(HARNESS + "/", "<harness>/").replace(HOME, "~")


def opts(argv, name):
    return [argv[i + 1] for i, x in enumerate(argv) if x == name and i + 1 < len(argv)]


def limits(argv):
    # Every taskq.md limit a result or ask card has (§ 2 Ask card, § 7 Result and close verdicts, R7 counting:
    # logical nonblank lines, Unicode characters, labels and numbering included). Strict: the R7 exemption for
    # exact commands and paths is not applied, so a long check command is reported, not excused.
    v, cmd = [], argv[0]
    text = [l for l in "\n".join(opts(argv, "--text")).splitlines() if l.strip()]
    links = opts(argv, "--link")
    if len(opts(argv, "--text")) > 1: v.append("--text given more than once")
    if cmd == "ask":
        o, rec = opts(argv, "--option"), opts(argv, "--recommend")
        if not text or not text[0].startswith("Done: "): v.append("line 1 is not Done:")
        elif len(text[0]) > 160: v.append(f"Done {len(text[0])} > 160")
        if len(text) < 2 or not text[1].startswith("Problem: "): v.append("line 2 is not Problem:")
        prob = text[1:]
        if not 1 <= len(prob) <= 2: v.append(f"Problem {len(prob)} lines, want 1-2")
        v += [f"Problem line {len(l)} > 240" for l in prob if len(l) > 240]
        if o and not 2 <= len(o) <= 4: v.append(f"{len(o)} options, want 2-4 (or none for an owner action)")
        if o and (len(rec) != 1 or not rec[0].isdigit() or not 1 <= int(rec[0]) <= len(o)): v.append(f"--recommend {rec}, want exactly one of 1-{len(o)}")
        for k, x in enumerate(o, 1):
            n = len(f"{k}. {x}") + (2 if rec == [str(k)] else 0)
            if n > 160: v.append(f"option {k} {n} > 160")
        if len(links) > 2: v.append(f"{len(links)} links > 2")
        lines = len(text) + (1 if links else 0) + len(o) + 1
        if lines > 9: v.append(f"card {lines} lines > 9")
    elif cmd == "result":
        sha, checks = opts(argv, "--sha"), opts(argv, "--checks")
        if len(sha) != 1 or not re.fullmatch(r"[0-9a-f]{40}", sha[0]): v.append("--sha is not one full SHA")
        if not 1 <= len(checks) <= 8: v.append(f"{len(checks)} checks, want 1-8")
        v += [f"check without 'command -- outcome': {c[:40]}" for c in checks if " -- " not in c]
        v += [f"Checks line {len('Checks: ' + c)} > 240" for c in checks if len("Checks: " + c) > 240]
        i_open = next((i for i, l in enumerate(text) if l.startswith("Open: ")), None)
        if not text or not text[0].startswith("Changed: "): v.append("line 1 is not Changed:")
        if i_open is None: v.append("no Open: line")
        else:
            if not 1 <= i_open <= 2: v.append(f"Changed {i_open} lines, want 1-2")
            if not 1 <= len(text) - i_open <= 2: v.append(f"Open {len(text) - i_open} lines, want 1-2")
        v += [f"line {len(l)} > 240" for l in text if len(l) > 240]
        if len(text) + len(checks) > 12: v.append(f"body {len(text) + len(checks)} lines > 12")
        if links: v.append("--link on a result without a decision card")
    return v


def usage(d, rt, ev):
    # Per-request token usage events, in order.
    if rt == "claude":
        seen, out = set(), []
        for e in ev:
            if e.get("type") == "assistant" and e["message"]["id"] not in seen:
                seen.add(e["message"]["id"]); u = e["message"]["usage"]
                out.append({k: u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")})
        return out
    tid = next(e["thread_id"] for e in ev if e["type"] == "thread.started")
    roll = glob.glob(os.path.expanduser(f"~/.codex/sessions/*/*/*/rollout-*-{tid}.jsonl"))[0]
    out = []
    for l in open(roll):
        p = json.loads(l).get("payload", {})
        if p.get("type") == "token_count" and p.get("info"):
            out.append(p["info"]["last_token_usage"])
    return out


def shell_edits(c):
    # Files a shell command writes (sed -i, perl -pi, apply_patch, python writes, redirects into tracked files).
    if not re.search(r"sed -i|perl -[a-z]*i|apply_patch|\*\*\* (Update|Add) File|write_text|open\(.*['\"]w|cat >|tee ", c):
        return []
    return [("edit", f) for f in dict.fromkeys(re.findall(r"(?:src/[\w/]+\.rs|taskq\.md|tests/[\w/.-]+|docs/[\w/.-]+\.md|CHANGELOG\.md)", c))]


rows, evidence, traces = [], [], []
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
    tokens = usage(d, rt, ev)
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
             valid_first=bool(term) and not term[0]["errors"], limits_first=bool(term) and not limits(term[0]["argv"]),
             limits_final=bool(final) and not limits(final["argv"]), task_rule=rule, commit=commit, outside=outside)
    rows.append(r)
    ci_line = "Do not wait for CI" in open(d + "/brief.txt").read()
    evidence.append(dict(r, ci_line=ci_line, calls=[dict(argv=[clean(x, d) for x in c["argv"]], stub_errors=c["errors"], limit_violations=limits(c["argv"])) for c in term],
                         requests=len(tokens), tokens=tokens))
    traces.append(dict(rep=rep, run=r["run"], ci_line=ci_line, trace=[(k, v[:200]) for k, v in acts]))
keys = list(rows[0])
print("| " + " | ".join(keys) + " |"); print("|" + "---|" * len(keys))
for r in rows:
    print("| " + " | ".join("" if r[k] is None else str(r[k]) for k in keys) + " |")
for var, recs in (("EVIDENCE", evidence), ("TRACES", traces)):
    if os.environ.get(var):
        with open(os.environ[var], "w") as f:
            for e in recs:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
