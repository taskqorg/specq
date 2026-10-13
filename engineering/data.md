# Data and storage

Rules for the state a tool keeps on disk. Consumer contracts name their store, schemas, paths, durability class and retention bounds.

## Store

- Default store is SQLite in the tool's own process, WAL mode. No separate database or cache server unless the contract shows a need the file cannot meet.
- Name the durability class in the contract. `synchronous=NORMAL` survives a process crash, not a power loss; use `FULL` where losing an acknowledged write is unacceptable. Never `synchronous=OFF` or an in-memory journal for data the user relies on.
- One writer connection with prepared statements and a `busy_timeout`; readers may use separate connections. Let the database build the response shape (for example JSON) when that removes an object layer.
- Group commit is allowed: several requests' writes share one transaction, and every response waits for that commit. A failed batch fails every waiting request honestly and rolls back; nothing uncommitted is visible.

## Files

- Write a state file atomically: temporary file in the same directory, fsync, rename, directory fsync. Readers never see a partial file.
- Serialize writers with a lock file. A busy lock is an error, never a silently skipped run.
- A corrupt, unreadable or newer-schema state file is kept for investigation and reported as unknown ([unknown is never healthy](verification.md#unknown-is-never-healthy)). Never reset it silently.
- Everything that grows has a bound and a pruner in the same service: logs, releases, caches, incidents, queues. The contract names each bound.
- A backup is not a restore proof; see [Documentation](../caveman/rules/documentation.md#density-without-ambiguity).

## Checks

- One crash test per store: acknowledged writes survive `SIGKILL` and restart; failed writes stay isolated.
- One corruption test per state file: a truncated or foreign file reads as unknown and is preserved.
