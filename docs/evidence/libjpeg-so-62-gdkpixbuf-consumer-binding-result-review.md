# `libjpeg.so.62` GdkPixbuf consumer-binding result review

## Decision

```text
requirement: OJ-001
result archive SHA-256:
    b010695561974c491aa0706600e867ea3a2b8b8abf43f8573c075418a047d92a
candidate: libjpeg.so.62.4.0
candidate SHA-256:
    a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
consumer: libgdk_pixbuf-2.0.so.0.4200.12
consumer SHA-256:
    16d15168c69d4ad61862462da9fe811b5be3bef898b940a4023e15b039f5b43c
static binding: complete, 22 required JPEG symbols and 0 missing
functional result: SIGSEGV, exit 139, before structured probe output
protected state: unchanged
candidate identity: retained
provider authority: not accepted
```

The read-only analyzer reached the functional call only after exact candidate and consumer identity checks, exact `DT_NEEDED=libjpeg.so.62`, complete static JPEG symbol coverage, conflict inventory, and probe compilation. The process then received `SIGSEGV` while calling `gdk_pixbuf_new_from_file()` for the fixed JPEG fixture. No decode dimensions, `dladdr` result, or `/proc/self/maps` proof were emitted.

Canonical machine-readable review:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libjpeg-so-62-gdkpixbuf-consumer-binding-result-review.tsv
```

## What the failure establishes

The following facts remain accepted:

```text
candidate source/build/member identity
ELF64 AArch64 DYN
DT_SONAME=libjpeg.so.62
no DT_RPATH or DT_RUNPATH
LIBJPEG_6.2 and LIBJPEGTURBO_6.2 symbol versions
exact retained GdkPixbuf consumer identity
consumer DT_NEEDED=libjpeg.so.62
22 required JPEG symbols, 0 missing
protected live state unchanged
```

The failure establishes that the attempted runtime composition did not produce usable functional evidence. It does **not** isolate the defect to the candidate.

## Unresolved runtime boundary

The failed process used the project `glibc-exec` wrapper. Therefore the loader and core libc came from the Termux-glibc prefix while the exact GdkPixbuf consumer and most of its dependency world came from the Debian rootfs. The analyzer also used the file-oriented `gdk_pixbuf_new_from_file()` path, which may involve GLib/GIO and loader-module behavior beyond the direct JPEG ABI.

The empty functional stdout/stderr means the crash occurred before the probe could record the mapped provider. The current evidence cannot distinguish among:

```text
candidate-specific libjpeg ABI or behavior failure
mixed Termux-glibc / Debian dependency-world failure
GdkPixbuf file/GIO path failure unrelated to direct JPEG decode
consumer-module or dependency collision
```

## Required diagnostic matrix

The next analyzer must remain scratch-only and compare isolated controls:

```text
1. direct libjpeg decode with the project candidate under the Termux loader;
2. direct libjpeg decode with the Debian oracle libjpeg under the same loader;
3. GdkPixbuf memory-loader decode with candidate versus oracle;
4. original file API with stage markers for candidate versus oracle;
5. where supported, repeat GdkPixbuf controls under the Debian rootfs loader;
6. record loader/libc/dependency maps before the functional call and on failure.
```

A candidate-specific failure requires the candidate controls to fail while the otherwise identical oracle controls pass. A mixed-runtime or API-path failure is established when both providers fail in the same boundary or when a narrower direct decode succeeds but the broader GdkPixbuf path fails.

## Authority effect

The corrected candidate identity remains valid, but functional equivalence and exact mapped consumer binding remain open. This review accepts no provider authority, composition, target membership, installation, materialization, deployment, or activation.
