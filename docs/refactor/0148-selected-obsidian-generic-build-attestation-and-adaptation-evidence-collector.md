# 0148 — Selected Obsidian generic build-attestation and adaptation evidence collector

## Status

```text
COLLECTOR: IMPLEMENTED / BOUNDED / READ-ONLY
REVIEW REQUIREMENTS: 16
PINNED RECIPE ROOTS: 28
OBJECT WORK UNITS: 37
FOUNDATION ARTIFACTS REVERIFIED: 34
FOUNDATION DRIFT TARGET ELFS REVERIFIED: 15
BUILD ATTESTATIONS ACCEPTED: 0
TERMUX/ANDROID ADAPTATIONS ACCEPTED: 0
CONCRETE FILENAME DRIFTS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction implements the next bounded evidence-collection step for the `0147` review set. It records locally available recipe, artifact/member and root/object evidence while explicitly separating missing external build provenance, semantic decisions and update/rollback policy.

## Canonical implementation

```text
recipe/collect-generic-build-attestation-and-adaptation-evidence.py
recipe/run-generic-build-attestation-and-adaptation-evidence.sh
```

The runner first executes the already bounded recipe-binding/drift-target foundation collector. That foundation revalidates:

```text
34 exact cached artifacts
28 pinned recipe roots
37 recipe/object rows
15 drift target ELF members
```

The evidence collector then compiles the `0147` review set without running builds or mutating supply state.

## Output receipt

```text
analysis.status
claim-boundary.txt
next-state.txt
summary.tsv
input-verification.tsv
requirement-evidence-status.tsv
root-evidence-observations.tsv
recipe-file-evidence.tsv
recipe-build-script-signal-evidence.tsv
root-object-impact-crosswalk.tsv
artifact-member-output-evidence.tsv
external-evidence-gaps.tsv
foundation-recipe-binding-and-drift-target/*
```

### Local recipe evidence

For each pinned recipe root, the collector records every Git blob with:

```text
path
mode
blob OID
byte size
content SHA-256
bounded file class
```

Non-comment `build.sh` lines are recorded only when they match bounded syntactic signal classes such as Termux prefix references, configure/build steps, package hooks, subpackage declarations or Android platform references.

These signals are not semantic classifications. They do not prove that a change is Android-required, runtime-relevant or accepted.

### Artifact/member output evidence

The 37 object rows are joined to the reviewed member receipt and the freshly revalidated foundation receipt.

```text
21 exact member rows:
    artifact digest + exact member path/digest + observed SONAME

15 filename-drift rows:
    artifact digest + alias path/target + target member path/digest + observed SONAME

1 blocked object row:
    libjpeg.so.62 requirement remains unsatisfied
```

This satisfies only local output-observation portions of `BA-003` and `CF-002`. It does not bind those bytes to a producing build invocation.

### Requirement availability states

The collector emits one row for every `BA-*`, `AD-*`, `CF-*` and `OJ-*` requirement.

Locally observable evidence is recorded for:

```text
BA-003 artifact/member output observations
AD-001 complete pinned recipe file/signal inventory
AD-002 upstream declarations, but not semantic comparison
AD-004 root/object crosswalk, but not accepted impact analysis
AD-006 full recipe manifests, but not no-token equivalence
CF-002 exact current alias/target/member evidence
```

The receipt explicitly records gaps for:

```text
BA-001 digest-bound producing build provenance
BA-002 producing build environment/toolchain/dependency record
BA-004 independent reproduction or signed provenance
BA-005 attestation continuity policy
AD-003 necessity classification
AD-005 adaptation update/rollback policy
CF-001 consumer binding evidence
CF-003 successor filename-drift policy
CF-004 rollback filename-drift policy
OJ-001 libjpeg.so.62 requirement correction
```

## Mutation boundary

The collector is read-only with respect to the project, pinned source checkout and artifact cache.

It performs no:

```text
network acquisition
package installation/removal/upgrade/downgrade
maintainer-script execution
artifact build
payload filesystem extraction
runtime execution
provider promotion
target row population
materialization or activation
launcher/loader/RPATH mutation
```

The foundation collector may stream package archive members in memory. No package payload is materialized into a filesystem tree.

## Authority boundary

Collected evidence remains review input only.

```text
artifact-to-recipe build attestations accepted: 0
Termux/Android adaptations accepted:            0
concrete filename drifts accepted:              0
final provider decisions accepted:              0
target rows populated:                           0
```

Current host state is never substituted for the historical producing-build environment. Recipe co-location, source URL declarations, package version alignment, output digest observations and syntactic delta tokens remain separate evidence classes.

## Next state

```text
REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_RECEIPT
```

A later repository-side review must evaluate the receipt and preserve every unresolved external, semantic, policy and object-correction gap. The collector itself cannot accept authority.

## Stop line

Do not:

```text
treat local evidence availability as requirement satisfaction;
treat a recipe root as a producing-build attestation;
treat current host state as the historical build environment;
treat syntactic recipe signals as semantic adaptation classification;
treat a root/object crosswalk as object-impact proof;
treat current alias/SONAME evidence as drift policy acceptance;
substitute libjpeg.so.8 for libjpeg.so.62;
accept provider authority;
populate target rows;
write or run extraction/materializer logic;
install, remove, upgrade or downgrade packages;
run maintainer scripts;
materialize or activate a successor;
modify current, launcher, loader state or RPATH.
```
