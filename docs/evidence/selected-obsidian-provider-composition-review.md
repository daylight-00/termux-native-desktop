# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  26
accepted exact members:           33
included members:                 32
deferred members:                  1
selected GTK identity gaps:       10
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, or activation.

## Latest bounded tranche

Exact `libpixman-1.so.0.46.4` is included only as the pixel image compositing prerequisite directly required by exact `libcairo.so.2.11802.2`. Its runtime SONAME alias is `libpixman-1.so.0`; the selected `libpixman-1.so.0.44.0` label is retained as older reference evidence rather than target-path authority.

The accepted Class B boundary covers the exact approved package and member digests, stable alias, direct Cairo `DT_NEEDED` edge, standard Meson delegation, and generic implementation selected by disabling architecture-specific SIMD and the GTK helper surface. Upstream byte or performance equivalence, acceleration guarantees, package-wide surfaces, development aliases, Cairo provider authority, complete composition, target population, and activation remain excluded.

## Next tranche

The next reviewed-root tranche is `CAIRO_BOUNDED_PROVIDER_AUTHORITY`. It must review exact `libcairo.so.2.11802.2` and `libcairo-gobject.so.2.11802.2` as one atomic recipe-root tranche, reconcile the selected `1.18.4` concrete labels with retained `1.18.2` candidates, preserve SONAMEs `libcairo.so.2` and `libcairo-gobject.so.2`, and bound configure, patch, Termux-prefix, dependency, Pango/GTK rendering, GObject consumer, conflict, update, and rollback semantics. The exact Pixman prerequisite edge is now accepted and must remain pinned as part of the Cairo dependency boundary.
