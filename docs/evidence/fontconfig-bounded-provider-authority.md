# Fontconfig bounded provider authority and filename continuity

## Decision

The exact Termux glibc member `libfontconfig.so.1.14.0` is accepted only as the Fontconfig provider used by Pango 1.54.0 for font discovery, matching, and pattern properties in the selected GTK 3.24.49 text path.

```text
root review:       generic-root-review:26c46ad7612eb40ca721
recipe root:       gpkg/fontconfig
recipe tree:       c5c62dc15d6a897251c88cb7c2306b2a12dd16ba
build script blob: 6ab48ee860385da68de98305aec285a39000126c
artifact:          fontconfig-glibc 2.15.0-1
artifact SHA-256:  c6bc4c9801ee7a45b506d3cc501f1c73a2fe6f1d4b5690eddede158f2b78aafb
selected row:      selected:33fe337448a19e2c6f2f
selected label:    libfontconfig.so.1.12.1
member:            libfontconfig.so.1.14.0
member SHA-256:    33769b91e5bc82e4453766c957733fecc45cf6d0c696fe52c3cdb4084daa591e
SONAME:            libfontconfig.so.1
```

## Exact recipe and Class B boundary

The pinned three-file recipe tree contains `build.sh`, `fcatomic.c.patch`, and `fontconfig-utils.subpackage.sh`. Reconstructing those exact blobs produces the recorded tree `c5c62dc15d6a897251c88cb7c2306b2a12dd16ba`.

The bounded adaptation effects are:

- `termux_step_configure()` delegates to the standard Termux Meson helper;
- package revision 1 binds the revised source archive and font-directory policy;
- the default font-directory, hinting, and sub-pixel arguments alter generated `fonts.conf` policy and compiled default paths;
- the `fcatomic.c` patch makes cache locking use a directory sentinel rather than a hard link, avoiding reliance on hard-link support;
- the utilities subpackage moves `glibc/bin` only and does not move the `libfontconfig.so*` runtime member.

This accepts the exact artifact's library, alias, and bounded cache-lock semantics. It does not promote the package-generated configuration or claim byte equivalence to an unpatched upstream build.

## Concrete filename continuity

Upstream Fontconfig 2.15.0 derives `soversion` as major minus one and the concrete library version as `<soversion>.<minor minus one>.0`. The result is concrete member `libfontconfig.so.1.14.0` and SONAME `libfontconfig.so.1`.

The retained artifact contains:

```text
libfontconfig.so.1 -> libfontconfig.so.1.14.0
```

The selected `libfontconfig.so.1.12.1` label is an older reference filename, not target-path authority. The SONAME alias satisfies the selected runtime identity; neither that older concrete filename nor the unversioned development alias may be synthesized.

## Consumer binding

Pango 1.54.0 links Fontconfig for its FreeType backend. `pango/pangoft2.c` directly builds and matches patterns with `FcPatternBuild` and `FcFontMatch`, reads file, index, transform, antialias, hinting, and autohint properties through `FcPatternGet*`, and then opens and configures the corresponding FreeType face. This is the selected font-discovery and matching consumer path used by the accepted Pango family and GTK text rendering.

## Configuration, font data, and cache boundary

Package defaults are not target policy. The Termux arguments add `/system/fonts`, Termux font directories, hinting, sub-pixel rendering, config directories, and cache directories to generated configuration and compiled defaults. Those paths and files remain outside this provider decision.

The project-owned runtime contract already requires:

- an explicit immutable generation font directory;
- an explicit receipt-owned `FONTCONFIG_FILE` and derived `FONTCONFIG_PATH`;
- a receipt-local writable cache directory;
- no use of an implicit `current` path;
- a fresh cache when the provider, configuration, or font set changes.

The cache-lock patch is accepted only inside that receipt-owned mutable cache boundary. Package or global caches are not promoted, and caches must not be carried across immutable generations.

## Dependency, conflict, and exclusions

Exact FreeType and libexpat providers are already accepted separately. The retained evidence exposes one exact dynamic Fontconfig candidate with matching SONAME and alias, and no accepted member or alias collision exists.

Package-generated `fonts.conf`, package/default font directories, global caches, system-font authority, font population, CLI utilities, headers, pkg-config metadata, static libraries, development aliases, package-wide authority, complete text composition, target population, materialization, deployment, and activation remain outside this decision.

## Update and rollback

Re-review the artifact version and revision, artifact and member digests, SONAME, all three recipe blobs, configure arguments, patch and subpackage semantics, upstream filename formula, Pango tag and direct Fontconfig API surface, FreeType and expat dependency authority, receipt-owned configuration/font/cache contract, and candidate multiplicity on change. Regenerate the cache whenever the provider, configuration, or font set changes.

Before materialization, rollback is revocation of this provider and composition row. After a future materialization, reverse the selector to the prior immutable generation with its matching Fontconfig library, configuration, font set, and fresh receipt-local cache. Do not rewrite the active alias or reuse a cache from another generation in place.

## Composition effect

```text
accepted bounded provider roots overall: 25
accepted roots inside 28-root inventory: 20
open roots inside inventory:              8
accepted exact members:                  32
included members:                        31
deferred members:                         1
unresolved selected identities:          11
composition: REVIEWED_COMPLETE_PROVIDER_SET_TARGET_MANIFEST_NOT_ACCEPTED
target manifest allowed: NO
activation: BLOCKED
```
