# Repository and release security

Repository settings, workflow, dependency and release controls of the [security baseline](security.md), and its review routine. Consumer contracts name any exception.

## Repository

- The main branch of every repository is protected: no force push, no deletion, required status checks before merge, administrators included. Protection stops history rewrite; it does not add approvals beyond [one approval per task](release-contract.md#delivery-speed).
- Two-factor authentication is required at the organization level. Collaborators get the lowest role that the task needs; the list is reviewed at every access change.
- Platform scanners are on: secret scanning with push protection, dependency vulnerability alerts and automated security updates. No third-party scanner until a native one proves insufficient on a named case.
- Every workflow declares `permissions:` at the top and grants only what the job needs; the default is `contents: read`. Actions are pinned at least to a major tag, and to a commit SHA where the job holds a secret or publishes an artifact.
- No workflow checks out pull-request code under `pull_request_target`, and no job pipes a download into a shell.
- Every public repository has a `SECURITY.md` naming where to report a vulnerability and the expected response time.

## Dependencies and releases

- The lockfile is committed and a dependency change is reviewed like code. An advisory that reaches a shipped code path is fixed in the next release; the rest wait for the normal upgrade cadence.
- Releases publish checksums and installers verify them before activation ([release contract](release-contract.md#rules)). Build provenance attestation is the next step once checksums are in place, where the platform offers it at no cost.

## Review

A security review is a normal task, run after a new repository or host and at least once a quarter.

1. Run `engineering/scripts/repo-security-check.sh <org>` and read each line as present, absent or unknown ([unknown is never healthy](verification.md#unknown-is-never-healthy)).
2. Fix every absent item of the security baseline and this page in the same task; record an accepted exception in the consumer contract with its owner and reason.
3. Report what changed with read-back evidence ([verification](verification.md)).
