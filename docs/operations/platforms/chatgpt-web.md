# ChatGPT web capability and fallback profile

This profile records concrete platform behavior for a web chat whose sandbox, connectors, network, execution budget, and context are not a persistent repository-native coding environment. Platform-neutral workflow and transaction rules live in [`../WORKFLOW.md`](../WORKFLOW.md) and [`../EXECUTION.md`](../EXECUTION.md).

The machine-readable limitation registry is [`chatgpt-web-limitations.tsv`](chatgpt-web-limitations.tsv). Every reusable newly observed limitation must be added there and reflected here or in [`../TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) in the same accepted repository transition.

## Stop-loss rule

Do one bounded representative probe when capability availability is uncertain. When the result clearly identifies an environmental or tool-contract boundary, stop retrying that path.

```text
probe once
    -> identify the missing capability
    -> preserve exact error and requested object coordinates
    -> choose the registered fallback
    -> continue through the correct authority owner
```

Do not spend a session repeatedly trying mirrors, proxy variants, alternate clone transports, filename variations, or equivalent connector calls unless the active task is specifically diagnosing that platform failure. A failed capability probe does not lower evidence requirements; it changes where the required action occurs.

## Capability matrix

| Surface | Appropriate use | Not authoritative or unavailable |
|---|---|---|
| Session sandbox | materialize an attached full Git bundle locally; inspect and author; local commits; candidate bundles; package construction; shell/static/synthetic tests; selective result review; bounded public HTTP fetch when it actually works | network-backed repository clone/pull/push; Android runtime; Termux deployment; GPU/device validation; user application data; guaranteed DNS or outbound access |
| User Termux | authoritative repository clone/pull/push/commit/`gh`; exact dependency and source acquisition; deployment and local-layout mutation; Android/package/runtime inspection; device tests; `rclone`; future full-bundle creation | delegated broad manual editing or log analysis when the agent can package it |
| GitHub connector | repository metadata; commit confirmation; comparison; PR/issue reads; exact small file reads at a known path/ref | clone; normal object database; complete code-search recall; context-efficient authoring; authoritative commit/push |
| Google Drive connector | primary exchange path for packages, results, patches, bundles, logs, safety artifacts, and evidence; attempt it first for each outbound artifact | automatic equivalence between a Drive reference and sandbox path; guaranteed local-path rewrite on the runtime's first upload |

Docker is not available and must not be used or proposed.

## Required fallback patterns

### Exact bytes blocked by DNS or outbound access

Use limitation `WEB-NET-DNS-001`.

Do not repeatedly retry the same host, invent unverified mirrors, disable digest checks, or change the requested version merely because the sandbox cannot resolve or reach the source.

The agent prepares one user-Termux acquisition/analyzer package containing:

```text
exact URL or repository coordinate;
expected SHA-256 or another accepted identity;
read-only download into scratch space;
archive/package integrity verification;
bounded extraction or analysis commands;
structured status and manifest;
one result .tar.zst;
no installation unless installation is the explicit task.
```

If the agent needs the bytes, the result archive includes the exact verified object. If only facts such as control metadata, members, `DT_NEEDED`, `DT_SONAME`, symbols, or hashes are needed, analyze on Termux and return compact structured evidence instead of transferring a large object.

### Git object graph unavailable through connectors

Use limitation `WEB-GIT-OBJECT-001`.

A GitHub URL or repeated raw-file reads are not a repository transport. Use a user-created full Git bundle, verify it, clone locally, and follow `START_HERE.md`.

If GitHub search misses a known file or slash-containing ref, do not infer absence. Use an exact path/ref read or user-Termux Git and compare exact commit coordinates.

### Device or Android fact required

Use limitation `WEB-DEVICE-001`.

Do not treat a sandbox simulation as Android, loader, package-manager, GPU, filesystem, or runtime evidence. Generate the smallest self-contained Termux runner that collects or executes only the named claim and returns a compact result archive.

### Connector upload boundary

Use `WEB-DRIVE-UPLOAD-001` or `WEB-DRIVE-RUNTIME-FIRST-UPLOAD-001`.

Google Drive is the first and only connector attempt for each outbound artifact. If that one attempt fails for runtime warm-up, local-path rewrite, connector-object, filename, path, or action-contract reasons:

1. preserve the exact bytes and checksum;
2. do not make another connector call in the same delivery;
3. do not retry through another path, filename, ASCII copy, or user-side upload route;
4. expose the identical artifact through one user-visible sandbox link and end the delivery;
5. on the next outbound artifact, attempt Drive first again.

When Drive publication succeeds, provide one `rclone copyto` command that downloads the package to `$HOME/Downloads`. When Drive publication fails, do not add `rclone` as an alternate delivery path in that response.

### Shared filesystem or execution-budget mismatch

Use `WEB-FS-001` or `WEB-TIMEOUT-001`.

`/mnt/data` is an exchange surface and can have different performance or filesystem semantics from local Termux storage. Prefer `/tmp` or another local sandbox filesystem for synthetic transaction simulation, then use Termux as final authority.

When a combined test call is terminated, inspect logs and process state first. Split the already-defined test set into bounded independent calls or use a persistent shell session and polling. Do not rerun the entire expensive sequence blindly.

## Repository input

The normal first input is a full Git bundle created by the user from a clean accepted Termux checkout and attached directly to the chat.

```text
user Termux main
    -> full Git bundle
    -> chat attachment
    -> sandbox local bundle materialization
    -> START_HERE.md
```

A GitHub URL or connector is not a replacement for the bundle. Network-backed repository clone, pull, and push occur only in user Termux. The sandbox may only materialize the attached bundle locally. Raw-text file operations consume model context and do not reproduce object-based Git collaboration.

## Drive-specific constraints

- A local file is upload-eligible only when it is located anywhere under `/mnt/data`; it need not be a direct child.
- After the web-chat runtime is initialized or reset, its first upload attempt can block local-path-to-file-reference rewriting even in an existing chat. Attempt Drive once, expose a user-visible link without another connector/path attempt for that delivery, and attempt Drive first again for the next outbound artifact.
- An upload action may require a connector file-reference object and reject a raw local path even under `/mnt/data`.
- A connector file reference is not automatically a local sandbox path.
- Binary fetches may materialize with a `.bin` suffix; trust byte identity and checksum, not the suffix.
- Prefer exact folder listing and file IDs over fuzzy binary filename search.
- Verify size, SHA-256, zstd integrity, safe members, and internal manifest after upload or fetch.
- When valid bytes are rejected because of connector, path, or filename handling, make no alternate-path or alternate-name retry in the same delivery; expose the identical user-visible artifact and retry Drive first only for the next outbound artifact.

## Context and continuity

The platform does not automatically read repository files, preserve a working tree between sessions, or guarantee a graceful session close. Therefore:

- current state is committed at accepted transition time;
- default onboarding remains bounded by `START_HERE.md`;
- historical documents are not loaded by default;
- uncommitted sandbox work is disposable unless a checkpoint is explicitly justified;
- the first response after clone is the onboarding receipt, not an ungrounded local plan.
