# Labels and status color

Make labels easy to identify and compare in the host platform's native rendering.
Products define their own vocabulary, reserved names, state mapping and palette.

- Prefer short, unambiguous names. Avoid cryptic abbreviations; use a prefix only when it distinguishes a useful group.
- Describe each managed label's meaning, effect and change mechanism.
- Distinguish membership, status, priority and constraints. Do not make every category compete for attention.
- Reserve strong color for meaningful activity, required decisions, failure or urgency. Keep routine metadata subdued.
- Preserve textual meaning without color. Verify contrast in each supported platform and theme; an API color is not a rendering guarantee.
- Do not create labels solely to spell out an implicit default unless users need that distinction.
- Keep naming migrations separate from semantic changes. Inspect existing usage and preserve unrelated labels and assignments.

Apply [shared verification](../engineering/verification.md) to adoption and migration. Product contracts define compatibility, authorization, readback and closed-item handling.
