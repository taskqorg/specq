# Review and learning

How a reviewer judges a frozen result, and how work learns from friction. [Agent workflow](agent-workflow.md) owns the work cycle that calls these steps.

## Review

- Report task fit and implementation quality separately: missing, incorrect or unrequested behavior versus standards violations and maintenance risks. Neither substitutes for the other.
- Distinguish binding violations from judgement calls. A code smell alone is not a rejection; follow the project's acceptance rules. Tool-enforced rules need no duplicate manual checklist.
- Read the owner's original text that the task quotes or links, not only the spec. Reject a change that narrows it, in the spec, the code or a simplification marker ([keep the owner's request](spec-first.md#keep-the-owners-request)). A spec change made for an owner request without that quote or link is a task-fit gap.
- Reject an unapproved change to decided behavior or its protection ([decided rules](agent-workflow.md#decided-rules)). For duplicate-check removal, review the named retained detection; do not require another copy of the check.
- An experiment task without a verdict, recommendation and proposed next tasks is a task-fit gap ([experiment tasks](task-planning.md#experiment-tasks)).
- Diff size alone is never a finding; review does not ask to split a coherent outcome ([prepare the task](task-planning.md#prepare-the-task)).
- Report every gap in one pass over the whole result. A later round checks only the requested fixes and their direct effects; a new finding on unchanged lines is a separate task or note, not a rejection.
- Two axes do not require two agents. Keep safety, compatibility and architectural constraints available to the implementer; load detailed review guidance when needed.

## Learn from friction

After repeated rework, prolonged diagnosis or a material owner correction, inspect the attempt evidence: time lost or error, cause, smallest remedy and how to verify it. Skip routine work; record it in the task or result, not a report file or completion gate.

- Before adding a check or navigation pointer, look for an existing one that is missing, disconnected or broken.
- Prefer a deterministic check for a mechanically detectable mistake; reserve prose for judgement and decisions. Inspect tool cost and missing information when they caused the friction.
- Propose only evidence-backed improvements, most consequential first. Fixes within the authorized task proceed normally; changes to shared decisions follow [spec first](spec-first.md#improve-shared-rules). Do not auto-apply speculative findings or expand access.
- A remedy that changes how work is done lives in the owning specification or a check, never only in agent memory. Agent memory keeps private and host facts and a pointer to the rule.
