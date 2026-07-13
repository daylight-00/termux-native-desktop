# 0146 — Selected Obsidian generic recipe-binding and drift-target ELF receipt review

## Status

```text
DEVICE RECEIPT: PASS / REVIEWED
PINNED RECIPE LINEAGE CANDIDATES: 37 / 37 CONFIRMED
DRIFT-TARGET ELF EXPECTED SONAME: 15 / 15 CONFIRMED
ARTIFACT-TO-RECIPE BUILD ATTESTATION: 0 / 37 ACCEPTED
TERMUX/ANDROID ADAPTATION: 0 / 37 ACCEPTED
CONCRETE FILENAME DRIFT: 0 / 15 ACCEPTED
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction reviews the bounded `0145` device receipt. It validates the exact pinned source state, all 34 cached artifact identities, 84 recipe-file inventory rows, 37 recipe-lineage candidate rows and 15 stream-inspected drift-target ELFs.

The review accepts none of those observations as independent artifact build provenance, semantic adaptation acceptance, concrete-filename drift policy, final provider authority or target population permission.

## Reviewed receipt

```text
archive:
    termux-native-desktop-recipe-drift-stream-drain-recovery-result-20260713T130022Z.tar.zst

SHA-256:
    a415601cb3cfd6d3d85a69c589f38f9d2ba4151483b887c0e611d40a17beccd0

transaction:
    PASS

collector:
    PASS

stream-drain hotfix:
    PASS
```

The archive is one safe-root Zstandard tar containing only regular files and directories. It contains no cached `.deb` payloads and no source checkout archive.

## Canonical review inputs

```text
review policy:
    review/generic-recipe-binding-and-drift-target-receipt-review-rules.tsv

collector contract:
    review/generic-recipe-binding-and-drift-target-rules.tsv
    review/generic-recipe-binding-and-drift-target-metadata.tsv

artifact registry:
    review/generic-artifact-member-comparison-artifacts.tsv

review implementation:
    recipe/review-generic-recipe-binding-and-drift-target-elf.py
```

Canonical outputs:

```text
review/generic-recipe-binding-and-drift-target-receipt-review.tsv
review/generic-recipe-binding-and-drift-target-receipt-metadata.tsv
```

## Receipt denominator

```text
review identities:                 37
selected artifacts referenced:     29
full cached artifacts verified:    34
unique recipe roots:               28
recipe file inventory rows:        84
exact-member rows:                 21
drift-target ELF rows:             15
expected-alias-absent rows:         1
```

Pinned source state:

```text
repository:
    https://github.com/termux-pacman/glibc-packages.git

HEAD:
    fd2ae25e04f3ea26d6c7b4678020814889331d86

tree:
    e502a4c18ab9092ec119e3a498a0bf192ef60e6f

worktree:
    CLEAN

fsck:
    PASS
```

All 34 cached artifacts matched their exact package, version, architecture, byte length and SHA-256. No package operation was performed.

## Recipe-lineage review

All 37 rows retain:

```text
PINNED_RECIPE_LINEAGE_CANDIDATE_CONFIRMED
```

This means the artifact family/version aligns with one exact pinned recipe tree, build script and complete recipe-file manifest.

Every row also retains:

```text
OPEN_NO_INDEPENDENT_BUILD_PROVENANCE_OR_BYTE_REPRODUCTION
```

Family/version/tree alignment is not evidence that the indexed artifact bytes were produced by that recipe object. No signed provenance, retained build log bound to the artifact digest, reproducible-build comparison or independent byte reproduction is present.

```text
artifact build attestations accepted: 0
```

## Adaptation evidence review classes

Recipe evidence tokens are classified into three semantic-review queues.

### Material recipe delta evidence

```text
rows: 20
state:
    MATERIAL_RECIPE_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED
```

At least one of the following is present:

```text
PATCH_FILE
CUSTOM_TERMUX_STEP
LAYOUT_OR_HOOK
```

These rows require semantic review of what the patch, custom build step or layout/hook changes relative to upstream and whether the change is required for Android/Termux or only package maintenance.

### Configuration or packaging delta evidence

```text
rows: 8
state:
    CONFIGURATION_OR_PACKAGING_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED
```

The evidence is limited to tokens such as:

```text
EXTRA_CONFIGURE_ARGS
BUILD_IN_SRC
PACKAGE_REVISION
SUBPACKAGE_SCRIPT
TERMUX_PREFIX_REFERENCE
```

Those tokens are still not self-explanatory adaptation acceptance. Their semantic effect, output membership and runtime relevance remain open.

### No explicit delta token observed

```text
rows: 9
state:
    NO_EXPLICIT_DELTA_TOKEN_OBSERVED_SEMANTIC_REVIEW_OPEN
```

Absence of a bounded token is not proof that the artifact is an unmodified upstream build. It only means the collector did not observe one of the defined token classes in the pinned recipe files.

```text
Termux/Android adaptations accepted: 0
```

## Object/member review

### Exact concrete member and expected SONAME

```text
rows: 21
state:
    EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED
```

These rows retain candidate object/member evidence. They still require build attestation and adaptation review before provider authority can be considered.

### Concrete filename drift with expected SONAME

```text
rows: 15
state:
    DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED
```

Every streamed target was:

```text
ELF64
little-endian
AArch64 machine 183
DT_SONAME equal to the expected SONAME alias
```

This closes the narrow question that the symlink target ELF carries the expected runtime SONAME. It does not accept the different concrete filename as a policy-compatible replacement.

```text
concrete filename drifts accepted: 0
```

Each row remains:

```text
OPEN_EXPECTED_SONAME_MATCH_ONLY_CONCRETE_FILENAME_DRIFT_NOT_ACCEPTED
```

A later review must decide whether the first-generation concrete filename was merely a build-version oracle, whether consumers bind only to the SONAME, and whether exact update/rollback policy may safely follow the package-provided concrete target.

### Expected alias absent

```text
row:
    libjpeg.so.62.3.0

state:
    EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED
```

The reviewed artifact provides the `.so.8` family, not `libjpeg.so.62`. It is not a substitute candidate. Either the required object identity must be corrected from authoritative workload evidence or a matching `.so.62` candidate must be found.

## Authority boundary

The review accepts:

```text
recipe lineage candidates:          37
object/member candidate rows:       36
```

It does not accept:

```text
artifact build attestations:         0
Termux/Android adaptations:           0
concrete filename drift policies:     0
final provider decisions:             0
target rows populated:                0
```

The 36 object/member-complete rows are eligible only for bounded build-attestation and adaptation review. The `libjpeg.so.62` row is not eligible because the object requirement is unsatisfied.

## Next valid state

```text
DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_REVIEW_SET
```

The next repository-side task must define, per recipe root and object row:

```text
what exact evidence could attest artifact bytes to the pinned recipe;
which recipe deltas require semantic Android/Termux review;
which 15 concrete-filename drifts require an explicit acceptance policy;
which rows can share one recipe-root review;
which evidence is already retained and which evidence is absent;
how libjpeg.so.62 remains excluded until corrected.
```

That task must not build packages, fetch new sources, install packages, extract payloads, populate targets or promote provider authority.

## Stop line

Do not:

```text
treat pinned recipe alignment as artifact build provenance;
treat token presence as accepted adaptation;
treat token absence as proof of an unmodified upstream build;
treat matching DT_SONAME as acceptance of a different concrete filename;
treat libjpeg.so.8 as libjpeg.so.62;
accept a final provider or capability composition;
install, remove, upgrade or downgrade packages;
execute maintainer scripts;
extract cached artifacts into a filesystem tree;
populate target paths, aliases, modes or owners;
write or run a materializer;
modify generation/current, launcher, loader state or RPATH.
```
