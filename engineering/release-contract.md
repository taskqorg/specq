# Release, update, service

The contract a taskqorg tool follows when it ships as a binary. Modelled on taskq v4; [taskq.md](https://github.com/taskqorg/taskq/blob/main/taskq.md) § 8 is the reference implementation and the canonical detail.

## Release

- One static binary per OS and architecture, built by CI on a `v*` tag: `<tool>-<ver>-<os>-<arch>`.
- The release carries `SHA256SUMS` and `latest.json`. A failing selftest publishes nothing.
- The release repository is built into the binary; no config changes it. Trust is HTTPS plus who can push tags.

## Update

- Install layout: immutable `releases/<ver>/`, a `current` file with `<ver>` (atomic rename) and `previous`.
- `<tool> update`: read `latest.json`; not newer: stop. Download into `releases/<ver>.tmp/`, verify sha256, rename. Smoke: `releases/<ver>/<tool> selftest`; failure deletes it and keeps current.
- The launcher runs `releases/$(current)/<tool>`. A version that fails to start repeatedly is rolled back to `previous`.
- Running children keep their own release folder: no drain, no manual resume.
- Compatibility N/N-1: a release changes shared data only additively, so the previous version keeps working next to it.

## Service

- `<tool> service install|run|pause|resume|status|restart|stop|uninstall|list`.
- One OS unit per host runs `<install>/<tool> service run`; install makes its binary `current` when newer.
- The service writes `status.json` (host, version, error, heartbeat time, work in progress) that every UI reads; no UI talks to the backend directly.
- Unknown or stale values say so with a reason, never zero or success.
