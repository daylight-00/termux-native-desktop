# Selected-provider materializer/runtime-preflight design boundary acceptance

## Decision

```text
acceptance id: SELECTED-PROVIDER-MATERIALIZER-DESIGN-ACCEPT-001
decision: ACCEPTED_BOUNDED_NON_EXECUTING_READ_ONLY_MATERIALIZER_RUNTIME_PREFLIGHT_DESIGN
candidate: SELECTED-PROVIDER-MATERIALIZER-DESIGN-REVIEW-001
execution authorized: NO
local supply map produced: NO
target population authorized: NO
```

The exact v112 non-executing design candidate is accepted as a bounded Class D design authority record. Acceptance covers the immutable design algorithms, ordering, validation and recovery contracts only. It does not authorize implementation or any provider or filesystem byte effect.

## Frozen candidate

The acceptance freezes all nine generated candidate artifacts by SHA-256:

```text
selected-target-materializer-runtime-preflight-design.json
323d834e58397364561a4b89f4b344a9633e4f3c472728e75e5b620017db44be
selected-target-materializer-design-metadata.tsv
dac9fe85533f73fab95eca51db85cf4148e0e94a9e2767ad852e5b174b99fc72
selected-target-materializer-input-contract.tsv
70feee05112fee4f0f98dfa6132a10550a87e11ac6569a86e258a47f5e7b94c4
selected-target-materializer-object-plan.tsv
759102d4a209a39119b7bd5a92f1995993e7c302149b11f174d11cd0dd08b0f7
selected-target-materializer-state-machine.tsv
8d9e97c43d5bee1db3cd0632e1fe3be2a7d69fa5e2f9b2e9327ddced7d4b0408
selected-target-materializer-operation-contract.tsv
76f2f779ee9aea8eb01bcb3f0a3d2d8fdd44fe7f63680ee2ce95f2ae795be755
selected-target-runtime-preflight-contract.tsv
2a68a1543b058b035387b86eb4dd1c5e3e7e6cdedc18af2c5fe146f45f3fd14d
selected-target-materializer-verification-contract.tsv
0d3c354fdaf395985569e6f203625b49dbd2256491f118d5717eeaa901b3cb0e
selected-target-materializer-publication-recovery-contract.tsv
786a036d23b90b61d43965bcd6ced36caffadcd1563c6d02cd25078e5d012304
```

Historical candidate metadata remains `QUALIFIED_NON_EXECUTING_READ_ONLY_DESIGN_CANDIDATE` with its acceptance gate open. This acceptance is recorded separately and does not rewrite the candidate-time artifact.

## Accepted structural boundary

```text
canonical inputs: 13
object-plan rows: 41
state-machine rows: 20
ordered operations: 24
runtime-preflight checks: 20
publication-blocking verification checks: 18
publication/recovery contracts: 11
target-policy rows: 82
regular objects / aliases: 41 / 41
atomic families: 4
exact member bytes: 29,047,112
receipt reservation: 1,048,576
runtime free-space preflight: 59,142,800
```

Accepted invariants include content-addressed object identity, hardlink-only reuse with no copy fallback, regular-before-alias ordering, complete atomic-family barriers, a separate execution-authorization gate before mutation, canonical receipt overflow abort, immutable generation publication, `previous` before `current` selector ordering, selector-only rollback, exact-transaction resume and report-only treatment of unknown orphan state.

## Authority boundary

Acceptance does not authorize a local supply map, provider/result archive reads or downloads, member extraction, generation-root creation, implementation or execution, target population, materialization, publication, deployment or activation.

A later execution decision must bind this acceptance digest, an exact 41-row accepted local supply map and a separately approved effect set. Design acceptance alone cannot satisfy that gate.

## Update and rollback

Any source digest, object plan, state, operation, preflight, verification, recovery, budget, copy policy, atomic-family, selector or authority change requires a new Class D design review. Before implementation this acceptance may be revoked directly. Revocation never authorizes mutation of any future immutable generation.

## Next action

```text
generate-and-review-non-mutating-selected-provider-local-supply-map-contract
```

The next transaction may define a 41-row map schema and evidence requirements only. It may not acquire, read, extract or localize provider bytes.
