# Dashboards and widgets

A dashboard gives the owner a useful overview at a glance and stays current without manual reload. Apply [operator design](operator-ui.md), [design workflow](workflow.md) and [implementation fidelity](implementation-fidelity.md); this page owns dashboard-specific rules.

## First-screen overview

- **W1. Prioritize the first viewport.** Show the owner's frequent questions, consequential warnings and essential current values together. Supporting detail follows below; diagnostics and historical detail come last. These are priority levels, not a requirement for three screens or pages.
- **W2. Structure moderate density.** Group related information, reuse alignment and keep headings and semantic icons concise. Use readable type and purposeful spacing. Remove repetition before shrinking text; avoid both oversized cards and a wall of metrics. Product contracts name the primary questions and target viewport.
- **W3. Show dynamics where they matter.** Pair a current value with its unit and a compact trend when change over time informs a decision. Label the time window and scale. Missing samples remain gaps; a new reading alone cannot establish a trend.

## Continuous updates

- **W4. Refresh automatically.** Normal use never requires reloading the page. Update values in place, preserve focus, scroll, expanded detail and stable row positions. Show data freshness and refresh failure; retain the last successful values with their age. Product contracts own cadence and source freshness limits.
- **W5. Make change legible and quiet.** Draw brief, local attention to a changed value or status; leave unchanged content still. No whole-page flashes, looping pulses, layout jumps or rolling digits that delay reading the actual value. Coalesce rapid changes instead of restarting an endless effect. Respect reduced-motion preferences; values and status remain understandable without animation.
- **W6. Color means consequence.** Improvement and deterioration may use restrained green and red emphasis where the metric's meaning is known. Numeric increase alone does not mean improvement. Neutral changes use neutral emphasis; unknown and stale data never look healthy. Pair direction or status with text or a symbol, and keep enduring warnings visible after the transient cue ends.

## Widget consistency

- **W7. Keep the summary useful.** Expose the subject, relevant value or state, scope and freshness without opening detail. Use concise Unicode or consistent icons as semantic cues with accessible labels; avoid decorative repetition and verify glyphs on target platforms. Product contracts select metrics and symbols.
- **W8. Preserve evidence in detail.** Group related observations by an explicit key and retain access to the underlying records. Grouping does not establish a shared cause. Keep historical records distinct from current failures and observation gaps. Put relevant evidence and existing work-item links beside their subjects.

## Bars, trends and changing numbers

- **W9. Match the visual to the question.** Use a filled bar for current utilization against a known capacity; show used/total and units beside it. Use a compact line chart for change over time. Combine them when both headroom and direction matter; never replace exact values with graphics alone.
- **W10. Make comparisons truthful.** Comparable utilization plots share a fixed percentage scale and time window. Show scale and window once per unambiguous group. Bars run from zero to total capacity. An unknown total cannot produce a utilization bar; missing history cannot produce a continuous line.
- **W11. Mark actionable limits.** Put a visible threshold mark on capacity bars when a defined limit exists. Use a calm common color for ordinary measurements and semantic warning/failure colors for breached limits, with a textual or symbolic status. Example thresholds do not become operational policy.
- **W12. Update the value, then signal the change.** Render the new number immediately in tabular figures, retaining unit placement and space for changes in digit count. Briefly tint only the changed value; show direction and a correctly labelled delta when useful. Update its bar, trend and summary from the same sample. Unchanged values stay still; apply W4–W6 to motion, continuity and status.

## Project board summaries

- **W13. Separate work, decisions and failures.** Use one aligned row per project with stable counter order. Distinguish active work, an owner's answer, task failure, ready work and dependency blocking. Product contracts define exact state mappings; an unreadable source is unknown, never an empty queue. Aggregate totals state their coverage when any source is unavailable.
- **W14. Show queue composition, not fake progress.** An optional segmented bar uses the same state order and colors as counters, with one shared count scale across projects. It represents the current open-task mix, not percent completion. Keep exact counts visible and retain access to omitted states.
- **W15. Make counters useful.** Selecting a nonzero count reveals that project's matching tasks in place, including state, identity/title, age and the reason or decision needed. Keep owner questions and dependent work distinct. Pair each project with a recognizable board icon linked directly to its actual board; give icon links accessible names. Read-only dashboards link to the source for actions rather than silently changing tasks.

## Acceptance

Verify the first viewport against the owner's named questions with representative data, warnings, missing sources and long labels. Check the agreed screen sizes and text scale, both themes, reduced motion and several consecutive refreshes. Confirm that detail remains reachable, reading position stays stable, changes remain noticeable without distraction, and failed refreshes cannot look like a fresh all-clear.

Each product records exact metrics, ordering, breakpoints, cadence, thresholds, trend windows and effect parameters. Unresolved parameters stay proposals; this shared page does not silently choose them or claim a consumer is implemented.
