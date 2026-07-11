# 0104 — Selected Obsidian Phase B9 First-Run Hard-Link Publication Failure

## Status

The first Phase B9 materialization attempt failed at the first content-object publication operation.

```text
analysis.status:
    FAIL

failure stage:
    content_materialization

runtime launch:
    NO

promoted runtime mutation:
    NO
```

This is a materializer implementation failure. It does not invalidate the completed Phase B8 source, content, alias, or generation-layout preflight.

## Authoritative failure receipt

Archive:

```text
selected-obsidian-phase-b9-staging-generation-materialization-20260711-233842.tgz
```

Archive SHA-256:

```text
598313be19c38599aad0028fbfc183df2d505c0e8645c7270467f1e9ae3e9ba1
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    9272f8f20e89fec92a9d7772ba86ca2537cb4ea2
```

The archive contained 33 safe members under one relative Termux path.

```text
absolute paths:
    0

parent traversal:
    0

symlink/hardlink/device/special archive members:
    0
```

## Completed gates before failure

All 19 required Phase B8 inputs were present and marked `PASS`.

Source-at-copy identity recheck:

```text
checks:
    133

MATCH:
    133

failures:
    0
```

Distribution:

```text
ELF:
    91

fonts:
    4

schema sources:
    37

schema compiler:
    1
```

Strict GSettings generation completed cleanly:

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

`current` was absent before the transaction:

```text
state:
    ABSENT

path:
    $HOME/gl/selected/obsidian/current
```

## Failure

The materializer created and fsynced a temporary object, verified its hash, changed it owner-read-only, and attempted no-overwrite publication with `os.link()`.

The first object was:

```text
SHA-256:
    00396daf5ba60830460f12aa64c9e4edf52cb57dcb3546de772ac5b1f12c3807

object path:
    $HOME/gl/selected/obsidian/objects/sha256/00/00396daf5ba60830460f12aa64c9e4edf52cb57dcb3546de772ac5b1f12c3807
```

Observed exception:

```text
PermissionError: [Errno 13] Permission denied
```

The source temporary file and destination were in the same object-prefix directory. The device environment rejected the hard-link operation itself.

The receipt does not establish which Android kernel/LSM/filesystem policy produced `EACCES`; it establishes that hard-link publication is not an acceptable portable primitive for this deployment environment.

## Partial-state boundary

The failure occurred before a content object was successfully published.

The receipt has no:

```text
object-materialization.tsv
summary.tsv
generation-validation.tsv
current-state-after.tsv
```

Therefore it proves no successful content-object publication and no final-generation publication.

The script's exception cleanup attempts to remove the unique staging generation and schema-build directory. Empty generation-base, object-prefix, staging, or generations directories may remain and are harmless. Their device state must still be inspected before the corrected run.

No command should blindly delete a completed content object or generation path.

## Corrective design

Replace hard-link publication with Linux `renameat2(..., RENAME_NOREPLACE)`.

Required semantics:

```text
same-directory temporary file;
fully written and fsynced temporary byte;
verified SHA-256;
owner-read-only mode;
atomic rename;
no destination overwrite;
EEXIST mapped to existing-object verification;
unsupported syscall or other errno treated as failure;
object-directory fsync after publication.
```

The corrected entry point wraps the accepted base materializer and substitutes only the publication syscall. It verifies the exact Git blob of the base materializer before executing it.

No unsafe fallback to check-then-rename is accepted because that would reopen a race capable of replacing an existing content-addressed object.

## Claim boundary

This failure receipt proves:

```text
Phase B8 inputs remained stable at copy time;
strict schema generation remained reproducible;
current was absent before materialization;
hard-link publication is rejected on this device;
the materializer failed before final-generation publication.
```

It does not prove:

```text
all temporary directories were removed from the live filesystem;
renameat2 RENAME_NOREPLACE is supported;
any content object exists;
a generation exists;
current remained absent after the process without a device-side check.
```

## Next action

Run the corrected Phase B9 entry point after a narrow live-state inventory.

Do not rerun Phase B1-B8.

## Stop line

Do not:

```text
retry the uncorrected hard-link materializer;
replace the hard-link call with ordinary overwrite-capable rename;
blindly remove object-store or generation directories;
create current;
launch Obsidian;
change the promoted launcher.
```
