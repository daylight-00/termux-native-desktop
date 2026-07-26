# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_COMPLETE_PROVIDER_SET_TARGET_MANIFEST_NOT_ACCEPTED
accepted bounded provider roots:  31
accepted exact members:           42
included members:                 41
deferred members:                  1
selected GTK identity gaps:        0
target manifest allowed:          NO
activation allowed:               NO
```

The generated accepted-member table is `selected-provider-composition-members.tsv`; `selected-provider-composition-gaps.tsv` contains only its header after exact consumer reselection eliminated the last oracle-only edge. This review is non-materializing and is not composition acceptance.

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

The libSELinux direct-consumer review selected `DEPENDENCY_ELIMINATION_OR_RESELECTION`. The next tranche is `COMPLETE_SELECTED_PROVIDER_COMPOSITION_BOUNDARY_ACCEPTANCE_REVIEW`; it does not authorize target-manifest generation or population.


## Last-gap disposition: libSELinux oracle edge eliminated

`LIBSELINUX-CONSUMER-NECESSITY-001` proves that Debian oracle `libmount1 2.41-5` carried optional SELinux-enabled hooks, while selected exact `libmount-glibc 2.40.2-1` has no `libselinux.so.1` `DT_NEEDED` entry or imported SELinux symbols. The v101 complete GTK candidate used the selected replacement successfully.

The historical observation remains in provenance ledgers but is not an active provider gap. No libSELinux provider authority or build authorization is created. The provider set is reviewed complete with zero selected identity gaps; separate Class D composition acceptance is still required before target-manifest review.

```text
next review tranche: COMPLETE_SELECTED_PROVIDER_COMPOSITION_BOUNDARY_ACCEPTANCE_REVIEW
```
