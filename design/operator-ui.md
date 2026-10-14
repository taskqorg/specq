# Dense operator interfaces

Maximize readable, useful information within the smallest practical area.
Apply to operator tools; product contracts define entities, status semantics, dimensions and controls.

Implementation and review follow [F1–F6](implementation-fidelity.md); product contracts supply dimensions, fixtures and platform evidence.

## Principles

- **D1. Keep related content together.** Present an entity as one flowing block. Metadata and title start together; wrapping does not create a separate column.
- **D2. Use one grid.** Align names left and compact counter groups right. Reuse edges and spacing across levels. Align visible marks, not just containers.
- **D3. Preserve readability.** Use large, adjustable text. Keep secondary text readable and respect system scaling.
- **D4. Give whitespace a purpose.** Size to content. Do not stretch gaps between names, counts and navigation. Remove duplicate cards and labels. Let grouping, alignment and a shared heading carry repeated meaning before adding words. Use a familiar semantic symbol when it remains clear; keep units, uncertainty and accessible names.
- **D5. Keep primary actions direct.** Reveal detail on demand; do not add an intermediate screen just to expose a link.
- **D6. Let long text use the row.** Wrap titles from the full block's left edge, below metadata. Keep atomic identifiers intact. Avoid fixed metadata columns that squeeze titles or force horizontal scrolling.
- **D7. Give color stable meaning.** Use restrained colors and text contrast of at least 4.5:1. Add position, symbols or labels so color is never the only signal.
- **D8. Make controls truthful.** Links reach their named targets. Explain unavailable actions. Provide keyboard focus and accessible names.
- **D9. Density is not crowding.** Remove duplication and excess gaps before reducing width. Never shrink text to win a pixel count. Prevent multi-digit collisions.
- **D10. Group counters.** Keep order and placement stable; pair values with semantic symbols. Hide zero only when absence conveys the same meaning. Unknown is not zero. Product specifications define exceptions.
- **D11. Put small actions beside their subjects.** Prefer a compact icon to a separate full-width button when meaning remains clear. Preserve accessible names and usable hit targets; avoid decorative icons.
- **D12. Keep specifications concise.** Follow the [documentation profile](../caveman/rules/documentation.md).
- **D13. Put attention first.** Decisions and failures precede ordinary lists. Completed conversations and maintenance details must not displace active work.
- **D14. Put actions in their section headers.** Place add beside the section name and external links beside the entity name. Group settings by purpose with recognizable icons and labels.

## Review each change

1. Does each element help recognition, decision or action? Remove it if not.
2. For each label, can it disappear because position, a shared heading or a semantic symbol already conveys its meaning? Compare before/after; retain it if removal introduces ambiguity. Remove duplicate rows and gaps before shrinking text.
3. Are alignment, direct actions and accepted features preserved?
4. Check long text, large fonts, narrow surfaces, both themes and system scaling.
5. Review the complete route: list, detail, action, result, error and return. A polished home screen does not compensate for unusable deeper views.

Validate one real component before spreading a rule. Inspect rendered output at its intended size; calculation tests alone do not establish visual quality.
Product acceptance criteria define concrete fixtures, dimensions and platform checks.
A product-specific exception needs a reason and an owner decision. Never silently substitute a spacious dashboard.

## Stable adaptation

Keep essential controls in stable locations. Adapt information to current consequences and explicit user preferences; avoid opaque frequency-based rearrangement. Preserve pointer and keyboard targets during updates.

Review against normal operation, blocked work, critical faults and frequent use. Product contracts choose ranking, visible limits and emergency semantics.
