# Selected Obsidian provider composition review

## Decision

```text
accepted bounded provider roots: 13
accepted exact members:          19
included in current GTK scope:    18
deferred profile member:          1
selected GTK runtime identities: 36
unresolved selected identities:  19
accepted SONAME collisions:       0
accepted alias collisions:        0
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
target manifest allowed:          NO
```

This Class D review names accepted members without copying, installing, aliasing, populating or activating them. Canonical generated surfaces are `selected-provider-composition-members.tsv`, `selected-provider-composition-gaps.tsv`, and `selected-provider-composition-metadata.tsv` under the provider review directory.

## Included accepted members

Eighteen exact members are included in the bounded selected GTK/GdkPixbuf/X11 scope:

```text
libXfixes.so.3.1.0       -> libXfixes.so.3
libXcomposite.so.1.0.0   -> libXcomposite.so.1
libXi.so.6.1.0           -> libXi.so.6
libXinerama.so.1.0.0     -> libXinerama.so.1
libXcursor.so.1.0.2      -> libXcursor.so.1
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
```

Every proposed alias is the observed ELF SONAME and targets one exact reviewed member. No accepted SONAME or alias basename collides. `libblkid` is included as the accepted transitive dependency of exact `libmount`; it is not one of the 36 selected GTK ledger identities.

`libXcursor` is included only for GTK 3.24.49 X11 cursor theme, image, surface and custom-cursor calls. Cursor-theme data, package-wide development surfaces and target paths remain outside its provider decision.

## Deferred accepted provider

`libtasn1.so.6.6.4 -> libtasn1.so.6` remains accepted but deferred because its scope is external GnuTLS ASN.1/security and no selected security/printing profile has been accepted.

## Completeness result

The selected ledger contains 36 identities. Seventeen selected identities have exact included providers, while `libblkid` is one additional required transitive member. Nineteen selected identities remain unresolved:

```text
open reviewed-root provider gaps: 10
outside-28 or no accepted Termux candidate: 9
```

The next priority gap is exact `libthai.so.0.3.1`. Other blockers continue to include GTK/GDK, Cairo, Fontconfig, FreeType, HarfBuzz, FriBidi, datrie, Pixman, ATK/AT-SPI, Xdamage, xkbcommon and SELinux surfaces. A historical Debian object proves demand only; it never grants target authority.

## Conflict and exclusion policy

The review excludes Debian oracle bytes, static archives, unversioned development aliases, the libjpeg SONAME-8 family, unreviewed Pango surfaces, libepoxy EGL/Wayland, cursor-theme data, and any member without an accepted provider decision. Ordering or `LD_LIBRARY_PATH` precedence cannot resolve a conflict.

## Update and rollback boundary

Re-review is required on provider scope, member/artifact digest, SONAME/alias, selected identity ledger, profile inclusion, candidate multiplicity, collision set, gap count or root mapping changes. Before materialization, rollback is revocation of rows. Any future materialization must use a new immutable generation and preserve the previous generation for selector rollback.

## Decision rationale

```text
REVIEWED_BLOCKED_INCOMPLETE
```

The review is sufficient to reject target-manifest generation, not to accept complete composition. The next smallest tranche is exact `libthai.so.0.3.1`, with Class B `BUILD_IN_SRC`, consumer/data/dependency, conflict, update and rollback boundaries reviewed before any materialization.

## Explicitly prohibited inference

This review does not establish complete runtime composition, target membership or paths, materialization readiness, deployment, activation, cursor-theme data authority, or provider authority for any of the 19 gap rows.
