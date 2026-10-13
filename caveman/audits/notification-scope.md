# Notification adoption scope

**Status: planning reference; no integration or deployment claim.**

This document defines a bounded review scope for adopting the Caveman
communication standard. It does not inventory private repositories, hosts,
senders, credentials, schedules or delivery paths. It is not evidence that a
sender is enabled, changed, tested, or deployed.

## In scope for a named integration

Review one sender at a time with its owner:

- the sender's audience and event types;
- the stored text format and final output syntax;
- dynamic-value escaping at the output sink;
- authorization, delivery acknowledgement and release checks;
- rendered output for success, failure and recovery states.

## Out of scope

Do not infer adoption from this public library. The following require separate,
owner-approved work in the affected project or environment:

- changing a sender, job, plugin, gateway or message configuration;
- publishing private operational paths, inventories or delivery metadata;
- treating a successful pipeline as proof of deployment or delivery;
- applying operational-release grammar to user-facing product notifications
  without a review of their distinct requirements.

## Next use

Apply [Change communication](../rules/changes.md) at a named sender only after
its owner confirms scope, sink syntax and release path. Preserve each sender's
existing authorization, delivery acknowledgement and deployment gates.
