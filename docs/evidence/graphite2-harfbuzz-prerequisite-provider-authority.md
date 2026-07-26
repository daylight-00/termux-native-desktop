# Graphite2 bounded HarfBuzz prerequisite provider authority

## Decision

The exact Termux glibc member `libgraphite2.so.3.2.1` is accepted only as the Graphite shaping-engine prerequisite compiled into exact HarfBuzz 10.1.0 for Graphite-enabled fonts within the selected Pango 1.54.0 and GTK 3.24.49 text scope.

```text
authority root:      outside-28-root:gpkg/libgraphite
recipe root:         gpkg/libgraphite
recipe tree:         4e3ab8e653cedfa4b31e8de229966af2b28c89a1
build script blob:   1fd081fa93558fd044a053afb26a170a2cef6a09
artifact:            libgraphite-glibc 1.3.14
artifact size:       84252
artifact SHA-256:    2144bb899adc6511df6ebf287b518d339c70b864dcfac3e3d31508187c87dfef
result archive SHA:  b0ae73019a2b442d96daa148219cfcf21f265b8dec48d82aef74dd95d536f29f
selected row:        selected:5de74dd687fd1dd5ee3a
selected label:      libgraphite2.so.3.2.1
member:              libgraphite2.so.3.2.1
member SHA-256:      6caaa46abe585228b0fa45a60bdbb5e9951384148963856d1ce2e886e5b06e7f
SONAME:              libgraphite2.so.3
```

## Exact package and alias continuity

The approved index identified only `libgraphite-glibc_1.3.14_aarch64.deb` under `pool/stable/`. Its declared size and SHA-256 exactly matched the downloaded archive. The extracted runtime contains:

```text
libgraphite2.so.3 -> libgraphite2.so.3.2.1
libgraphite2.so   -> libgraphite2.so.3
```

The selected concrete label and candidate concrete member are identical. Runtime authority covers the exact member and stable SONAME alias only. The unversioned development alias is excluded.

## Recipe and Class B boundary

The pinned recipe root contains one `build.sh`; its reconstructed Git tree is `4e3ab8e653cedfa4b31e8de229966af2b28c89a1`. It uses Graphite2 1.3.14 and has no package-specific patch or custom build function. Its bounded configuration:

- disables install RPATH;
- disables the compare renderer;
- selects the direct Graphite VM;
- depends on `gcc-libs-glibc`.

This is accepted as a bounded Class B build/configuration decision for the exact runtime member. It does not claim byte or performance equivalence to another build, nor authority for tools, tests, headers, CMake metadata, static output, development aliases, or all package contents.

## HarfBuzz consumer binding

The accepted HarfBuzz recipe enables Graphite2. In HarfBuzz 10.1.0, that feature adds `hb-graphite2.cc`, its public integration header, and the Graphite dependencies to core `libharfbuzz`.

The integration is not token-only: `hb-graphite2.cc` creates a Graphite face from HarfBuzz table callbacks, resolves language features, applies requested feature values, calls `gr_make_seg`, then consumes `gr_seg_*` and `gr_slot_*` segment and slot results to populate HarfBuzz glyph output. The bounded consumer is therefore the Graphite-font shaping path inside exact HarfBuzz 10.1.0, reached through the already accepted Pango shaping provider.

This decision does not widen general HarfBuzz provider authority or claim that every Graphite font and feature set has been functionally validated.

## Runtime dependency closure

The exact Graphite2 ELF records only:

```text
libc.so.6
ld-linux-aarch64.so.1
```

No additional unresolved selected provider edge is introduced. Package control declares only `gcc-libs-glibc`.

## Conflict, update, and rollback

No accepted member or alias collision exists. Debian oracle bytes, other concrete versions, development aliases, and package-wide surfaces are excluded.

Re-review the approved-index coordinate, artifact size and digest, member digest, SONAME and alias, complete one-file recipe tree, CMake options, HarfBuzz Graphite feature build path, direct Graphite API surface, runtime dependencies, and candidate multiplicity on change.

Before materialization, rollback is revocation of this row and the HarfBuzz Graphite-feature prerequisite scope. After future materialization, reverse the selector to a prior immutable generation containing a matching HarfBuzz/Graphite2 pair; never rewrite an active alias in place.

## Composition effect

```text
accepted bounded provider roots overall: 28
accepted roots inside 28-root inventory: 21
open roots inside inventory:              7
accepted exact members:                  37
included members:                        36
deferred members:                         1
unresolved selected identities:           6
composition: REVIEWED_COMPLETE_PROVIDER_SET_TARGET_MANIFEST_NOT_ACCEPTED
target manifest allowed: NO
activation: BLOCKED
```
