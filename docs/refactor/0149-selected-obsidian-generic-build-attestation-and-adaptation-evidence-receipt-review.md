# 0149 — Selected Obsidian generic build-attestation and adaptation evidence receipt review

## Status

```text
DEVICE RECEIPT: PASS / REVIEWED / BOUNDED
EVIDENCE REQUIREMENTS: 16 / 16 REVIEWED
LOCAL EVIDENCE OR PARTIAL EVIDENCE: 6 REQUIREMENT ROWS CONFIRMED AS REVIEW INPUT
EXTERNAL / SEMANTIC / POLICY / CORRECTION GAPS: 10 REQUIREMENT ROWS CONFIRMED
PINNED RECIPE ROOTS: 28 / 28 REVIEWED
NAMED OBJECTS: 37 / 37 REVIEWED
ARTIFACT BUILD ATTESTATIONS: 0 ACCEPTED
TERMUX/ANDROID ADAPTATIONS: 0 ACCEPTED
CONCRETE FILENAME DRIFTS: 0 ACCEPTED
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction reviews the bounded device receipt produced by `0148`. It confirms local recipe, object/member and crosswalk observations only as review inputs, and it records every missing provenance, semantic, policy and correction requirement explicitly.

It does not infer build provenance from repository co-location, classify syntactic recipe signals as Android/Termux necessity, accept concrete filename drift from provider SONAME evidence alone, or promote any provider.

## Reviewed receipt

```text
archive:
    termux-native-desktop-build-attestation-adaptation-evidence-collector-result-20260713T163504Z.tar.zst

SHA-256:
    34e5fa934f05b4eb035925adfcb22a646983a53bbae9fa39897a0d61dd69d169

transaction:
    PASS

validation:
    PASS

evidence collection:
    PASS

source branch:
    docs/post-graphics-architecture-audit

source HEAD:
    540976e7bb8bc49e2d2ab732f8c2f75a90c3b63a

source tree:
    bd042154b7eadd0655d52477677129fa54bfdbd1
```

The receipt archive is a single safe-root Zstandard tar. Its source checkout manifest is unchanged before and after collection. The collector performed no package operation, maintainer-script execution, filesystem payload extraction, network acquisition, provider promotion or target population.

## Canonical review products

```text
review/generic-build-attestation-adaptation-evidence-receipt-review-rules.tsv
review/generic-build-attestation-adaptation-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-root-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-object-evidence-receipt-review.tsv
review/generic-build-attestation-adaptation-evidence-receipt-metadata.tsv
recipe/review-generic-build-attestation-and-adaptation-evidence.py
tests/repository/generic-build-attestation-adaptation-evidence-receipt-review-smoke.sh
```

The reviewer binds the receipt back to the exact `0147` requirement, root and object review sets. It rejects denominator drift, canonical field drift, missing gap rows, output-class drift, authority promotion and target population.

## Receipt denominator

```text
requirements:                         16
root work units:                      28
object work units:                    37
foundation artifacts reverified:      34
recipe files inventoried:             84
bounded build-script signal rows:      74
exact member output rows:              21
alias-target output rows:              15
object-requirement blocked rows:        1
local/partial evidence requirements:    6
explicit gap requirements:             10
```

Root review tiers remain:

```text
T0 object requirement correction:       1
T1 material delta + filename drift:      8
T2 material delta + exact member:        6
T4 configuration/packaging + exact:      6
T5 no explicit token + drift:            1
T6 no explicit token + exact:            6
```

The tiers remain review ordering only. They are not authority ranking, runtime necessity or provider preference.

## Local evidence confirmed as bounded review input — 6 requirements

The following receipt observations are confirmed as internally consistent evidence inputs:

```text
BA-003
    37 artifact/object output rows are bound to exact artifact and member identities.
    Producing-build linkage remains open.

AD-001
    84 pinned recipe files and 74 bounded script-signal rows are inventoried.
    Semantic meaning is not accepted.

AD-002
    Pinned upstream URL/hash declarations are recorded for all 28 roots.
    Upstream semantic comparison remains open.

AD-004
    37 root-to-object crosswalk rows are recorded.
    Object-level semantic impact remains open.

AD-006
    Full pinned recipe manifests exist for roots with no explicit collector token.
    Absence of a token is not upstream equivalence.

CF-002
    15 exact current alias-to-target chains, target digests and target SONAMEs are recorded.
    Consumer binding and successor/rollback drift policy remain open.
```

Receipt review state:

```text
LOCAL_EVIDENCE_CONFIRMED_BOUNDED_REVIEW_INPUT
```

This state accepts only the observation and its exact bounded identity. It has no automatic authority effect.

## Explicit gaps confirmed — 10 requirements

### External build provenance — 3

```text
BA-001 digest-bound producing build invocation
BA-002 immutable producing build environment/toolchain/dependency record
BA-004 independent reproduction or independently verifiable provenance
```

### Continuity policy — 4

```text
BA-005 successor and rollback attestation continuity
AD-005 adaptation update and rollback policy
CF-003 successor concrete-filename drift policy
CF-004 rollback concrete-filename drift policy
```

### Semantic and consumer evidence — 2

```text
AD-003 object-bound Android/Termux necessity classification
CF-001 consumer binding to the SONAME or stable alias
```

### Object requirement correction — 1

```text
OJ-001 libjpeg.so.62 requirement correction or exact matching candidate
```

Receipt review state:

```text
EXTERNAL_SEMANTIC_POLICY_OR_CORRECTION_GAP_CONFIRMED
```

A confirmed gap is not negative authority evidence and is not permission to substitute a nearby family.

## Object evidence review

### Exact member output evidence — 21

For 21 objects, the receipt confirms:

```text
exact artifact SHA-256
exact member path
exact member SHA-256
expected ELF DT_SONAME
pinned recipe root/tree crosswalk
```

Review state:

```text
EXACT_MEMBER_DIGEST_AND_SONAME_CONFIRMED_REVIEW_INPUT
```

The producing build record, adaptation semantic impact, final provider and target row remain open.

### Alias-target output evidence — 15

For 15 filename-drift objects, the receipt confirms:

```text
expected SONAME alias member
exact current alias target
exact target member SHA-256
expected target ELF DT_SONAME
pinned recipe root/tree crosswalk
```

Review state:

```text
ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_CONFIRMED_REVIEW_INPUT
```

Still required:

```text
consumer binding evidence
successor filename-drift policy
rollback filename-drift policy
producing-build linkage
adaptation semantic impact
```

### Unsatisfied object requirement — 1

```text
identity:
    libjpeg.so.62.3.0

review state:
    NO_OUTPUT_BINDING_OBJECT_REQUIREMENT_UNSATISFIED
```

The observed `libjpeg.so.8` family is not substituted for `libjpeg.so.62`.

## Authority boundary

Accepted by this transaction:

```text
receipt integrity and bounded execution:       PASS
requirement evidence/gap classification:       16 / 16
root evidence consistency:                     28 / 28
object evidence consistency:                   37 / 37
local evidence observations as review inputs:   6 requirement dimensions
explicit remaining gaps:                       10 requirement dimensions
```

Not accepted:

```text
artifact-to-recipe build attestations: 0
Termux/Android adaptations:            0
concrete filename drifts:              0
final provider decisions:              0
target rows populated:                 0
```

All requirement and object rows remain:

```text
authority_state:
    OPEN_NO_ACCEPTANCE

target_population_state:
    UNPOPULATED
```

## Next state

```text
DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_SET
```

The next transaction must convert the ten confirmed gaps and six remaining local semantic/build-link obligations into deterministic, bounded work units. It must distinguish:

```text
external immutable build provenance
repository-side semantic comparison
object-bound necessity and impact classification
consumer binding evidence
successor/rollback continuity policy
object requirement correction
```

Each later evidence source requires a separate receipt and repository-side review before any acceptance.

## Stop line

Do not:

```text
treat local output binding as a producing-build attestation;
treat recipe files or syntactic signals as accepted Android/Termux adaptation;
treat a root-to-object crosswalk as semantic object impact;
treat target SONAME equality as consumer binding;
treat current alias-target evidence as successor or rollback drift policy;
substitute libjpeg.so.8 for libjpeg.so.62;
accept final provider authority;
populate target rows;
write or run extraction/materializer logic;
install packages or execute maintainer scripts;
modify generation/current, launcher, loader state or RPATH.
```
