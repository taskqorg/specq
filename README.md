# specq

Public reusable rules of taskqorg. Private material (host inventory, identities, SoT) stays outside this repository.

Every taskqorg project works by these rules: [working principles](engineering/principles.md).

## Spec areas

One owner page per area. Other pages in the area link from it.

- Texts: [caveman/](caveman/README.md).
- Notifications: [caveman/rules/notifications.md](caveman/rules/notifications.md).
- Design: [design/](design/README.md).
- Engineering: [engineering/](engineering/README.md).

## Folders

- [caveman/](caveman/README.md): Caveman style library. Moved with history from `gitlab.ufobe.com/gradus-public/caveman` (archived); pinned links to commit `62579538` stay valid here.
- [design/](design/README.md): shared design rules: workflow, operator interfaces, implementation fidelity and labels.
- [engineering/](engineering/README.md): shared engineering rules: Ponytail, spec first, agent workflow, [verification](engineering/verification.md), data, performance, release, update, service and [security](engineering/security.md).

Check: `python3 caveman/scripts/check.py` and `git diff --check`.

## Adoption

Project content follows [Caveman Core](caveman/rules/core.md) and the applicable profile; persistent documentation follows [Documentation](caveman/rules/documentation.md) in English.
Project contracts link shared rules and contain only their own decisions and exceptions. Propose reusable improvements through [Spec first](engineering/spec-first.md#improve-shared-rules).
