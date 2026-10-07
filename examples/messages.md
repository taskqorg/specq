# Examples

All values below are illustrative, not current measurements or captured
production deliveries.

## Notification patterns

```text
👁️ ⚠️ 🖥️ host disk nearly full · remaining 12.3% (49.3 GiB) · Details
👁️ 🛑 🗄️ Database metrics unavailable · Details
👁️ ♻️ 🖥️ Alert cleared: HTTP 5xx rate · Details
🚚 ✅ 🏁 example.app · sha: <commit link> · pipeline: <pipeline link>
🚚 🛑 🏁 example.app halted: build failed, production unchanged · pipeline: <link>
```

The compact deploy examples omit optional commit/author detail. Real links must
be clickable, correctly escaped and point to the relevant incident or release.

## Footer pattern

```text
model · 🙂 12% · 🌕 96% ↻ 2h
model · 😕 74% · 🌗 48% ↻ 6d
model · 🥵 93% · 🌑 8% ↻ <1h
model · 😐 55% · ? unavailable
```

Context is used capacity; quota is remaining capacity. Reset is independent.
See [Indicators](../rules/indicators.md) for exact thresholds and rounding.

## Agent rewrite

Before: “Sure, I have successfully completed the implementation and would like
 to let you know that everything should now be working as expected.”

After: “Fix implemented. Regression test passed. Not deployed.”

## Progress with honest uncertainty

```text
Copy complete. Checksum verification running; percentage unavailable.
Old data retained. Sites remain online.
```

Not: “Almost done” without evidence, or “Healthy” because a process exists.

## Documentation rewrite

Before: “It is important to note that before proceeding with this operation,
 you should make sure that you have a backup available.”

After: “Verify a restorable backup before migration. Stop if verification fails.”
