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

Selected `libXdamage.so.1.1.0` remains `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`; its only observed package is in the ordinary Termux/X11 bionic world and the pinned glibc recipe source has no producing root.

The coupled selected `libatk-bridge-2.0.so.0.0.0`, `libatk-1.0.so.0.25611.1`, and `libatspi.so.0.0.1` family is also `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. The approved `at-spi2-core-glibc` query returned neither policy metadata nor a package stanza. Only ordinary bionic `at-spi2-core`, `atk`, and `at-spi2-atk` entries were observed, and pinned recipe path/search checks found no AT-SPI2/ATK root. This is not authority to copy installed bionic bytes or activate an accessibility service.

The selected `libgdk-3.so.0.2417.32` and `libgtk-3.so.0.2417.32` core pair is likewise `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. All bounded glibc package-name queries returned no policy metadata or package stanza, only ordinary Termux/X11 bionic `gtk3 3.24.52` was observed, and pinned recipe path/search checks found no GTK 3 producing root. This is not authority to copy installed bionic bytes or infer backend, settings, theme, accessibility, input, printing, or service behavior.

## Next tranche

The next tranche is `LIBSELINUX_PROVIDER_EVIDENCE_ACQUISITION`. The next action is read-only approved-index and pinned-repository inspection for exact selected `libselinux.so.1`, followed by exact member, SONAME, alias, dependency, recipe-semantics, Android/Termux SELinux-boundary and consumer-binding review if a candidate exists.
