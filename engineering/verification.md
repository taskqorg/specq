# Evidence

Report what observations establish. Delivery, exit code and a finished conversation do not prove application or completion.
Use the shared [Core review](../caveman/rules/core.md#review) for reporting; the rules below define engineering evidence.

- Read back changed state before claiming application. Report partial results separately.
- Keep missing, stale or untested observations unknown; name the affected claim or platform.
- Separate model, adapter, process and target-platform checks. Passing one does not qualify the others.
- Verify the exact candidate or artifact being accepted; identify relevant checks and remaining gaps.
- Visual evidence follows the [review set](../design/workflow.md#review-sets) cap.

## Unknown is never healthy

- A collection error, unsupported platform, corrupt state or stale value reads unknown with a reason.
- Never report such a value as ok, zero or success. Health, status and counts follow this rule in every interface.
- For attempts without a terminal stage record, apply the service detection and reporting rule in [Agent work profiling](profiling.md#agent-work).

## Remediation

- Diagnose read-only first.
- Then make only explicitly authorized ([approval boundaries](agent-workflow.md#approval-boundaries)), scoped changes. Each change has ownership proof, a rollback path and a verification step.

## Test classes

Definitions and the decision procedure live in [Testing](testing.md#before-adding-or-changing-a-test). This heading preserves existing links.

## Run policy by stage

The canonical [run policy](testing.md#run-policy-by-stage) lives in Testing. This heading preserves existing links.

## State-driven systems

See [behavioral models](behavioral-models.md#state-driven-systems).

## Formal checks (optional)

See [behavioral models](behavioral-models.md#formal-checks-optional).

## Agent integration

See [rule delivery](rule-delivery.md#agent-integration).
