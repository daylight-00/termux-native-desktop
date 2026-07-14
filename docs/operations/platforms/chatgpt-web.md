# ChatGPT web session profile

This profile defines how the project operates in a web chat whose sandbox, connectors, and context do not behave like a persistent repository-native coding agent.

## Session repository input

The normal first input is a full Git bundle created by the user from the authoritative Termux checkout.

```text
user Termux repository
    -> full Git bundle
    -> direct chat attachment
    -> sandbox clone
    -> repository START_HERE.md
```

The bundle should represent a clean accepted repository boundary. The agent verifies it, clones it with ordinary Git, checks out `main`, records `HEAD` and tree, then follows the repository initialization documents.

A GitHub repository URL or connector is not a replacement for the bundle.

## GitHub connector boundary

The connector is suitable for:

- repository metadata;
- remote commit confirmation;
- branch comparison;
- pull requests and issues;
- small targeted file reads when a local bundle is unavailable for read-only inspection.

It is not suitable for:

- cloning the repository;
- obtaining a normal Git object database and working tree;
- large repository reconstruction;
- context-efficient bulk authoring;
- authoritative commit, branch, or push workflows.

The connector's raw-text file operations can consume substantial model context and do not reproduce ordinary object-based Git collaboration. Do not use them to simulate a clone.

## Sandbox boundary

The session sandbox is appropriate for:

- cloning the supplied bundle;
- repository inspection and authoring;
- local commits and candidate bundles;
- patch and runner construction;
- shell/static/synthetic tests;
- selective result-archive analysis.

It is not authoritative for:

- Android package or runtime behavior;
- Termux deployment state;
- GPU/device validation;
- the user's remote Git mutation;
- user application data or live payload state.

Docker is not available and must not be introduced into project plans.

## User Termux authority

The user's Android Termux environment owns:

```text
authoritative repository fetch / commit / push / gh
live deployment and local-layout mutation
Android package and runtime inspection
GPU and application tests
rclone exchange
full bundle creation for a future web session
```

The agent should reduce device work to one bounded wrapper whenever possible.

## Google Drive exchange

Drive is the bidirectional exchange channel for runner packages, patches, bundles, results, safety artifacts, logs, and evidence.

Operational constraints:

- Local files are upload-eligible only when located anywhere under `/mnt/data`.
- In a new chat, local-path upload rewriting may be blocked on the first assistant turn. Do not repeat the same failing upload in that turn.
- A Drive file reference is not automatically a sandbox path.
- Binary fetches may materialize with a `.bin` suffix; trust byte identity and checksum, not the local suffix.
- After upload or fetch, verify size, SHA-256, zstd integrity, member safety, and the internal manifest when present.
- Prefer exact folder listing and file IDs over fuzzy binary filename search.

## Session continuity

There is no narrative handoff requirement.

Accepted state must be committed to canonical repository documents during the accepted transition. A new session starts from a new full bundle and reads current state from the repository.

Uncommitted sandbox work is not durable. Preserve it only when explicitly necessary by producing a patch or checkpoint ref; otherwise restart from the latest accepted bundle.

## Onboarding behavior

A new session must not immediately propose a local technical plan. It first produces the onboarding receipt required by `START_HERE.md`, including the tool and authority boundary.

When the repository current state is internally inconsistent, the first task is to report the inconsistency and follow the explicit active-task stop conditions. Do not choose an old handoff or historical record as current truth by convenience.
