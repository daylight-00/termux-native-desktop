# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  28
accepted exact members:           36
included members:                 35
deferred members:                  1
selected GTK identity gaps:        7
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, or activation.

## Latest bounded tranche

Exact `libgraphite2.so.3.2.1` is included only as the Graphite shaping-engine prerequisite compiled into exact HarfBuzz 10.1.0 for Graphite-enabled fonts within the selected Pango 1.54.0 and GTK 3.24.49 text scope. Its stable runtime alias is `libgraphite2.so.3`; the unversioned development alias is excluded.

The Class B boundary covers the approved `libgraphite-glibc` 1.3.14 archive, exact member and alias, one-file recipe tree, disabled install RPATH and compare renderer, direct Graphite VM, libc/loader-only runtime closure, and direct HarfBuzz Graphite integration. General HarfBuzz widening, package-wide surfaces, all-font functional validation, complete composition, target population, and activation remain excluded.

## Latest gap disposition

Selected `libXdamage.so.1.1.0` remains open. The approved glibc query `libxdamage-glibc` returned no package, the only observed `libxdamage` stanza belongs to the ordinary Termux/X11 bionic repository, and the pinned glibc recipe repository has no libXdamage root. The recorded HTTP 404 came from combining a bionic repository filename with the glibc base; changing only the URL would still produce the wrong ABI world. This is `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`, not a provider rejection and not authority to reuse bionic bytes.

## Next tranche

The next tranche is `AT_SPI2_CORE_PROVIDER_EVIDENCE_ACQUISITION`. Exact Graphite2 1.3.14 is now included only as the bounded prerequisite for the Graphite shaping path compiled into exact HarfBuzz 10.1.0. The next action is read-only approved-index and pinned-repository inspection for the coupled selected ATK bridge, ATK core and AT-SPI identities, followed by exact member, SONAME, alias, dependency, recipe-semantics and GTK accessibility consumer review if candidates exist.
