# Pango bounded provider authority and concrete-filename continuity

## Decision

```text
root: gpkg/pango
provider decision: ACCEPTED_BOUNDED_PROVIDER
accepted exact family: libpango-1.0.so.0 + libpangoft2-1.0.so.0 + libpangocairo-1.0.so.0
consumer scope: GTK 3.24.49 text layout, X11/FreeType/Fontconfig and Cairo rendering
CF-001 through CF-004: decided
complete composition: not accepted
target population: not accepted
materialization: not performed
activation: not accepted
```

The exact Termux glibc Pango 1.54.0 artifact is accepted as one three-member provider family. The decision is Class B project integration over a Class A package-specific recipe boundary.

Canonical records:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    pango-reference-consumed-provider-authority.tsv
    pango-concrete-filename-continuity-policy.tsv
```

## Exact artifact and members

```text
root review:  generic-root-review:0dacddae106c6bd1006b
recipe tree: f9e9e2303e2c91322f7edcf1bc0c3b99f2d1d74a
package:      pango-glibc 1.54.0
artifact id:  generic-artifact:7fdbef58f2a4fff712db
artifact SHA: 7fdbef58f2a4fff712db62b7fcd0cab0bde91373eb4d1d133e97e947b9f43084
```

| Capability | Exact member | SHA-256 | `DT_SONAME` | Observed SONAME alias target |
|---|---|---|---|---|
| Pango core layout | `libpango-1.0.so.0.5400.0` | `7debdcbc3dec18f7377e53a07a4d14159cde68b4cc07f0ed1c087f9d56268336` | `libpango-1.0.so.0` | `libpango-1.0.so.0.5400.0` |
| FreeType/Fontconfig backend | `libpangoft2-1.0.so.0.5400.0` | `d80ef53ee344d7661acfa9b2fc863a61f24a2ff4f4492162eaa1582d62c2b305` | `libpangoft2-1.0.so.0` | `libpangoft2-1.0.so.0.5400.0` |
| Cairo rendering | `libpangocairo-1.0.so.0.5400.0` | `c5ac95a46ad20c9536c0d63b38e1ee728f2d71e865e5aad6034e65f89f0ba708` | `libpangocairo-1.0.so.0` | `libpangocairo-1.0.so.0.5400.0` |

The three observed aliases bind to exact reviewed ELF targets whose `DT_SONAME` equals the lookup name.

## Why `5400.0` is the exact 1.54.0 concrete family

Pango 1.54.0 computes its library version from the project minor and micro version while keeping `soversion = 0`:

```text
binary_age = 54 * 100 + 0
interface_age = 0
libversion = 0.5400.0
```

The same `pango_libversion` and `pango_soversion` are used for `libpango`, `libpangoft2`, and `libpangocairo`. Therefore the Termux `5400.0` suffix is the upstream-defined concrete family for the pinned 1.54.0 source. The oracle labels ending in `5600.3` describe a different Pango release and are not a target filename contract.

Authoritative source coordinates:

```text
GNOME/pango tag 1.54.0
    meson.build
    pango/meson.build
```

## GTK and Pango consumer binding

GTK 3.24.49 requires Pango 1.41 or newer and links `pangocairo`. For X11 or Wayland builds it additionally links `pangoft2`. Pango 1.54.0 constructs:

```text
libpango
    core internationalized text layout

libpangoft2
    links libpango and supplies FreeType/Fontconfig support

libpangocairo
    links libpango and, when the FreeType backend is selected, libpangoft2
```

The pinned Pango recipe declares Cairo, Fribidi, HarfBuzz, LibThai, Xft and introspection dependencies without package-specific patches, hooks, build options or output transformations. Exact dependency-provider authority remains separate; this decision only binds the three Pango members to the selected GTK text capability.

## CF-001 — alias necessity

```text
decision: ACCEPT_SONAME_ALIAS_CONTINUITY_REQUIRED
```

A future immutable provider generation must expose each accepted SONAME lookup name so that it resolves to the reviewed exact member with the same `DT_SONAME`.

This does not choose the final target directory and does not authorize package-native absolute paths or unversioned development aliases such as `libpango-1.0.so`.

## CF-002 — successor selection

```text
decision: ACCEPT_EXACT_1_54_0_THREE_MEMBER_FAMILY_AS_BOUNDED_SUCCESSOR
```

The exact Termux 1.54.0 family is accepted as the bounded successor to the oracle concrete labels because selection is based on:

```text
exact artifact and member digests
matching stable SONAMEs
upstream-defined 1.54.0 concrete version
GTK 3.24.49 capability and minimum-version binding
one internally coherent three-member artifact family
```

The decision does not claim byte equivalence with the oracle. A changed concrete suffix alone is neither proof of compatibility nor proof of incompatibility.

## CF-003 — update boundary

Any new Pango artifact must receive a new review row and immutable generation. Re-review is mandatory for changes to:

```text
artifact version or SHA-256
any of the three member digests or SONAMEs
alias names or targets
recipe tree or upstream feature resolution
GTK minimum version or consumer set
Pango dependency and backend selection
candidate conflict set
```

An unchanged SONAME does not automatically authorize new bytes. A concrete suffix change alone does not require rejection when the complete bounded contract is re-established.

## CF-004 — rollback continuity

```text
decision: ROLL_BACK_WHOLE_FAMILY_AND_ALIASES_TO_PRIOR_IMMUTABLE_GENERATION
```

The three objects and three SONAME aliases form one atomic rollback unit. A future rollback must reverse the selected immutable generation to the prior complete family. Mixing `libpango`, `libpangoft2`, or `libpangocairo` objects or aliases from different generations is rejected.

This transaction does not create a generation or mutate a selector.

## Conflicts and exclusions

```text
one exact dynamic Termux glibc artifact family accepted
Debian/oracle 5600.3 bytes excluded from target authority
unversioned development aliases excluded
pangoxft and other unreviewed Pango members excluded
Cairo, Fontconfig, FreeType, HarfBuzz, Fribidi, Xft and LibThai provider authority remains separate
complete GTK/application composition excluded
target paths, ownership, materialization and activation excluded
```

## Authority effect

This decision closes the final no-token provider root and the four Pango continuity issues. It accepts only the exact three-member Pango family for the selected GTK 3.24.49 text capability and its immutable SONAME continuity rules.

The next task is the `libjpeg.so.62` object-requirement/provider-candidate correction. It precedes broader reference-adapted provider review because it is the sole T0 requirement mismatch.
