# 0033 — Obsidian Control Maps Captured; Provenance Split Required

## Status

The pre-wall-clock-correction Obsidian control harness eventually completed its long survival observation and reached final process/map capture.

The run produced:

```text
processes.tsv
mapped-objects.tsv
unique-objects.tsv
```

but did not produce:

```text
class-counts.tsv
process-class-observation-counts.tsv
```

before returning control.

This is classified as:

```text
TOPOLOGY_CAPTURE_VALID
SURVIVAL_OBSERVATION_COMPLETED
FINAL_PROCESS_MAPS_CAPTURED
UNIQUE_OBJECT_SET_CAPTURED
PROVENANCE_ENRICHMENT_FAILED_ON_NON_ELF_BUILD_ID_PROBE
```

The evidence root is:

```text
$PREFIX/tmp/selected-obsidian-control-survival-20260710-220652
```

## Exact enrichment failure mechanism

The old integrated enrichment loop applied:

```text
readelf -n <mapped object>
```

to every regular mapped file while running under:

```text
set -o pipefail
```

The captured APP_LOCAL set begins with non-ELF objects such as:

```text
chrome_100_percent.pak
chrome_200_percent.pak
icudtl.dat
```

For a non-ELF input, `readelf -n` returns non-zero. Under `pipefail`, the Build-ID helper therefore returned non-zero and the assignment invoking it terminated the script under `set -e`.

This explains the exact evidence boundary:

```text
unique-objects.tsv
    present

object-identities.tsv
    incomplete

class-counts.tsv
    absent

process-class-observation-counts.tsv
    absent
```

The separated enrichment tool now treats non-ELF Build-ID absence as:

```text
build_id = NONE
```

rather than as an experiment failure.

## Final process set

The final captured process set was:

```text
main      1
zygote    3
utility   1
renderer  1
```

This refines the earlier topology interpretation.

The correct contract is:

```text
required early stable classes:
    main
    renderer
    zygote

late/optional but captured classes:
    utility
    gpu
    crashpad
    helper
```

`utility` was absent during the earlier startup polling evidence but present in the later final process set. It must therefore not be used as an early stabilization requirement, but it remains part of the final runtime topology when observed.

## APP_LOCAL set

The captured AppDir-local set included:

```text
chrome_100_percent.pak
chrome_200_percent.pak
icudtl.dat
libEGL.so
libGLESv2.so
libffmpeg.so
libvulkan.so.1
locales/en-US.pak
obsidian
resources.pak
v8_context_snapshot.bin
```

This confirms that a real Obsidian runtime domain contains both executable/shared-object locality and app-local data payload locality.

A selected external provider closure must not flatten or override this AppDir-local set by default.

## PREFIX_GLIBC set

The control maps contained a large prefix-resident set including:

```text
protected substrate candidates:
    loader
    libc
    libm
    libdl
    libpthread
    libresolv

prefix provider candidates:
    X11/xcb family
    wayland client family
    libdrm
    compression libraries
    Kerberos/GSSAPI libraries
    libcap-glibc
    libstdc++
    libgcc_s
    locale archive components
```

This reinforces the D-Bus pilot finding:

```text
prefix location
    !=
semantic world ownership
```

Prefix objects require package ownership and semantic classification.

## ROOTFS_PROVIDER set

The rootfs-mapped set was much broader than the three-object D-Bus pilot.

Observed categories included:

```text
GTK/GDK
ATK/AT-SPI
GLib/GObject/GIO
Cairo/Pango/Harfbuzz/Freetype/Fontconfig
NSS/NSPR
GNUTLS/nettle/hogweed/p11-kit
CUPS/Avahi
X11 extension libraries
ALSA
libsystemd/libudev/libdbus
Mesa device-select layer and GBM
font files
GSettings compiled schema data
```

This is important because the application-domain runtime dependency is not representable as a single flat shared-library closure.

The control evidence contains at least three different external capability kinds:

```text
shared ELF providers
font/data providers
schema/data providers
```

They may share a supply source while requiring different semantic owners and lifecycle contracts.

## Harness finding

The first control script coupled three phases:

```text
live process/map capture
summary generation
package/hash/Build-ID enrichment
```

For a large application runtime set this is a poor transaction boundary.

The live capture must close quickly and durably once process maps have been obtained.

Provenance enrichment is now a separate post-processing action over the captured evidence:

```text
capture-control.sh
    -> topology/survival/maps/unique sets

enrich-control-identities.sh
    -> package ownership/version
    -> SHA-256
    -> Build ID or NONE for non-ELF objects
```

The enrichment implementation batches package ownership and version queries rather than starting one Debian login transaction per rootfs object.

## Architecture consequence

The Obsidian pilot already disproves a simplistic next step such as:

```text
copy every ROOTFS_PROVIDER path into candidate/lib
```

because the observed external set includes non-ELF runtime data and capability-specific resources.

The next step is therefore:

```text
1. complete provenance enrichment over the captured control evidence
2. classify PREFIX_GLIBC objects by package ownership and semantic role
3. separate ROOTFS ELF providers from font/schema/data capabilities
4. preserve APP_LOCAL locality
5. only then define candidate composition boundaries
```

Candidate materialization remains blocked until those boundaries are explicit.
