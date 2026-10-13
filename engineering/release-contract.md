# Release, update, service

Rules for tools distributed as binaries with a managed background service.
Consumer contracts define platforms, commands, artifact names, paths, schemas, dependencies and thresholds.

## Rules

- Build versioned artifacts in CI for each supported platform and architecture.
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

## Service

- Define service ownership and lifecycle in the consumer contract; installation must not create competing owners.
- Expose observable health, version, current work and errors through a documented status interface.
- UIs consume the service interface; they do not duplicate backend state or orchestration.
- Mark stale or missing observations as unknown with a reason, never zero or success.
- Verify install, restart, stop, uninstall and recovery on each supported platform.
