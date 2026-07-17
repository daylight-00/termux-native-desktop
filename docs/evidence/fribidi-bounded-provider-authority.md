# Bounded FriBidi provider authority

> Decision: `ACCEPTED_BOUNDED_PROVIDER`
>
> Scope: exact `libfribidi.so.0.4.0` for Pango 1.54.0 core Unicode bidirectional character classification, bracket handling and paragraph embedding-level resolution used by selected GTK 3.24.49 text processing.

## Exact coordinates

```text
recipe root:    gpkg/fribidi
recipe tree:    41ad596c81980f710112cd74d4f1b428cfbc6d6a
build blob:     c251a59a3b7464fa5ae6dd5b5b65df62a12f9600
artifact:       fribidi-glibc 1.0.16
artifact SHA:   9e99711a88e10441c0eee7af77c64b9ee1a6c93484b0e16ac381ed242057219f
member:         libfribidi.so.0.4.0
member SHA:     71668fd02e89fa7546446bb7961bb618f6d22e1506f7444bbea6788befbb7895
SONAME:         libfribidi.so.0
selected row:   selected:5d210dfa49b6cf4c1077
```

## Class B custom-step boundary

The pinned recipe declares a custom `termux_step_configure()` whose entire body calls the generic `termux_step_configure_meson` helper. It supplies no extra arguments, patches, generated data, post-install object rewrite, ABI option or SONAME change. The token is therefore retained as Class B because it is an explicit hook, but its bounded semantic result is standard Meson delegation with no package-specific runtime-object delta. This is not a producing-build-equivalence claim.

## Consumer binding

Pango 1.54.0 requires FriBidi `>= 1.0.6` unconditionally and adds it to the core `pango_deps` set. Its bidi implementation includes `fribidi.h` and directly calls:

```text
fribidi_get_bidi_type()
fribidi_get_bracket()
fribidi_get_par_embedding_levels_ex()
```

These calls implement Unicode bidirectional character classification, bracket analysis, base-direction resolution and paragraph embedding levels. The selected GTK 3.24.49 text path consumes the accepted Pango core family, so static source and dependency evidence close the bounded consumer binding without a device probe.

## Dependency and conflict boundary

GLib/glibc and the accepted Pango family remain retained dependencies. HarfBuzz, Fontconfig, FreeType, Cairo and the remaining text/GTK providers are separate composition decisions. One exact dynamic Termux-glibc candidate is present with no member or SONAME drift and no accepted-member or alias collision.

## Exclusions

- FriBidi CLI, headers, pkg-config, documentation, tests and development surfaces;
- Debian oracle bytes as target authority;
- the remaining text stack, complete Pango/GTK composition or target paths;
- target population, materialization, deployment or activation;
- producing-build equivalence.

## Update and rollback

Re-review on artifact/member/version/SHA/SONAME, recipe tree, build-script blob or delegation body, Pango tag, required FriBidi version, dependency or bidi API call surface, or candidate multiplicity changes. Before materialization revoke this row; after a future immutable generation, roll back the selector to the prior generation.

## Authority effect

The exact member is accepted only for selected Pango 1.54.0 and GTK 3.24.49 Unicode bidirectional-text processing. Composition remains incomplete; target population and activation remain blocked.
