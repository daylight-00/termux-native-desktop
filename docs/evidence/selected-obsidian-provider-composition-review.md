# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  27
accepted exact members:           35
included members:                 34
deferred members:                  1
selected GTK identity gaps:        8
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, or activation.

## Latest bounded tranche

Exact `libcairo.so.2.11802.2` and `libcairo-gobject.so.2.11802.2` are included atomically for selected Pango 1.54.0 Cairo rendering, GTK 3.24.49 core Cairo drawing/surface use, and Cairo GObject integration. Their stable runtime aliases are `libcairo.so.2` and `libcairo-gobject.so.2`; the selected `1.18.4` concrete labels remain reference evidence rather than target paths.

The Class B boundary covers the exact package and member digests, stable aliases, non-selected backend/test disablement, utility-only Termux temporary-path patches, exact accepted runtime dependency closure, and the already accepted exact Pixman prerequisite. Cairo-script/FDR utilities, non-selected backends, tools, development surfaces, complete composition, target population, and activation remain excluded.

## Latest gap disposition

Selected `libXdamage.so.1.1.0` remains open. The approved glibc query `libxdamage-glibc` returned no package, the only observed `libxdamage` stanza belongs to the ordinary Termux/X11 bionic repository, and the pinned glibc recipe repository has no libXdamage root. The recorded HTTP 404 came from combining a bionic repository filename with the glibc base; changing only the URL would still produce the wrong ABI world. This is `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`, not a provider rejection and not authority to reuse bionic bytes.

## Next tranche

The next tranche is `GRAPHITE2_PROVIDER_EVIDENCE_ACQUISITION`. Selected `libgraphite2.so.3.2.1` has a pinned `gpkg/libgraphite` 1.3.14 recipe root but no retained exact glibc artifact/member. The next action is read-only approved-index acquisition and exact member, SONAME, alias, dependency, recipe-semantics and Pango/HarfBuzz consumer review.
