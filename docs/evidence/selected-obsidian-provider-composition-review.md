# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  24
accepted exact members:           31
included members:                 30
deferred members:                  1
selected GTK identity gaps:       12
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, or activation.

## Latest bounded tranche

Exact `libharfbuzz.so.0.61010.0` is included only for Pango 1.54.0 core OpenType shaping in the selected GTK 3.24.49 text-layout scope. Its runtime SONAME alias is `libharfbuzz.so.0`; the selected `libharfbuzz.so.0.61020.0` label is retained as later-version reference evidence rather than target-path authority.

The accepted Class B boundary covers the exact five-file recipe's exception-flag cleanup, standard Meson delegation, C++17 compiler-dialect patch, disabled documentation, enabled Graphite2/introspection options, and sibling subpackage splits. No package-wide, dependency, sibling-library, complete text-composition, target-population, or activation authority follows.

## Next tranche

The next reviewed-root tranche is `FONTCONFIG_BOUNDED_PROVIDER_AUTHORITY`. It must reconcile selected identity `libfontconfig.so.1.12.1` with retained exact candidate `libfontconfig.so.1.14.0`, preserve SONAME `libfontconfig.so.1`, and bound the custom step, configure arguments, package revision, patch, subpackage, Termux-prefix and selected Pango/GTK font-discovery consumer and data-policy boundary.
