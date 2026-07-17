# Selected Obsidian provider composition review

## Decision

```text
accepted bounded provider roots: 17
accepted exact members:          23
included in current GTK scope:    22
deferred profile member:          1
selected GTK runtime identities: 36
unresolved selected identities:  16
accepted SONAME collisions:       0
accepted alias collisions:        0
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
target manifest allowed:          NO
```

This Class D review names accepted members without copying, installing, aliasing, populating or activating them. Canonical generated surfaces are `selected-provider-composition-members.tsv`, `selected-provider-composition-gaps.tsv`, and `selected-provider-composition-metadata.tsv` under the provider review directory.

## Included accepted members

Twenty-two exact members are included in the bounded selected GTK/GdkPixbuf/X11 scope:

```text
libXfixes.so.3.1.0       -> libXfixes.so.3
libXcomposite.so.1.0.0   -> libXcomposite.so.1
libXi.so.6.1.0           -> libXi.so.6
libXinerama.so.1.0.0     -> libXinerama.so.1
libXcursor.so.1.0.2      -> libXcursor.so.1
libcloudproviders.so.0.3.6 -> libcloudproviders.so.0
libepoxy.so.0.0.0        -> libepoxy.so.0
libpango-1.0.so.0.5400.0 -> libpango-1.0.so.0
libpangoft2-1.0.so.0.5400.0 -> libpangoft2-1.0.so.0
libpangocairo-1.0.so.0.5400.0 -> libpangocairo-1.0.so.0
libjpeg.so.62.4.0        -> libjpeg.so.62
libgdk_pixbuf-2.0.so.0.4200.12 -> libgdk_pixbuf-2.0.so.0
libglib-2.0.so.0.8200.2  -> libglib-2.0.so.0
libgobject-2.0.so.0.8200.2 -> libgobject-2.0.so.0
libgmodule-2.0.so.0.8200.2 -> libgmodule-2.0.so.0
libgio-2.0.so.0.8200.2   -> libgio-2.0.so.0
libpng16.so.16.47.0      -> libpng16.so.16
libmount.so.1.1.0        -> libmount.so.1
libblkid.so.1.1.0        -> libblkid.so.1
libthai.so.0.3.1         -> libthai.so.0
libdatrie.so.1.4.0       -> libdatrie.so.1
libiconv.so.2.7.0        -> libiconv.so.2
```

Every proposed alias is the observed ELF SONAME and targets one exact reviewed member. No accepted SONAME or alias basename collides. `libblkid` is included as the accepted transitive dependency of exact `libmount`; it is not one of the 36 selected GTK ledger identities.

`libXcursor` remains bounded to GTK X11 cursor handling. The Thai stack is included only for Pango 1.54.0 Thai breaking: exact libthai and libdatrie selected identities, exact transitive libiconv, and separately recorded `thbrk.tri` content. `libcharset`, CLI/header surfaces and the future dictionary target path are excluded.

## Deferred accepted provider

`libtasn1.so.6.6.4 -> libtasn1.so.6` remains accepted but deferred because its scope is external GnuTLS ASN.1/security and no selected security/printing profile has been accepted.

## Completeness result

The selected ledger contains 36 identities. Twenty selected identities have exact included providers, while `libblkid` and `libiconv` are two additional required transitive members. Sixteen selected identities remain unresolved:

```text
open reviewed-root provider gaps: 7
outside-28 or no accepted Termux candidate: 9
```

The next priority gap is exact `libfreetype.so.6.20.2`. Other blockers continue to include GTK/GDK, Cairo, Fontconfig, FreeType, HarfBuzz, Pixman, ATK/AT-SPI, Xdamage, xkbcommon and SELinux surfaces. A historical Debian object proves demand only; it never grants target authority.

## Conflict and exclusion policy

The review excludes Debian oracle bytes, static archives, unversioned development aliases, the libjpeg SONAME-8 family, unreviewed Pango surfaces, libepoxy EGL/Wayland, cursor-theme data, and any member without an accepted provider decision. Ordering or `LD_LIBRARY_PATH` precedence cannot resolve a conflict.

## Update and rollback boundary

Re-review is required on provider scope, member/artifact digest, SONAME/alias, selected identity ledger, profile inclusion, candidate multiplicity, collision set, gap count or root mapping changes. Before materialization, rollback is revocation of rows. Any future materialization must use a new immutable generation and preserve the previous generation for selector rollback.

## Decision rationale

```text
REVIEWED_BLOCKED_INCOMPLETE
```

The review is sufficient to reject target-manifest generation, not to accept complete composition. The next smallest tranche is exact `libfreetype.so.6.20.2`, with Class B custom-step/configuration semantics, Pango consumer binding, conflict, update and rollback boundaries reviewed before any materialization.

## Explicitly prohibited inference

This review does not establish complete runtime composition, target membership or paths, materialization readiness, deployment, activation, cursor-theme data authority, or provider authority for any of the 16 gap rows.
