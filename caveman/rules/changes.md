# Change communication

**State the change and its user impact without hiding release facts.**

This profile covers commit subjects, merge-request descriptions and release or
deploy messages. Follow the project's required commit convention, tracker
references and release process. Do not rewrite published history to improve old
wording. Merge-request and release text: [merge and release](merge-and-release.md).

## Keep the source and sink separate

A commit subject is plain text. Store literal UTF-8 text, not Markdown, HTML,
JSON escapes or Telegram entities. Do not pre-escape a subject for a future
notification.

An MR body is Markdown. Use Markdown only where it improves scanning. A Telegram
message is rendered HTML when that sender uses Telegram HTML parse mode. Format
for the sink once, at the final output boundary:

- Keep source strings literal and preserve them verbatim in diagnostics.
- Escape dynamic text and link attributes once for Telegram HTML. Keep an
  apostrophe literal or use the numeric `&#39;`; never use a named apostrophe entity.
- Serialize the final API payload with a JSON serializer. JSON serialization is
  separate from HTML escaping and is not a second text transformation.
- Do not decode, trim, normalize or truncate a diagnostic string in a way that
  changes its meaning. Do not impose an arbitrary subject limit that removes
  essential meaning.

## Write the right artifact

### Commit subject: plain text

Prefer a short, meaningful subject that says what changed and why it matters.
Keep a project-required Conventional Commit prefix when applicable. Use a body
for material tests, limitations, migration notes or non-obvious context.

Before and after (invented):

```text
fix: fix issue
fix(events): prevent localized village page crashes
```

Avoid vague subjects such as `fix bug`, `updates`, `merge main`, or a raw merge
branch subject. The default merge branch subject records Git history; it is not
a human change description.

### Merge-request description: Markdown

See [merge and release](merge-and-release.md#merge-request-description-markdown).

### Deploy message: rendered Telegram HTML

See [merge and release](merge-and-release.md#deploy-message-rendered-telegram-html).

## Release check

See [merge and release](merge-and-release.md#release-check).
