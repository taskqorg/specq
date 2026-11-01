# Task planning

How a task is shaped, filed and dispatched before and around the work. [Agent workflow](agent-workflow.md) owns the work cycle; projects keep their own commands, gates and approval owners in their contract.

## Prepare the task

- For a substantial behavior change, walk the relevant [scenarios](use-cases.md) to uncover decisions missing from the request. Investigate facts in code and current state; bring only unresolved choices that change behavior, authority, cost or risk to the owner, as [decision questions](../caveman/rules/core.md#decision-questions).
- Group independent choices in a short round; ask dependent questions after their prerequisites are settled. Reuse accepted answers. Resolve material choices before dependent implementation; routine changes need no interview or extra approval round.
- One worker delivers one coherent outcome, across the required layers, in one task and one session, even when the diff is large; fewer tasks mean less coordination. Split only for a real blocking dependency, a step on a different host or owner, or context the worker cannot hold. Diff or review size alone is never a split reason, and a worker does not ask to split for it.
- One task is one user-visible outcome; its steps, hosts and surfaces are acceptance items, not tasks. A batch of fixes to the same screen, module or file goes to one task and one session, and a new fix for that surface joins its open task instead of starting a parallel writer. A repeated check (a probe per host, a periodic measure) is one recipe run, not one task per run.
- A plan or chain of changes on one surface is one task. Owner feedback on that surface steers its open task; it does not start a new one.
- A complex task lists ordered stages (analyse, change, verify) as acceptance items, each ending in a checkpoint the worker reports on the task. The PM steers at checkpoints. No stage becomes its own task.
- A gap found in review is fixed inside the task, up to three review rounds; a task stays open until its outcome is proved rather than spawning follow-up tasks for its own acceptance ([review](review.md#review)).
- A task whose outcome is a decision (research, design, proposal, "try method X") is an [experiment task](#experiment-tasks). A closed task never buries a decision.
- Acceptance follows the [run policy](testing.md#run-policy-by-stage); it names evidence for changed behavior and its risks without adding unrelated snapshots or platform matrices.

## Experiment tasks

An experiment task tests an idea and ends in a decision, whatever its type label. It never just ends.

- At filing, the body states the Hypothesis (the expected result and why), the Metric or decision rule (the observation that confirms or refutes it, fixed before the work) and the Budget (the most time, attempts or cost to spend).
- When the owner's words lack a field, the PM fills it at the [intake](#task-intake) readback.
- Close carries a Verdict, `confirmed`, `refuted` or `inconclusive`, with its evidence against the decision rule, a Recommendation and the proposed next tasks. An empty list proposes no task.
- An `inconclusive` verdict names the missing evidence and how to get it. A spent budget without a result is `inconclusive`, never a silent extension.
- No verdict, no close: review returns a hand-in without one to the worker ([review](review.md#review)).
- Review closes the task against its acceptance. The outcome is then undecided: it stays in the supervisor's focus (board status and each PM tick) until Make tasks, Drop, or Later with a revisit date. Later without a date is not a decision; at the date the outcome returns to focus.
- The PM decides technical outcomes. It asks the owner only product, scope or visual outcomes, as [decision questions](../caveman/rules/core.md#decision-questions).
- No task starts on an undecided outcome. When another task already depends on the decision, the worker raises the decision as an ask before close.

Sources: [autoresearch](https://github.com/karpathy/autoresearch) (fixed budget, one metric, keep or discard), [long-running agent harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (verified state, never done without a test), [Kanban explicit policies](https://kanban.university/kanban-guide/), [ADR](https://adr.github.io/) (each decision has a status).

## Task intake

Workers must not claim a task before its body is final.

- Every new task enters the board held, as a draft: a PM task, a worker follow-up, a retro item or a review finding alike.
- The PM (whoever supervises the board) starts a draft only after reading it back from the board and confirming: one goal, verifiable acceptance, scope, dependencies, no duplicate of an open task and no conflict with a specification.
- Triage comes before filing or starting: the PM reads the open tasks on the same surface and picks one of steer the open task, merge the drafts into one, add a dependency, file a new task, or reject. The PM checks the acceptance against the specification of that surface; acceptance that contradicts a [decided rule](agent-workflow.md#decided-rules) is rejected or becomes an owner ask.
- The PM decides triage without an owner confirmation; the owner joins only when the PM escalates an ask it cannot resolve.
- A draft that fails the readback is edited or closed by the PM; it is never started as is.
- A draft that passes the readback is started at once, plan tasks included; `Depends on` orders them. A draft is never kept held to wait for another task: hold has no automatic exit. Only an owner gate keeps it held, and the card names who releases it.
- A started task body is not edited. A change to started work goes through a steer or a requeue with its reason.
- No trial or placeholder task is added to a live board.
- A third follow-up for the same symptom is not started, whoever files it (PM, worker, retro or review). Same symptom means the same observable signal: the same failing check, error text or telemetry metric, not similar title wording. The PM files one root-cause task instead; it names the earlier tasks, and its acceptance proves the symptom is gone (a test, or a telemetry window without the signal). Earlier open follow-ups depend on it or close as superseded.
- Intake gates only new work: a started task never waits for the PM.

## Runtime preference

Design, UI, visual and image work prefers codex; all other work (code, infrastructure, release, host, docs, research) prefers claude. Every review prefers claude, including review of codex work.

- At work and review intake, automatically use eligible codex when claude is unavailable, including disabled capacity `0`, missing installation or login, or a quota hold. No owner ask is needed for fallback. A type preference must not become a mandatory `run-claude` label.
- An explicit owner runtime pin takes precedence; fallback never overrides it. Eligibility respects runtime grants ([permission authority](permission-authority.md)), configured capacity and common admission gates. Fallback never weakens security or enlarges permissions.
- Fallback selects new launches only. Preserve active sessions and work; never duplicate or migrate a live execution. Unknown liveness does not permit a replacement launch.
- If neither runtime is eligible, or an owner pin excludes the eligible alternative, report the factual blocker and automatic recheck condition. Keep unknown evidence unknown; missing evidence does not establish availability.

How a task states its preference or pin, how eligibility is checked and when automatic rechecks run belong to the consumer contract.
