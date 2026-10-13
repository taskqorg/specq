# Specification-led product design

Entry point for collaborative product and interface work. Adopt this workflow and its linked rules; keep product decisions in the consuming project. Resume from recorded decisions, not from a fresh redesign.

## Working agreement

- Start with the user's outcome and current product. Inspect the applicable contract, approved references and actual implementation before proposing replacements.
- Read [spec first](../engineering/spec-first.md), [use cases](../engineering/use-cases.md) and [documentation style](../caveman/rules/documentation.md). Interface work also applies [dense operator design](operator-ui.md) and [implementation fidelity](implementation-fidelity.md).
- Persistent specifications, interface copy and handoffs use concise English. Conversation follows the user's language. Remove words that add no meaning; preserve constraints, exceptions and evidence.
- The agent resolves routine engineering details within approved constraints. Escalate API, synchronization or format choices only when they change product behavior, authority, cost or risk.
- The owner chooses product direction. The agent investigates, recommends, records decisions and completes authorized work. Ask only for unresolved choices that materially change behavior, design or risk.
- Accepted choices persist. Do not ask again, reintroduce rejected alternatives or treat a mock as approval of its incidental behavior.

## One home per rule

| Content | Canonical home |
|---|---|
| Reusable design, writing, workflow or verification principle | Applicable shared specification |
| Product entities, state meanings, operations and authority | Project root contract and linked specifications |
| Dimensions, assets, platform policies and acceptance fixtures | Project design package |
| Scenarios and product-specific exceptions | Project use cases / contract |
| Observations, screenshots and test results | Revision-specific evidence |

Project documents link shared rules. Do not copy their prose. Shared rules contain no consumer names, paths, catalogs or product-specific thresholds.
A correction that reveals a reusable principle follows [improve shared rules](../engineering/spec-first.md#improve-shared-rules). A local shared edit does not prove publication, consumer adoption or deployment.

Dashboard and widget work also follows [W1–W15](dashboards.md): first-screen priorities, bars, trends, automatic refresh and legible changes.

## Iteration loop

Use the next incomplete step. Scale the work to the change; a small correction need not repeat discovery.

1. **Establish the baseline.** Identify current source/release, accepted decisions, existing capabilities and evidence gaps. Distinguish observed behavior from user reports and design targets.
2. **Describe use cases.** Capture intent, context, action, expected outcome, failure/recovery and operator decisions. Merge duplicates only when no meaningful scenario disappears.
3. **Design behavior.** Map scenarios to navigation, information priority, controls, states and permissions. Include empty, waiting, unknown, failure, long-content and recovery cases. Identify backend gaps explicitly.
4. **Compare useful alternatives.** Use the same scenario and data. State the user-visible difference and cost; recommend one. If the distinction cannot be explained briefly, refine the alternatives before asking for selection. Vary the disputed decision, preserving accepted parts. Offer a different approach only when it tests a real trade-off.
5. **Record the choice.** Update canonical requirements before the next implementation/prototype revision. Mark proposals separately. Approval of structure does not automatically approve styling or unresolved policies.
6. **Refine a representative view.** Prove density, readable type, alignment and direct actions at actual size. Then apply the chosen rules across all affected levels and states.
7. **Complete the design package.** Connect use cases, requirements, references, assets, fixtures and acceptance checks. Preserve existing functions or record approved removals. Resolve required choices before dependent implementation.
8. **Implement and review.** Follow [F1–F6](implementation-fidelity.md). Compare actual product behavior and pixels with the approved reference; fix shared causes, preserve useful improvements and recheck affected scenarios.

Before closing an iteration, trace material requests through existing decision IDs, specifications, references, implementation and evidence. Report missing links and unresolved decisions; do not create a duplicate ledger or claim unimplemented links are complete.

After each iteration report: changed decision, canonical location, evidence and next unresolved choice. Keep updates short; do not narrate routine tooling.

## Operator design default

Use [D1–D14](operator-ui.md) as the preference profile: readable density, large adjustable type, stable alignment, direct actions, restrained semantic color and attention-first information.

- Optimize useful information per area before styling. Extra gaps, repeated labels and decorative blocks must earn their space.
- Keep frequent actions and consequential states close; preserve stable controls. Adapt content without moving targets unexpectedly.
- Review the complete route: list, detail, action, result, error and return. A polished home screen cannot compensate for unusable deeper views.
- Prefer compact groups and content-fit surfaces. Check long text, large values, large fonts and constrained screens before accepting a layout.
- Product-specific exceptions require a reason and owner decision. Do not silently substitute a spacious dashboard or shrink text to simulate density.

## Process every correction

1. Identify the mismatch: behavior, information hierarchy, visual rule, implementation defect or missing evidence.
2. Route it to the shared rule, product specification, implementation or evidence. Update both shared and product sources only when both decisions change.
3. Preserve unaffected approvals. Once an option is chosen, explore variants within it; stop showing discarded branches unless the owner reopens the decision.
4. Update affected references and acceptance criteria. Add a focused fixture when it prevents recurrence; do not encode defects as new expected output.
5. Recheck the original use case and adjacent affected states. Report remaining gaps explicitly.

Do not turn every bug into policy. Existing-rule violations need fixes; repeated ambiguity may need a clearer rule. Useful implementation deviations need review before becoming the new reference.

## Handoff and acceptance

Keep one project package index linking:

- Contract and shared rules; accepted decisions and unresolved proposals.
- Use cases and requirement-to-scenario coverage.
- Current implementation inventory, required backend work and preservation/removal decisions.
- Editable reference, generated preview, licensed assets and rendering constraints.
- Deterministic fixtures, acceptance ledger, review report and artifact revisions.

The implementer can proceed without the chat transcript. Required unresolved decisions have options and an owner; placeholders remain gaps.
Builder supplies evidence; reviewer checks and polishes; owner decides design changes. These are responsibilities, not a requirement to spawn separate agents.
Report design accepted, implementation verified, published and deployed separately. Unchecked platforms remain Not tested. Follow the project's required gates and the shared [verification rules](../engineering/verification.md).

## End-to-end simplicity

Compare the actions, concepts and manual setup required to complete the scenario. Reuse existing capabilities before adding a mechanism. Competitor research identifies the user need first; importing a competitor's architecture requires its own justification. Preserve required alternatives without burdening the default route.

## AI-assisted controls

- Prefer the simplest composition that covers the scenario. Ship recommended flows as visible, editable defaults; expose useful alternatives on demand. Preserve explicit overrides when defaults evolve, and review any broader effects before applying them.

- For AI-enabled tools, accept intent in ordinary language. Let AI propose a short, inspectable plan; expose only unresolved decisions and useful overrides.
- Agents interpret, decompose and explain. The execution service enforces identity, confirmed effects, dependencies, capacity and receipts; a model's prose is not execution proof.
- Put an explained question and its choices at the work item. A normal choice submits the displayed answer directly; consequential effects retain their explicit review.
- Preserve choice identifiers across interfaces. Show the same source numbers, order, meaning and recommendation in buttons, text and receipts; presentation never changes answer identity.

Accepted refinement coverage: [workflow review](workflow-review.md). The linked owner sections below define the rules.
