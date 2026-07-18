# libXdamage provider evidence blocker

## Decision

```text
selected identity:       libXdamage.so.1.1.0
required SONAME:         libXdamage.so.1
provider authority:      OPEN_BLOCKED_NO_GLIBC_CANDIDATE
composition effect:      NONE; the selected identity remains one of eight gaps
target/activation:       BLOCKED
```

The read-only acquisition result is retained by SHA-256
`5cb840b494176e8671d57cfc2617142a5d15663275456e102f075bc0796f3f55`.
The probe did not install or upgrade a package and did not modify the repository or any provider target.

## What the approved indexes established

The glibc package query `libxdamage-glibc` returned no package. A separate query for
`libxdamage` returned the ordinary Termux X11 package:

```text
package:          libxdamage 1.1.7
architecture:     aarch64
filename:         pool/main/libx/libxdamage/libxdamage_1.1.7_aarch64.deb
size:             5208
index SHA-256:     2ded05bd7a409cff0dce05942d69028b962921a20d1c3559b302a75711e10c98
```

That filename belongs to the normal Termux/X11 bionic repository. Combining it with the
Termux glibc repository base produced HTTP 404. Changing only the base URL would retrieve a
bionic artifact, not an artifact for the separate glibc application world, so it is not a valid
provider-candidate correction.

## Recipe provenance boundary

At pinned glibc recipe commit `9bdd20c1d36524a0ab016d9b71c748b0cbb20a34`,
`termux-pacman/glibc-packages` has no `gpkg/libxdamage/build.sh` root and repository search
finds no libXdamage recipe. The ordinary Termux recipe exists separately at
`termux/termux-packages@552a825cc8433e3aced966ff4bf5c8ea9255ca7d` under
`x11-packages/libxdamage/build.sh`; it is evidence about source version and dependencies only,
not a glibc provider candidate.

## Consumer binding retained

GTK 3.24.49 treats `xdamage` as an optional X11 dependency. When found it sets
`HAVE_XDAMAGE`, includes the dependency in the X11 package set, and links it into the GDK X11
backend. This establishes why the selected SONAME matters, but consumer binding cannot create
a missing provider artifact.

## Stop condition and reopening gate

ADR 0005 requires this tranche to stop without authority because no approved Termux glibc
package/member and no pinned glibc recipe root exist. Reopening requires one exact glibc
artifact plus package digest, exact member digest, SONAME, alias chain, pinned recipe, runtime
dependency closure, and bounded GTK consumer review. A bionic package, source-level ABI
expectation, or upstream build is not interchangeable with that evidence.

The next independent composition tranche is Graphite2 evidence acquisition.
