# Use-case specifications

Use scenarios to verify requirements before committing to interface or implementation choices.
Product scenarios belong in the product repository; this file defines the method.

- Assign stable IDs. Record source and status: observed need, owner requirement, proposal or approved behavior.
- State relevant initial conditions, intent, actions, observable result, exceptions and open decisions.
- Separate requirements, illustrative examples, preferences and unresolved questions in free-form input. Give each material request a specification home or an explicit deferral. Examples do not automatically constrain the solution.
- Keep user intent separate from a proposed interface and from implemented capability.
- Preserve counts, scope, hosts and constraints when they affect meaning. Exclude secrets and private paths.
- Link applicable contracts. Record conflicts as decisions to resolve; scenarios do not silently amend runtime rules.
- Map capabilities to primary cases. Reuse cases for overlapping flows; make provider/platform variations separate only when behavior differs.
- Check cancellation, ambiguity, empty results, unavailable dependencies, stale state, partial success, retry and preservation of active work where applicable.
- Describe coverage honestly; a finite set covers the stated requirements, not every possible scenario.

Review the scenario set with the owner, update affected product requirements, then validate the interface and implementation against it.
