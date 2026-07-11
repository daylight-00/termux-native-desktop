# 0109 — Selected Obsidian Phase B10 Short-Runtime Topology Pass and GTK Pixbuf Survival Failure

## Status

The short-runtime Phase B10 discriminator passed process-topology startup and disproved the long-path-only startup failure, but the main process aborted during the 100-second survival gate.

```text
analysis.status:
    FAIL

failure stage:
    capture

topology.status:
    PASS

survival.status:
    FAIL main process exited

maps capture:
    NOT REACHED

current pointer changed:
    NO
```

Phase B10 remains open. Phase B9 remains valid and the immutable generation remains unactivated.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b10-short-runtime-cpu-validation-20260712-012415.tgz
```

Archive SHA-256:

```text
529e42fbc338148f5adf36cbabc1c8a1ebc16e9408e5850dd56f5194ac92f9fe
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    e9a44c7bcd52b35e433d9b9850469c9b1bb7db99
```

Archive members:

```text
regular files:
    94

directories:
    41

application-created symlinks:
    4

absolute member paths:
    0

parent traversal:
    0
```

One application-created symlink uses an absolute target:

```text
runtime-evidence/xdg/config/obsidian/SingletonSocket
    -> $PREFIX/tmp/o10.oZVc1s8U/tmp/scoped_dirIbzNVr/SingletonSocket
```

This is valid runtime evidence but means generic archive extraction should not follow symlinks. Inspection must treat archive symlinks as metadata.

## Short runtime-path contract

```text
validation root:
    $PREFIX/tmp/o10.oZVc1s8U

validation-root length:
    48

TMPDIR length:
    52

XDG_CONFIG_HOME length:
    59

runtime root ownership:
    YES

snapshot:
    MATCH
```

The short live runtime was copied to the stage receipt before cleanup.

## Loader and activation boundary

```text
launcher-shell LD_LIBRARY_PATH:
    UNSET

candidate loader injection:
    EXEC_ENV_ONLY

candidate loader path:
    <generation>/lib:$PREFIX/glibc/lib

GL_GPU:
    0

main flag:
    exact --disable-gpu

current before:
    ABSENT

current after:
    ABSENT
```

The real capture exit status was correctly recorded as `1`.

## Topology result

The short path allowed Chromium single-instance state and the complete required CPU topology to form.

Observed stable process set:

```text
main:
    1

zygote:
    3

utility:
    1

renderer:
    1

GPU process:
    0
```

The renderer contained:

```text
--disable-gpu-compositing
```

Runtime evidence now contains:

```text
SingletonLock
SingletonSocket
SingletonCookie
Chromium scoped temporary directory
```

Therefore the preceding long-path hypothesis is supported for early startup: shortening the paths moved the run from short-lived main-only behavior to a stable main/renderer/zygote topology.

## Survival result

The required topology survived through 28 recorded survival samples. The main process then aborted approximately 72 seconds after startup, before the 100-second gate completed.

The fatal chain was:

```text
Gtk warning:
    user-home-symbolic-ltr not found
    hicolor theme not found

Gtk warning:
    failed to load /org/gtk/libgtk/icons/48x48/status/image-missing.png

GdkPixbuf error:
    Unrecognized image file format

Gtk fatal assertion:
    gtkiconhelper.c:495 ensure_surface_for_gicon

application result:
    Bail out / main process exit
```

The stderr also contained non-fatal environment warnings for inotify sysctl access, missing system D-Bus, and missing `xdg-settings`. Those are not the fatal boundary in this receipt.

## Architecture finding

The B1-B8 closure was derived primarily from mapped regular objects plus selected retained data. That model closed ELF, fonts, GSettings, and locale identities, but did not establish every file or dynamically loaded module opened later by GTK.

The current generation contains:

```text
libgdk_pixbuf-2.0.so.0
libpng16.so.16
libjpeg.so.62
```

but the B9 data manifest contains only:

```text
4 selected fonts
1 generated GSettings aggregate
12 protected-world locale files
```

It contains no explicit:

```text
gdk-pixbuf loaders.cache
gdk-pixbuf loader modules
icon-theme index/data
shared MIME database
```

The fatal error therefore exposes an open runtime-data/plugin capability boundary. It does not yet prove which exact subset is necessary.

## Next discriminator

The next stage is read-only source/provenance inventory:

```text
recipe/inspect-gtk-pixbuf-runtime-capability.py
```

It will:

```text
verify the accepted B9 and short-runtime B10 receipts;
inventory rootfs gdk-pixbuf loader caches and loader modules;
parse cache module references;
record package, version, SHA-256, and size;
inventory icon-theme indexes and shared MIME database files;
report which paths are absent from the B9 semantic manifest;
perform no workload launch;
perform no generation mutation.
```

Expected next state:

```text
READY_FOR_CONTROLLED_PIXBUF_RUNTIME_DIAGNOSTIC
```

Only after that inventory may a controlled diagnostic point the application at a receipt-local relocated loader cache and rootfs loader modules. Such a run is diagnostic, not acceptance, because rootfs provider mappings would be intentionally permitted and recorded.

## Claim boundary

This receipt proves:

```text
short runtime/socket paths are viable;
main/renderer/zygote topology forms;
CPU mode has no GPU process;
current remains absent;
the generation reaches functional application startup;
the main later aborts in GTK icon/pixbuf handling.
```

It does not prove:

```text
100-second survival;
all 125 expected immutable identities are mapped;
which pixbuf loader/cache/icon/mime files are necessary;
the immutable generation data manifest is complete;
activation or rollback readiness.
```

## Direction decision

```text
Phase B10 topology:
    PASS

Phase B10 survival:
    FAIL

Phase B10 mapped-identity acceptance:
    NOT REACHED

short-path hypothesis:
    SUPPORTED FOR STARTUP

GTK runtime data/plugin closure:
    OPEN

next action:
    READ-ONLY PIXBUF/ICON/MIME SOURCE INVENTORY
```

## Stop line

Do not:

```text
rerun Phase B1-B9;
modify the immutable generation blindly;
copy all rootfs icon or MIME data wholesale;
add the broad farm or rootfs to the accepted loader path;
create current;
change the promoted launcher;
claim B10 PASS from topology alone;
follow archived SingletonSocket symlinks during extraction.
```
