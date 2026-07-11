# 0107 — Selected Obsidian Phase B10 First-Run Launcher-Environment Failure

## Status

The first Phase B10 explicit-generation CPU validation failed before Obsidian was executed.

```text
analysis.status:
    FAIL

failure stage:
    capture

required process topology:
    NOT OBSERVED

runtime launch:
    NO OBSIDIAN PROCESS

current activation:
    NO
```

This is a launcher implementation failure. It does not invalidate the Phase B9 materialized generation.

## Authoritative failure receipt

Archive:

```text
selected-obsidian-phase-b10-explicit-generation-cpu-validation-20260712-005240.tgz
```

Archive SHA-256:

```text
0d983e798471c1a85ae17cfe1423f40e237963ecd4e7df1a8a5c838aefe5c211
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    3cadf35190cad9b6b2c675e0e8a7b714cb278371
```

The archive contained 42 safe members under one relative Termux path.

```text
absolute paths:
    0

parent traversal:
    0

symlink/hardlink/device/special archive members:
    0
```

## Pre-launch gates

The B9 generation was resolved from the completed receipt:

```text
generation ID:
    obsidian-cpu-435ac66d15de2e9a3188

generation directory:
    $HOME/gl/selected/obsidian/generations/obsidian-cpu-435ac66d15de2e9a3188
```

`current` was absent before the capture:

```text
state:
    ABSENT
```

The receipt-local launcher copy matched the repository launcher:

```text
source SHA-256:
    e668f9d9e398eb6fb7ebdde9252d20a9e73edf1963e6d9b4d08041c452636ad8

runtime copy SHA-256:
    e668f9d9e398eb6fb7ebdde9252d20a9e73edf1963e6d9b4d08041c452636ad8
```

Receipt-local XDG, temporary, fontconfig, and launcher roots were created successfully.

## Observed failure

The capture launcher PID was created, but no process-tree member survived long enough to be observed.

```text
launch PID:
    25474

poll-observed rows:
    0

last process rows:
    0

main/renderer/zygote:
    0 / 0 / 0
```

`launch.stderr` contained:

```text
CANNOT LINK EXECUTABLE "mkdir":
"$PREFIX/glibc/lib/libc.so" has bad ELF magic: 2f2a2047
```

The first four magic bytes decode to:

```text
/* G
```

which is source/linker-script text rather than an ELF object.

## Root cause

The explicit launcher sourced the normal glibc environment, then exported:

```text
LD_LIBRARY_PATH=<generation>/lib:$PREFIX/glibc/lib
```

inside the launcher shell.

It then executed a Termux/bionic utility:

```text
mkdir -p "$LAUNCH_RECEIPT_DIR"
```

The bionic `mkdir` inherited the candidate glibc loader path and attempted to resolve `libc.so` from the glibc world. That object is not a bionic-compatible ELF runtime library, so `mkdir` failed before the launcher reached the final Obsidian `exec`.

Therefore the timeout message was secondary. The application did not start; topology classification was not the primary failure.

## Corrective design

Candidate loader policy must be consumer-scoped to the final glibc application exec.

The corrected launcher now:

```text
validates paths while still in the bionic-safe environment;
sources $HOME/gl/env;
restores the receipt-provided explicit-generation variables;
unsets inherited LD_LIBRARY_PATH;
clears Vulkan/Mesa and over-scoped toolkit overrides;
records launch contracts without candidate LD_LIBRARY_PATH exported;
performs no external bionic command under the candidate loader path;
uses one final exec env invocation to set LD_LIBRARY_PATH only for Obsidian.
```

Final boundary:

```text
launcher shell and Termux utilities:
    LD_LIBRARY_PATH unset

Obsidian exec only:
    LD_LIBRARY_PATH=<generation>/lib:$PREFIX/glibc/lib
```

The launch receipt additionally records:

```text
launcher_shell_ld_library_path:
    UNSET

candidate_loader_injection:
    EXEC_ENV_ONLY
```

## Current-pointer evidence boundary

The first receipt contains `current-state-before.tsv` but not `current-state-after.tsv`, because the runner exited immediately when capture failed.

The launcher contains no `current` mutation path, and it failed before Obsidian exec. Nevertheless, the archive alone does not prove the live after-state.

The runner is corrected to write and compare `current-state-after.tsv` even when capture fails.

## Claim boundary

This receipt proves:

```text
the published generation was found;
the receipt-local validation setup succeeded;
current was absent before launch;
the launcher copy matched the repository source;
no Obsidian process topology was observed;
the launcher poisoned a bionic mkdir with candidate LD_LIBRARY_PATH;
the failure occurred before Obsidian exec.
```

It does not prove:

```text
the corrected launcher starts Obsidian;
the generation ELF set is selected;
the expected 125 immutable mapped identities appear;
current remained absent after the failed capture;
process survival or CPU-mode maps.
```

## Next action

Do not rerun Phase B1-B9.

Sync the corrected launcher and repeat only Phase B10 with a new stage-specific receipt.

## Stop line

Do not:

```text
export the candidate LD_LIBRARY_PATH in the bionic launcher shell;
run Termux utilities under the candidate glibc library path;
create current;
change the promoted launcher;
mutate the immutable generation;
interpret the topology timeout as an application compatibility failure.
```
