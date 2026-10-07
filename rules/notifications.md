# Notifications

**One event. One clear status. One useful line when possible.**

## Grammar

```text
<source-icon> <status-icon> <target-icon> <target> <state> · <essential context> · <details link>
```

Use the [shared catalog](indicators.md). Existing Cyprus senders use all three
roles; new compact senders may omit redundant source or target icons. Do not
introduce decorative emoji runs. Keep status understandable as text.

## Content

- Name the affected system and actual state. Include remaining capacity for disk warnings.
- Include impact or action if needed to interpret the event safely.
- Link logs and diagnostics rather than dumping them into chat.
- No greeting, unsubscribe instructions, job IDs, routine dates or repeated footer
  unless necessary for routing, compliance or action.
- Deduplicate by incident; send meaningful transitions, not repeated noise.
- Recovery requires a recovery check. An alert clearing proves only that its
  condition cleared; say `Alert cleared` when that is all you know.
- A monitoring failure is not a confirmed application outage.
- Keep secrets, personal data and raw request bodies out of notifications.

## Established Grafana profile

One line per alert: source/status/target, condition, optional environment and
`Details` link. Technical thresholds, durations and diagnostic explanations live
in annotations. Render mixed firing and cleared alerts separately.
This is a specific operational profile, not a ban on essential safety context
in other notification types.

## Telegram and scheduled jobs

Use explicit HTML parse mode where the sender supports it; escape all dynamic
text and link attributes. Other channels use their native supported formatting.

Hermes `cron.wrap_response: false` removes the standard cron header, job ID and
management footer. It does not shorten the task's own content or every runtime
message. Task prompts and deterministic scripts must format their own concise
results. Do not hide actionable failures in the name of quiet output.
