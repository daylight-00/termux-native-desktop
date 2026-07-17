# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  22
accepted exact members:           29
included members:                 28
deferred members:                  1
selected GTK identity gaps:       14
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, or activation.

## Latest bounded tranche

Exact `libfreetype.so.6.20.2` is included for Pango 1.54.0 and GTK 3.24.49 font-face loading, transforms, sizing, metrics/extents, kerning, and glyph rasterization. Exact `libbrotlicommon.so.1.1.0`, `libbrotlidec.so.1.1.0`, `libbz2.so.1.0.8`, and `libz.so.1.3.1` are included only as FreeType transitive feature closure. Existing exact `libpng16.so.16.47.0` remains reused.

No package-wide authority follows. Brotli encoder, CLIs, static/development surfaces, Fontconfig, HarfBuzz, Cairo and the rest of the text stack remain outside this decision.

## Next tranche

The next smallest reviewed-root tranche is `LIBXKBCOMMON_BOUNDED_PROVIDER_AUTHORITY`. It must reconcile selected identity `libxkbcommon.so.0.0.0` with the retained exact Termux candidate filename `libxkbcommon.so.0.8.0`, while preserving SONAME `libxkbcommon.so.0` and bounding the custom Termux step and GTK XKB consumer path.
