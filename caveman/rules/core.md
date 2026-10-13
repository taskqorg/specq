# Core

**Compress wording, not thought or evidence.**

## Priority

1. Safety, correctness, permissions and explicit user requirements.
2. Facts, uncertainty, conditions, sequence and exact technical payload.
3. Readability and accessible structure.
4. Brevity and visual consistency.

A specific profile refines these rules; it cannot weaken them.

## Write

- Lead with the answer, outcome or current state.
- One idea per sentence or bullet. Prefer active voice and concrete verbs.
- Remove greetings, filler, repeated summaries and offers to help.
- Keep negations, exceptions, prerequisites, units and consequences.
- Preserve commands, paths, identifiers, quoted errors and values verbatim.
- Keep source text separate from its output syntax; encode dynamic values once at the final sink.
- For commit, merge-request and release communication, follow [Change communication](changes.md).
- Distinguish observed facts, estimates, hypotheses and unknowns.
- Separate implemented, tested, published, deployed and verified.
- Say what failed and what it affects. Do not present a guessed cause as fact.
- Keep numbers when they add evidence; omit unrelated timestamps and IDs.
- Expand when compression makes two interpretations possible.

## Make scanning easy

Use short descriptive headings, whitespace and parallel bullets. Put the main
point first. Avoid dense paragraphs, deep nesting and unnecessary tables.
Design for readers with limited attention, including ADHD readers; do not claim
one layout works for every person or guarantees accessibility.

Icons encode information, not mood or decoration. Never rely on color alone.
Use the [indicator catalog](indicators.md); retain a textual status or exact value.

## Review

- Can the reader identify the result and required action immediately?
- Did every important condition, risk and uncertainty survive shortening?
- Are technical tokens unchanged and claims backed by evidence?
- Does each icon add meaning rather than repeat nearby decoration?
- Does the message remain clear without color, emoji rendering or prior context?
- Is this the shortest clear version, rather than the shortest possible version?
