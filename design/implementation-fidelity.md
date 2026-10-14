# Design fidelity and acceptance

Translate an approved design into observable product behavior. A similar screenshot is insufficient.
Use [operator principles](operator-ui.md) and [engineering evidence](../engineering/verification.md).

## F1 Source and change control

- Pin the specification, reference assets, fixture data and implementation revision used for review.
- Product contract owns behavior; design specification owns geometry; approved assets own shapes. Exploratory mock behavior is not a missing backend contract.
- Inventory existing features before replacement. Map every feature to its destination or an explicitly approved removal.
- Implement shared tokens/assets once. Do not redraw an accepted icon from memory or replace fonts, symbols or graph semantics for convenience.
- Conflicting references require a recorded decision. Never pass by updating expected output to match a defect.
- A useful implementation improvement is a candidate: show its benefit, affected rules and before/after. Adopt after review, then update the canonical specification/reference.

## F2 Size to content, then constrain

- Measure natural content at the selected font and intended width. Include native chrome in the available-space calculation.
- Fit to the anchor monitor's usable work area, excluding reserved OS regions; do not use a percentage of total screen height as a substitute.
- Expand to fit when space exists. Scroll only when natural content exceeds available space. Product contracts set margins, width limits and anchoring.
- Keep width stable during ordinary refresh. Reflow on font, monitor, DPI or navigation changes; never shrink text to avoid overflow.
- Measure unconstrained content, not an already clipped viewport. Recompute after fonts, asynchronous content, disclosure changes and native scale changes.
- Avoid resize loops and visible oscillation. A scrollbar must not repeatedly change wrapping and reverse the sizing decision.

## F3 Scroll and focus

- One primary scroll region per navigation surface. Fixed controls remain visible and never flex-shrink under overflowing content.
- No horizontal scrolling for ordinary text/forms. Reflow counters and metadata before truncating meaningful content.
- Preserve scroll, selection, drafts and focus during data refresh. Back restores the prior navigation position.
- New detail starts at its heading. Validation reveals the error without losing edits. Keyboard navigation scrolls the focused control into view.
- Follow new chat output only while the user is at the bottom; show a new-content action otherwise. Composer stays reachable.
- Test scroll appearance and disappearance at the actual boundary, not just a short and a huge example.

## F4 Raster and graph geometry

- Define geometry in logical units; convert once using the target scale. Render at final device resolution.
- Snap straight filled chart marks to physical pixel edges. Use shared integer bar width, gap and baseline; avoid accumulated fractional offsets.
- If the slot cannot hold the prescribed number of marks, use an approved aggregation or fallback. Never hide samples or smear them into a false continuous signal.
- Equal quantities share one scale. Stack cumulative boundaries; round boundaries, not independent segment heights.
- Empty data, zero, stale data and unknown data remain distinct. Color order and data meaning must match across renderers.
- Inspect at natural size first, then enlarged nearest-neighbor detail. Font antialiasing may differ; missing series, unequal gaps and altered shapes are not font tolerance.

## F5 Acceptance package

Keep one project package index. It links the contract and shared rules; accepted decisions and unresolved proposals; use cases with requirement-to-scenario coverage; the [F1](#f1-source-and-change-control) implementation inventory, required backend work and preservation/removal decisions; editable references, generated previews, licensed assets and rendering constraints; and the items below with their artifact revisions. Required unresolved decisions have options and an owner; placeholders remain gaps.

Deliver:
1. Feature/navigation ledger: every required control, destination, supported state and requirement ID.
2. Deterministic fixtures: normal, empty, long, dense, unknown, failure and boundary cases.
3. Target-platform images and interaction evidence tied to exact artifact hashes; include environment, font, theme, scale and usable-area dimensions.
4. Automated results separated into data/model, adapter, geometry and runtime checks.
5. Review report findings: requirement, expected, observed, reproduction, severity, evidence and disposition.

Every mandatory criterion is Pass, Fail or Not tested. “Looks close” is not a verdict. Missing platform evidence stays Not tested.
Do not average away a failed action, missing state, wrong data meaning or unreachable control with a visual score.

## F6 Build, polish, accept

- Builder completes the feature ledger and captures actual product output. Placeholders and prototype-only actions remain gaps.
- Reviewer compares identical fixtures against the approved reference; tests navigation and resizing, not just pixels. Report reproducible differences.
- Polish fixes defects in the shared component or renderer; recheck all affected surfaces and preserve useful verified implementation work.
- Owner reviews design changes; unchanged requirements need no repeated design approval.
- Freeze the candidate and repeat affected acceptance checks. Final report distinguishes design accepted, runtime verified and deployed.
- Keep unresolved semantic or platform failures open. An implementation agent cannot declare its own changed design approved.
- Builder, reviewer and owner are responsibilities, not a requirement to spawn separate agents.
