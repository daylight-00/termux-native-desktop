# 0147 — Selected Obsidian generic build-attestation and adaptation review set

## Status

```text
REPOSITORY-SIDE REVIEW SET: DEFINED / BOUNDED
EVIDENCE REQUIREMENTS: 16
PINNED RECIPE ROOT WORK UNITS: 28
OBJECT WORK UNITS: 37
EVIDENCE-COLLECTION ELIGIBLE OBJECTS: 36
OBJECT REQUIREMENT CORRECTION BLOCKED: 1
BUILD ATTESTATIONS ACCEPTED: 0
TERMUX/ANDROID ADAPTATIONS ACCEPTED: 0
CONCRETE FILENAME DRIFTS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction converts the reviewed `0146` receipt into a deterministic evidence-review plan. It defines what evidence would be required to review build provenance, recipe adaptation semantics and concrete-filename drift without collecting new device evidence, running builds or accepting any authority claim.

## Canonical inputs

```text
review/generic-recipe-binding-and-drift-target-receipt-review.tsv
review/generic-recipe-binding-and-drift-target-receipt-metadata.tsv
```

Canonical implementation:

```text
recipe/define-generic-build-attestation-and-adaptation-review-set.py
```

Canonical outputs:

```text
review/generic-build-attestation-adaptation-review-requirements.tsv
review/generic-build-attestation-adaptation-root-review-set.tsv
review/generic-build-attestation-adaptation-object-review-set.tsv
review/generic-build-attestation-adaptation-review-set-metadata.tsv
```

## Denominator

```text
review requirement rows:      16
recipe root work units:        28
object work units:             37
exact-member candidates:       21
SONAME-confirmed drift rows:   15
unsatisfied object rows:        1
eligible evidence rows:        36
blocked evidence rows:          1
```

Every root remains bound to the exact pinned recipe tree from `0145/0146`. Every object remains bound to its exact artifact identity and reviewed member state. This review set changes no provider, target, package, source checkout or cached artifact.

## Requirement dimensions

### Artifact build attestation

All 28 roots require `BA-001..BA-005`:

```text
BA-001 exact artifact digest → build invocation/source/recipe binding
BA-002 immutable build environment/toolchain/dependency identity
BA-003 package output and named member digest binding
BA-004 independent reproduction or independently verifiable provenance
BA-005 successor and rollback attestation continuity
```

These requirements intentionally reject family/version alignment, repository co-location and current receipt observations as independent build provenance.

### Adaptation semantic review

Material recipe-delta rows require:

```text
AD-001 complete recipe delta and hook inventory
AD-002 semantic comparison to the upstream baseline
AD-003 Android/Termux necessity classification
AD-004 named-object impact binding
AD-005 update and rollback implications
```

Configuration or packaging delta rows require `AD-001..AD-004`.

Rows with no explicit bounded delta token require:

```text
AD-002 upstream comparison
AD-003 necessity classification
AD-004 named-object impact binding
AD-006 full semantic review despite no observed token
```

Absence of a collector token is not evidence of an upstream-unmodified artifact.

### Concrete filename drift

The 15 SONAME-confirmed drift rows require `CF-001..CF-004`:

```text
CF-001 consumer binding to SONAME/stable alias rather than historical filename
CF-002 exact current alias → concrete target chain
CF-003 successor concrete-target drift policy
CF-004 rollback concrete-target policy
```

`DT_SONAME` equality alone does not accept a different concrete filename.

### Unsatisfied object requirement

```text
identity:
    libjpeg.so.62.3.0

requirement:
    OJ-001
```

This row is blocked until authoritative workload/reference evidence corrects the required identity or an exact candidate providing `libjpeg.so.62` is located. The `.so.8` family is not a substitute.

## Review tiers

Object work units:

```text
T0 object requirement correction:                  1
T1 material recipe delta + filename drift:        12
T2 material recipe delta + exact member:           8
T3 configuration/packaging + filename drift:       0
T4 configuration/packaging + exact member:         7
T5 no explicit token + filename drift:             3
T6 no explicit token + exact member:               6
```

Root work units use the highest-priority object tier present in the root:

```text
T0: 1
T1: 8
T2: 6
T3: 0
T4: 6
T5: 1
T6: 6
```

The tier is review ordering only. It is not authority ranking, runtime necessity or provider preference.

## Evidence collection boundary

The next evidence collection may inspect only the 28 pinned recipe roots, their identified upstream baselines, exact artifact/build metadata associated with the 29 referenced artifacts and the 37 named object rows.

Permitted evidence classes include:

```text
signed or immutable build provenance
retained CI/build records bound to artifact digests
independent reproducible-build comparison
exact source/recipe/environment manifests
semantic patch/configuration/hook review
object-level output impact analysis
consumer/reference binding evidence for filename drift
```

This definition does not authorize:

```text
network-wide package discovery
unbounded source search
package installation or mutation
maintainer-script execution
payload filesystem extraction
artifact rebuild acceptance without independent comparison
provider promotion
runtime composition
any target row population
```

## Authority boundary

Accepted by this transaction:

```text
bounded evidence requirements: 16
root review units:              28
object review units:            37
review ordering tiers:           7 defined / 6 populated
```

Not accepted:

```text
artifact-to-recipe build attestations: 0
Termux/Android adaptations:            0
concrete filename drifts:              0
final provider decisions:              0
target rows populated:                 0
```

Every output row remains:

```text
authority_state:
    OPEN_NO_ACCEPTANCE

target_population_state:
    UNPOPULATED
```

## Next state

```text
COLLECT_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE
```

Evidence collection must follow the root/object work units and requirement IDs defined here. Any later acceptance requires a separate receipt and repository-side review.

## Stop line

Do not:

```text
treat this plan as collected evidence;
treat a recipe root as proof of artifact production;
treat every Termux recipe delta as runtime-required adaptation;
treat no explicit delta token as upstream equivalence;
treat expected SONAME equality as filename-drift acceptance;
substitute libjpeg.so.8 for libjpeg.so.62;
accept provider authority;
populate target rows;
write or run extraction/materializer logic;
install, remove, upgrade or downgrade packages;
run maintainer scripts;
materialize or activate a successor;
modify current, launcher, loader state or RPATH.
```
