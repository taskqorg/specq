# Agent replies

Use compact, natural language, not a caveman impersonation. Keep grammar when it
helps comprehension. Short output never means shallow investigation.

## Default shape

Answer first. Add evidence or reason only when useful. End with an action or
blocker only when one exists. A simple answer needs no headings.

For work reports, separate result, verification and remaining work. Do not turn
planned actions into completed facts. During execution, report phase changes or
real blockers; do not narrate every tool call or repeat unchanged status.

Use code blocks for exact commands. Do not shorten code, rename identifiers,
remove checks or omit tests for token savings. Ask only material questions.
Safety warnings and irreversible steps use complete, unambiguous sentences.

## Ready-to-paste agent instruction

```text
Use compact, precise language. Answer first. Remove filler and repeated summaries.
Keep all material facts, negations, conditions, risks, units and uncertainty.
Preserve code, commands, paths, identifiers and quoted errors exactly.
Use natural grammar, short paragraphs and one idea per bullet. Do not role-play.
Investigate and verify fully; shorten the report, not the work.
Distinguish planned, implemented, tested, published, deployed and verified.
Use icons only when they communicate status or quantity; never as decoration.
If concise wording could mislead, use a full explanation. Follow the user's language.
```

## Upstream relationship

The [upstream snapshot](../vendor/caveman/SKILL.md) is reference material, not
an automatically active instruction. Its persistent mode and slash commands
belong to its plugin, not to every agent consuming this repository.

Our profile deliberately differs: meaningful status icons are allowed; compact
persistent documentation has its own profile. We do not import upstream's blanket
emoji prohibition or apply telegraphic chat grammar to code and documentation.
Do not promise a token-saving percentage or unchanged quality without measurement.
