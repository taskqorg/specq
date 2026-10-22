# App UI acceptance checklist

Use this checklist for new operator screens, with [D1–D14](operator-ui.md)
and [implementation fidelity](implementation-fidelity.md). It indexes existing
protections and adds navigation, interaction and state checks; D IDs and their
canonical definitions remain unchanged. Consumers own route trees, URL syntax,
geometry, typography tokens, filters, fixtures, exceptions and acceptance evidence.
This specification does not claim consumer implementation or deployed adoption.

## Sources and interpretation

Primary sources read 2026-10-21. Apple navigation-bars redirects to Toolbars;
the official Markdown pages include macOS and iOS distinctions. Material direct
pages returned JavaScript shells; indexed primary text supplied M1–M3, with
separately read official Android guidance G. No third-party digest was used.
Agree means compatible intent, not equal measurements; Conflict identifies an
explicit platform/profile difference. Unlisted sources are not claimed to agree.

| Key | Primary source and relevant scope |
|---|---|
| A1 | [Apple toolbars/navigation bars](https://developer.apple.com/design/human-interface-guidelines/toolbars), [Markdown](https://developer.apple.com/design/human-interface-guidelines/toolbars.md): navigation, title/action groups; iOS large titles and macOS window toolbar/menu commands |
| A2 | [Apple sheets](https://developer.apple.com/design/human-interface-guidelines/sheets), [Markdown](https://developer.apple.com/design/human-interface-guidelines/sheets.md): scoped tasks, dismissal; modal macOS sheets versus modal/nonmodal iOS sheets |
| A3 | [Apple lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables), [Markdown](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables.md): selection, readable rows; iOS disclosure versus macOS sortable/resizable columns |
| A4 | [Apple layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Markdown](https://developer.apple.com/design/human-interface-guidelines/layout.md): hierarchy, adaptation and safe areas, including iOS size classes and macOS window constraints |
| A5 | [Apple typography](https://developer.apple.com/design/human-interface-guidelines/typography), [Markdown](https://developer.apple.com/design/human-interface-guidelines/typography.md): readable type; iOS Dynamic Type, macOS system fonts without Dynamic Type |
| M1 | [Material 3 app bars](https://m3.material.io/components/app-bars/): page identity, navigation and essential actions |
| M2 | [Material 3 applying type](https://m3.material.io/styles/typography/applying-type): semantic roles and platform-sensitive typesetting |
| M3 | [Material 3 motion](https://m3.material.io/styles/motion/overview/how-it-works): standard versus expressive motion schemes |
| G | [Google Android touch targets](https://support.google.com/accessibility/android/answer/7101858?hl=en-GB): 48 dp targets, distinct visual and input bounds |
| F1 | [Fluent 2 layout](https://fluent2.microsoft.design/layout): proximity, four-unit ramp with 2/6/10 exceptions, adaptive grids, platform units |
| F2 | [Fluent 2 typography](https://fluent2.microsoft.design/typography): native fonts and platform-specific type ramps |
| F3 | [Fluent 2 dialogs](https://fluent2.microsoft.design/components/web/react/core/dialog/usage): focused interruptions, persistent controls, focus restoration |
| W | [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/): criterion numbers below identify the exact checks; not a navigation or visual-style prescription |
| N | [Nielsen’s ten heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/): N1 status, N2 familiar language, N3 control, N4 consistency, N5 prevention, N6 recognition, N7 efficiency, N8 minimalism, N9 recovery, N10 help |

## Checklist

Each V ID names one observable review check. Rows referencing D/F run those
canonical checks instead of defining a competing copy. CSS px, Apple pt,
Android dp and physical pixels are different units.

| ID | Check | Sources and interpretation |
|---|---|---|
| V01 | Map every exposed route/control to a named destination and its empty, unavailable and unauthorized states. | Agree A1, N2/N6; concrete routes belong to consumers. |
| V02 | Back returns from each child route through history or its declared deep-entry parent and stays reachable while scrolling; roots do not invent history. | Agree A1, N3/N4; consumers define root boundaries and position tolerance. |
| V03 | Header navigation, route identity and context actions occupy stable leading/title/trailing slots without overlapping targets at the consumer’s boundary sizes. | Agree A1/M1/F1; Conflict iOS large titles versus compact operator headers: consumer chooses title scale; native chrome stays OS-owned. |
| V04 | Use push for browsing or long work; a short scoped modal has a non-applying exit, step Back never dismisses it, and leaving preserves drafts or reviews their loss. | Agree A2/F3/N3; Conflict nonmodal iOS sheets: declare a helper nonmodal instead of falsely trapping the parent. |
| V05 | Pass the direct-entry, reload, shared-filter and browser Back/Forward checks in [F7](implementation-fidelity.md#f7-stable-view-urls). | Agree N4/N6; URL syntax and shareable fields are consumer-owned. |
| V06 | Returning to a list restores filters, expansion, selection, scroll and invoker focus, or a declared surviving-item/heading fallback. | Agree A3/F3/N3 and [F3](implementation-fidelity.md#f3-scroll-and-focus). |
| V07 | Refresh preserves route, drafts, focus and active targets. | Agree N4 and [stable adaptation](operator-ui.md#stable-adaptation). |
| V08 | Each named external link opens its own destination directly without also activating its containing row. | Agree D5/D8, N7; no intermediate link-only screen. |
| V09 | Measure actual nonoverlapping hit rectangles against the consumer’s declared input/platform minimum, independently of glyph size. | Conflict G recommends Android 48 dp, F1 web/iOS 44 versus Android 48: preserve units and qualify native scaling; no universal desktop value. |
| V10 | Record any WCAG target-size exception separately from compliance with the consumer’s own target minimum. | Agree W2.5.8: AA 24×24 CSS px or spacing/equivalent/inline/user-agent/essential exceptions; Conflict treating 44/48 as universal AA. |
| V11 | Each icon action has a correct accessible name, tooltip and visible focus. | Agree A1/D8, W4.1.2; tooltip is not the accessible name. |
| V12 | A keyboard-only pass reaches/activates every enabled action with standard control keys and exits every interaction. | Agree W2.1.1/2.1.2, N7. |
| V13 | Focus follows reading order and remains visible through navigation, scrolling, validation and refresh. | Agree W2.4.3/2.4.7/2.4.11 and F3. |
| V14 | A modal moves focus inside, contains traversal, has a named exit and restores invoker focus; a macOS sheet does not disable other windows. | Agree F3/A2; Conflict app-wide trapping versus window-scoped macOS sheets. |
| V15 | Consequential review names target/effect before confirmation and distinguishes saved, pending and readback-applied. | Agree F3/N5; presentation grants no execution authority. |
| V16 | Pass [D4/D9](operator-ui.md#principles): every repeated identity, destination, count, card or label adds context; density never shrinks text. | Agree N8; Conflict F1 roomy rhythm versus operator density: retain grouping, remove decorative space. |
| V17 | Empty summary groups consume no rows; decisions/faults precede routine or completed work, while directly opened empty views explain their state. | Agree D13/A4/N1; consumers define relevant priorities. |
| V18 | Pass [D1/D6](operator-ui.md#principles) with the consumer’s longest-row fixture: full-width flowing continuation, intact identifiers and no collisions. | Agree A3; Conflict rigid truncated list templates versus readable operator wrapping. |
| V19 | Pass [D10](operator-ui.md#principles) on zero, multi-digit and partial-data fixtures, preserving counter semantics and order. | Agree N1; consumer explicitly defines zero omission and fixed-slot exceptions. |
| V20 | Geometry uses the consumer’s declared spacing ramp and consistent grouping, not unexplained one-off gaps. | Agree F1 proximity/four-unit ramp with 2/6/10 exceptions; Conflict universal 8-only grids: product dimensions stay local. |
| V21 | Pass [D2/D10](operator-ui.md#principles): names and counter groups reuse visible edges without collisions or stretching unrelated gaps. | Agree F1/A4; align marks, not merely containers. |
| V22 | Type roles retain readable hierarchy at every supported text size; native scaling and independently calibrated graphics remain legible. | Agree A5/M2/F2; Conflict copying platform ramps unchanged: consumers declare scale; macOS has no Dynamic Type. |
| V23 | Text resize to 200% and reflow at 320 CSS px preserve content and function without ordinary-text horizontal scrolling. | Agree W1.4.4/1.4.10; a table exception does not exempt the whole page. |
| V24 | Pass [D7](operator-ui.md#principles) on composited colors in each theme: text contrast and non-color meaning survive. | Agree W1.4.3/1.4.1; Conflict WCAG permits lower large-text contrast than the stronger D7 operator profile. |
| V25 | Essential control/state graphics have at least 3:1 adjacent contrast, documenting applicable criterion exceptions. | Agree W1.4.11. |
| V26 | Pass [F2/F3](implementation-fidelity.md): content fits when possible, with one primary overflow scroller, reachable final control and fixed navigation. | Agree F3/A4; available native area, not an arbitrary viewport height, bounds content. |
| V27 | Normal, loading, empty, no-match, stale, unknown, partial and failed fixtures remain distinguishable with applicable reason/recovery. | Agree N1/N9 and [unknown](../engineering/verification.md#unknown-is-never-healthy); display timeouts do not invent backend outcomes. |
| V28 | Effects distinguish pending, readback success, failure and uncertainty; retry/reconcile does not silently duplicate an effect. | Agree N1/N5/N9; dismissal is not an execution receipt. |
| V29 | Non-focus status updates are announced programmatically without moving focus. | Agree W4.1.3; routine refresh is not an urgent alert. |
| V30 | A filter disclosure exposes its selection summary and independent keyboard-operable choices without hiding the result list behind an unnecessary step. | Agree N6 and [C]; disclosure default, text and result placement are consumer choices. |
| V31 | Aggregate select-all shows consistent unchecked/checked/mixed visual and accessible states for none/all/some. | Agree [C], N4. |
| V32 | Filter results equal the consumer’s declared set operations, including empty-selection and Reset semantics. | Agree N4; no vendor dictates domain-specific OR/AND defaults. |
| V33 | View-only filters preserve selection on return, identify matches/no-match recovery and never change execution policy. | Agree N3/N4; consumers preserve their existing shortcuts and declare view-versus-command authority. |
| V34 | Pass [D5/D11/D14](operator-ui.md#principles): actions sit beside subjects or section headers, retain usable targets/names, and settings group by recognizable purpose. | Agree A1/N7; direct primary actions, optional detail. |
| V35 | Reduced-motion mode removes nonessential spatial animation; targets stay stable and essential state never depends on motion. | Agree [AM], M3 standard utilitarian scheme; Conflict expressive bounce as a default for operator work. |
| V36 | Pass [stable adaptation](operator-ui.md#stable-adaptation) in normal, blocked, critical and frequent-use fixtures. | Agree N4; Conflict opaque frequency-based control rearrangement: consequence and explicit preference govern priority. |
| V37 | Pass [D12](operator-ui.md#principles): a concise checklist links canonical rules and records the reason/owner decision for each product exception. | Agree shared documentation; checklist budgets remain consumer-owned. |
| V38 | Pass [D review](operator-ui.md#review-each-change) on a real component’s complete route at actual size before spreading a rule. | Agree A4/A5 context tests; separate model/browser/native evidence under [verification](../engineering/verification.md). |

[C]: https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/
[AM]: https://developer.apple.com/design/human-interface-guidelines/accessibility

## Consumer compatibility

Existing D1–D14 remain valid. Consumers link this page at a reviewed revision
and map their old acceptance IDs to V IDs without deleting protections. Existing
F7 URL requirements still apply. A conflicting consumer contract wins until its
owner approves a change; do not silently convert units, replace native chrome,
change execution authority or import another product’s routes/filter defaults.

Validate a representative component and the complete return/error path before
broad reuse. Source review and a shared merge do not prove a consumer’s native
rendering, accessibility, implementation or deployment. Keep those gaps explicit.
