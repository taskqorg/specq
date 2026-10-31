# Caveman

**Less text. Same meaning. Clear next action.**

taskqorg style rules for agents, operational notifications and documentation.
This is a style library, not a coding framework or a deployment policy.

## Choose a profile

- [Core](rules/core.md): shared principles, precedence and agent reply shape.
- [Agent replies](rules/agents.md): ready-to-paste instruction and upstream relationship.
- [Change communication](rules/changes.md): commit subjects and source and sink encoding.
- [Merge and release](rules/merge-and-release.md): merge-request descriptions, deploy messages and the release check.
- [Notifications](rules/notifications.md): compact operational messages.
- [Indicators](rules/indicators.md): icon vocabulary, ranges and reset notation.
- [Documentation](rules/documentation.md): scannable, compact persistent writing.
- [Examples](examples/messages.md): established patterns and illustrative rewrites.
- [Notification scope](audits/notification-scope.md): adoption boundary; no integration or deployment claim.
- [Sources](SOURCES.md): provenance and upstream differences.

## Adopt

Read Core, then only the profile needed. Link these files from your agent or
project instructions. For agents without repository access, paste the block in
Agent replies. Adopting this repository does not silently change other projects.

## Check

Run `python3 scripts/check.py`. Then review meaning, readability and uncertainty
using the checklist in Core. Mechanical checks cannot prove semantic fidelity.

Maintainer: Tight <tight@kirs.online>.
