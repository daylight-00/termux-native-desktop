# 0034 — Obsidian Control Semantic Decomposition

## Status

The successful Obsidian control evidence has now been enriched with package provenance and identity information.

Observed path-class counts:

```text
APP_LOCAL        11
OTHER_ABSOLUTE   26
PREFIX_GLIBC     59
ROOTFS_PROVIDER  65
```

Total unique mapped paths:

```text
161
```

The first enrichment run recorded 160 objects because one captured path was no longer a regular file when enrichment ran. Enrichment is now coverage-preserving: every path in `unique-objects.tsv` receives a record, with vanished paths marked:

```text
state = MISSING_AT_ENRICHMENT
sha256 = MISSING
build_id = MISSING
```

## APP_LOCAL decomposition

The 11 AppDir-local objects split directly into:

```text
APP_LOCAL_ELF   5
APP_LOCAL_DATA  6
```

ELF payload:

```text
obsidian
libEGL.so
libGLESv2.so
libffmpeg.so
libvulkan.so.1
```

Data payload:

```text
chrome_100_percent.pak
chrome_200_percent.pak
icudtl.dat
locales/en-US.pak
resources.pak
v8_context_snapshot.bin
```

This proves that AppDir locality is both executable and data locality.

## PREFIX_GLIBC decomposition

Observed package summary:

```text
glibc                     18
libxcb-glibc               8
krb5-glibc                 4
libwayland-glibc           3
gcc-libs-glibc             3
libx11-glibc               2
brotli-glibc               2
and 19 additional one-object provider packages
```

The 18 `glibc`-owned prefix objects split semantically into:

```text
WORLD_SUBSTRATE_ELF   6
PROVIDER_LOCALE_DATA 12
```

The six core ELF objects are:

```text
ld-linux-aarch64.so.1
libc.so.6
libdl.so.2
libm.so.6
libpthread.so.0
libresolv.so.2
```

The twelve locale objects are the mapped `en_US.utf8` locale components.

This is an important correction to a possible ownership shortcut:

```text
package owner == glibc
    does not imply
semantic owner == world substrate
```

Package ownership is provenance evidence. Semantic ownership still depends on capability role.

The remaining non-glibc prefix set is primarily ELF provider material and must be modeled as prefix provider capability, not world substrate.

## ROOTFS_PROVIDER decomposition

Observed rootfs mapped-path count:

```text
65
```

The non-ELF subset is exactly:

```text
4 font files
1 compiled GSettings schema file
```

Therefore the first semantic decomposition is:

```text
PROVIDER_ROOTFS_ELF  60
PROVIDER_FONT_DATA    4
PROVIDER_SCHEMA_DATA  1
```

The schema path:

```text
/usr/share/glib-2.0/schemas/gschemas.compiled
```

was reported as `UNOWNED` by package-path lookup in the captured rootfs state. This must be treated as a runtime artifact provenance question, not silently assigned to an arbitrary package owner.

The rootfs ELF package distribution is broad. High-count examples include:

```text
libnss3                6
libglib2.0-0t64        4
libnspr4               3
libgtk-3-0t64          2
```

with many one-object packages across GUI, font rendering, security, TLS, audio, X11 extension, systemd/udev, and Mesa-related capabilities.

## OTHER_ABSOLUTE interpretation

The 26 `OTHER_ABSOLUTE` paths include runtime state/cache categories such as:

```text
fontconfig caches
Mesa shader cache
Obsidian Cookies / DIPS
Dawn caches
GPU cache
WebStorage quota state
spell-check dictionary data
```

These are not provider candidate bytes merely because they appear in process maps.

The classifier separates known mutable/cache domains and leaves unexpected ELF/data paths in explicit review classes.

## Architecture conclusion

The Obsidian pilot now supports a stronger architecture than a single selected-library directory.

The application domain composes at least:

```text
app.obsidian local payload
    APP_LOCAL_ELF
    APP_LOCAL_DATA

world.glibc substrate
    WORLD_SUBSTRATE_ELF

provider.locale.glibc
    PROVIDER_LOCALE_DATA

prefix provider capabilities
    PROVIDER_PREFIX_ELF

selected rootfs ELF provider closure
    PROVIDER_ROOTFS_ELF

provider.fonts.glibc
    PROVIDER_FONT_DATA

provider shared-data / GSettings capability
    PROVIDER_SCHEMA_DATA

mutable runtime state
    APP_MUTABLE_STATE
    RUNTIME_CACHE_*
```

This is not yet a final physical directory design. It is the minimum semantic decomposition supported by current maps and provenance evidence.

## Reuse relation to the D-Bus pilot

The Obsidian rootfs ELF set contains the same D-Bus chain family observed in the first pilot:

```text
libdbus
libsystemd
```

alongside a much larger desktop-runtime set.

This suggests possible reusable provider components, but current evidence does not yet prove that one monolithic global `provider.shared-libs.glibc` object is the correct owner.

A better next question is:

```text
which provider capability groups are independently reusable,
and which closure edges are application-domain composition bindings?
```

## Next gate

Before candidate materialization:

```text
1. rerun coverage-preserving identity enrichment
2. run semantic classifier
3. inspect MISSING_AT_ENRICHMENT and REVIEW classes
4. identify APP_LOCAL vs external SONAME collisions
5. derive rootfs ELF static closure and compare with runtime-selected set
6. define candidate composition as multiple capability inputs, not one flat directory
```

Candidate materialization remains blocked until the review set and locality-shadowing check are resolved.
