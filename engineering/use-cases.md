# Use-case specifications

Scenarios verify requirements before interface or implementation choices. This page defines the method; product scenarios live in the product repository.

- Assign stable IDs. Record source and status: observed need, owner requirement, proposal or approved behavior.
- State relevant initial conditions, intent, actions, observable result, exceptions and open decisions.
- Separate requirements, illustrative examples, preferences and unresolved questions in free-form input. Each material request gets a specification home or an explicit deferral. Examples do not constrain the solution by themselves.
- Keep user intent separate from a proposed interface and from implemented capability.
- Define ambiguous domain terms once in the owning contract or linked domain reference and use the same meanings in scenarios, code and interfaces. Distinguish terms with different behavior; name misleading synonyms. Add a separate glossary only when the definitions outgrow the contract.
- Preserve counts, scope, hosts and constraints when they affect meaning. Exclude secrets and private paths.
- Link applicable contracts. Record conflicts as decisions to resolve; scenarios do not silently amend runtime rules.
- Map capabilities to primary cases. Reuse cases for overlapping flows; make provider/platform variations separate only when behavior differs.
- Check cancellation, ambiguity, empty results, unavailable dependencies, stale state, partial success, retry and preservation of active work where applicable.
- State coverage honestly: a finite set covers the stated requirements, not every possible scenario.

Review the scenario set with the owner, update affected product requirements, then validate the interface and implementation against it.
