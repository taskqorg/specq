# Request counter interval coverage

A committed request summary proves its observed incremental counts. It does not prove a complete service interval from a first timestamp, current collector health or missing records. Old summaries remain valid with coverage unknown.

## Typed descriptor

The optional `request_coverage` object belongs only to `product: taskq`, `kind: requests`, `operation: requests.summary`, `source: service` in the existing `coreq-observation/1` record. No other context admits it. Version 1 has exactly these keys:

| Key | Type and meaning |
| --- | --- |
| `version` | Integer 1. Other versions are refused. |
| `epoch` | 32 lowercase hex characters: an opaque counter epoch bound to the original service lifecycle receipt, not a PID alone. |
| `sequence` | Positive u64, contiguous within that epoch. |
| `start_ms`, `end_ms` | Unsigned UTC milliseconds no larger than i64::MAX, with end >= start. Unknown boundaries may be null only when state is unknown. |
| `state` | `valid` or `unknown`; valid requires both times and reason none. |
| `reason` | `none` for valid; otherwise `counter-poisoned`, `clock-regressed`, `identity-unknown` or `reset-unknown`. |

Unknown keys, wrong types, invalid identities, reversed times and unknown versions are refused. These fixed codes, quantities and opaque identities carry no content, credentials, paths or control authority. They are not a generic nested payload exception.

## Original identity and completion

The immutable logical batch identity uses the existing identified Event seam with namespace `taskq.requests` and key `<epoch>.<sequence>`. Multipart records retain that logical identity through the existing count-summary group and part identities; every part must have identical coverage metadata. No second batch identity, transport, metric or store is added.

The producer initializes the epoch boundary before counting requests and serializes interval cuts, counts and sequence in one state lock. Admission refusal retains the same pending batch and its boundary; once enqueued, its identity and contents cannot change. Enqueue is not commit. Only retained committed records with matching original lifecycle identity, adjacent sequences and equal previous-end/next-start boundaries can establish their exact measured interval. Missing parts, loss, pruning, poison, reset, unknown boundaries or an unknown final tail keep completeness unknown. Current health cannot repair an earlier gap. Descriptor shape validation alone proves none of these runtime facts.

A service emits a positive empty summary at its actual interval boundary through the same path. This changes service empty suppression; it does not infer zero from silence. CLI positive-empty behavior, incremental counts and observed-only legacy reports stay unchanged. A late 304 across a legacy summary boundary remains an estimated billed count unless independently bound final-response evidence establishes otherwise.

## Compatible rollout

Shared schema acceptance precedes CoreQ qualification and canonical source release. The sink then adopts that actual compatible release and applies the same public typed validator before admission; it must preserve the exact descriptor in storage, forwarding, replay and multipart assembly. A temporary object-free validation view may feed the existing generic metadata check; the stored record must not lose the descriptor.

Producer emission comes last, after the sink's required source checks, canonical delivery and actual compatibility qualification. Old CoreQ refuses this field. An older sink may admit its shape through generic metadata validation without enforcing its semantics; that is not safe typed compatibility. Existing stored descriptors must be validated at any read path before coverage is trusted. Records without the object remain readable with unknown coverage. Existing grants, enrollment schemas, permissions and deployment authority are unchanged; a source change does not authorize access or rollout.
