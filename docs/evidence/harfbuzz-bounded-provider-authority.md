# HarfBuzz bounded provider authority and filename continuity

## Decision

The exact Termux glibc member `libharfbuzz.so.0.61010.0` is accepted only as the HarfBuzz core OpenType shaping provider used by Pango 1.54.0 in the selected GTK 3.24.49 text-layout scope.

```text
root review:       generic-root-review:706bd01fdd0555fcabc9
recipe root:       gpkg/harfbuzz
recipe tree:       f353d5f116250f7bcab7ecf062cdb13728b0ecc8
build script blob: 904a87a0e4debe61c0c6408178823bf1da34cbff
artifact:          harfbuzz-glibc 10.1.0
artifact SHA-256:  d0e4a83180560341dc02fccd3b2df1892338a84c4cecfa4c7f6bc1c2566eacfc
selected row:      selected:c41cd8cc82847fba1410
selected label:    libharfbuzz.so.0.61020.0
member:            libharfbuzz.so.0.61010.0
member SHA-256:    179133d6e95f6e378f44ad9222255620ecdd39c30c5aedce028d99f2b28470c6
SONAME:            libharfbuzz.so.0
```

## Exact recipe and Class B boundary

The pinned five-file recipe tree consists of `build.sh`, one Meson patch, and three subpackage scripts. Its reconstructed Git tree is the recorded `f353d5f116250f7bcab7ecf062cdb13728b0ecc8`.

The bounded adaptation effects are:

- `termux_step_pre_configure()` removes inherited `-fexceptions`; upstream HarfBuzz already adds `-fno-exceptions`, so this prevents contradictory compiler flags.
- `termux_step_configure()` delegates to the standard Termux Meson helper.
- the patch changes the requested C++ dialect from C++11 to C++17 and does not change the public C SONAME policy;
- documentation is disabled;
- Graphite2 and introspection are enabled, but this does not grant authority to Graphite2, GIR/typelib output, or other dependencies;
- the Cairo, ICU, and utility subpackage scripts move sibling libraries, headers, metadata, and tools, not the core `libharfbuzz.so*` member.

This accepts the exact artifact's bounded build and packaging semantics. It does not claim byte equivalence to an unpatched upstream build.

## Concrete filename continuity

Upstream 10.1.0 computes its integer library version as `60000 + major*100 + minor*10 + micro`, then emits concrete version `0.<integer>.0` with shared-library `soversion` `0`. Therefore 10.1.0 produces `libharfbuzz.so.0.61010.0`; the selected `0.61020.0` label corresponds to a later 10.2.0 reference filename and is not target-path authority.

The retained artifact contains:

```text
libharfbuzz.so.0 -> libharfbuzz.so.0.61010.0
```

The alias and exact member satisfy the selected SONAME identity. The older or newer concrete filename and the unversioned development alias must not be synthesized.

## Consumer binding

Pango 1.54.0 requires HarfBuzz at build time and directly uses the core API in `pango/shape.c`: it creates and configures buffers and sub-fonts, adds UTF-8 text, sets direction, script and language, invokes `hb_shape`, and consumes the resulting glyph information and positions. This closes the bounded Pango shaping consumer binding without a device probe.

## Dependency, conflict, and exclusions

The retained evidence exposes one exact dynamic Termux glibc candidate with matching SONAME and SONAME alias. No accepted member or alias collision exists.

FreeType and GLib remain separately accepted providers. Cairo, Graphite2, ICU, GObject/introspection, `libharfbuzz-subset`, `libharfbuzz-cairo`, `libharfbuzz-icu`, tools, headers, pkg-config, GIR/typelib, static libraries, development aliases, package-wide authority, complete text composition, target population, materialization, deployment, and activation remain outside this decision.

## Update and rollback

Re-review the artifact and member digests, SONAME, complete five-file recipe tree, pre-configure/configure bodies, Meson options, C++17 patch, upstream concrete-version formula, Pango tag and API surface, feature dependency set, and candidate multiplicity on change.

Before materialization, rollback is revocation of this provider and composition row. After a future materialization, reverse the selector to the prior immutable generation; do not rewrite the active alias in place.

## Composition effect

```text
accepted bounded provider roots overall: 24
accepted roots inside 28-root inventory: 19
open roots inside inventory:              9
accepted exact members:                  31
included members:                        30
deferred members:                         1
unresolved selected identities:          12
composition: ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION
target manifest allowed: NO
activation: BLOCKED
```
