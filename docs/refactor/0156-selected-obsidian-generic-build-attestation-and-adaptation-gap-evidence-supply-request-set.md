# 0156 — Selected Obsidian generic build-attestation and adaptation gap-evidence supply-request set

## Status

```text
SUPPLY REQUEST SET: DEFINED / BOUNDED / NOT ISSUED
SUPPLY BATCHES: 6
REQUIREMENT REQUESTS: 16 / 16
DEPENDENCY COMPONENTS: 14
CYCLIC DEPENDENCY COMPONENTS: 1
CYCLIC REQUIREMENTS: 3
ROOT SUPPLY-REQUEST ROWS: 28
OBJECT SUPPLY-REQUEST ROWS: 37
ROOT REQUEST EDGES: 303
OBJECT REQUEST EDGES: 414
REQUESTS ISSUED: 0
RESPONSES RECEIVED: 0
CANDIDATE EVIDENCE ACQUIRED: 0
BUILD ATTESTATIONS ACCEPTED: 0
TERMUX/ANDROID ADAPTATIONS ACCEPTED: 0
CONCRETE FILENAME DRIFTS ACCEPTED: 0
OBJECT CORRECTIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

The reviewed production receipt in `0155` proved that another empty acquisition run would add no information. This transaction converts every open evidence requirement into an exact supply request with one responsible supplier role, one transport boundary, one required deliverable, exact ROOT or OBJECT scope, canonical acquisition mode, integrity fields, dependency component and post-supply review boundary.

It does not issue the requests, receive a response or accept evidence.

## Canonical inputs

```text
review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv
review/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv
review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review-metadata.tsv
```

The definer binds those files to their exact SHA-256 values and rejects receipt candidate invention, requirement suppression, source-class substitution, acquisition-unit drift, authority promotion and target population.

Canonical implementation:

```text
recipe/define-generic-build-attestation-and-adaptation-gap-evidence-supply-request-set.py
```

Canonical outputs:

```text
review/generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv
review/generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv
review/generic-build-attestation-adaptation-object-gap-evidence-supply-request-set.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-request-set-metadata.tsv
```

## Six supply batches

### SUP-01 — authoritative object correction

```text
requirement: OJ-001
supplier: agent reference research with operator decision
source: immutable authoritative reference
scope: one OBJECT unit
```

The response must establish the exact required libjpeg identity or bind an exact candidate with the required SONAME. `libjpeg.so.8` cannot substitute for `libjpeg.so.62`, and ABI-family similarity cannot resolve the row.

### SUP-02 — producing-build provenance and output linkage

```text
requirements: BA-001, BA-002, BA-003
supplier: producing-build record custodian
sources: immutable build record, signed provenance, output manifest
scope: ROOT units
```

The invocation, environment and package/member output manifest must refer to one producing build and remain bound to exact recipe trees and artifact digests. Repository co-location, version alignment and receipt-only output observations remain insufficient.

### SUP-03 — independent verification

```text
requirement: BA-004
supplier: independent Linux-workstation witness or signed-provenance custodian
prerequisite batch: SUP-02
```

A same-host replay is not independent verification. The response must be an independent reproduction receipt or independently verifiable signed provenance.

### SUP-04 — semantic baseline and object-impact review

```text
requirements: AD-001, AD-002, AD-003, AD-004, AD-006
supplier: project agent with pinned upstream references
sources: pinned upstream baseline and bounded semantic review
```

The work is repository-authorable, but not self-proving. It must pin upstream inputs, inventory complete recipe deltas, classify Android/Termux necessity and bind every relevant delta to named objects or explicit no-impact results. Token presence, Termux origin and unpinned latest upstream content are prohibited shortcuts.

### SUP-05 — consumer capture and alias-policy fixed point

```text
requirements: CF-001, CF-002, CF-003, CF-004
supplier: device capture operator and project agent
```

`CF-001` requires bounded passive consumer evidence. `CF-002`, `CF-003` and `CF-004` form one strongly connected dependency component: the alias-chain review and successor/rollback policies must be drafted, checked against consumer capture and iterated to a fixed point. A false linear order is rejected.

### SUP-06 — build and adaptation continuity policy

```text
requirements: BA-005, AD-005
supplier: project agent policy author
prerequisites: SUP-02, SUP-03, SUP-04
```

Successor and rollback policy is finalized only after the underlying provenance, independent verification and semantic review inputs exist. Current-version-only claims are rejected.

## Dependency result

The sixteen requirement nodes form fourteen dependency components:

```text
acyclic components: 13
cyclic components:   1
cyclic members:      CF-002, CF-003, CF-004
```

The cycle is a bounded policy/review iteration, not permission to omit a dependency or to accept the current filename chain as permanent policy.

## Supplier and transport boundary

```text
agent reference research with operator decision: 1 request
producing-build record custodian:                3 requests
independent witness or signed provenance:        1 request
agent semantic review:                           5 requests
device passive capture:                          1 request
agent consumer/alias review:                     1 request
agent policy authoring:                          4 requests
```

Transport does not create authority. The canonical relative exchange layout is:

```text
evidence-supply/requests/<batch-id>/
evidence-supply/responses/<batch-id>/
```

The human operator remains a minimal execution and connector boundary. Repository research, response drafting, manifest construction and review logic belong to the agent except where the request explicitly requires producing-build custody, independent witness execution or bounded device capture.

## Response contract

Every supplied payload must eventually be represented by the `0154` acquisition-input manifest fields:

```text
input_id
acquisition_unit_id
requirement_id
lane_id
scope_kind
scope_id
source_kind
acquisition_mode
locator_class
source_locator
relative_path
sha256
size_bytes
evidence_class
claim_boundary
```

The supply-request claim boundary is:

```text
SUPPLY_REQUEST_ONLY_NO_EVIDENCE_OR_AUTHORITY_EFFECT
```

A response is not accepted evidence. It must pass the bounded acquirer and a separate receipt review before any evidence claim can be considered, and even that does not automatically establish provider authority.

## Root and object fan-out

```text
root rows:            28
root request edges:  303
object rows:          37
object request edges: 414
```

Each row preserves its exact acquisition-unit ID, manifest scope, requirement set, supplier roles, dependency components and completion gate. Every object remains:

```text
final_provider_state:    UNRESOLVED
authority_state:         OPEN_NO_ACCEPTANCE
target_population_state: UNPOPULATED
```

## Next state

```text
FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01
```

The first response transaction is the isolated P0 authoritative correction request for `OJ-001`. It must produce a bounded reference-backed candidate response package, not an authority decision.

## Stop line

Do not:

```text
treat request definition as request issuance or evidence acquisition;
ask the human operator to author repository evidence manually;
substitute transport location for source authority;
accept unsigned names or version alignment as build provenance;
use the producing host as its own independent witness;
infer adaptation necessity from tokens or Termux origin;
linearize or ignore the CF-002/CF-003/CF-004 fixed-point dependency;
infer consumer binding from provider SONAME equality;
treat current concrete filenames as permanent continuity policy;
substitute libjpeg.so.8 for libjpeg.so.62;
accept build attestation, adaptation, filename drift, object correction or provider authority;
populate target rows;
write or run materialization or activation logic.
```
