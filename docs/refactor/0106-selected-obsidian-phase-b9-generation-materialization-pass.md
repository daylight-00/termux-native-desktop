# 0106 — Selected Obsidian Phase B9 Generation Materialization Pass

## Status

Corrected Phase B9 passed.

```text
analysis.status:
    PASS

next state:
    READY_FOR_EXPLICIT_GENERATION_VALIDATION

publication state:
    PUBLISHED_NEW_GENERATION

runtime launch:
    NO

current pointer changed:
    NO

promoted runtime mutation:
    NO
```

The selected CPU content store and one immutable generation now exist. The generation is not activated.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136.tgz
```

Archive SHA-256:

```text
ad351651e82d958c1805eed421dc9991ee573b1f79794c34aea6f079df84ec53
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    57aa19febd6df33435afd074eb3b47c150768998
```

The archive contained 41 safe members under one relative Termux path.

```text
regular files:
    39

directories:
    2

absolute paths:
    0

parent traversal:
    0

symlink/hardlink/device/special archive members:
    0
```

## Input and source gates

All nineteen required Phase B8 inputs were present and marked `PASS`.

```text
source identity checks:
    133

source identity MATCH:
    133

source identity failures:
    0
```

Distribution:

```text
selected ELF:
    91

selected fonts:
    4

GSettings sources:
    37

GSettings compiler:
    1
```

## Schema generation

```text
compiler:
    $PREFIX/bin/glib-compile-schemas

compiler SHA-256:
    5f8cfe28f5eed9e5b9400260ec0127cae5c3f881437915df3fcdca33cbe5d165

mode:
    strict

return code:
    0

stdout:
    empty

stderr:
    empty

generated SHA-256:
    457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938

expected SHA-256:
    457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938
```

## Content-object result

The 96 objects created by the preceding failed publication attempt were retained and independently verified.

```text
content objects:
    96

created this run:
    0

reused after hash verification:
    96

content bytes:
    70,897,301
```

The object-materialization rows exactly match the accepted Phase B8 content-object plan for:

```text
content kind;
SHA-256;
source identity;
object-store relative path.
```

No new object-publication syscall was required in this run, so `publication-primitive-attempts.tsv` contains only its header.

## Generation publication mode

The corrected entry point accepted the exact reviewed base materializer Git blob:

```text
expected:
    98a188a314178e345049cfe296c51d60a485fc2a

observed:
    98a188a314178e345049cfe296c51d60a485fc2a
```

Generation publication probes established the device behavior:

```text
PROBE_FROZEN_ROOT
    source mode: 0555
    primitive: libc.renameat2 RENAME_NOREPLACE
    result: EACCES

PROBE_WRITABLE_ROOT
    source mode: 0700
    primitive: libc.renameat2 RENAME_NOREPLACE
    result: PUBLISHED

GENERATION_PUBLICATION
    source mode: 0700_THEN_0555
    primitive: libc.renameat2 RENAME_NOREPLACE
    result: PUBLISHED
```

The final generation root was restored to `0555` and fsynced before immutable validation.

No overwrite-capable rename fallback was enabled.

## Published generation

```text
generation ID:
    obsidian-cpu-435ac66d15de2e9a3188

generation directory:
    $HOME/gl/selected/obsidian/generations/obsidian-cpu-435ac66d15de2e9a3188

aliases:
    175

content objects:
    96
```

The generation contains aliases, manifests, and receipts. Content bytes remain in the shared SHA-256 object store.

## Generation validation

The printed failure view contained only the table header because every validation row passed.

```text
validation rows:
    1851

PASS:
    1851

FAIL:
    0
```

Independent structural reconstruction:

```text
staging-generation checks:
    912

final-generation checks:
    939

combined:
    1851
```

Check distribution:

```text
alias_is_symlink:
    350

alias_target_text:
    350

alias_resolves_to_object:
    350

alias_object_hash:
    350

object_hash:
    192

object_not_owner_writable:
    192

manifest_hash:
    36

generation_node_not_owner_writable:
    27

generation_root_plain_directory:
    2

alias_path_set:
    2
```

The doubled alias/object/manifest checks represent validation before and after publication. Immutable-node checks apply to the final published generation.

## Current-pointer boundary

```text
before:
    ABSENT

after:
    ABSENT

changed:
    NO
```

The published generation is not selected by `current`, the promoted launcher, or any workload receipt.

## Materialization result

```text
candidate bytes materialized:
    YES

immutable generation published:
    YES

explicit generation selected:
    NOT YET

current activated:
    NO

workload equivalence:
    NOT PROVEN
```

## Next validation claim

Explicit-generation validation must:

```text
use the final generation absolute path, not current;
use the generation lib directory instead of the broad farm;
set GSETTINGS_SCHEMA_DIR to the generation schema directory;
scope selected-font discovery to the generation font directory;
isolate mutable XDG state under the validation receipt;
run CPU mode with exact --disable-gpu;
observe main, renderer, and zygote survival;
observe no GPU process;
prove mapped selected bytes resolve to the 96 object-store paths;
prove no rootfs provider or broad-farm object is mapped;
prove app-local and protected-world identities remain unchanged;
leave current absent or unchanged.
```

The expected regular mapped identity set is:

```text
selected object-store identities:
    96

app-local identities:
    11

protected-world identities:
    18

expected total:
    125
```

The eleven excluded graphics-feature identities must remain absent in CPU mode.

## Claim boundary

Phase B9 proves:

```text
all copy-time sources matched;
strict schema generation reproduced the accepted aggregate;
the 96 object-store entries are present and hash-correct;
the 175-alias generation is complete;
the final generation is owner-non-writable;
generation publication uses a device-probed no-overwrite transaction;
current did not change.
```

Phase B9 does not prove:

```text
the dynamic loader selects the generation;
all expected generation objects are mapped;
rootfs and broad-farm leakage are absent at runtime;
process topology and survival;
font and schema consumption;
activation or rollback;
control equivalence.
```

## Direction decision

```text
Phase B9:
    CLOSED / PASS

content-store materialization:
    CLOSED

immutable generation publication:
    CLOSED

current activation:
    NOT STARTED

next action:
    EXPLICIT-GENERATION CPU RUNTIME VALIDATION
```

## Stop line

Do not:

```text
rerun Phase B1-B9 without a source or validation trigger;
create current before explicit-generation validation;
change the promoted launcher;
run the candidate through the broad farm;
include the excluded graphics feature in CPU validation;
mutate the published generation;
garbage-collect the generation or its objects.
```
