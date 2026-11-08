# AgentQ runtime release adoption

This note applies to TaskQ, PilotQ, Pipe/AssetQ and every product using AgentQ. It implements the consumer adoption requirement; it does not declare native acceptance complete.

## Adopt a release

1. Resolve the canonical immutable runtime tag to its exact source commit. Update the manifest and lock together; retain a coherent CoreQ resolution. Follow the [shared implementation release rules](release-contract.md#shared-implementations), including signed or qualified identity exceptions. Never retarget an existing tag.
2. Read the release delta and migrate deprecated calls through the [runtime trait](agent-runtimes.md), including typed history and events. Remove product-native parsing only when the replacement preserves the original behavior and failing-before checks. Runtime names and native transport details remain inside AgentQ.
3. Run meaningful affected product checks on the exact candidate and supported platforms. Record the resolved source, caller path and checks; producer doubles do not qualify a product caller.
4. Under the existing host, account, model and operation authority, qualify real product-host start, same-session resume and cancel. If restart/recovery is an original criterion, also verify that actual caller path and retained ownership. Bind receipts to product/runtime/client versions, host, selected profile, opaque session and original process/scope identity. Do not publish credentials or raw private transcripts.
5. Distinguish original-process exit, whole-scope absence, native turn completion and unknown numeric exit. An acknowledgment, healthy service, native CLI used outside the product or another host's receipt proves none of the missing product lifecycle steps. Preserve authority, no replay and unknown-cleanup fences.
6. Publish through the product's canonical release path only under release authority. Preserve previous-version rollback and immutable identities. Record installed adoption separately from native worker qualification.

## Current compatibility baseline

The accepted baseline is `runtime-v0.16.0`, source `540f017124e096015b23237416bc580f8e1b1c49`. Its existing compatibility pins remain immutable. The shared [calendar format](release-contract.md#calendar-product-release-identity) governs each product's next real release.

For this baseline, native approval/steer, login/home isolation, platform parity and consumer lifecycle criteria require their own exact receipts. Historical owner-SKIPPED observations remain SKIPPED, not PASS. This note supplies adoption instructions, not those missing receipts or new account, model, grant, board or deployment authority.
