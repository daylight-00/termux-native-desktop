# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  23
accepted exact members:           30
included members:                 29
deferred members:                  1
selected GTK identity gaps:       13
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, or activation.

## Latest bounded tranche

Exact `libxkbcommon.so.0.8.0` is included only for the selected GTK 3.24.49 Wayland XKB context, keymap, keyboard-state, modifier, and keysym translation path. Its runtime SONAME alias is `libxkbcommon.so.0`; the selected `libxkbcommon.so.0.0.0` label is retained as reference evidence rather than target-path authority.

No package-wide authority follows. XKB configuration data and path policy, `libxkbcommon-x11`, `libxkbregistry`, sibling capabilities, tools, development surfaces, complete input composition, target population, and activation remain outside this decision.

## Next tranche

The next reviewed-root tranche is `HARFBUZZ_BOUNDED_PROVIDER_AUTHORITY`. It must reconcile selected identity `libharfbuzz.so.0.61020.0` with retained exact candidate `libharfbuzz.so.0.61010.0`, preserve SONAME `libharfbuzz.so.0`, and bound the custom step, configure arguments, patch, subpackage, and selected Pango/GTK shaping consumer path.
