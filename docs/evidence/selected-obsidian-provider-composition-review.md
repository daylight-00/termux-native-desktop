# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  25
accepted exact members:           32
included members:                 31
deferred members:                  1
selected GTK identity gaps:       11
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, or activation.

## Latest bounded tranche

Exact `libfontconfig.so.1.14.0` is included only for Pango 1.54.0 font discovery, matching, and pattern-property consumption in the selected GTK 3.24.49 text path. Its runtime SONAME alias is `libfontconfig.so.1`; the selected `libfontconfig.so.1.12.1` label is retained as older reference evidence rather than target-path authority.

The accepted Class B boundary covers the exact three-file recipe, standard Meson delegation, revision-1 source and font-path policy, generated default font-directory/rendering settings, directory-sentinel cache-lock patch, and utilities subpackage split. Package-generated `fonts.conf`, package or system font directories, global caches, font population, CLI tools, development surfaces, complete text composition, target population, and activation remain excluded. Any future runtime must use an explicit receipt-owned configuration, immutable generation font directory, and fresh receipt-local cache.

## Next tranche

The next reviewed-root tranche is `CAIRO_BOUNDED_PROVIDER_AUTHORITY`. It must review exact `libcairo.so.2.11802.2` and `libcairo-gobject.so.2.11802.2` as one atomic recipe-root tranche, reconcile the selected `1.18.4` concrete labels with retained `1.18.2` candidates, preserve SONAMEs `libcairo.so.2` and `libcairo-gobject.so.2`, and bound configure, patch, Termux-prefix, dependency, Pango/GTK rendering, GObject consumer, conflict, update, and rollback semantics.
