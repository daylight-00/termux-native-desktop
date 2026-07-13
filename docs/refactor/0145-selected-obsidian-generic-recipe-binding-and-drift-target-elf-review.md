# 0145 — Selected Obsidian bounded generic recipe binding and drift-target ELF review

## Status

```text
REPOSITORY CONTRACT: PASS / READY FOR DEVICE EXECUTION
ARTIFACT-TO-RECIPE BUILD ATTESTATION: OPEN
TERMUX/ANDROID ADAPTATION ACCEPTANCE: OPEN
FINAL PROVIDER AUTHORITY: OPEN
TARGET POPULATION: BLOCKED
```

This transaction defines the next bounded evidence collector after `0144`. It correlates the 37 direct-family member-review identities with the pinned `termux-pacman/glibc-packages` source checkout and performs stream-only ELF inspection of the 15 concrete symlink targets whose filenames drift from the first-generation oracle.

It does not build packages, install packages, execute maintainer scripts, extract payloads into a filesystem tree, accept provider authority or populate target paths.

## Controlling inputs

```text
member receipt review:
    review/generic-artifact-member-inventory-receipt-review.tsv

exact artifact registry:
    review/generic-artifact-member-comparison-artifacts.tsv

new canonical contract:
    review/generic-recipe-binding-and-drift-target-rules.tsv
    review/generic-recipe-binding-and-drift-target-metadata.tsv
```

Pinned source checkout:

```text
origin:
    https://github.com/termux-pacman/glibc-packages.git

HEAD:
    fd2ae25e04f3ea26d6c7b4678020814889331d86

tree:
    e502a4c18ab9092ec119e3a498a0bf192ef60e6f
```

Verified artifact cache:

```text
work/artifacts/generic-artifact-member-inventory/
```

The cache must contain the same 34 `.deb` artifacts previously verified by size, SHA-256 and control identity. No network acquisition is performed by this stage.

## Canonical denominator

```text
review identities:                         37
selected artifacts referenced by rows:     29
full verified cache artifacts rechecked:    34
unique pinned recipe roots:                28
family/version-aligned recipe candidates:  37
exact member rows already inspected:       21
drift target ELF rows:                     15
expected alias absent / correction needed:  1
```

All 37 recipe mappings are pinned to one exact recipe-tree object and one exact build-script blob. Artifact package version and the statically resolved recipe version/revision align for every row.

This alignment proves only a bounded recipe-lineage candidate:

```text
PINNED_RECIPE_FAMILY_VERSION_ALIGNED_NO_BUILD_ATTESTATION
```

It does not prove that the indexed artifact was built from that recipe tree. No build log, reproducible-build attestation, signed provenance or independent byte reproduction is available.

## Recipe evidence inventory

Implementation:

```text
recipe/collect-generic-recipe-binding-and-drift-target-elf.py
recipe/run-generic-recipe-binding-and-drift-target-elf.sh
```

For each of the 28 recipe roots, the collector verifies:

```text
recipe subtree Git tree ID;
build.sh blob ID and content SHA-256;
complete recipe-file manifest SHA-256;
recipe file and patch/subpackage/hook cardinalities;
source declaration and source SHA-256 retained in the canonical rule;
artifact package/version/architecture/byte identity;
source checkout and artifact-cache immutability.
```

Termux-specific recipe evidence is inventoried with bounded tokens such as:

```text
PATCH_FILE
SUBPACKAGE_SCRIPT
LAYOUT_OR_HOOK
EXTRA_CONFIGURE_ARGS
CUSTOM_TERMUX_STEP
TERMUX_PREFIX_REFERENCE
BUILD_IN_SRC
PACKAGE_REVISION
```

The resulting state is:

```text
PINNED_RECIPE_ADAPTATION_EVIDENCE_INVENTORIED_REVIEW_OPEN
```

Presence of a patch or Termux-specific build function is not an adaptation acceptance decision. The semantic effect and necessity of those deltas remain open.

## Drift-target ELF inspection

For the 15 rows classified by `0144` as:

```text
EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT
```

the collector opens the already verified `.deb` with:

```text
dpkg-deb --fsys-tarfile
```

It streams only the unique regular symlink target into bounded memory and records:

```text
normalized member path;
member size and mode;
member SHA-256;
ELF class, byte order and machine;
DT_SONAME;
comparison with the expected SONAME alias.
```

It does not call tar extraction methods and does not create a payload tree.

Expected passing state:

```text
DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED
```

A matching `DT_SONAME` strengthens candidate object/member evidence. It does not prove workload compatibility, recipe provenance, adaptation acceptance, necessity or final provider authority.

## `libjpeg.so.62` boundary

The current `libjpeg-turbo-glibc` artifact contains the `.so.8` family and no `libjpeg.so.62` alias. This stage does not inspect `.so.8` as a substitute for `.so.62`.

```text
NOT_APPLICABLE_EXPECTED_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED
```

A correct exact candidate or explicit source correction remains required.

## Collector outputs

A passing receipt contains:

```text
analysis.status
source-repository-state.tsv
artifact-verification.tsv
recipe-file-inventory.tsv
recipe-binding-review.tsv
drift-target-elf-review.tsv
summary.tsv
claim-boundary.txt
next-state.txt
```

The receipt contains no cached `.deb` files and no source checkout archive.

## Validation

Repository validation covers:

```text
37-row canonical denominator and stop states;
21 / 15 / 1 review-class cardinalities;
28 pinned recipe-root identities;
forbidden package, source-network and extraction command scan;
synthetic pinned source checkout and exact recipe-tree verification;
synthetic cached .deb control/byte verification;
stream-only target ELF SHA-256 and SONAME parsing;
source checkout and artifact cache immutability;
zero authority and zero target-population assertions.
```

The synthetic fixture is independent of caller `umask`, and no repository smoke uses an interactive stdin.

## Next valid state

```text
RUN_BOUNDED_GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_COLLECTOR
```

After receipt collection, review the 37 recipe-lineage rows and the 15 target-ELF observations. Keep artifact-to-recipe binding open unless independent build provenance or byte reproduction closes it.

## Stop line

Do not:

```text
treat family/version/tree alignment as build attestation;
treat recipe patches or Termux-specific functions as accepted adaptation;
treat a matching drift-target SONAME as final compatibility or provider authority;
treat libjpeg.so.8 as libjpeg.so.62;
fetch or update the pinned source checkout;
install, remove, upgrade or downgrade packages;
execute maintainer scripts;
extract .deb payloads into a filesystem tree;
populate target paths, aliases, modes or owners;
write or run a materializer;
modify generation/current, launcher, loader state or RPATH.
```
