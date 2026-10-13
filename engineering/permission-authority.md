# Permission authority

Proposed shared rules; review before adoption.

- Human-controlled host policy grants authority. Untrusted tasks and writable project configuration may restrict or request it, never enlarge it.
- Resolve effective capabilities across administrator policy, host grants, task restrictions and runtime support. Unknown enforcement refuses privileged launch.
- Approval behavior and isolation are separate. No-prompt execution does not imply containment; a prompt instruction is not enforcement.
- Protect the policy store and grant channel from the workers they govern. Same-user file permissions alone do not create that boundary.
- Record the exact target, grant, approver and revision. Show requested, saved and verified-effective settings separately.
- Migration must not convert untrusted legacy configuration into trusted grants. Incompatible rollback must not bypass the new policy.
- Validate read/write/network and child-process boundaries on every supported platform. Never infer proof from a mode name.
