# 0028 — Selected D-Bus Candidate Validation Passed

## Status

The first selected-provider candidate was materialized from the successful ownership-aware D-Bus closure evidence and validated in an isolated loader context.

The result is:

```text
SELECTED_PROVIDER_BYTES_MATERIALIZED
PROVENANCE_RECEIPT_RECORDED
CANDIDATE_ACTUAL_SELECTION_PROVEN
BROAD_FARM_LEAKAGE_ZERO
ROOTFS_PROVIDER_LEAKAGE_ZERO
PROTECTED_SUBSTRATE_BOUNDARY_VALID
BOUNDED_DBUS_SELECTED_CLOSURE_PILOT_PASS
```

## Candidate identity

Candidate path used for the first device run:

```text
$PREFIX/tmp/selected-dbus-candidate-20260710-201047
```

Candidate ID:

```text
198a0ea278f09518a6b0ead7a228bb198a837e4096343228cfb32b1115286e6b
```

The candidate contained three concrete provider files and three candidate-internal SONAME links.

## Materialized provider set

Concrete bytes:

```text
libdbus-1.so.3.38.3
libsystemd.so.0.40.0
libcap.so.2.75
```

Candidate-internal links:

```text
libdbus-1.so.3  -> libdbus-1.so.3.38.3
libsystemd.so.0 -> libsystemd.so.0.40.0
libcap.so.2     -> libcap.so.2.75
```

No candidate symlink points back into the mutable Debian rootfs.

## Provenance receipt

The receipt preserved source and candidate identities for each selected provider.

### libdbus

```text
package:
    libdbus-1-3:arm64

version:
    1.16.2-2

source SHA-256:
    33dc83ad1eb603068542245eab12d67bca6c6f8323c08fe4600ef3b0868966af

source Build ID:
    f7d07c8924acc61f4014b2998e2180c90c660f32

candidate SHA-256:
    33dc83ad1eb603068542245eab12d67bca6c6f8323c08fe4600ef3b0868966af

candidate Build ID:
    f7d07c8924acc61f4014b2998e2180c90c660f32
```

### libsystemd

```text
package:
    libsystemd0:arm64

version:
    257.13-1~deb13u1

source SHA-256:
    e3ecd5cf99aa5a9aa88422ab21bde152e998be07b38ebed7ac20cc7d2dd6fe8f

source Build ID:
    dd895903c09f791495c1f87d06cf6fcc0476b011

candidate SHA-256:
    e3ecd5cf99aa5a9aa88422ab21bde152e998be07b38ebed7ac20cc7d2dd6fe8f

candidate Build ID:
    dd895903c09f791495c1f87d06cf6fcc0476b011
```

### libcap

```text
package:
    libcap2:arm64

version:
    1:2.75-10+deb13u1+b1

source SHA-256:
    2d74e5a4d536311c2e84d1603edb4c8dd7cdfaa92f1305ec4e317edcd062ddec

source Build ID:
    7b0893c1fc978622d9f946fa601c096227772257

candidate SHA-256:
    2d74e5a4d536311c2e84d1603edb4c8dd7cdfaa92f1305ec4e317edcd062ddec

candidate Build ID:
    7b0893c1fc978622d9f946fa601c096227772257
```

The materializer verified source identity before copying and candidate identity after copying.

## Isolated validation context

The probe was validated with the explicit library search path:

```text
candidate/lib:$PREFIX/glibc/lib
```

The broad farm and Debian rootfs were not included in the candidate loader path.

## Relocation result

The candidate relocation check resolved:

```text
libdbus-1.so.3
    -> candidate/lib/libdbus-1.so.3

libsystemd.so.0
    -> candidate/lib/libsystemd.so.0

libcap.so.2
    -> candidate/lib/libcap.so.2

libc.so.6
    -> $PREFIX/glibc/lib/libc.so.6

libm.so.6
    -> $PREFIX/glibc/lib/libm.so.6

ld-linux-aarch64.so.1
    -> $PREFIX/glibc/lib/ld-linux-aarch64.so.1
```

No undefined-symbol error was reported.

## Runtime probe result

The same bounded probe executed successfully:

```text
libdbus runtime version: 1.16.2
hold seconds: 20
```

## Actual mapped candidate provider set

`/proc/<pid>/maps` proved that the actual mapped candidate provider realpaths were exactly:

```text
candidate/lib/libdbus-1.so.3.38.3
candidate/lib/libsystemd.so.0.40.0
candidate/lib/libcap.so.2.75
```

The validator compared this actual mapped set with the receipt provider set and reported:

```text
candidate receipt/map equality: PASS
```

This proves the candidate files were not merely present or configured; they were the provider bytes actually mapped by the probe process.

## Leakage checks

The validation reported:

```text
no broad-farm/rootfs provider leakage: PASS
```

Therefore the process maps contained no provider object under:

```text
$HOME/gl/lib/
```

and no provider object under:

```text
$PREFIX/var/lib/proot-distro/containers/debian/rootfs/
```

The selected runtime provider bytes came from the candidate directory only.

## Protected world boundary

The validator also reported:

```text
mapped prefix objects are within protected world set: PASS
```

For this bounded probe, the allowed protected world substrate set was:

```text
ld-linux-aarch64.so.1
libc.so.6
libm.so.6
```

all owned by the `glibc` package in the captured substrate state.

## Validation evidence path

First successful candidate validation evidence:

```text
$PREFIX/tmp/selected-dbus-candidate-validation-20260710-202400
```

The evidence directory contains the relocation output, loader debug log, process maps, mapped candidate set, leakage checks, receipt comparison inputs, and validation status.

## Architecture conclusion

The pilot has now proven that a selected provider closure can exist as a real materialized object with:

```text
bounded selected bytes
explicit provenance
source/candidate identity equality
candidate-internal SONAME links
candidate-specific loader context
actual mapped-provider proof
protected substrate exclusion
broad-farm independence
rootfs runtime independence
```

This is stronger than a broad farm symlink generation.

The broad farm remains useful as:

```text
research compatibility pool
control/reference environment
discovery oracle
```

but this pilot proves that it is not intrinsically required for the tested D-Bus workload.

## Scope limit

The exact proven claim is:

```text
for the bounded dbus_get_version() probe under the captured substrate,
a three-object materialized provider closure is sufficient and is actually selected
without broad-farm or rootfs provider leakage.
```

This does not yet prove:

```text
all D-Bus runtime modes
system/session bus behavior
plugin/dlopen closure
all Electron applications
all glibc applications
global shared-provider scope
application-local $ORIGIN preservation under selected closure composition
```

Those remain separate claims.
