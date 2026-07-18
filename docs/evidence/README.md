
# Evidence documentation

This index routes observed facts, experiment interpretations, raw captures, receipts, and transaction records.

## Experiment evidence

Start at [`../../experiments/README.md`](../../experiments/README.md).

Within an experiment:

```text
README.md
    current canonical interpretation of that experiment

report.md
    detailed first-hand report and provenance

evidence/
    raw or minimally processed captures

recipe/
    reproduction material
```

A historical report may describe a superseded architecture. Use the experiment README for its current interpretation.

## Transaction evidence

[`../refactor/README.md`](../refactor/README.md) indexes the numbered repository/provider-authority transaction records. The numbered files preserve bounded state transitions and receipts. They are historical evidence, not a default current-state surface.

## Evidence-to-authority boundary

Evidence can establish an observation, candidate, identity, or bounded comparison. Promotion to provider authority, composition, target population, activation, or acceptance requires the applicable current contract and accepted decision.

The accepted assurance-depth policy is in [`../decisions/0005-proportional-assurance-depth.md`](../decisions/0005-proportional-assurance-depth.md).

The current provider claim inventory and SUP-02 reclassification are in [`provider-claim-classification.md`](provider-claim-classification.md).

The completed seven-root Class A recipe review is in [`no-token-recipe-semantic-review.md`](no-token-recipe-semantic-review.md). The four bounded X.Org provider decisions are in [`xorg-reference-consumed-provider-authority.md`](xorg-reference-consumed-provider-authority.md). The bounded libtasn1 decision is in [`libtasn1-reference-consumed-provider-authority.md`](libtasn1-reference-consumed-provider-authority.md).

The bounded libepoxy decision is in [`libepoxy-reference-consumed-provider-authority.md`](libepoxy-reference-consumed-provider-authority.md). Its scope is GTK 3.24.49 X11 GLX dispatch only; EGL is not claimed.

The bounded Pango family and CF-001–CF-004 continuity decisions are in [`pango-reference-consumed-provider-authority-and-filename-continuity.md`](pango-reference-consumed-provider-authority-and-filename-continuity.md).

The OJ-001 `libjpeg.so.62` repository-candidate disposition and pinned-source compatibility-provider production boundary are in [`libjpeg-so-62-provider-candidate-disposition.md`](libjpeg-so-62-provider-candidate-disposition.md). The first scratch-built candidate result and its blocking colon-only `DT_RUNPATH` are reviewed in [`libjpeg-so-62-compatibility-provider-candidate-result-review.md`](libjpeg-so-62-compatibility-provider-candidate-result-review.md). The corrected runpath-free candidate identity and bounded consumer-validation boundary are reviewed in [`libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md`](libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md).

- [`libjpeg-so-62-gdkpixbuf-diagnostic-matrix-result-review.md`](libjpeg-so-62-gdkpixbuf-diagnostic-matrix-result-review.md) — non-dispositive first diagnostic matrix and corrected loader boundary.
- [`libjpeg-so-62-loader-isolated-provider-authority.md`](libjpeg-so-62-loader-isolated-provider-authority.md) — exact loader-isolated candidate/oracle controls and bounded GdkPixbuf JPEG provider-authority decision.

- [`selected-obsidian-provider-composition-review.md`](selected-obsidian-provider-composition-review.md) records the current Class D non-materializing composition manifest, 35 exact accepted members, exclusions, collisions and 8 blocking selected GTK identities.

- [`gdkpixbuf-core-provider-acquisition-result-review.md`](gdkpixbuf-core-provider-acquisition-result-review.md) binds the exact GLib-family and libpng candidate identities, records the missing Termux GdkPixbuf package/recipe, and routes the upstream 2.42.12 scratch build.

- [`gdkpixbuf-2-42-12-provider-candidate-result-review.md`](gdkpixbuf-2-42-12-provider-candidate-result-review.md) — exact official-source GdkPixbuf object, four-cell JPEG/PNG functional evidence, bounded provider decision, and open reference/transitive dependency boundary.

- [`gdkpixbuf-exact-util-linux-provider-authority.md`](gdkpixbuf-exact-util-linux-provider-authority.md) — exact official libmount/libblkid bounded GDK Pixbuf transitive provider decision.
- [`libxcursor-bounded-provider-authority.md`](libxcursor-bounded-provider-authority.md) — exact Class B libXcursor provider decision for GTK 3.24.49 X11 cursor handling.

- [`libthai-libdatrie-iconv-bounded-provider-authority.md`](libthai-libdatrie-iconv-bounded-provider-authority.md) — exact signed-index libthai/libdatrie/libiconv chain, `thbrk.tri` content and bounded Pango 1.54.0 Thai-break authority.

- [`libcloudproviders-bounded-provider-authority.md`](libcloudproviders-bounded-provider-authority.md) — exact Class B libcloudproviders provider decision for GTK 3.24.49 PlacesSidebar cloud-account integration; DBus services and accounts remain separate.

- [`fribidi-bounded-provider-authority.md`](fribidi-bounded-provider-authority.md) — exact Class B FriBidi provider decision for Pango 1.54.0 core Unicode bidirectional text processing.

- [`freetype-bounded-provider-authority.md`](freetype-bounded-provider-authority.md) — exact FreeType member, shared-output recipe semantics, PangoFT2 binding and bounded compression-feature closure.

- [`libxkbcommon-bounded-provider-authority.md`](libxkbcommon-bounded-provider-authority.md) — exact libxkbcommon member, upstream concrete-filename continuity, standard Meson delegation and bounded GTK 3.24.49 Wayland XKB authority.

- [`harfbuzz-bounded-provider-authority.md`](harfbuzz-bounded-provider-authority.md) — exact HarfBuzz member, five-file Class B build/packaging semantics, upstream concrete-version formula and bounded Pango 1.54.0 core OpenType shaping authority.
- [`fontconfig-bounded-provider-authority.md`](fontconfig-bounded-provider-authority.md) — exact Fontconfig member, three-file Class B recipe/config/cache semantics, stable SONAME continuity, and bounded Pango 1.54.0 font discovery and matching authority.
- [`pixman-cairo-prerequisite-provider-authority.md`](pixman-cairo-prerequisite-provider-authority.md) — exact Pixman 0.46.4 generic implementation, stable SONAME continuity, and direct exact-Cairo prerequisite authority from retained acquisition and ELF evidence.

- [`cairo-bounded-provider-authority.md`](cairo-bounded-provider-authority.md): exact atomic Cairo core and Cairo-GObject provider authority for selected Pango/GTK rendering and GObject integration.

- [`libxdamage-provider-evidence-blocker.md`](libxdamage-provider-evidence-blocker.md) — exact read-only acquisition failure disposition proving that only a bionic package is indexed, no glibc package or recipe root exists, and libXdamage authority remains open.
- [`graphite2-harfbuzz-prerequisite-provider-authority.md`](graphite2-harfbuzz-prerequisite-provider-authority.md) — exact Graphite2 1.3.14 member and stable SONAME accepted only for the Graphite shaping path compiled into exact HarfBuzz 10.1.0.
- [`at-spi2-core-provider-evidence-blocker.md`](at-spi2-core-provider-evidence-blocker.md) — coupled three-identity blocker proving that the approved index and pinned recipe source contain no Termux glibc AT-SPI2/ATK provider candidate while bionic packages remain non-authoritative.
