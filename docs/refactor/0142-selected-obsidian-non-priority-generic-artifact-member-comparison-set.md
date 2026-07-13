# 0142 — Selected Obsidian Non-Priority Generic Artifact/Member Comparison Set

## Status

The exact retained candidate receipt has been narrowed into a named artifact/member comparison contract.

```text
direct-family identities:
    37

exact indexed artifacts in download/member-inventory scope:
    34

identity-to-artifact member-search edges:
    44

compressed bytes if the full named set is later acquired:
    51,771,348

static/development artifacts excluded from download scope:
    15

network download performed by this transaction:
    NO

.deb extraction performed by this transaction:
    NO

authority decisions accepted:
    0

target rows populated:
    0
```

Verdict:

```text
named comparison set:
    DEFINED / BOUNDED

exact artifact acquisition:
    NOT PERFORMED

object-to-artifact member binding:
    OPEN

artifact-to-recipe build binding:
    OPEN

Termux/Android adaptation acceptance:
    OPEN

final provider authority:
    OPEN

ApplicationRuntimeComposition:
    NOT REACHED

target population, materialization and activation:
    BLOCKED
```

`AUTH-009` remains `OPEN_OBJECT_SOURCE_BINDING`.

## Inputs and locks

The definition is derived only from:

```text
bounded candidate receipt:
    termux-native-desktop-generic-exact-candidate-evidence-result-20260713T034510Z.tar.zst

receipt archive SHA-256:
    361d2105c57c6ce3f446de16aedd966a55593fbba4e77d8a40e92b857ca02ea7

apt candidate table SHA-256:
    328b5df70eba851036ba8069d0bace69d5a0d29f1e433b0a9a8d2a6bb3f942f6

canonical reviewed receipt SHA-256:
    cc160e340e78491a6b6e1659ff8e4a52636da99dcc382a16498d67c6c2b95e11

repository metadata identity:
    repository-metadata:01

repository base:
    https://packages-cf.termux.dev/apt/termux-glibc/

Packages index SHA-256:
    565df3058a51a200fd83e851cce2d99a2faa2277142c50adc20f071d6c7b4a3a
```

The repository trust policy remains open. Captured index and artifact identities are exact bounded evidence, not a claim that future mutable repository state is trusted or retained.

## Canonical products

```text
review/generic-artifact-member-comparison-artifacts.tsv
    34 exact artifact identities selected for a later download-only transaction

review/generic-artifact-member-comparison-edges.tsv
    44 named object-to-artifact member-search edges covering all 37 direct identities

review/generic-artifact-member-comparison-exclusions.tsv
    15 exact static/development artifacts excluded from the dynamic member search

review/generic-artifact-member-comparison-metadata.tsv
    input locks, output hashes, cardinalities, byte total and claim boundary
```

Generator:

```text
recipe/define-generic-artifact-member-comparison-set.py
```

The generator performs no network access, package operation, `.deb` inspection, extraction or target mutation.

## Download/member-inventory scope

The 34 named artifacts are exact indexed identities. They include runtime or split-package candidates such as:

```text
alsa-lib-glibc
dbus-glibc
glib-glibc
libcairo-glibc
libgnutls-glibc
libnettle-glibc
libsqlite-glibc
mesa-glibc
mesa-vulkan-icd-freedreno-glibc
mesa-vulkan-icd-swrast-glibc
pango-glibc
util-linux-glibc
```

The complete set is hash-, size-, version-, architecture-, repository-path- and Packages-index-bound.

Member search is exact-basename-oriented. A later collector may determine whether a named `.deb` data archive contains the requested identity, but it may not install the package or execute payloads or maintainer scripts.

## Edge cardinality

```text
31 identities:
    one named artifact candidate

5 identities:
    two named artifact candidates

1 identity:
    three named artifact candidates
```

The multi-artifact rows are retained because package-family evidence alone cannot determine split-package ownership. Examples include:

```text
sqlite / libsqlite
Mesa core versus Vulkan ICD subpackages
gnutls / libgnutls
nettle / libnettle
libmount / util-linux
```

Exact member inventory is required before reducing these edges.

## Explicit exclusions

Fourteen `*-glibc-static` artifacts are excluded from the download set:

```text
reason:
    STATIC_ONLY_PACKAGE_OUTSIDE_DYNAMIC_MEMBER_SEARCH
```

One `mesa-dev-glibc` artifact is excluded:

```text
architecture:
    all

reason:
    ARCH_ALL_DEVELOPMENT_PACKAGE_OUTSIDE_AARCH64_ELF_MEMBER_SEARCH
```

These exclusions do not claim that the packages are invalid or globally unnecessary. They establish only that static archives and an architecture-independent development package are outside the named search for selected aarch64 dynamic ELF members.

Every one of the 37 direct identities retains at least one non-excluded exact artifact edge.

## Indirect and absent identities

The following remain outside the comparison set:

```text
INDIRECT_TOKEN_ONLY:
    13

NO_RETAINED_CANDIDATE:
    11
```

No artifact is downloaded merely because a broad token appeared in dependency, description, patch or unrelated recipe metadata.

Absence from the retained snapshot remains a source-correction gap rather than a rejection of all possible providers.

## Claim boundary

This stage establishes:

```text
which exact indexed artifacts are permitted in the next bounded comparison;
which named selected identity each artifact may be searched for;
which static/development artifacts are outside that dynamic-member search;
that all 37 direct-family identities remain covered;
the exact maximum compressed download set and repository metadata lock.
```

It does not establish:

```text
that an artifact contains the requested member;
that a matching member has the required SONAME or ABI;
that indexed artifact bytes were built from the pinned recipe tree;
that recipe patches provide the required Android adaptation;
that a candidate is necessary for the final runtime;
that any candidate has final provider authority;
that any artifact path, mode, owner or alias is target policy;
that any target may be populated.
```

## Validation

Repository validation checks:

```text
34 artifact rows;
44 comparison edges;
15 explicit exclusions;
37/37 direct identity coverage;
zero indirect-only or absent identities in the edge set;
51,771,348 exact compressed bytes;
14 static exclusions and one architecture-all development exclusion;
all artifact/member/adaptation/final states remain open or unresolved;
all target states remain BLOCKED;
network download, `.deb` extraction, authority acceptance and target population remain zero;
deterministic regeneration from the canonical reviewed receipt and exact artifact identities;
existing receipt-review, collector, source-boundary, application-boundary and repository smoke regression.
```

## Next valid task

```text
IMPLEMENT_BOUNDED_GENERIC_ARTIFACT_MEMBER_INVENTORY_COLLECTOR
```

The next transaction may implement a collector that:

```text
downloads only the 34 exact named artifacts;
accepts only the locked repository base and exact repository paths;
verifies exact size and SHA-256 before inspection;
reuses only a byte-identical private artifact cache;
inventories control and data archive members without installation;
records exact-basename and ELF SONAME matches;
executes no package payload or maintainer script;
keeps every authority and target state open or blocked.
```

It must not install packages, update apt indexes, follow unapproved redirects, compose a runtime, populate targets or mutate the selected generation/current/launcher/loader state.
