# specq

Public reusable rules of taskqorg. Private material (host inventory, identities, SoT) stays outside this repository.

## Principles

- **R1.** Every taskqorg project works by these rules: [working principles](engineering/principles.md).

## Spec areas

One owner page per area. Other pages in the area link from it.

- Texts: [caveman/](caveman/README.md), the Caveman style library. Moved with history from `gitlab.ufobe.com/gradus-public/caveman` (archived); pinned links to commit `62579538` stay valid here.
- Notifications: [caveman/rules/notifications.md](caveman/rules/notifications.md).
- Design: [design/](design/README.md): workflow, operator interfaces, implementation fidelity and labels.
- Engineering: [engineering/](engineering/README.md): Ponytail, spec first, [project contracts](engineering/contracts.md), agent workflow, [verification](engineering/verification.md), [testing](engineering/testing.md), data, performance, release, update, service and [security](engineering/security.md).

Check: `python3 caveman/scripts/check.py` and `git diff --check`.
