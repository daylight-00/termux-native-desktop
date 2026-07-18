# Cairo and Cairo-GObject bounded provider authority and filename continuity

## Decision

The exact Termux glibc members `libcairo.so.2.11802.2` and `libcairo-gobject.so.2.11802.2` are accepted as one atomic provider root only for Pango 1.54.0 Cairo rendering, GTK 3.24.49 core Cairo drawing/surface use, and Cairo GObject type integration.

```text
root review:              generic-root-review:0263d4b55d6a43edad7b
recipe root:              gpkg/libcairo
recipe tree:              b80a0990d43609e09f1480394225d2b068ce5881
build script blob:        8b848a1277895bdaf1283626ef37fc1c8ddcb399
utility patch blobs:      721e922afa575e5bc6d186c0ca7e94a332992a6d
                          5403431999d0d439e124a135b18708de2e64b609
artifact:                 libcairo-glibc 1.18.2
artifact SHA-256:         3250dba4dc3312b4fcaa763c788614c63ba611ee82451224ba10da50622a0db2
artifact size:            579172
result archive SHA-256:   3df4f72452b6fb36525ea651f58a0d9d0e551d6ab1f0076653588e767fb1ad9a
core member:              libcairo.so.2.11802.2
core SHA-256:             43cd64f07e1c33e5bd574fe7f50a20062a2ab6836adf80e1b5f4b6846e05264d
core SONAME:              libcairo.so.2
GObject member:           libcairo-gobject.so.2.11802.2
GObject SHA-256:          2440680a9d0c94d58d87d5916d168535b7dc4263648df9aa0b787ef2f7d3a166
GObject SONAME:           libcairo-gobject.so.2
```

## Exact recipe and Class B boundary

The pinned recipe tree contains `build.sh`, `cairo-script-operators.c.patch`, and `fdr.c.patch`; the exact blobs reconstruct the recorded tree. The Meson-native build disables DWrite, Spectre, symbol lookup, and tests. These options exclude non-selected platform, document, diagnostic, and test surfaces rather than replacing the selected Linux/X11 public ABI.

Both prefix patches touch utility sources only: one redirects a Cairo-script interpreter temporary font file and the other redirects the FDR trace path from `/tmp` to the Termux classical prefix. They do not modify the core or Cairo-GObject public APIs, SONAMEs, or the two retained runtime ELF members. Utility authority is not granted.

## Concrete filename continuity

The retained artifact contains:

```text
libcairo.so.2 -> libcairo.so.2.11802.2
libcairo-gobject.so.2 -> libcairo-gobject.so.2.11802.2
```

The selected Debian `1.18.4` labels ending in `2.11804.4` are reference filenames, not target paths. The accepted runtime contract is the two stable SONAME aliases bound to the exact `1.18.2` members. The older or newer concrete reference filenames and unversioned development aliases must not be synthesized.

## Consumer binding

GTK 3.24.49 requires both `cairo` and `cairo-gobject` at version 1.14 or newer and also requires `pangocairo`. Pango 1.54.0 uses Cairo for its Cairo rendering backend. Exact Cairo-GObject records direct dependencies on `libcairo.so.2`, `libglib-2.0.so.0`, and `libgobject-2.0.so.0`, binding the GType integration member to the same accepted core Cairo member and GLib family.

The two members are atomic: Cairo-GObject is not accepted without the exact core Cairo provider, and rollback must move both together.

## Dependency boundary

Exact Cairo core records direct runtime edges to `libm`, zlib, libpng, Fontconfig, FreeType, libX11, libXext, libXrender, libxcb, libxcb-render, libxcb-shm, Pixman, libc, and the loader. Those provider identities are already accepted. The exact Pixman prerequisite is pinned separately by the same result archive. `liblzo-glibc` is package metadata only and is not a Cairo core `DT_NEEDED` edge in the retained ELF.

No additional runtime provider member is introduced by this decision beyond the two Cairo members.

## Conflict and exclusions

There is one exact dynamic package candidate with two reviewed members and matching SONAME aliases. No accepted member or alias collision exists.

Cairo-script interpreter, FDR, command-line tools, tests, DWrite, Spectre and other non-selected backends, static libraries, headers, pkg-config data, unversioned development aliases, package-wide authority, oracle bytes, complete rendering or GTK composition, target population, materialization, deployment, and activation remain outside this decision.

## Update and rollback

Re-review the source and artifact version, package digest and size, both member digests, SONAMEs and aliases, all three recipe blobs, Meson options, patch application and utility-only scope, GTK/Pango consumer binding, exact accepted dependency closure, and candidate multiplicity on change.

Before materialization, rollback is atomic revocation of both Cairo composition rows. After a future materialization, reverse the selector to the prior immutable generation with its matching Cairo core, Cairo-GObject, Pixman, and dependency set. Do not rewrite either active alias in place.

## Composition effect

```text
accepted bounded provider roots overall: 28
accepted roots inside 28-root inventory: 21
open roots inside inventory:              7
accepted exact members:                  36
included members:                        35
deferred members:                         1
unresolved selected identities:           7
composition: REVIEWED_BLOCKED_INCOMPLETE
target manifest allowed: NO
activation: BLOCKED
```
