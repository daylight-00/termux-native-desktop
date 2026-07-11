# 0103 — Selected Obsidian Phase B8 Generation-Layout Preflight Pass

## Status

Phase B8 passed.

```text
analysis.status:
    PASS

next state:
    READY_FOR_STAGING_MATERIALIZER_IMPLEMENTATION

runtime launch:
    NO

candidate bytes materialized:
    NO

promoted runtime mutation:
    NO
```

The result closes the read-only source-identity, immutable-content, combined-alias, and activation-contract preflight.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b8-generation-layout-preflight-20260711-231228.tgz
```

Archive SHA-256:

```text
d68205e9bf99f9a0d711068c560ac5047a5560f31d109efe7aeac107002d31e8
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    37c64a0c55fb76b71532888a1b603c4610c2aec0
```

The archive contained 30 safe members under one relative Termux path.

```text
regular files:
    28

directories:
    2

absolute paths:
    0

parent traversal:
    0

symlinks/hardlinks/devices/special members:
    0
```

All eleven required Phase B7 files were embedded and marked `PASS`.

## Repository-state note

The device showed:

```text
?? experiments/glibc/selected-obsidian-closure/recipe/__pycache__/
```

This is an untracked Python bytecode directory created by syntax checking.

The Phase B8 repository gate intentionally used:

```text
git status --porcelain --untracked-files=no
```

Therefore the directory did not affect the exact tracked-HEAD gate and did not invalidate the receipt.

It should be removed before the next command sequence to keep the working tree visually clean:

```bash
rm -rf experiments/glibc/selected-obsidian-closure/recipe/__pycache__
```

No architectural claim depends on this cleanup.

## Source identity result

```text
source identity checks:
    133

source identity failures:
    0
```

Distribution:

```text
selected ELF sources:
    91

selected font sources:
    4

GSettings source XML/override files:
    37

GSettings compiler:
    1
```

All rows were `MATCH` against the accepted Phase B7 and corrected Phase B6 identities.

Approximate checked source-byte totals were:

```text
ELF:
    50,115,320 bytes

fonts:
    20,739,384 bytes

schema sources:
    143,986 bytes

schema compiler:
    50,032 bytes
```

These are source-preflight totals, not final generation disk-usage claims.

## Immutable content plan

```text
copied ELF content objects:
    91

copied font content objects:
    4

generated GSettings content objects:
    1

content plan rows:
    96

unique content hashes:
    96

duplicate content hashes:
    0
```

Content-addressed path rule:

```text
objects/sha256/<first-two-hex>/<full-sha256>
```

The 96-row content plan exactly matched:

```text
Phase B7 candidate ELF manifest;
Phase B7 selected-font rows;
Phase B7 schema build contract expected aggregate.
```

## Generation identity

```text
generation digest:
    435ac66d15de2e9a3188a31bde073ec778dfcb176190d104b513e643e7b4bc5b

generation ID:
    obsidian-cpu-435ac66d15de2e9a3188
```

The digest was independently recomputed from:

```text
Phase B7 head;
configured generation base;
96 canonical immutable content rows;
37 schema source identities and owners;
compiler identity;
accepted compile modes;
expected aggregate identity.
```

The independently computed digest and generation ID matched the receipt.

Including the configured generation base in the digest means the generation ID describes both content/build contract and deployment-base contract.

## Physical layout direction

```text
generation base:
    $HOME/gl/selected/obsidian

existing base ancestor:
    $HOME/gl

base device ID:
    65082
```

Planned paths:

```text
$HOME/gl/selected/obsidian/
    objects/sha256/
    staging/
    generations/
        obsidian-cpu-435ac66d15de2e9a3188/
    current
```

Explicit candidate paths:

```text
library:
    generations/obsidian-cpu-435ac66d15de2e9a3188/lib

fonts:
    generations/obsidian-cpu-435ac66d15de2e9a3188/share/fonts/selected

GSettings:
    generations/obsidian-cpu-435ac66d15de2e9a3188/share/glib-2.0/schemas
```

Phase B8 did not create any of these paths.

## Combined alias namespace

```text
ELF aliases:
    170

font aliases:
    4

schema aliases:
    1

total generation aliases:
    175

generation alias collisions:
    0
```

ELF alias composition:

```text
lookup-name aliases:
    91

additional source-basename aliases:
    79

additional distinct SONAME aliases:
    0
```

All selected SONAMEs equal their lookup names in this receipt, so SONAME aliases deduplicate into the lookup-name entries.

All 175 alias relative paths were unique.

For every alias, independent lexical resolution verified:

```text
generation/<alias-parent>/<relative-target>
    == generation-base/objects/sha256/<prefix>/<sha256>
```

No alias path contained an absolute component or parent traversal, and no relative target resolved outside the configured generation base.

## Activation contract

The accepted activation sequence is:

```text
materialize content-addressed objects;
construct a generation under same-filesystem staging;
validate hashes, aliases, manifests, and generated schema;
publish the complete immutable generation with one rename;
validate with the explicit generation path;
only then replace current with temporary-symlink + atomic rename.
```

`current` must not change during construction or explicit-generation validation.

## Rollback contract

```text
record the previously resolved current generation;
never mutate an immutable generation;
rollback by atomically replacing current with a symlink to the previous complete generation;
retain every generation referenced by current, previous-generation receipt, or active validation receipt.
```

Garbage collection remains out of scope.

## Launcher-selection contract

Candidate validation must use explicit paths and must not rely on:

```text
current;
the broad farm;
rootfs provider paths as final authority.
```

Required explicit boundaries include:

```text
candidate generation lib directory;
GSETTINGS_SCHEMA_DIR pointing at the candidate generation;
selected-font discovery scoped to the candidate generation or receipt-owned fontconfig input;
protected world glibc and locale referenced outside the generation;
app-local $ORIGIN locality preserved.
```

## Architecture consequence

The selected Obsidian CPU generation now has a complete read-only physical plan:

```text
96 immutable content identities;
175 collision-free generation aliases;
one deterministic generation ID;
one same-filesystem staging/publication contract;
one explicit-validation-before-activation contract;
one rollback contract.
```

The next stage may materialize candidate bytes, but it must remain non-activated.

## Claim boundary

Phase B8 proves:

```text
all materialization inputs still match their accepted identities;
the immutable content set has 96 unique hashes;
the combined alias namespace has 175 unique paths and zero collisions;
all planned relative aliases resolve to the intended object-store entries;
the generation ID is reproducible;
staging/publication/activation/rollback boundaries are explicit.
```

Phase B8 does not prove:

```text
content objects were written safely;
a generated schema was rebuilt during materialization;
a generation directory exists;
filesystem permissions or crash-durability are correct;
the explicit generation loads or runs;
current activation or rollback works.
```

## Direction decision

```text
Phase B8:
    CLOSED / PASS

source identity preflight:
    CLOSED

content and alias plan:
    CLOSED

generation/activation design:
    READY FOR IMPLEMENTATION

candidate bytes:
    NOT MATERIALIZED

next action:
    STAGING-ONLY CONTENT/GNERATION MATERIALIZER + IMMUTABLE VALIDATOR
```

## Stop line

Do not:

```text
rerun Phase B1-B8 without a source trigger;
write selected objects into the broad live farm;
change current during materialization;
publish a partially validated generation;
use absolute generation aliases;
activate before explicit-generation loader/workload validation;
garbage-collect any object or generation before reference tracking exists.
```
