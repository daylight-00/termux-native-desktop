# AT-SPI2 core provider evidence blocker

## Decision

```text
selected identities:     libatk-bridge-2.0.so.0.0.0
                         libatk-1.0.so.0.25611.1
                         libatspi.so.0.0.1
required SONAMEs:        libatk-bridge-2.0.so.0
                         libatk-1.0.so.0
                         libatspi.so.0
provider authority:      OPEN_BLOCKED_NO_GLIBC_CANDIDATE
composition effect:      NONE; all three selected identities remain gaps
target/activation:       BLOCKED
```

The read-only acquisition result is retained by SHA-256
`8647eac52880a85bdd0702a1b2e5b64192f4c50d355b7574edf1cd04519a61dc`.
The probe did not install, upgrade, start an accessibility service, mutate D-Bus state, or modify the repository or any provider target.

## What the approved indexes established

The exact glibc query `at-spi2-core-glibc` returned no policy entry and no package stanza. The available index entries were ordinary Termux/bionic packages only:

```text
at-spi2-core  2.60.5-1  stable/main  aarch64  installed and candidate
atk           2.48.0    x11/main     aarch64  installed and candidate
at-spi2-atk   2.48.0    x11/main     aarch64  candidate
```

The index describes `atk` and `at-spi2-atk` as metapackages that install `at-spi2-core`. These package names and installed bionic runtime state do not supply a Termux glibc archive, exact glibc member, or cross-world provider authority.

## Recipe provenance boundary

At pinned glibc recipe commit `9bdd20c1d36524a0ab016d9b71c748b0cbb20a34`, exact-path checks for `gpkg/at-spi2-core/build.sh`, `gpkg/atk/build.sh`, and `gpkg/at-spi2-atk/build.sh` failed, and repository search found no AT-SPI2/ATK producing root. The recipe root therefore remains unavailable for this approved glibc world.

This finding is narrower than an upstream-source rejection. It does not claim that AT-SPI2 cannot be built for glibc, that the three SONAMEs are incompatible, or that the bionic package is defective. It records only that the currently approved package and pinned-recipe sources contain no candidate that ADR 0005 permits this project to accept.

## Coupled consumer boundary

The three identities are retained as one accessibility tranche because GTK consumes the bridge/core family as a coupled runtime surface. Consumer relevance cannot create a missing glibc artifact or authorize service activation. Broad AT-SPI bus ownership, registry daemon lifecycle, D-Bus activation, accessibility policy, helper executables, introspection data, schemas, and package-wide files remain outside this decision.

## Stop condition and reopening gate

ADR 0005 requires this tranche to stop without authority. Reopening requires an exact approved Termux glibc archive or coherent archive set, package digest, all three exact member digests and SONAME aliases, pinned recipe tree, runtime dependency closure, GTK accessibility binding, service and D-Bus lifecycle boundary, collision review, update boundary, and rollback boundary.

Bionic package availability, installed bionic bytes, Debian oracle identities, source-level ABI expectations, or a metapackage relationship are not interchangeable with that evidence.

The subsequent GTK 3.24.49 core-pair tranche also stopped without a glibc candidate; the next independent composition tranche is exact `libselinux.so.1` provider evidence acquisition.
