# 0158 — Selected Obsidian generic build-attestation and adaptation gap-evidence supply batch SUP-01 response review

## Status

```text
SUPPLY BATCH: SUP-01
REQUEST: SRQ-OJ-001
RESPONSE REVIEW: PASS / BOUNDED
OBJECT REQUIREMENT CORRECTION: ACCEPTED
PRIOR ORACLE CONCRETE IDENTITY: libjpeg.so.62.3.0
ACCEPTED REQUIRED IDENTITY: libjpeg.so.62
REJECTED SUBSTITUTE: libjpeg.so.8
MATCHING SONAME-62 PROVIDER CANDIDATES BOUND: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
NEXT BATCH: SUP-02
```

The review accepts one narrow semantic correction: `OJ-001` must require the stable ELF SONAME `libjpeg.so.62`, not the Debian oracle's provider-versioned concrete filename `libjpeg.so.62.3.0`.

The completion gate for `OJ-001` is disjunctive: correct the required identity **or** bind an exact matching provider candidate. The authoritative response satisfies the first branch. It does not satisfy the second branch and does not accept a provider.

## Decision

```text
libjpeg.so.62.3.0
    -> retained as one observed provider-versioned concrete filename

libjpeg.so.62
    -> accepted stable required ABI identity

libjpeg.so.8
    -> rejected incompatible ABI family
```

Pinned upstream libjpeg-turbo 3.1.0 definitions establish that default v6b emulation uses SOVERSION 62, while `WITH_JPEG8=ON` is backward-incompatible and uses SOVERSION 8. The selected Termux recipe enables `WITH_JPEG8=ON`, and the selected artifact contains only the `libjpeg.so.8` family. Alias invention or ABI-family similarity cannot bridge that boundary.

## Accepted effect

```text
OJ-001 requirement model:
    CLOSED_BY_REQUIRED_IDENTITY_CORRECTION

matching provider candidate:
    ABSENT / SUPPLY STILL REQUIRED IF THIS OBJECT IS SELECTED

object row:
    OPEN

final provider authority:
    OPEN

target population:
    BLOCKED
```

This correction closes the P0 requirement-definition defect. It does not prove that the selected Termux artifact supplies the required ABI, does not select Debian as the provider, and does not populate any runtime target.

## Canonical implementation

```text
recipe/review-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-01-response.py
```

Canonical review inputs:

```text
review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv
review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv
evidence-supply/responses/SUP-01/SRQ-OJ-001/
```

Canonical outputs:

```text
review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review-rules.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-object-review.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review-metadata.tsv
```

## Stop line

The review does not:

```text
accept libjpeg.so.8 as libjpeg.so.62;
create a libjpeg.so.62 alias;
bind a matching provider candidate;
accept build provenance or adaptation;
accept final provider authority;
populate a target row;
write extraction or materializer behavior;
install, remove, upgrade or downgrade a package;
run maintainer scripts;
materialize or activate a successor;
change current, launcher, loader state or RPATH.
```

## Next state

```text
FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02
```

`SUP-02` requests digest-bound invocation, immutable environment and producing-build output linkage for `BA-001`, `BA-002` and `BA-003`. Repository co-location, version alignment and receipt-only member observations remain insufficient.
