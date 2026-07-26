# FreeType bounded provider authority

## Decision

The exact Termux glibc member `libfreetype.so.6.20.2` is accepted only as the FreeType engine used by Pango 1.54.0 and GTK 3.24.49 for font-face loading, transforms, sizing, metrics and extents, kerning, and glyph rasterization.

```text
root review:       generic-root-review:af39bbec812180537c5a
recipe root:       gpkg/freetype
recipe tree:       3a92f7895a8a4ef5cfe33fcc8b806acccffd0313
build script blob: a2ebf194e945c35b0f8147a4d9f0ed2d2a43fd26
artifact:          freetype-glibc 2.13.3
artifact SHA-256:  8e1d9d34f13c6c95aba5e9a5f636facc94e0ca7c073f68cf605858a499a54e7b
member:            libfreetype.so.6.20.2
member SHA-256:    04723b724b36bd516936461db4ee32a692f15af7abb99cd52cd287afa36118cf
SONAME:            libfreetype.so.6
selected row:      selected:654806f659f7b97ba9d1
```

## Class B boundary

The custom `termux_step_configure()` delegates exactly to `termux_step_configure_meson`. The only extra configure argument is `-Dfreetype2:default_library=shared`. Upstream FreeType defines this option as output-form selection: build the shared library instead of the default static/shared set. It does not change the module list, public ABI, SONAME, compression features, font data, or runtime path policy.

The decision must be re-reviewed if the recipe tree, build-script blob, delegation body, output-form argument, feature dependency set, member digest, or SONAME changes.

## Consumer binding

Pango 1.54.0 builds its FT2 path with FreeType on the selected Linux/Fontconfig route. `pangoft2.c` directly uses `FT_New_Face`, `FT_Set_Transform`, `FT_Set_Char_Size`, `FT_Get_Kerning`, and `FT_Done_Face`, and exposes the locked native `FT_Face`. This statically closes the bounded Pango/GTK consumer binding without a device probe.

## Exact transitive feature closure

The following exact objects already had conditional object-scoped authority. They are now included only for the exact FreeType feature closure:

| member | SHA-256 | bounded role |
|---|---|---|
| `libbrotlicommon.so.1.1.0` | `46ae61c88b9a2f32b13dfe81a3353a6aef2c83f3cbacf5270197878c47aab9be` | common runtime for Brotli decoding |
| `libbrotlidec.so.1.1.0` | `8faac8e6d945bf1d5f113d986502bf28883fa0cf7a0feb529840124d2b804a87` | Brotli/WOFF2 decompression |
| `libbz2.so.1.0.8` | `93de8c4bb245b253dfc357349a9b81e5ed6fb01ac1c9513e0c36fbf5c5a84167` | bzip2 compressed font streams |
| `libz.so.1.3.1` | `6835963ff1be924f73cdd59f29f2e2521d1705b3ce2d0e90a0c0fd4c5773a070` | system zlib compressed font streams |

The already accepted exact `libpng16.so.16.47.0` is reused. This does not accept the Brotli encoder, CLIs, package tools, static libraries, headers, unversioned development aliases, or package-wide authority.

## Exclusions

This decision does not accept Fontconfig, HarfBuzz, Cairo, the complete text stack, arbitrary optional FreeType features, tool or development surfaces, target paths, population, materialization, deployment, activation, or producing-build equivalence.

## Update and rollback

Before materialization, revoke the FreeType and four transitive composition rows together if any pinned identity or consumer boundary changes. After a future materialization, reverse the selector to the prior immutable generation; do not mutate the active generation in place.

## Composition effect

```text
accepted bounded provider roots overall: 22
accepted roots inside 28-root inventory: 17
open roots inside inventory:             11
accepted exact members:                  29
included members:                        28
deferred members:                         1
unresolved selected identities:          14
composition: REVIEWED_COMPLETE_PROVIDER_SET_TARGET_MANIFEST_NOT_ACCEPTED
target manifest allowed: NO
activation: BLOCKED
```
