# Indicators

Use one visual family per metric. Keep direction consistent. Prefer a familiar
Unicode symbol to a custom asset; emoji appearance varies across clients, so
verify glyphs and spacing per output channel. Do not recolor standard emoji
through unsupported text formatting.

## Discrete operational status

Shared vocabulary:

- `✅` success / verified healthy.
- `🛑` failure / halted / action required.
- `⚠️` warning / degraded.
- `♻️` recovery or alert cleared; text must distinguish these claims.
- `⏭️` skipped / no-op, not success.
- `❓` unknown, not failure or zero.

Source: `🚚` deploy, `👁️` observability, `☁️` infrastructure, `🐞` application error,
`🖥️` host, `💓` health. Target: `🏗️` development, `🏁` production, `🗄️` database,
`🖥️` host. `📄` introduces commit/author context when needed. Omit redundant roles.

## Continuous indicators

A continuous metric stays in one family; never switch from a battery to a stop
sign halfway through its scale. Keep the exact value beside the quantized icon.

### Context used

- 0–39%: `🙂`
- 40–69%: `😐`
- 70–79%: `😕`
- 80–89%: `😣`
- 90% and above: `🥵`

This describes occupancy, not measured loss of model intelligence. Use the
runtime's displayed percentage without independent rounding. Omit context the
renderer cannot provide.

### Weekly quota remaining

- 0–12%: `🌑`
- 13–37%: `🌘`
- 38–62%: `🌗`
- 63–87%: `🌖`
- 88–100%: `🌕`

As quota falls: `🌕 → 🌖 → 🌗 → 🌘 → 🌑`. Illumination indicates remaining
capacity; do not cycle back to a brighter moon. Validate input before bucketing.
Unknown data is `? unavailable`, never `🌑 0%`. Retained stale data carries
`· stale <minutes>m`.

### Footer and reset

```text
model · FACE context-used% · MOON quota-remaining% ↻ reset
```

`↻` means quota reset, not server restart. The reset reads as a
[countdown](#time). Do not imply that quota usage determines reset time.

## Time

Every surface writes time the same way: UI, tray, CLI, notifications, reports.
Relative time leads; the exact time sits beside it or on hover. One function per
product renders each form below; surfaces do not format time themselves.

Countdown to a future moment. Minutes matter only inside the last five hours.
Round up, so the moment never arrives later than the number says.

| Time left | Reads | Example |
|---|---|---|
| 24 h or more | whole days | `3d` |
| 5 h to 24 h | whole hours | `21h` |
| under 5 h | `H:MM` | `4:12`, `0:47` |
| none | `now` | `now` |

Age of a past moment. Use the largest whole unit, rounded down, one unit only:
`<1m`, `5m`, `2h`, `3d`. Add `ago` unless a label or column already says so. A
negative age reads `<1m`.

Exact time:

- For one viewer: viewer-local, 24-hour, `Thu Nov 05, 14:30`. Add the year when
  it is not the current year.
- Across hosts or time zones, or in board comments, logs and public text:
  `YYYY-MM-DD HH:mm UTC`.
- For machines: RFC 3339 in UTC, `2026-11-05T14:30:00Z`, or integer epoch.
  Never parse a display form back.

Omit the date when it does not affect interpretation. An unknown time reads
`? unavailable`, never `0:00`, `now` or an empty cell.
