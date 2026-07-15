# ChatGPT web capability profile

This profile records concrete platform behavior for a web chat whose sandbox, connectors, and context are not a persistent repository-native coding environment. Platform-neutral workflow and transaction rules live in [`../WORKFLOW.md`](../WORKFLOW.md) and [`../EXECUTION.md`](../EXECUTION.md).

## Capability matrix

| Surface | Appropriate use | Not authoritative or unavailable |
|---|---|---|
| Session sandbox | clone supplied bundle; inspect and author; local commits; candidate bundles; package construction; shell/static/synthetic tests; selective result review | Android runtime; Termux deployment; GPU/device validation; user application data; remote Git mutation |
| User Termux | authoritative fetch/commit/push/`gh`; deployment and local-layout mutation; Android/package/runtime inspection; device tests; `rclone`; future full-bundle creation | delegated broad manual editing or log analysis when the agent can package it |
| GitHub connector | repository metadata; commit confirmation; comparison; PR/issue reads; small targeted read-only lookup | clone; normal object database; bulk reconstruction; context-efficient authoring; authoritative commit/push |
| Google Drive connector | exchange of packages, results, patches, bundles, logs, safety artifacts, and evidence | automatic equivalence between a Drive reference and sandbox path |

Docker is not available and must not be used or proposed.

## Repository input

The normal first input is a full Git bundle created by the user from a clean accepted Termux checkout and attached directly to the chat.

```text
user Termux main
    -> full Git bundle
    -> chat attachment
    -> sandbox clone
    -> START_HERE.md
```

A GitHub URL or connector is not a replacement for the bundle. Raw-text file operations consume model context and do not reproduce object-based Git collaboration.

## Drive-specific constraints

- A local file is upload-eligible only when it is located anywhere under `/mnt/data`; it need not be a direct child.
- In a new chat, local-path rewriting can be blocked on the first assistant turn. Do not repeat the same failing upload in that turn.
- A connector file reference is not automatically a local sandbox path.
- Binary fetches may materialize with a `.bin` suffix; trust byte identity and checksum, not the suffix.
- Prefer exact folder listing and file IDs over fuzzy binary filename search.
- Verify size, SHA-256, zstd integrity, safe members, and internal manifest after upload or fetch.
- When valid bytes are rejected because of path handling, copy the identical bytes to a short ASCII path under `/mnt/data`, publish with the intended name, and verify readback. Do not transform the artifact.

## Context and continuity

The platform does not automatically read repository files, preserve a working tree between sessions, or guarantee a graceful session close. Therefore:

- current state is committed at accepted transition time;
- default onboarding remains bounded by `START_HERE.md`;
- historical documents are not loaded by default;
- uncommitted sandbox work is disposable unless a checkpoint is explicitly justified;
- the first response after clone is the onboarding receipt, not an ungrounded local plan.
