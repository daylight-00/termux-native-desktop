# Provider claim classification under ADR 0005

## Status

```text
classification: COMPLETE / REVIEWED BOUNDED INVENTORY
policy: ADR 0005
roots: 28
objects: 37
claims: 91
new evidence collected: 0
provider authority accepted inside inventory: 21
project-candidate provider authority accepted outside inventory: 1
composition accepted: 0
target rows accepted: 0
activation accepted: 0
```

This document is the current review surface for the provider-authority decision boundary accumulated in records 0118–0165. It replaces the former assumption that every root must complete the same producing-build evidence campaign before any claim can be reviewed.

The classification is generated from the current canonical review tables by:

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    generate-provider-claim-classification.py
```

Canonical outputs:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    provider-claim-classification.tsv
    provider-sup-02-request-disposition.tsv
    provider-claim-classification-metadata.tsv
```

## Claim separation

The classification does not permit one package or root row to stand for every authority state. Each of the 28 roots has three distinct claims:

```text
ARTIFACT_IDENTITY
    exact reference artifact and named-member candidate identity

ADAPTATION_SEMANTICS
    whether the pinned recipe is unchanged for the claim or contains bounded Termux/Android adaptation

PROVIDER_AUTHORITY
    whether the exact member may be selected as the runtime provider for its capability scope
```

The inventory also records separately:

```text
OJ-001 required-object identity
supplier producing-build provenance
application runtime composition
target population
selected-generation activation
```

Artifact identity can be sufficiently evidenced while adaptation and provider authority remain open. Provider authority can later be accepted without implying complete composition, target membership, or activation.

## ADR class result

```text
Class A: 36 claims
    28 exact artifact/member identity claims
     7 no-explicit-delta adaptation claims confirmed by bounded semantic review
     1 authoritative required-object identity claim

Class B: 50 claims
    21 reference-adapted recipe claims
    29 project integration/provider-selection claims

Class C: 2 active bounded producing claims
    exact libjpeg-turbo 3.1.0 v6b compatibility candidate production
    exact libXdamage 1.1.6 isolated candidate production
    each producing record remains distinct from its separately accepted bounded provider claim

Class D: 3 global project-authored claims
    composition
    target population
    activation
```

The two Class C rows record the project-produced runpath-free `libjpeg.so.62.4.0` candidate and exact isolated `libXdamage.so.1.1.0` candidate. Source, build invocation, toolchain, output manifest, ELF identity and symbol versions are recorded. A separate loader-isolated review accepted bounded GdkPixbuf JPEG file and memory decode authority; the Class C row does not imply broader libjpeg family or composition authority.

## Existing evidence retained

The classification retains the following evidence without overpromoting it:

- exact package metadata and artifact SHA-256;
- stream-inspected artifact members, member digests, and observed SONAMEs;
- pinned recipe root, recipe tree, upstream source locator and source digest;
- recipe-file inventory and bounded adaptation tokens;
- selected/reference runtime evidence and capability coverage;
- the accepted OJ-001 correction that the required ABI identity is `libjpeg.so.62`, not `libjpeg.so.8`;
- all historical SUP-02 request, acquisition, receipt, and producer records.

These remain evidence inputs. They do not create final provider authority by themselves. Twenty-one inventory-root provider claims and one exact project-candidate provider claim are accepted only through their separate bounded provider reviews.

## SUP-02 disposition

All 28 issued requests remain historical records, but none is currently required for execution.

```text
STILL_NECESSARY: 0
NARROWED:       14
REPLACED:        7
UNNECESSARY:     7
```

### Narrowed — 14 roots

The T1 and T2 material-delta roots remain Class B. They require semantic recipe review, platform-necessity classification, and object-impact review first.

A custodian export is retained only as an escalation path for a claim-specific field when:

```text
recipe semantics cannot bound generated output;
an observed artifact conflicts with the pinned recipe;
the claim is explicitly reclassified as Class C;
a high-consequence output remains opaque after bounded review.
```

The original three-record export for every root is not the default next action.

### Replaced — 7 roots

T4 configuration/packaging roots and the T5 no-token-with-drift root use:

```text
authoritative artifact/member identity
    + pinned recipe/upstream semantic review
    + project integration and drift-policy evidence
```

This is proportionate to a reference-consumed or reference-adapted claim. It does not require independent reproduction by default.

### Unnecessary — 7 roots

Six T6 no-token roots have completed bounded recipe/upstream semantic comparison and are confirmed Class A for package-specific adaptation. Their historical SUP-02 requests remain unnecessary.

The `libjpeg-turbo` SUP-02 request is also unnecessary at the current boundary because producing-build evidence for a package that does not provide the required `libjpeg.so.62` identity cannot close OJ-001.

## Current authority states

```text
bounded provider authority accepted inside inventory: 21
project-candidate provider authority accepted outside inventory: 1 roots
provider authority still open:                        7 roots
application runtime composition:     NOT REACHED
target population:                   BLOCKED
selected-generation activation:      BLOCKED
```

The twenty-one accepted root rows are `libxfixes`, `libxcomposite`, `libxi`, `libxinerama`, `libxcursor`, `libtasn1`, `libepoxy`, `pango`, the exact project-built `libjpeg.so.62.4.0`, `glib`, `libpng`, `util-linux`, `libthai`, `libdatrie`, `libcloudproviders`, `fribidi`, `freetype`, `libxkbcommon`, `harfbuzz`, `fontconfig`, and the atomic `cairo` core/Cairo-GObject root. Outside this fixed inventory, exact `libpixman-1.so.0.46.4` is additionally accepted as a bounded Cairo prerequisite and exact `libgraphite2.so.3.2.1` is accepted as a bounded HarfBuzz Graphite-shaping prerequisite; it does not add or merge a claim into the 89-row canonical claim inventory. The GLib four-member family and libpng shared member are accepted only for the exact GdkPixbuf 2.42.12 JPEG/PNG file and memory decode scope; the exact official libmount/libblkid pair is accepted only for the bounded GdkPixbuf transitive runtime. Each decision remains limited to an exact identity and named consumer capability. The classification still does not authorize extraction, installation, target population, complete composition, selected-generation mutation, or activation.

## Seven-root semantic-review result

The seven-root no-token semantic review is complete:

```text
confirmed Class A: 7
reclassified Class B: 0
provider authority accepted inside inventory: 21
project-candidate provider authority accepted outside inventory: 1
```

Canonical review surface:

```text
docs/evidence/no-token-recipe-semantic-review.md
experiments/glibc/selected-obsidian-provider-authority/review/no-token-recipe-semantic-review.tsv
```

For all seven roots, the pinned recipe contains only source/version identity and dependency/package metadata. No package-specific patch, hook, build option, install transform, or output rewrite was found. The generic Termux glibc cross-build framework and upstream build defaults remain relied-upon supplier boundaries rather than project-owned producing claims.

`pango` concrete-filename drift remains a separate provider-integration and continuity question. It was not closed by the Class A recipe result.

## Completed bounded provider tranches and smallest next phase

The exact `libXcursor.so.1.0.2` provider is accepted for GTK 3.24.49 X11 cursor theme, image, surface and custom-cursor handling. Its Class B patch only relocates built-in cursor search paths into the Termux prefix. It does not grant cursor-theme data, package-wide surfaces, complete composition, target or activation authority.

The exact `libcloudproviders.so.0.3.6` provider is accepted for selected GTK 3.24.49 PlacesSidebar cloud-account integration. Its Class B delta disables Vala binding generation only; DBus services, accounts and service activation remain separate.

The exact `libfribidi.so.0.4.0` provider remains accepted only for Pango 1.54.0 core Unicode bidirectional processing. Exact `libfreetype.so.6.20.2` remains accepted for the bounded Pango/GTK FT2 font-engine path, with four pre-existing conditional objects included only for its compression-feature closure. Exact `libxkbcommon.so.0.8.0` remains accepted for the bounded GTK 3.24.49 Wayland XKB path. Exact `libharfbuzz.so.0.61010.0` remains accepted for Pango 1.54.0 core OpenType shaping. Exact `libfontconfig.so.1.14.0` is now accepted for Pango 1.54.0 font discovery, matching and pattern-property consumption, with SONAME `libfontconfig.so.1`, explicit `1.12.1` reference-to-`1.14.0` candidate continuity, and bounded Meson, generated-default-policy, package-revision, directory-sentinel cache-lock and utilities-subpackage semantics. Package-generated configuration, system or package font directories, global caches, font population, CLI and development surfaces remain excluded; future activation requires receipt-owned configuration and cache. The next smallest phase is the coupled Cairo/Cairo-GObject root. No target paths are generated.

## Stop line

Do not:

- treat claim classification alone as provider acceptance outside the twenty explicit bounded provider review rows;
- fulfill a SUP-02 request solely because it was historically issued;
- combine artifact identity, adaptation, provider authority, composition, target population, and activation into one decision;
- use package metadata or build provenance as a substitute for runtime provider selection;
- use successful launch as proof of complete composition;
- populate or activate a target before the corresponding Class D claim is reviewed.
