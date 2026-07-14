# 0153 — Selected Obsidian generic build-attestation and adaptation gap-evidence acquisition set

## Status

```text
REPOSITORY-SIDE ACQUISITION SET: DEFINED / BOUNDED / NOT EXECUTED
CLOSURE LANES: 6
EVIDENCE REQUIREMENTS: 16 / 16 MAPPED
SOURCE CONTRACTS: 10
PINNED ROOT ACQUISITION ROWS: 28
NAMED OBJECT ACQUISITION ROWS: 37
ROOT REQUIREMENT EDGES: 303
OBJECT REQUIREMENT EDGES: 414
CANDIDATE EVIDENCE ACQUIRED: 0
BUILD ATTESTATIONS ACCEPTED: 0
TERMUX/ANDROID ADAPTATIONS ACCEPTED: 0
CONCRETE FILENAME DRIFTS ACCEPTED: 0
OBJECT CORRECTIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction converts the reviewed no-candidate receipt from `0152` into deterministic evidence-acquisition contracts. It defines what may be imported, captured or authored for each requirement; how that evidence must be scoped and integrity-bound; and which separate review remains mandatory.

It performs no acquisition and accepts no evidence or authority claim.

## Canonical inputs

```text
review/generic-build-attestation-adaptation-gap-closure-lanes.tsv
review/generic-build-attestation-adaptation-gap-closure-requirements.tsv
review/generic-build-attestation-adaptation-gap-closure-receipt-review.tsv
review/generic-build-attestation-adaptation-gap-closure-lane-receipt-review.tsv
review/generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv
review/generic-build-attestation-adaptation-object-gap-closure-receipt-review.tsv
review/generic-build-attestation-adaptation-gap-closure-receipt-review-metadata.tsv
```

Canonical implementation:

```text
recipe/define-generic-build-attestation-and-adaptation-gap-evidence-acquisition-set.py
```

Canonical outputs:

```text
review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv
review/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv
review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-set-metadata.tsv
```

## Strict collector compatibility

Every acquisition deliverable must be representable by the existing `0151` strict manifest:

```text
evidence_id
requirement_id
lane_id
scope_kind
scope_id
evidence_class
source_kind
source_locator
relative_path
sha256
size_bytes
claim_boundary
```

The acquisition set fixes the claim boundary as:

```text
CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT
```

Acquisition success therefore cannot satisfy a requirement by itself. Every candidate remains subject to a separate gap-closure receipt review.

## Ten source contracts

```text
AUTHORITATIVE_REFERENCE
IMMUTABLE_BUILD_RECORD
SIGNED_PROVENANCE
INDEPENDENT_REPRODUCTION
OUTPUT_MANIFEST
PINNED_UPSTREAM_BASELINE
SEMANTIC_REVIEW
CONSUMER_REFERENCE
LOADER_POLICY
CONTINUITY_POLICY
```

Each source contract defines:

```text
allowed requirement IDs;
allowed ROOT or OBJECT manifest scopes;
permitted import, capture or authoring mode;
required immutable locator class;
SHA-256 and byte-size binding;
payload contract;
prohibited inference.
```

A valid digest does not permit source-class substitution. For example, a semantic review cannot be reclassified as immutable producing-build provenance, and provider SONAME evidence cannot be reclassified as consumer binding.

## Requirement acquisition classes

### GC-01 — authoritative correction

```text
OJ-001
    operator-supplied authoritative reference or bounded reference review;
    OBJECT-scoped manifest record;
    no libjpeg.so.8 substitution for libjpeg.so.62.
```

### GC-02 — producer provenance and independent verification

```text
BA-001 / BA-002
    import immutable build records or signed provenance;

BA-004
    import an independent reproduction receipt or signed provenance;

all records remain bound to the exact root, recipe tree and artifact digest.
```

### GC-03 — output linkage

```text
BA-003
    import a producing-build output manifest;
    bind package and named-member digests to the same producing build run.
```

### GC-04 — upstream and adaptation semantic review

```text
AD-001 / AD-003 / AD-004 / AD-006
    author bounded semantic review records;

AD-002
    acquire or import the pinned upstream baseline and author the comparison;

no token, repository-origin or no-token inference is accepted as necessity.
```

### GC-05 — consumer binding

```text
CF-001
    passively capture bounded consumer references or loader policy;

CF-002
    review the exact alias chain with consumer and continuity evidence;

provider SONAME equality alone remains insufficient.
```

### GC-06 — successor and rollback policy

```text
BA-005 / AD-005 / CF-003 / CF-004
    author explicit continuity-policy records;
    define successor and rollback validation and rejection gates.
```

## Root acquisition rows

The 28 pinned roots retain exact recipe roots and recipe-tree identities. Each row now records:

```text
one deterministic acquisition-unit ID;
all applicable requirements and closure lanes;
permitted source kinds;
direct-gap and local-foundation subsets;
ROOT manifest scope ID;
priority-ordered acquisition sequence;
separate-review completion gate.
```

The 28 rows contain 303 root-to-requirement edges. This is a planning denominator, not package-wide authority.

## Object acquisition rows

The 37 named objects retain exact artifact and object identities. Each row records:

```text
one deterministic acquisition-unit ID;
exact object and evidence-row IDs;
artifact digest and recipe root;
object class;
all applicable requirements and source kinds;
OBJECT manifest scope ID;
priority-ordered acquisition sequence;
root-prerequisite plus object-review completion gate.
```

The 37 rows contain 414 object-to-requirement edges. All rows remain:

```text
final_provider_state:    UNRESOLVED
authority_state:         OPEN_NO_ACCEPTANCE
target_population_state: UNPOPULATED
```

## Execution boundary

A later acquirer may only execute the named modes and source contracts. It may:

```text
import already-existing immutable or signed build records;
import independent reproduction receipts;
import exact output manifests;
acquire or import pinned upstream source baselines;
author deterministic semantic and continuity review records;
passively capture bounded consumer references;
produce a strict-manifest-compatible evidence root.
```

It must not:

```text
perform unbounded network discovery;
select latest upstream state instead of a pinned baseline;
install, remove, upgrade or downgrade packages;
run maintainer scripts;
build artifacts unless a separately bounded independent-reproduction unit authorizes it;
extract payloads into runtime paths;
execute target runtime payloads;
promote providers or corrections;
populate target rows;
materialize or activate a successor;
change current, launcher, loader state or RPATH.
```

## Accepted by this transaction

```text
10 source contracts;
6 acquisition-lane contracts;
16 requirement acquisition contracts;
28 root acquisition rows and 303 root requirement edges;
37 object acquisition rows and 414 object requirement edges;
strict-manifest compatibility and integrity requirements;
separate receipt-review requirement.
```

Not accepted:

```text
candidate evidence;
object-requirement correction;
producing-build provenance;
independent reproduction;
adaptation necessity;
consumer binding;
continuity policy;
filename drift;
final provider authority;
target population.
```

## Next state

```text
IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER
```

The acquirer must be fail-closed, preserve all exact scope identities, and produce no automatic authority effect.

## Stop line

Do not treat this acquisition plan as collected evidence. Do not collapse import, passive capture, semantic authoring and independent reproduction into one unrestricted action. Do not substitute source classes, scope IDs, ABI families or current-version assumptions.
