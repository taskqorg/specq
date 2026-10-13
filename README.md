# specq

Public reusable rules of taskqorg. Private material (host inventory, identities, SoT) stays outside this repository.

Every taskqorg project works by these rules: [working principles](engineering/principles.md).

## Spec areas

One owner page per area. Other pages in the area link from it.

- Texts: [caveman/](caveman/README.md).
- Notifications: [caveman/rules/notifications.md](caveman/rules/notifications.md).
- Design: pending; a separate design task adds the owner page.
- Engineering: [engineering/](engineering/README.md).

## Folders

- [caveman/](caveman/README.md): Caveman style library. Moved with history from `gitlab.ufobe.com/gradus-public/caveman` (archived); pinned links to commit `62579538` stay valid here.
- [engineering/](engineering/README.md): engineering contract. Ponytail, spec first, release/update/service contract modelled on taskq v4.

Check: `python3 caveman/scripts/check.py` and `git diff --check`.
