# 0140 — Selected Obsidian Non-Priority Generic Exact-Candidate Evidence Collector

## Status

Repository-side collector implementation completed at:

```text
branch:
    docs/post-graphics-architecture-audit

base HEAD:
    2a6a428e5d618c4ac3203d6cdb8bed6107963a1b

base tree:
    ef70af3c867d49dcbd8503f4a26ff04451db9038
```

Verdict:

```text
61-object exact-candidate search contract:
    PASS / CANONICAL

read-only apt/source/cache collector:
    READY FOR DEVICE EXECUTION

exact repository artifact candidate discovery:
    NOT YET EXECUTED ON DEVICE

object-to-artifact member binding:
    OPEN

semantic final provider authority:
    OPEN

ApplicationRuntimeComposition:
    NOT REACHED

target population, extraction, materialization and activation:
    BLOCKED
```

This transaction adds a bounded evidence collector. It does not install, remove, upgrade, download, fetch source, build, extract a `.deb`, execute a provider, populate a target, materialize a successor or alter `current`.

## Authority and inputs

Controlling order remains:

```text
0116 provider-authority intervention
    -> 0135 architecture-audit corrections
    -> 0136 normalized coverage and registry state
    -> 0137 world/locale/loader lifecycle boundary
    -> 0138 application identity and launcher boundary
    -> 0139 generic source-class boundary
    -> this exact-candidate evidence collector
```

Canonical repository inputs are:

```text
review/non-priority-generic-authority-ledger.tsv
review/non-priority-generic-authority-ledger/*.tsv
review/generic-source-authority-boundary.tsv
review/generic-exact-candidate-search-tokens.tsv
review/unresolved-authority-ledger.tsv
```

Retained device inputs are read only:

```text
$PREFIX/etc/apt
$PREFIX/var/lib/apt/lists
$PREFIX/var/cache/apt/archives
$PREFIX/var/lib/dpkg/status

experiments/glibc/selected-obsidian-provider-authority/work/source/
    termux-pacman-glibc-packages
```

The source checkout must remain a full, clean, non-bare checkout at the previously accepted pin:

```text
fd2ae25e04f3ea26d6c7b4678020814889331d86
```

No network operation is permitted during collection.

## Canonical search contract

`review/generic-exact-candidate-search-tokens.tsv` contains exactly 61 rows, one for every non-priority generic identity.

Each row records:

```text
evidence identity and capability partition;
lookup name and SONAME;
Debian/rootfs oracle package and version;
bounded search tokens;
candidate-only state;
open object-member binding state;
unresolved final provider state;
blocked target population state.
```

Search tokens are discovery hints only. They do not prove package ownership, object membership, ABI compatibility, Termux/Android adaptation, necessity or final authority.

## Collector behavior

Implementation:

```text
recipe/collect-generic-exact-candidate-evidence.py
recipe/run-generic-exact-candidate-evidence.sh
```

The collector:

1. verifies the canonical 61-row denominator and stop states;
2. snapshots retained apt, dpkg and cached `.deb` inputs by size and SHA-256;
3. verifies the pinned source checkout HEAD, tree, refs, clean state and connectivity;
4. parses already-present `Packages` indexes without `apt update`;
5. inventories current pinned `gpkg` recipes and source declarations without `git fetch`;
6. derives object-to-package and object-to-recipe candidate edges;
7. records exact repository `Filename`, `Size` and `SHA256` fields where available;
8. records recipe tree, version, source URL, source SHA-256, dependencies and file/blob identities;
9. hashes matching cached `.deb` files without extraction;
10. proves apt/dpkg/cache and source-repository state are unchanged after collection.

Candidate discovery states are:

```text
APT_AND_RECIPE_CANDIDATE
APT_ONLY_CANDIDATE
RECIPE_ONLY_CANDIDATE
NO_CANDIDATE_FOUND_IN_RETAINED_INPUTS
```

These states describe retained evidence coverage only.

## Explicit non-claims

Even an `APT_AND_RECIPE_CANDIDATE` edge does not establish:

```text
that the candidate artifact contains the named object;
that artifact bytes equal the accepted oracle bytes;
that the recipe built the indexed artifact;
that patches provide the required Termux/Android adaptation;
that the object belongs in a coherent provider set;
that the candidate is necessary for an accepted workload;
that the candidate is the final provider;
that the candidate may be populated into a target.
```

`.deb` extraction is deliberately excluded. Object/member comparison requires a separately reviewed bounded transaction after this receipt is inspected.

## Outputs

A passing device receipt contains:

```text
analysis.status
summary.tsv
claim-boundary.txt
next-state.txt
source-repository-state.tsv
apt-index-files.tsv
apt-candidate-records.tsv
recipe-candidate-records.tsv
recipe-file-manifest.tsv
cached-deb-candidates.tsv
object-candidate-edges.tsv
input/
recipe-files/
```

Expected next state:

```text
READY_FOR_GENERIC_CANDIDATE_ARTIFACT_MEMBER_COMPARISON_OR_GAP_REVIEW
```

The receipt is archived as `.tar.zst` with a basename-only SHA-256 sidecar.

## Validation

Repository validation includes:

```text
61-row denominator and unique identity check;
all rows candidate-only, final-provider unresolved and target blocked;
forbidden package/network/source-fetch/deb-extraction command scan;
synthetic apt index and pinned source-repository execution;
61-row output coverage;
non-zero candidate discovery in the synthetic fixture;
source and apt input immutability checks;
existing generic/application/repository smoke regression.
```

## Ledger effect

`AUTH-009` remains:

```text
OPEN_OBJECT_SOURCE_BINDING
```

The repository is now ready to gather exact candidate identities without broadening authority. No provider, package, object, source tree or target row is accepted by this implementation transaction.

## Next valid task

```text
RUN_NON_PRIORITY_GENERIC_EXACT_CANDIDATE_EVIDENCE_COLLECTOR
```

After receipt review, choose exactly one of:

```text
bounded cached-artifact member comparison;
bounded download-only artifact acquisition proposal;
source/recipe gap correction;
candidate rejection because no coherent exact source exists.
```

Do not compose providers or populate targets from search-token matches.
