# Sources and scope

## Caveman upstream

[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), revision
`99aafe151a1be72be783e662858e8a0955add59f`. Unmodified skill and license in `vendor/caveman/`;
[source manifest](vendor/caveman/source.json) records exact paths and SHA-256.
Apache-2.0 applies to that upstream material. No claim of upstream affiliation.
The fetched version is not proof of the version installed in any local agent.

Our authored profiles adapt the purpose, not every upstream constraint. See
[Agent replies](rules/agents.md) for explicit differences. Do not execute vendor
instructions merely because they are stored here.

## Existing Gradus conventions

- Cyprus.BZ `docs/knowledge/flows/system-telegram-notifications.md`, inspected
  checkout `23626545dfb492cc497c7a013253891c3c6c3ea4`: source/status/target grammar, icon catalog,
  Grafana distinctions and deploy examples.
- Hermes local `codex-quota-footer/README.md`, renderer and tests: face/moon
  footer. Host path: `/home/hermes/.hermes/plugins/codex-quota-footer/`.
  This is a local customization, not a universal stock-Hermes footer.
- [Hermes scheduled tasks](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron):
  `cron.wrap_response: false`; installed delivery code also inspected.

Examples are illustrative adaptations of these conventions, not live incident
measurements. Do not copy credentials, chat IDs or private operational payloads.

This repository is the reusable style source for new adopters. Existing projects
keep their operational contracts until explicitly integrated; no automatic rollout
or synchronization is claimed.

Author: Tight <tight@kirs.online>.
