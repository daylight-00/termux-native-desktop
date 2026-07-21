# GTK 3 core provider evidence blocker

## Decision

```text
selected identities:     libgdk-3.so.0.2417.32
                         libgtk-3.so.0.2417.32
required SONAMEs:        libgdk-3.so.0
                         libgtk-3.so.0
provider authority:      OPEN_BLOCKED_NO_GLIBC_CANDIDATE
composition effect:      NONE; both selected identities remain gaps
target/activation:       BLOCKED
```

The read-only acquisition result is retained by SHA-256
`26ac394a3808b59d0999a6cc5c4ae1210fa6f6257932b3c51a1056530f568b4d`.
The probe did not install, upgrade, mutate the repository, populate a provider target, deploy GTK, or activate any display, accessibility, settings, theme, input-method, or D-Bus surface.

## What the approved indexes established

The candidate-name set was derived without assuming one package name:

```text
gtk-3-glibc
gtk-glibc
gtk3-glibc
libgtk-3-glibc
libgtk3-glibc
```

Every exact glibc query returned no policy entry and no package stanza. The only GTK 3 runtime package observed was ordinary Termux/X11 bionic `gtk3` version `3.24.52`, installed and selected from `x11/main` for `aarch64`. That package is a different ABI world and does not supply a Termux glibc archive, exact glibc member, or cross-world provider authority for the selected Debian 3.24.49 identities.

## Recipe provenance boundary

At pinned glibc recipe commit `9bdd20c1d36524a0ab016d9b71c748b0cbb20a34`, exact-path checks for the plausible roots
`gpkg/gtk3/build.sh`, `gpkg/gtk/build.sh`, `gpkg/gtk-3/build.sh`, `gpkg/libgtk3/build.sh`, and `gpkg/libgtk-3/build.sh` failed, and repository search found no GTK 3 producing root. The recipe root therefore remains unavailable for this approved glibc world.

This finding is narrower than an upstream-source or ABI rejection. It does not claim that GTK 3 cannot be built for glibc, that the two SONAMEs are incompatible, or that the bionic package is defective. It records only that the currently approved package and pinned-recipe sources contain no candidate that ADR 0005 permits this project to accept.

## Atomic pair and backend boundary

The two identities remain one atomic core tranche because `libgtk-3.so.0` directly binds `libgdk-3.so.0`, and backend, input, theme, settings, accessibility, printing, portal, and service behavior cannot be inferred from one member in isolation. Consumer relevance and an existing bionic installation cannot create missing glibc bytes.

Broad GTK package contents, tools, demos, schemas, icon caches, themes, input modules, print backends, Wayland/X11 backend enablement, accessibility integration, D-Bus activation, and package-wide files remain outside this decision.

## Source-coordinate correction

The package/recipe absence decision remains valid, but the previous project-selected GTK commit was not the 3.24.49 release commit. `GTK3-SOURCE-COORDINATE-001` supersedes that source coordinate with official tag object `9003f198803b9b8b1d7def25a2359f8ebb4b25cf`, peeled commit `198aeace1e9e119c77f4d669bd8efdf337828ad1`, and archive SHA-256 `a2958d82986c81794e953a3762335fa7c78948706d23cced421f7245ca544cbc`. Archive/tag byte-manifest equivalence and protected-state invariance passed. This correction does not create a glibc GTK candidate or widen provider authority.

## Stop condition and reopening gate

ADR 0005 requires this tranche to stop without authority. Reopening requires an exact approved Termux glibc archive or coherent archive set, package digest, both exact member digests and SONAME aliases, pinned recipe tree, runtime dependency closure, GTK-to-GDK direct binding, optional-backend boundary, collision review, update boundary, and rollback boundary.

Bionic package availability, installed bionic bytes, Debian oracle identities, source-level ABI expectations, or an upstream release version are not interchangeable with that evidence.

The next independent composition tranche is exact `libselinux.so.1` provider evidence acquisition.
