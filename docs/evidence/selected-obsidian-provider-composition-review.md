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

Selected `libselinux.so.1` is also `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. The approved index contained no bounded `libselinux*` or `selinux-glibc` coordinate; only installed ordinary Termux/bionic `libandroid-selinux 14.0.0.11-1` was observed, Android platform libraries remain boundary evidence only, and pinned recipe checks found no libSELinux-producing root. This is not authority to create a cross-world alias, load policy, relabel filesystems, change enforcing state, or infer glibc compatibility.

All seven unresolved selected identities are now reviewed blockers. The Class D composition remains incomplete and no target manifest is allowed.

## Next tranche

The next tranche is `MISSING_GLIBC_PROVIDER_PRODUCTION_BOUNDARY_DEFINITION`. The next action is a non-mutating comparison of supplier, package-contribution and separately authorized project-production lanes for the four blocker families. It does not authorize source checkout, build, packaging, installation, target population, policy mutation, deployment or activation.
