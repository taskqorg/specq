# Release, update, service

The contract a taskqorg tool follows when it ships as a binary. [coreq](https://github.com/taskqorg/coreq) is the shared Rust implementation; [coreq.md](https://github.com/taskqorg/coreq/blob/main/coreq.md) defines every step, name and threshold. [taskq](https://github.com/taskqorg/taskq/blob/main/taskq.md) is the reference consumer. [dashq](https://github.com/taskqorg/dashq) is where each tool's `status.json` is seen.

## Rules

- A tool depends on coreq, pinned by git tag (`v0.1.0`), and passes its own name, title, release repository and version. It does not copy release, update or service code.
- Release: one static binary per OS and architecture, built by CI on a `v*` tag, with checksums and a manifest. A failing selftest publishes nothing.
- Update: immutable release folders, an atomic `current` and `previous`, a verified download, a selftest smoke and launcher rollback. Running children keep their own release folder.
- Compatibility N/N-1: a release changes shared data only additively, so the previous version keeps working next to it.
- Service: one OS unit per host runs `<tool> service run`. Each pass writes `status.json`; every UI reads it and none talks to the backend directly.
- Unknown or stale values say so with a reason, never zero or success.
- A change to a step or threshold edits coreq.md first ([spec first](spec-first.md)); this file changes only when a rule changes.
