# Testing

Keep the smallest set that protects meaningful behavior and risks. Select effort by failure likelihood and impact. Project contracts own commands, selection rules, environments and time budgets; changing existing gates follows [Spec first](spec-first.md). Report results under [verification](verification.md).

## Before adding or changing a test

Answer these questions in order. Reuse the task or change description; no separate questionnaire or report is required.

1. **What must work, and what could fail?** Name the requirement, observable behavior and distinct failure risk. If expected behavior is unclear, use [disagreements](#when-evidence-disagrees) before encoding an assumption.
2. **Does an existing check catch that failure?** Inspect it. Reuse it or add a missing case before creating another test. Covering the same lines is not proof of catching the same failure.
3. **Is this investigation or regression protection?** A development check answers a temporary question; delete it once answered or promote it. A persistent check protects against recurrence. Non-trivial logic keeps the smallest runnable regression check, which may already exist. A one-time trace or readback proves that observation, not future regression protection.
4. **What is the cheapest sufficient boundary?** Choose logic, component, contract or end-to-end checks by the failure they can detect. Use a full chain when the risk is in its connections. Persistent checks, also called chain checks in existing contracts, must name their requirement and risk; they need not each run the whole system.
5. **When must it run, and what does it cost?** Place it under the run policy below, account for setup and dependencies, and reuse the existing runner. Add no tool or infrastructure without a demonstrated gap.

## Keep or remove

- Delete obsolete checks, implementation-mirroring assertions, trivial-helper tests and duplicate risk coverage. Before deleting a redundant check, identify the remaining check that detects its failure. An unnamed risk calls for inspection, not blind deletion.
- No coverage percentage or test-count targets. Prefer data cases and generated sequences to repeated test code; fewer test functions alone do not mean less work.
- Looks, sound and feel are accepted by the owner from pictures or video. A numeric gate follows that acceptance and encodes the accepted result; avoid snapshot churn.

## Run policy by stage

- **Development:** run the affected check. For a defect, reproduce it safely at the smallest behavior boundary, then rerun the same check after the fix. If reproduction is unsafe or unavailable, state why and give alternative evidence; do not claim before/after proof. Trivial and documentation changes need no mandatory test-first work.
- **Merge candidate:** run a cheap deterministic core plus checks affected through code or dependencies, new checks and previously failing checks. The stored suite is not the mandatory suite for every change. Documentation-only changes use documentation checks.
- **Unknown impact:** broaden selection for shared code, configuration, build or dependency changes. If impact cannot be bounded, run the full relevant suite. Validate selection against full runs at project-defined triggers; a selector that misses failures needs repair before relying on it again.
- **Release or deployment:** apply the [release contract](release-contract.md), including artifact verification. Run affected platform, client, lifecycle, outage and live integration checks before exposing the changed risk. Expensive or paid evaluations run only when the behavior they measure changes, not for documentation edits or unchanged redeploys.

Keep the candidate revision, command, result and relevant seed, events or native logs with the evidence. Failures name the broken behavior. Reuse results only for unchanged tested code or artifacts, tests, dependencies and environment; mutable live state needs fresh evidence.

## Time budget

- The project defines one command for its selected merge gate and a numeric elapsed-time budget on a named runner. Measure build, setup and execution, plus repeat runs caused by instability. The core is deterministic and needs neither a human nor a paid service.
- Remove redundant runs, repeated setup and unnecessary external dependencies before adding parallelism. Replace fixed sleeps with bounded completion signals. Repair flaky checks; retries until green are not proof. Exceeding the budget requires diagnosis, not silently skipping required protection.

## When evidence disagrees

- Compare the contract, test assertion and observed behavior first. If the rule is clear, fix the code or test that violates it within the task. Do not change expected output just to make a failure green.
- Ask the owner only about a material missing or conflicting requirement, or a remedy that changes accepted behavior, required protection or a contract budget. Give the conflicting references, observed result, consequence, options and recommendation through [Spec first](spec-first.md#improve-shared-rules). Reuse prior decisions; pause only work that depends on the answer.
- A slow, flaky or redundant check is normally an engineering fix. Propose a cheaper equivalent before asking to weaken a gate. Missing release evidence remains a gap under [verification](verification.md), never a passing result.

Basis, adapted: [Paul Hammant, The Rise of Test Impact Analysis, 2017-08-22](https://martinfowler.com/articles/rise-test-impact-analysis.html); [Software Engineering at Google, 2020 edition, chapter 14](https://abseil.io/resources/swe-book/html/ch14.html). These inform the method; project contracts define its application.
