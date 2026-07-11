# 0108 — Selected Obsidian Phase B10 Second-Run Short-Lived Main Diagnostic

## Status

The second Phase B10 run advanced beyond the launcher-shell failure and executed the explicit-generation Obsidian main process, but the process exited before renderer/zygote topology stabilized.

```text
analysis.status:
    FAIL

failure stage:
    capture

explicit Obsidian exec reached:
    YES

stable main/renderer/zygote topology:
    NO

current pointer changed:
    NO
```

This is a runtime-path diagnostic receipt. It does not invalidate Phase B9 or prove a generation-content failure.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b10-explicit-generation-cpu-validation-corrected-20260712-010602.tgz
```

Archive SHA-256:

```text
01c14177d9ed32bb9de294aef2ccc64dba3e2afbbd1e82ed53eb705526ff3575
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    d6be102385140c61f92f1ca41028c90cbc866233
```

Archive members:

```text
regular files:
    33

directories:
    17

application-created symlinks:
    1
```

The only symlink was:

```text
runtime/xdg/config/obsidian/SingletonLock
    -> localhost-4594
```

It is a relative basename target with no traversal component. No archive member used an absolute path or parent traversal.

## Launcher correction verified

The corrected launch receipt recorded:

```text
launcher_shell_ld_library_path:
    UNSET

candidate_loader_injection:
    EXEC_ENV_ONLY

current_reference:
    NO

GL_GPU:
    0

GPU flag:
    --disable-gpu
```

The requested loader path was:

```text
<generation>/lib:$PREFIX/glibc/lib
```

and was injected only in the final application `exec env`.

The receipt-local launcher copy exactly matched the repository source:

```text
source SHA-256:
    6d8c4daf9d6b684c6be65ff8df94863af38883d3ac6655ad0afb68b2a6dd5e87

runtime-copy SHA-256:
    6d8c4daf9d6b684c6be65ff8df94863af38883d3ac6655ad0afb68b2a6dd5e87
```

Therefore the first B10 bionic/glibc launcher-shell contamination was corrected.

## Process observation

The capture observed the explicit-generation main command once:

```text
pid:
    4594

class:
    main

cmdline:
    $HOME/gl/apps/obsidian/obsidian
    --disable-dev-shm-usage
    --ozone-platform=x11
    --disable-gpu
```

No surviving process was present at the final topology sample.

```text
poll-observed process rows:
    1

last-process rows:
    0

observed-pid rows:
    0

stable renderer:
    0

stable zygote:
    0

maps captured:
    NO
```

The application reached its receipt-local config directory and created:

```text
obsidian.log
id
SingletonLock -> localhost-4594
```

It also created one Chromium scoped temporary directory.

This establishes that Obsidian main executed and began application initialization before exiting.

## Stderr classification

Observed stderr:

```text
Failed to read /proc/sys/fs/inotify/max_user_watches
Failed to connect to /run/dbus/system_bus_socket
```

These messages alone do not identify the process-exit cause. They are environmental warnings and contain no fatal loader, missing-library, or generation-path error.

Unlike the first B10 receipt, there was no bad-ELF or bionic loader-policy failure.

## Strongest discriminator: runtime/socket path length

The second run placed all runtime state below the long stage output path.

Observed path lengths included:

```text
XDG config application path:
    178 characters

Chromium scoped temporary path:
    179 characters

XDG runtime directory:
    170 characters
```

The application created `SingletonLock`, but the archive contains no:

```text
SingletonSocket
SingletonCookie
renderer process
zygote process
```

This pattern is consistent with failure during early Chromium single-instance/socket initialization. The receipt does not prove the precise internal Chromium errno, so path length remains a high-confidence hypothesis rather than a closed fact.

The next test changes only the runtime path length while preserving:

```text
generation ID;
content objects;
loader path;
CPU flags;
font selection;
schema selection;
current absence;
capture topology and survival gates.
```

## Capture-exit receipt bug

The runner wrote:

```text
capture-exit-status.txt:
    0
```

although `capture-control.sh` failed.

Cause:

```bash
if ! command; then
    capture_rc=$?
fi
```

Inside that branch, `$?` was the status of the shell negation and therefore zero.

The runner is corrected to use a normal `if command; then ... else capture_rc=$?` form, preserving the real capture exit status.

## Current-pointer boundary

```text
current before:
    ABSENT

current after:
    ABSENT

changed:
    NO
```

This second receipt closes the after-state gap left by the first B10 failure.

## Corrective design

The B10 runner now allocates a short, unique runtime root:

```text
$PREFIX/tmp/o10.XXXXXXXX
```

Runtime layout remains semantically identical:

```text
fontconfig/
xdg/config/
xdg/cache/
xdg/data/
xdg/state/
xdg/runtime/
tmp/
bin/
```

Expected path lengths on the device are approximately:

```text
runtime root:
    48 characters

TMPDIR:
    52 characters

XDG_CONFIG_HOME:
    59 characters
```

The runner enforces:

```text
TMPDIR length <= 64
```

before launch.

The short runtime root is transaction-owned. After capture it is copied byte-for-byte to:

```text
$OUT/runtime-evidence
```

The live and archived copies are compared with `diff -qr`, recorded as `MATCH`, and the short live root is then removed. Thus the final stage archive still contains the runtime evidence while the actual socket paths remain short during execution.

## Claim boundary

This receipt proves:

```text
the corrected exec-only loader injection was used;
the explicit Obsidian main process started;
receipt-local application state creation began;
the main exited before topology stabilization;
no maps or immutable-identity runtime claim was reached;
current remained absent before and after.
```

It does not prove:

```text
the long runtime path was the definite process-exit cause;
the immutable generation is incomplete;
selected objects failed to load;
the short-runtime correction passes;
renderer/zygote survival or mapped identity.
```

## Next action

Do not rerun Phase B1-B9.

Repeat only Phase B10 with the short transaction-owned runtime root and the same immutable generation.

## Stop line

Do not:

```text
change generation contents;
add broad-farm or rootfs loader paths;
create current;
change the promoted launcher;
interpret the two stderr warnings as a fatal diagnosis;
claim a generation-content failure before the short-path discriminator runs.
```
