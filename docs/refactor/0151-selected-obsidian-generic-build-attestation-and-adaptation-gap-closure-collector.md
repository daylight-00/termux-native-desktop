# 0151 — Selected Obsidian generic build-attestation and adaptation gap-closure collector

## Status

```text
COLLECTOR: IMPLEMENTED / BOUNDED / READ-ONLY
CLOSURE LANES: 6
REQUIREMENTS: 16
PINNED ROOT WORK UNITS: 28
NAMED OBJECT WORK UNITS: 37
OPTIONAL CANDIDATE EVIDENCE ROOT: STRICT MANIFEST CONTRACT
MISSING EVIDENCE: EXPLICIT GAP ROW REQUIRED
BUILD ATTESTATIONS ACCEPTED: 0
TERMUX/ANDROID ADAPTATIONS ACCEPTED: 0
CONCRETE FILENAME DRIFTS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction implements the bounded collector required by `0150`. The collector inventories exact candidate evidence files supplied under a strict manifest and carries forward the six canonical local-foundation review inputs from `0149`.

Collection success is not evidence acceptance. Every unavailable direct-gap requirement is emitted as an explicit gap, and every supplied file remains review input only.

## Canonical implementation

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    collect-generic-build-attestation-and-adaptation-gap-closure.py
    run-generic-build-attestation-and-adaptation-gap-closure.sh

tests/repository/
    generic-build-attestation-adaptation-gap-closure-collector-smoke.sh
```

The implementation consumes only the canonical closure inputs:

```text
review/generic-build-attestation-adaptation-gap-closure-lanes.tsv
review/generic-build-attestation-adaptation-gap-closure-requirements.tsv
review/generic-build-attestation-adaptation-root-gap-closure-set.tsv
review/generic-build-attestation-adaptation-object-gap-closure-set.tsv
review/generic-build-attestation-adaptation-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-root-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-object-evidence-receipt-review.tsv
```

It rejects denominator drift, unknown lane or requirement IDs, authority-state promotion, target-population promotion, unsafe evidence paths, symlinks, duplicate evidence IDs, duplicate file paths, digest mismatch, size mismatch, invalid source classes, and claim-boundary drift.

## Optional candidate-evidence root

Default location:

```text
$HOME/.cache/hw-t-evidence/termux-native-desktop/
    generic-build-attestation-adaptation-gap-closure/
```

The root is optional. If it does not exist, the collector succeeds and records that no new candidate evidence was supplied.

If the root exists, it must contain a regular file:

```text
evidence-manifest.tsv
```

The manifest contract is:

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

Accepted scope kinds are:

```text
GLOBAL / ALL
ROOT / exact root_review_id or recipe_root
OBJECT / exact object_review_id or evidence_row_id
```

Every file must be a regular non-symlink below the evidence root. Absolute paths, `..` traversal, special files, and unmanifested evidence claims are rejected.

## Bounded source classes

Candidate source classes are requirement-specific:

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

Examples of enforced separation:

```text
BA-001/BA-002:
    immutable build record or signed provenance only

BA-004:
    independent reproduction or signed provenance only

AD-003/AD-004:
    semantic review only

CF-001:
    bounded consumer reference or loader policy only

OJ-001:
    authoritative reference only
```

A file with a valid digest but an invalid source class is rejected rather than reclassified.

## Output receipt

```text
analysis.status
claim-boundary.txt
next-state.txt
summary.tsv
input-verification.tsv
evidence-file-inventory.tsv
requirement-collection-status.tsv
lane-collection-status.tsv
root-gap-closure-observations.tsv
object-gap-closure-observations.tsv
unavailable-evidence-gaps.tsv
```

### Requirement rows

The collector emits exactly one row for every requirement.

Six local-foundation requirements remain bounded review inputs:

```text
BA-003
AD-001
AD-002
AD-004
AD-006
CF-002
```

Without a new manifest candidate, these remain:

```text
LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN
```

The ten direct gaps remain:

```text
EVIDENCE_UNAVAILABLE_EXPLICIT_GAP
```

when no candidate file is supplied. If a bounded file is supplied and verified, the state becomes:

```text
CANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED
```

or, for a local-foundation requirement:

```text
LOCAL_FOUNDATION_AND_CANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED
```

None of these states satisfies a requirement.

### Lane, root, and object rows

Each lane records candidate counts, unavailable requirements, local-foundation-only requirements, its completion gate, and its stop condition.

Each root and object row records only evidence IDs whose exact scope applies, plus global evidence. Requirements without candidate evidence remain explicit. Package-wide inference is not performed.

All object rows remain:

```text
final_provider_state:    UNRESOLVED
authority_state:         OPEN_NO_ACCEPTANCE
target_population_state: UNPOPULATED
```

## Mutation boundary

The collector performs no:

```text
network acquisition;
package installation, removal, upgrade, or downgrade;
maintainer-script execution;
artifact build;
payload filesystem extraction;
runtime execution;
provider promotion;
target population;
materialization or activation;
launcher, loader, current, or RPATH mutation.
```

It reads repository TSVs and optionally hashes regular candidate files. The output directory must not already exist.

## Authority boundary

The only accepted result is a bounded candidate-evidence inventory and explicit gap receipt.

```text
artifact build attestations accepted: 0
Termux/Android adaptations accepted: 0
concrete filename drifts accepted: 0
final provider decisions accepted: 0
target rows populated: 0
```

A manifest is not provenance. A signed-looking file is not accepted merely because it is present. A semantic-review file is not an accepted adaptation decision. An authoritative-reference candidate does not correct `libjpeg.so.62` until a separate receipt review verifies its claim.

## Validation

The smoke test covers:

```text
absent evidence root with 6 local foundations and 10 explicit gaps;
valid bounded candidates for BA-001, CF-001, and OJ-001;
zero authority effect after candidate collection;
digest tamper rejection;
path-traversal rejection;
exact 6 / 16 / 28 / 37 denominators.
```

## Next state

```text
RUN_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_COLLECTOR
```

The production receipt must then be reviewed separately:

```text
REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_RECEIPT
```

## Stop line

Do not:

```text
treat manifest presence as evidence truth;
treat candidate collection as requirement completion;
treat local foundation as closure evidence;
treat repository co-location as build provenance;
treat recipe tokens as semantic adaptation necessity;
treat provider SONAME equality as consumer binding;
substitute libjpeg.so.8 for libjpeg.so.62;
accept a build attestation, adaptation, filename drift, object correction, or provider;
populate target rows;
write or run materialization or activation logic.
```
