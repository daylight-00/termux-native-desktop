# 0027 — D-Bus Static/Runtime Closure Agreement

## Status

The ownership-aware static discovery rerun completed successfully and its selected rootfs provider set matches the previously captured runtime mapped provider set.

This closes the pilot's first architecture gate:

```text
STATIC_SELECTED_PROVIDER_SET
    ==
RUNTIME_MAPPED_PROVIDER_SET
```

for the bounded D-Bus probe.

## Prefix ownership evidence

The prefix `libcap` object is:

```text
path:
    $PREFIX/glibc/lib/libcap.so.2.69

package owner:
    libcap-glibc

package version:
    2.69-1
```

This directly confirms:

```text
prefix path location
    !=
world substrate ownership
```

and validates the correction made in `0026`.

## Static selected rootfs provider set

The ownership-aware traversal selected exactly:

```text
libdbus-1.so.3.38.3
libsystemd.so.0.40.0
libcap.so.2.75
```

with provenance:

```text
libdbus-1-3:arm64
    version: 1.16.2-2
    SHA-256: 33dc83ad1eb603068542245eab12d67bca6c6f8323c08fe4600ef3b0868966af
    Build ID: f7d07c8924acc61f4014b2998e2180c90c660f32

libsystemd0:arm64
    version: 257.13-1~deb13u1
    SHA-256: e3ecd5cf99aa5a9aa88422ab21bde152e998be07b38ebed7ac20cc7d2dd6fe8f
    Build ID: dd895903c09f791495c1f87d06cf6fcc0476b011

libcap2:arm64
    version: 1:2.75-10+deb13u1+b1
    SHA-256: 2d74e5a4d536311c2e84d1603edb4c8dd7cdfaa92f1305ec4e317edcd062ddec
    Build ID: 7b0893c1fc978622d9f946fa601c096227772257
```

## Protected world substrate set

The static traversal classified these active objects as protected substrate based on package ownership by `glibc`:

```text
libc.so.6
ld-linux-aarch64.so.1
libm.so.6
```

Observed identities:

```text
libc.so.6
    package: glibc 2.42
    SHA-256: 665384fb6018e1a41ce21e542c6e7b4ee67850ec7292ce90329623b25a673834
    Build ID: 0b0a4cdb97355daecdb91d2915f61215924104c8

ld-linux-aarch64.so.1
    package: glibc 2.42
    SHA-256: 8eb7373d62cd66d8ddeb473a2704ea06d5d4d4397b3440fca2a9e74929984ac6
    Build ID: 0f24739d4563518b647beb2d6e6734dba391081b

libm.so.6
    package: glibc 2.42
    SHA-256: b4875f58f4614f15bf7d23c65d23bc3a1f6bd336099362bf9a9a2f73c5dfd48a
    Build ID: 78f6668a31dc320192e8d8610f16ba0971602bc7
```

## Static graph

The selected graph is:

```text
libdbus
    -> libsystemd            PROVIDER_ROOTFS
    -> libc                  WORLD_SUBSTRATE
    -> loader                WORLD_SUBSTRATE

libsystemd
    -> libcap                PROVIDER_ROOTFS
    -> libm                  WORLD_SUBSTRATE
    -> libc                  WORLD_SUBSTRATE
    -> loader                WORLD_SUBSTRATE

libcap
    -> libc                  WORLD_SUBSTRATE
    -> loader                WORLD_SUBSTRATE
```

No prefix provider object was selected in this control closure.

## Agreement with runtime maps

The earlier control runtime maps showed exactly three rootfs provider objects:

```text
libdbus
libsystemd
libcap
```

The ownership-aware static traversal now selects the same set.

Therefore the first boundedness/selection gate passes.

This does **not** prove that every runtime mode of D-Bus or libsystemd has no dynamic/plugin/data dependencies. It proves only the bounded probe claim:

```text
for dbus_get_version() under the captured control environment,
static selected provider closure matches the observed mapped provider closure
```

## Decision

The pilot may proceed to isolated candidate materialization.

The next experiment must:

```text
copy selected provider bytes into an isolated candidate directory
create only candidate-internal SONAME links
record source and candidate identities in a receipt
run the same probe with:
    candidate/lib:$PREFIX/glibc/lib
prove all selected providers map from candidate
prove protected world objects map from substrate
prove no broad-farm or rootfs provider path is mapped
verify mapped candidate hashes/Build IDs against the receipt
```

Still out of scope:

```text
global provider store
activation pointer
gl-sync
global fingerprint
broad-farm replacement
application-wide migration
```
