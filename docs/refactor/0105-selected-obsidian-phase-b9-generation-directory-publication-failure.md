# 0105 — Selected Obsidian Phase B9 Generation-Directory Publication Failure

## Status

The second Phase B9 attempt advanced through complete content-object publication and staged-generation construction, then failed while publishing the frozen generation directory.

```text
analysis.status:
    FAIL

failure stage:
    generation_publication

runtime launch:
    NO

promoted runtime mutation:
    NO
```

This is a second materializer implementation failure. It does not invalidate the completed Phase B8 plan or the 96 successfully published content objects.

## Authoritative failure receipt

Archive:

```text
selected-obsidian-phase-b9-staging-generation-materialization-corrected-20260712-001103.tgz
```

Archive SHA-256:

```text
20b191e2c834192dcf60b76ce16417344bc43d4997132f29220d27a41ab99a13
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    d44de24d7af612858ad51726355dcef3137ee1bc
```

The archive contained 36 safe members under one relative Termux path.

```text
regular files:
    34

directories:
    2

absolute paths:
    0

parent traversal:
    0

symlink/hardlink/device/special archive members:
    0
```

## Completed gates

All 19 required Phase B8 inputs were present and marked `PASS`.

Source-at-copy identity:

```text
checks:
    133

MATCH:
    133

failures:
    0
```

Strict schema generation:

```text
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

`current` was absent before the transaction.

## Content-object publication result

The corrected object publication primitive was accepted exactly as reviewed:

```text
base materializer expected Git blob:
    98a188a314178e345049cfe296c51d60a485fc2a

base materializer observed Git blob:
    98a188a314178e345049cfe296c51d60a485fc2a

publication primitive:
    libc.renameat2

flags:
    RENAME_NOREPLACE

overwrite-capable fallback:
    disabled
```

Publication attempts:

```text
attempts:
    96

PUBLISHED:
    96

failed:
    0
```

Materialized content:

```text
objects:
    96

CREATED:
    96

bytes:
    70,897,301
```

Every object-materialization row matches the accepted Phase B8 content-object plan for content kind, SHA-256, and object path.

The 96 content-addressed objects are valid retained state and should be reused after live hash verification. They must not be blindly deleted.

## Failure

After staged-generation construction, validation, fsync, and owner-read-only freeze, the base materializer attempted:

```text
os.rename(
    staging/obsidian-cpu-435ac66d15de2e9a3188.stage-31354-1783782664754429970,
    generations/obsidian-cpu-435ac66d15de2e9a3188,
)
```

Observed exception:

```text
PermissionError: [Errno 13] Permission denied
```

The failure occurred after the staged root had been changed to mode `0555`.

The receipt proves that the ordinary directory rename was denied in that state. It does not by itself prove whether the denial came from source-root mode, Python/libc syscall selection, directory contents, or another Android filesystem/security rule.

## Partial-state boundary

Present in the receipt:

```text
object-materialization.tsv
    96 CREATED rows

publication-primitive-attempts.tsv
    96 PUBLISHED rows
```

Absent because publication did not complete:

```text
generation-validation.tsv
current-state-after.tsv
summary.tsv
```

The base exception handler attempts to remove the unique staged generation and schema-build directory. Archive evidence cannot prove the resulting live filesystem state.

The final generation should be absent because the rename returned `EACCES`, but this must be confirmed on-device before the next run.

## Corrective design

The corrected entry point now also controls generation-directory publication.

Before publishing the real generation, it performs a same-boundary empty-directory probe:

```text
staging probe root mode 0555
    -> renameat2 RENAME_NOREPLACE

if EACCES or EPERM:
    change probe root to 0700
    -> renameat2 RENAME_NOREPLACE
```

Selected production behavior:

```text
frozen probe succeeds:
    publish the frozen generation directly with renameat2 RENAME_NOREPLACE

frozen probe denied but writable probe succeeds:
    temporarily change only the complete staged root from 0555 to 0700
    publish with renameat2 RENAME_NOREPLACE
    immediately change the published root back to 0555
    fsync the root and generations directory before returning
```

All generation children remain frozen before publication. No ordinary overwrite-capable rename fallback is accepted.

The writable-root path is permitted only after an explicit same-boundary `0555` failure and `0700` success. The chosen behavior and errno are recorded in:

```text
generation-publication-attempts.tsv
```

## Crash boundary

If the root-thaw path is required, there is a narrow internal interval after no-overwrite publication and before root refreeze when the complete final generation root is mode `0700`.

This is not activation:

```text
current remains absent or unchanged;
no launcher references the generation;
all child files and directories are already immutable;
the wrapper refreezes and fsyncs before returning to the base validator.
```

A process crash in that narrow interval would leave a complete but root-writable final generation. A later run must reject or explicitly repair that state; it must not silently claim immutable publication.

## Claim boundary

This receipt proves:

```text
all 133 source identities remained stable;
strict schema reproduction remained byte-identical;
all 96 content objects were atomically published with no-overwrite semantics;
the staged generation reached the publication step;
ordinary frozen-directory rename was denied;
current was absent before the transaction.
```

It does not prove:

```text
the live staged directory was removed;
the final generation is absent;
current remained absent after failure;
the new probed generation-publication path passes;
explicit-generation selection or workload behavior.
```

## Next action

Do not rerun Phase B1-B8.

Inventory live state, then rerun the corrected Phase B9 entry point at the new repository head. The 96 existing content objects should be verified and reported as reused.

## Stop line

Do not:

```text
delete the 96 content objects;
retry the old corrected entry point at d44de24;
use ordinary overwrite-capable rename;
create current;
launch Obsidian;
change the promoted launcher;
garbage-collect failed staging entries before inventory.
```
