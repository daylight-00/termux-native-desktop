# Project principles

> **Lifecycle:** historical evidence-policy provenance. Current engineering and assurance principles are canonical in [`constitution/PRINCIPLES.md`](constitution/PRINCIPLES.md) and accepted ADRs.

This project is not merely an attempt to make a Linux desktop application launch on Android. It builds an evidence-backed architecture for a conventional Linux/glibc application world hosted beside Termux/Android, with explicit ownership, lifecycle and promotion boundaries.

## What counts as progress

Progress moves through distinct states:

```text
observation
    -> candidate
    -> verified identity and provenance binding
    -> accepted provider authority
    -> composition decision
    -> target population
```

A later state must never be inferred from an earlier one. A package, release, workflow, artifact digest, file presence or successful launch can be useful evidence, but none of those alone establishes producing-build provenance, provider authority or target membership.

## Exact identity over similarity

The project uses exact identities whenever authority is at stake:

```text
repository and recipe tree;
package and artifact digest;
member path and ELF SONAME;
producing-build invocation, environment and output manifest;
request, response and receipt coordinates;
target population row.
```

Family resemblance, version proximity, filename aliases and repository metadata are not substitutes for the required binding.

## Bounded phases

Each transaction has one declared purpose. A review must not silently acquire evidence. A collector must not promote authority. A request definition must not pretend that a request was issued. Response receipt must not become evidence acceptance. Provider acceptance must not silently populate the runtime target.

Unknown and absent states are recorded explicitly. Fail-closed behavior is preferred to a plausible but unsupported conclusion.

## Reproducibility and authority

Every accepted transition should be recoverable from exact Git and receipt coordinates:

```text
branch + commit + tree
result archive SHA-256
structured transaction state
canonical generation or replay metadata
claim boundary and next state
```

Tree hashes are the cross-session content invariant. Receipts and numbered project records remain evidence; handoffs only point to the active boundary.

## Human and agent relationship

The user supplies the minimum environment-specific action. The agent performs authoring, validation, packaging and evidence review. This division reduces transcription errors and keeps every mutation inside one guarded, reproducible transaction. The durable mechanics are defined under [`session-operations/`](session-operations/README.md).

## Reading precedence

When documents differ, use this order:

```text
current controlling intervention or numbered refactor record;
verified result receipt and exact Git state;
STATUS.md current working conclusion;
integrated architecture documents;
current dated handoff;
historical handoffs and exploratory notes.
```

A handoff never overrides project evidence. It identifies what to read and what remains unverified.
