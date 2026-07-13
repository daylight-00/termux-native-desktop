# 0150 — Selected Obsidian generic build-attestation and adaptation gap-closure set

## Status

```text
REPOSITORY-SIDE GAP-CLOSURE SET: DEFINED / BOUNDED
CLOSURE LANES: 6
EVIDENCE REQUIREMENTS: 16 / 16 MAPPED
DIRECT GAP REQUIREMENTS: 10
LOCAL-FOUNDATION COMPLETION REQUIREMENTS: 6
PINNED RECIPE ROOT WORK UNITS: 28
NAMED OBJECT WORK UNITS: 37
EXACT-MEMBER OBJECTS: 21
ALIAS-TARGET DRIFT OBJECTS: 15
OBJECT-REQUIREMENT BLOCKED OBJECTS: 1
BUILD ATTESTATIONS ACCEPTED: 0
TERMUX/ANDROID ADAPTATIONS ACCEPTED: 0
CONCRETE FILENAME DRIFTS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction converts the reviewed `0149` receipt into deterministic gap-closure lanes and root/object work units. It defines what may be collected or reviewed next, which prerequisites apply, and what completion and rejection gates govern each requirement.

It collects no new evidence and accepts no authority claim.

## Canonical inputs

```text
review/generic-build-attestation-adaptation-review-requirements.tsv
review/generic-build-attestation-adaptation-root-review-set.tsv
review/generic-build-attestation-adaptation-object-review-set.tsv
review/generic-build-attestation-adaptation-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-root-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-object-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-evidence-receipt-metadata.tsv
```

Canonical implementation:

```text
recipe/define-generic-build-attestation-and-adaptation-gap-closure-set.py
```

Canonical outputs:

```text
review/generic-build-attestation-adaptation-gap-closure-lanes.tsv
review/generic-build-attestation-adaptation-gap-closure-requirements.tsv
review/generic-build-attestation-adaptation-root-gap-closure-set.tsv
review/generic-build-attestation-adaptation-object-gap-closure-set.tsv
review/generic-build-attestation-adaptation-gap-closure-set-metadata.tsv
```

## Six closure lanes

### GC-01 — object-requirement correction / P0

```text
requirements:
    OJ-001

bounded outcome:
    correct the authoritative required identity;
    or bind an exact artifact/member candidate providing the required SONAME.

stop line:
    do not substitute another ABI family such as libjpeg.so.8 for libjpeg.so.62.
```

This lane remains first because the blocked identity cannot enter ordinary provider review until the requirement itself is corrected or satisfied exactly.

### GC-02 — digest-bound build provenance / P1

```text
requirements:
    BA-001
    BA-002
    BA-004
```

Permitted evidence is immutable builder provenance, a signed equivalent, or an independent reproducible-build verification bound to the exact artifact digest and pinned source/recipe identities. Repository co-location, matching names, and version agreement remain insufficient.

### GC-03 — output-to-build link / P2

```text
requirement:
    BA-003
```

The 21 exact-member and 15 alias-target output observations are retained as local foundations only. Closure requires linking those package/member digests to the producing build accepted through GC-02.

### GC-04 — adaptation semantic review / P3

```text
requirements:
    AD-001
    AD-002
    AD-003
    AD-004
    AD-006
```

This lane reviews complete pinned recipe deltas, upstream behavior, Android/Termux necessity classification, and named-object impact. Token presence, Termux repository origin, and absence of an observed token remain non-authoritative.

### GC-05 — consumer binding review / P4

```text
requirements:
    CF-001
    CF-002
```

The exact current alias-to-target observations remain valid local input. Closure additionally requires bounded consumer/reference or loader-policy evidence showing that the stable SONAME or alias, rather than the historical concrete filename, is the runtime identity.

### GC-06 — successor and rollback continuity policy / P5

```text
requirements:
    BA-005
    AD-005
    CF-003
    CF-004
```

This lane defines explicit validation rules for successor and rollback build provenance, adaptations, alias/SONAME identity and concrete-target changes. Current-version-only reasoning and the first-generation concrete filename remain insufficient.

## Requirement dependency boundary

The 16 requirement rows are split without changing their authority state:

```text
direct evidence / semantic / policy / correction gaps: 10
local-foundation completion requirements:              6
```

Local-foundation rows are not closed. They retain verified observations while naming dependencies that must be completed before any separate acceptance review:

```text
BA-003 depends on digest-bound producing-build records;
AD-001/002/004/006 require semantic completion beyond inventories and crosswalks;
CF-002 depends on consumer binding and successor/rollback filename policy.
```

Every row remains:

```text
closure_state:
    WORK_UNIT_DEFINED_EVIDENCE_OR_REVIEW_NOT_ACCEPTED

authority_state:
    OPEN_NO_ACCEPTANCE
```

## Root work units

The 28 pinned recipe roots retain their exact root IDs, trees, resolved versions, artifact references and identity counts. Each root row now records:

```text
closure lanes;
root-scoped requirements;
dependent object-scoped requirements;
direct gaps;
local-foundation completion requirements;
prerequisite requirements;
separate-receipt completion gate.
```

A root work unit is complete only after its root requirements and all dependent named-object requirements have been reviewed in a later receipt. Root completion cannot promote package-wide authority.

## Object work units

The 37 object rows retain exact artifact, member, SONAME and alias observations from `0149`:

```text
exact-member work units:             21
alias-target drift work units:       15
object-requirement correction unit:   1
```

Each object row carries its root prerequisites, object requirements, lanes and completion gate. Exact-member observations still require build linkage and semantic object-impact review. Drift rows additionally require consumer binding and filename-continuity policy. The blocked libjpeg row must complete GC-01 first.

All rows remain:

```text
final_provider_state:
    UNRESOLVED

authority_state:
    OPEN_NO_ACCEPTANCE

target_population_state:
    UNPOPULATED
```

## Collector boundary

A later collector may operate only against the named closure lanes, pinned roots, artifact digests and object identities in this set. It may ingest or inspect bounded evidence such as:

```text
immutable build records or signed provenance;
independent reproduction receipts;
exact output manifests;
pinned upstream source/recipe comparisons;
object-level semantic impact records;
bounded consumer/reference or loader-policy evidence;
explicit successor/rollback policy documents;
authoritative workload/reference correction evidence.
```

It must not perform:

```text
unbounded network or package discovery;
package installation, removal, upgrade or downgrade;
maintainer-script execution;
payload filesystem extraction;
provider promotion;
runtime composition;
target row population;
materialization or activation.
```

## Authority boundary

Accepted by this transaction:

```text
six deterministic closure lanes;
16 requirement closure mappings;
28 root work units;
37 object work units;
requirement dependencies and completion/rejection gates.
```

Not accepted:

```text
new evidence;
artifact build provenance;
Termux/Android adaptation necessity;
consumer binding;
filename-drift continuity;
object-requirement correction;
final provider authority;
target population.
```

## Next state

```text
IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_COLLECTOR
```

The collector must preserve lane boundaries and emit an explicit gap for every unavailable evidence item. Collection success alone cannot become authority acceptance.

## Stop line

Do not:

```text
treat this plan as collected evidence;
treat a local foundation as a completed requirement;
collapse root and object requirements into package-wide authority;
use repository co-location as build provenance;
use recipe tokens as semantic necessity;
use provider SONAME equality as consumer binding;
use the historical concrete filename as a permanent oracle;
substitute libjpeg.so.8 for libjpeg.so.62;
accept a provider;
populate target rows;
write or run extraction/materializer logic.
```
