# `libjpeg.so.62` GdkPixbuf diagnostic-matrix result review

## Decision

The 12-cell matrix completed, but it did not create a valid provider comparison.

```text
result archive SHA-256:
    29bedb2494b54602e0768cfb27695acb58e55359f115422cfe5777d4917aaae0
cells: 12
passes: 0
failures: 12
reported classification: DIRECT_CONTROL_ENVIRONMENT_UNRESOLVED
candidate identity: retained
provider authority: not accepted
```

## Why the matrix is non-dispositive

The Termux cells invoked the Bionic `glibc-exec` shell script only after setting a glibc/Debian `LD_LIBRARY_PATH`. The Bionic interpreter therefore entered the foreign library environment before the script could invoke the glibc loader. Both candidate and oracle direct controls exited 139 under the same contaminated launcher boundary.

The raw loader-list path also exposed `$PREFIX/glibc/lib/libc.so`, which is a linker script rather than a runtime ELF object and produced `invalid ELF header`. Debian-loader cells ran Termux-built probes and exited 127 while looking for `libc.so`; they were not Debian-native controls.

These are analyzer defects. Zero passes do not reject either provider.

## Corrected boundary

The next analyzer must:

1. clear `LD_PRELOAD` and `LD_LIBRARY_PATH` before any Bionic command starts;
2. invoke `ld-linux-aarch64.so.1` directly, never through the shell wrapper;
3. construct a scratch runtime shim containing only resolved ELF objects;
4. use only candidate/oracle plus the core shim for direct decode;
5. add Debian consumer libraries only for GdkPixbuf cells;
6. treat Debian-native controls as optional and separate.

No installation, rootfs mutation, provider authority, composition, target population, deployment, or activation is created by this review.
