# Selected Obsidian AppDir Closure Pilot

## Status

Active architecture-discrimination experiment.

Current state:

```text
control topology capture: PASS
long survival observation: completed
final multiprocess maps capture: PASS
unique mapped-object set: captured
provenance enrichment: separated into post-processing stage
candidate materialization: blocked pending semantic classification
```

## Question

Can a real Electron AppDir application consume selected external provider closures while preserving valid application-local `$ORIGIN` locality and keeping external capability classes semantically separate?

## Current control evidence

Evidence root:

```text
$PREFIX/tmp/selected-obsidian-control-survival-20260710-220652
```

### Final process topology

```text
main      1
zygote    3
utility   1
renderer  1
```

The startup stabilization contract remains:

```text
required early:
    main
    renderer
    zygote

late/optional but captured:
    utility
    gpu
    crashpad
    helper
```

### APP_LOCAL

Observed AppDir-local runtime objects include the Obsidian executable, Electron-local graphics/media libraries, locale/resource packs, ICU data, and V8 snapshot data.

This is direct evidence that application locality includes both ELF and data payload objects.

### PREFIX_GLIBC

The prefix-mapped set includes both protected substrate candidates and non-world provider candidates.

The pilot therefore preserves the rule established by the D-Bus experiment:

```text
prefix path location
    !=
semantic world ownership
```

### ROOTFS_PROVIDER

The rootfs-mapped set is broad and heterogeneous.

Observed capability groups include:

```text
GTK/GDK and accessibility
GLib/GObject/GIO
font and text rendering stack
NSS/NSPR and TLS-related libraries
X11 extension libraries
sound
systemd/udev/D-Bus
Mesa-related objects
font files
compiled GSettings schema data
```

Therefore the next candidate cannot be modeled as a blind flat copy of every rootfs path into one `lib/` directory.

## Capture/enrichment split

The experiment now separates:

```text
capture-control.sh
    live process topology
    wall-clock survival gate
    process maps
    unique mapped object set
    fast class summaries

enrich-control-identities.sh
    batched package ownership lookup
    package versions
    SHA-256
    Build IDs
```

This keeps the live capture transaction bounded and allows provenance work to run later over immutable evidence.

## Next stage

Run provenance enrichment over the successful control evidence, then classify:

```text
APP_LOCAL
WORLD_SUBSTRATE
PROVIDER_PREFIX
PROVIDER_ROOTFS_ELF
PROVIDER_FONT_DATA
PROVIDER_SCHEMA_DATA
OTHER_RUNTIME_DATA
```

Only after these boundaries are explicit may candidate composition be designed.

## Stop line

Do not yet:

```text
rewrite Obsidian RPATH
change the promoted launcher
copy every rootfs path into candidate/lib
replace the broad farm
merge app-local bytes with external provider bytes
introduce a universal provider store
```

First complete provenance enrichment and semantic capability separation.
