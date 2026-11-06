# Release, update, service

Rules for tools distributed as binaries with a managed background service.
Consumer contracts define platforms, commands, artifact names, paths, schemas, dependencies and thresholds.

## Rules

- Build versioned artifacts in CI from source for each supported platform and architecture. Pin dependency versions and verify downloaded sources by checksum.
- Publish integrity metadata and a machine-readable release manifest.
- Verify release artifacts before publication. Failed checks block publication.
- Define the trusted release source and who may publish.
- Reuse a shared implementation where available; keep its identity and pinned version in the consumer contract.

## Shared implementations

A feature in a shared implementation reaches every consumer through its pin, so the pin stays exact and stays current.

- Each new tag of a shared implementation opens a pin update in each consumer automatically. A green merge queue merges it. A consumer whose pin is part of an approved signed or qualified identity names that exception in its contract, and its update goes through review.
- A consumer that reaches one shared implementation both directly and through another pins the version the other resolves, and updates both in one change.
- Merge-queue CI of a shared implementation builds and tests each consumer's main branch against the candidate. A consumer it breaks blocks the merge. The shared implementation's contract lists the checked consumers. A consumer behind on the pin joins that list once it has caught up.
- The manifest holds the pin. A contract points at the manifest and does not repeat the version.
- A breaking change ships with the consumer changes it needs.
- A pin update does not adopt a new API. A task that adds a capability consumers must call lists those consumers in its acceptance, and it is done when they use it.
- A merged pin update is a development candidate; it reaches hosts by [release](#delivery-speed).

## Update

- Keep installed releases immutable. Verify downloads before activation.
- Validate the candidate before switching the active version atomically.
- Preserve the previous working version and define a tested rollback path.
- Preserve running work during updates. State platform-specific limitations explicitly.
- Define compatibility for overlapping versions and a migration plan for incompatible changes.

## Self-maintenance

Install once, then leave it. The service maintains itself.

- The service runs its own update check, pruning, log rotation and rollback on its schedule. No second scheduler, cron entry or human routine.
- A failed update keeps the current version. A version that fails to become healthy after a bounded number of starts is rolled back automatically.
- Pausing stops updates, not health checks or the service's core work.
- Retries, timeouts and growing files are bounded per [data](data.md#files).

## Delivery speed

- Development and release are separate channels. The main branch is the development channel; the release branch (`live` unless the consumer contract names another) is the release channel.
- A merge to main is a development candidate. The development host builds it locally from source on demand: on an explicit request, or when a ready task depends on a merge that is not installed yet. One build takes the newest green main commit; no release run, tag or host rollout waits on it. Building every merge spends host CPU and holds spawns while nothing needs the build. The gates are the checks selected by [Testing](testing.md#run-policy-by-stage).
- Live acceptance of a merged change runs on the development build once that build is installed; the check requests it. Tasks depend on merge or close, never on a release; a check that needs a released artifact on every host goes to the next release task.
- A release fast-forwards the release branch to a main commit that already passed merge-queue CI. That push tags, publishes and rolls out to every host automatically. The owner decides when to release; that push is the only manual step.
- One approval per task, recorded in the task contract ([approval boundaries](agent-workflow.md#approval-boundaries)); no approval per step and no manual queue between a build request and the development build.
- Rollout and rollback are bounded in minutes and scripted; rollback is one command that activates the preserved previous version.
- Measure lead time from merge to running version, deployment frequency, change failure rate and time to restore. A slow or manual step in that path is a defect to remove, not a routine to keep.

## Release task

- A release task ends when its version PR is merged to main and the release branch is fast-forwarded to that merge commit. Acceptance names the version bump and the release-branch commit, nothing after it.
- Tagging, release assets and host updates follow the release-branch push automatically ([self-maintenance](#self-maintenance)). The task card has no tag, release-run or heartbeat condition, and no task or PM action starts them.
- The worker does not produce rollout evidence. Rollout evidence is the version each host reports in its heartbeat.
- The PM verifies rollout from host heartbeats and the DashQ hosts view.
- A follow-up task is justified only when a host stays behind the released version for more than one update interval. It names the host, the reported version and the observed interval.

## Host requirements

A missing or outdated host tool is a product defect, not a host patch.

- The consumer contract lists every external tool and library the product runs on a host (for example `gh`, `git`, `codex`, `claude`, a system library), each with its minimum version and what needs it.
- The product's doctor or selftest checks each listed requirement on the installed host. A missing tool or a version below the minimum fails with the tool, the found version, the required minimum and the fix.
- Install, onboarding and the update check bring listed requirements up to their minimum on hosts the product manages. When they cannot, they report the exact step and the doctor stays failed.
- A change that starts using a new tool, flag or API raises the listed minimum in the same change. Tests cover the oldest supported version.
- A failed call to an external tool is logged with the command and its error; it never reads as an empty result.

## Service

- Define service ownership and lifecycle in the consumer contract; installation must not create competing owners.
- Expose observable health, version, current work and errors through a documented status interface.
- UIs consume the service interface; they do not duplicate backend state or orchestration.
- Report stale or missing observations per [unknown is never healthy](verification.md#unknown-is-never-healthy).
- Qualify install, restart, stop, uninstall and recovery on each supported platform; rerun affected paths under [Testing](testing.md#run-policy-by-stage).
