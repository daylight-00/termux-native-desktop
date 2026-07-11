# 0100 — Selected Obsidian Phase B6 Source-Manifest Gap

## Status

The first Phase B6 receipt completed, but its reported next state is not the correct architectural interpretation.

```text
analysis.status:
    PASS

reported next state:
    REVIEW_SCHEMA_COMPILER_VERSION_DIFFERENCE

correct interpretation:
    REVIEW_SCHEMA_SOURCE_MANIFEST_GAP

runtime launch:
    NO

promoted runtime mutation:
    NO
```

The receipt remains valid as a diagnostic run. It does not prove a compiler-version difference because the attempted source set was incomplete.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b6-gsettings-schema-reproduction-20260711-220355.tgz
```

Archive SHA-256:

```text
553e52f917a6cc72e805ac8b94bb5fd7d8ecc36809d6c6b5e2e6b226a901b30a
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    68f3de93413dddb861e34d899bc06c49c3363c49
```

The archive contained 103 safe members under one relative Termux path. It contained no absolute path, parent traversal, symlink, hardlink, device, or special member.

## Primary receipt result

```text
Phase B5 source files consumed:
    36

source verification failures:
    0

compiler candidates present:
    1

runnable compiler candidates:
    1

compiler:
    $PREFIX/bin/glib-compile-schemas

compiler package:
    glib

compiler version:
    2.88.2

compiler SHA-256:
    5f8cfe28f5eed9e5b9400260ec0127cae5c3f881437915df3fcdca33cbe5d165

compile attempts:
    2

reported successful compiles:
    1

byte-identical outputs:
    0
```

Retained aggregate SHA-256:

```text
457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938
```

Default generated aggregate SHA-256:

```text
d15ce31342848a753b95d2bf825201474b2c1e83a8a7db6e98719234196443c5
```

## Why the reported version-difference state is not accepted

The default compiler attempt returned zero and emitted an aggregate, but stderr reported ten schema errors.

The compiler ignored these complete files:

```text
org.gnome.desktop.a11y.magnifier.gschema.xml
org.gnome.desktop.a11y.mouse.gschema.xml
org.gnome.desktop.background.gschema.xml
org.gnome.desktop.interface.gschema.xml
org.gnome.desktop.peripherals.gschema.xml
org.gnome.desktop.privacy.gschema.xml
org.gnome.desktop.screensaver.gschema.xml
org.gnome.desktop.wm.preferences.gschema.xml
org.gnome.system.location.gschema.xml
org.gnome.system.proxy.gschema.xml
```

Representative error:

```text
<enum id='org.gnome.desktop.GDesktopBackgroundStyle'> not (yet) defined
This entire file has been ignored.
```

The strict attempt stopped at the first missing enum definition:

```text
return code:
    1

generated aggregate:
    absent
```

Independent XML inspection found 33 referenced enum/flags identifiers with no definition in the copied 36-file set.

Therefore:

```text
default return code 0:
    not a clean successful compile

generated hash difference:
    caused at least by ignored schema files

compiler version difference:
    not yet isolated
```

## Root cause

Phase B5 discovered schema inputs using only:

```text
*.gschema.xml
*.gschema.override
```

That suffix filter omitted definition XML files whose names do not end in `.gschema.xml`.

Phase B6 trusted that incomplete manifest and copied only those 36 files.

The observed compiler errors are consistent with missing enum-definition XML input, not with a valid complete-source compile that merely serializes differently.

## Consequence for prior decisions

The following Phase B5 conclusions remain valid:

```text
17 retained data bytes are stable;
12 locale files are world-owned glibc data;
4 selected font files have exact package ownership;
the 36 captured schema XML/override files are package-owned.
```

The following conclusion must be narrowed:

```text
old claim:
    complete schema source ownership is closed

corrected claim:
    ownership of the 36 captured sources is closed;
    complete schema-source closure is still open
```

Candidate materialization remains blocked.

## Corrective action

A corrected Phase B6 must discover the source set from the retained schema directory rather than trusting the Phase B5 suffix filter.

It must:

```text
discover all relevant XML plus override inputs;
record the delta from the 36-file B5 manifest;
verify byte identity and package ownership for newly discovered inputs;
copy the complete discovered set to receipt-local directories;
run default and strict compiler modes;
reject return code 0 when stderr reports schema errors or ignored files;
compare only clean generated aggregates with the retained aggregate.
```

Possible corrected next states:

```text
READY_FOR_COMPLETE_DATA_MANIFEST
    clean byte-identical reproduction

REVIEW_SCHEMA_COMPILER_VERSION_DIFFERENCE
    clean compile succeeds but differs

REVIEW_SCHEMA_COMPILATION_ERRORS
    compiler is runnable but no clean compile succeeds

ACQUIRE_SCHEMA_COMPILER_ORACLE
    no runnable candidate exists
```

## Claim boundary

The first Phase B6 proves:

```text
a native Termux glib-compile-schemas 2.88.2 candidate exists;
the candidate identity and package owner are explicit;
the 36-file B5 manifest is internally stable;
the manifest is insufficient for clean schema compilation;
the default compiler can return zero while ignoring invalid/incomplete inputs.
```

It does not prove:

```text
a complete schema source set;
a clean generated aggregate;
a compiler-version-only difference;
aggregate reproducibility;
readiness for candidate materialization.
```

## Stop line

Do not:

```text
accept the default generated aggregate;
interpret return code zero as clean success without stderr inspection;
classify the hash difference as compiler-version-only;
install another compiler before correcting source discovery;
rerun Phase B1-B5;
materialize the candidate before corrected schema reproduction passes.
```
