# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  31
accepted exact members:           42
included members:                 41
deferred members:                  1
selected GTK identity gaps:        1
target manifest allowed:          NO
activation allowed:               NO
```

The generated accepted-member table is `selected-provider-composition-members.tsv`; the sole gap is in `selected-provider-composition-gaps.tsv`. This review is non-materializing.

## Latest bounded tranche: atomic GTK 3 core

The exact GTK 3.24.49 pair is included atomically:

```text
libgdk-3.so.0.2417.32 -> libgdk-3.so.0
libgtk-3.so.0.2417.32 -> libgtk-3.so.0
```

Both members come from one official source, one Class B production recipe, one independently reproduced Class C package, and one update/rollback lifecycle. GTK directly `DT_NEEDED`-binds GDK. The canonical-loader probe returned `3.24.49 GdkDisplay` with accepted private dependencies and exact private `libjpeg.so.62`, and no `$HOME/gl` or bionic mapping.

Only these two versioned runtime members and SONAME aliases are included. Unversioned aliases, headers, pkg-config, GAIL, helper tools, `broadwayd`, input modules, print backends, schemas, GIR/typelib target membership, data and documentation remain excluded. X11, Wayland and Broadway configuration does not authorize display or daemon operation. No module, cache, schema, printing, D-Bus, accessibility, portal, target, deployment or activation authority is accepted.

## Remaining gap

`libselinux.so.1` is the only unresolved selected identity. Android platform and ordinary Termux/bionic SELinux implementations remain wrong-ABI-world boundary evidence. No glibc candidate or build authorization exists.

The next tranche is `LIBSELINUX_DIRECT_CONSUMER_NECESSITY_REVIEW`: identify exact direct consumers, imported symbols, configuration cause, elimination/reselection feasibility, and security/policy semantics. This does not authorize candidate production.
