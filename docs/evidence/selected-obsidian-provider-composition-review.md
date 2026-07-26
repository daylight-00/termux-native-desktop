# Selected Obsidian provider composition review

## Decision

```text
composition decision:             ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION
composition acceptance review:    SELECTED-COMPOSITION-ACCEPT-001
accepted bounded provider roots:  31
accepted exact members:           42
included members:                 41
deferred members:                  1
selected GTK identity gaps:        0
target manifest generated:        NO
target manifest allowed:          NO
activation allowed:               NO
```

The generated member table is `selected-provider-composition-members.tsv`; `selected-provider-composition-gaps.tsv` contains only its header. The exact v103 review tables are frozen by SHA-256 in `selected-provider-composition-boundary-acceptance.tsv` and accepted as one bounded Class D application-runtime composition decision.

Acceptance covers the exact member identities, current-scope inclusion and libtasn1 deferment, SONAME-alias decisions, collision results, capability exclusions, atomic-family relations, update triggers, and rollback boundary. It does not decide target pathnames, filesystem copy order, dynamic-loader search order, package installation order, population, deployment, or activation.

## Atomic GTK 3 core

The exact GTK 3.24.49 pair is included atomically:

```text
libgdk-3.so.0.2417.32 -> libgdk-3.so.0
libgtk-3.so.0.2417.32 -> libgtk-3.so.0
```

Both members come from one official source, one Class B production recipe, one independently reproduced Class C package, and one update/rollback lifecycle. GTK directly `DT_NEEDED`-binds GDK. The canonical-loader probe returned `3.24.49 GdkDisplay` with accepted private dependencies and exact private `libjpeg.so.62`, and no `$HOME/gl` or bionic mapping.

Only these two versioned runtime members and SONAME aliases are included. Unversioned aliases, headers, pkg-config, GAIL, helper tools, `broadwayd`, input modules, print backends, schemas, GIR/typelib target membership, data and documentation remain excluded. X11, Wayland and Broadway configuration does not authorize display or daemon operation.

## Last-gap disposition

`LIBSELINUX-CONSUMER-NECESSITY-001` proves that Debian oracle `libmount1 2.41-5` carried optional SELinux-enabled hooks, while selected exact `libmount-glibc 2.40.2-1` has no `libselinux.so.1` `DT_NEEDED` entry or imported SELinux symbols. The historical observation remains in provenance ledgers but is not an active provider gap. No libSELinux provider authority or build authorization is created.

## Deferred provider boundary

`libtasn1.so.6.6.4 -> libtasn1.so.6` is an accepted bounded provider but remains excluded from current selected GTK target membership until a GnuTLS security or printing profile is selected. Composition acceptance does not silently include it.

## Next review tranche

```text
NON_MUTATING_SELECTED_TARGET_MANIFEST_GENERATION_AND_REVIEW
```

The next transaction may generate and review proposed target rows under the existing target-layout schema. It may not copy, install, populate, deploy, or activate anything.

Current next review tranche:

```text
NON_MUTATING_SELECTED_PROVIDER_LOCAL_SUPPLY_MAP_CONTRACT_ACCEPTANCE_REVIEW
```
