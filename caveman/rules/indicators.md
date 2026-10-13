# Indicators

Use one visual family per metric. Keep direction consistent. Prefer a familiar
Unicode symbol to a custom asset; emoji appearance varies across clients.
Do not recolor standard emoji through unsupported text formatting.

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

This describes occupancy, not measured loss of model intelligence. Use the same
displayed percentage as the runtime; do not introduce independent rounding.
Missing context may be omitted when the renderer cannot provide it.

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

`↻` means quota reset, not server restart. Round partial days up at 24 hours or
more, partial hours up below 24 hours; show `<1h` below one hour. Do not imply
that quota usage determines reset time. Use `YYYY-MM-DD HH:mm UTC` when an exact
cross-timezone time is required; omit dates when they do not affect interpretation.

Footer layout must be verified for each output channel; do not assume identical
glyphs or spacing across clients.
