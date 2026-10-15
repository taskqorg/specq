# Release, update, service

Rules for tools distributed as binaries with a managed background service.
Consumer contracts define platforms, commands, artifact names, paths, schemas, dependencies and thresholds.

## Rules

- Build versioned artifacts in CI from source for each supported platform and architecture. Pin dependency versions and verify downloaded sources by checksum.
- Publish integrity metadata and a machine-readable release manifest.
- Verify release artifacts before publication. Failed checks block publication.
- Define the trusted release source and who may publish.
- Reuse a shared implementation where available; keep its identity and pinned version in the consumer contract.

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

- A merge to the main branch is a deployment candidate. The only gates are the persistent chain checks ([test classes](verification.md#test-classes)) and the release checks above.
- One approval per task, recorded in the task contract ([approval boundaries](agent-workflow.md#approval-boundaries)); no approval per step and no manual queue between merge and rollout.
- Rollout and rollback are bounded in minutes and scripted; rollback is one command that activates the preserved previous version.
- Measure lead time from merge to running version, deployment frequency, change failure rate and time to restore. A slow or manual step in that path is a defect to remove, not a routine to keep.

## Release task

- A release task ends when its version PR is merged. Acceptance names the version bump in the merged PR and nothing after it.
- Tagging, release assets and host updates follow the merge automatically ([self-maintenance](#self-maintenance)). The task card has no tag, release-run or heartbeat condition, and no task or PM action starts them.
- The worker does not produce rollout evidence. Rollout evidence is the version each host reports in its heartbeat.
- The PM verifies rollout from host heartbeats and the DashQ hosts view.
- A follow-up task is justified only when a host stays behind the released version for more than one update interval. It names the host, the reported version and the observed interval.

## Service

- Define service ownership and lifecycle in the consumer contract; installation must not create competing owners.
- Expose observable health, version, current work and errors through a documented status interface.
- UIs consume the service interface; they do not duplicate backend state or orchestration.
- Report stale or missing observations per [unknown is never healthy](verification.md#unknown-is-never-healthy).
- Verify install, restart, stop, uninstall and recovery on each supported platform.
