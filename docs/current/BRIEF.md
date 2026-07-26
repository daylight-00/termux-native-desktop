# Current project brief

> Semantic state version: `2026-07-26.10`

## Purpose and operational boundary

`termux-native-desktop` develops a native Termux/glibc workstation while separating provider authority, composition, target policy, supply evidence, materializer design, design acceptance, execution authorization, population and activation. User Termux remains authoritative for execution and remote mutation.

## Current boundary

```text
claims:                          95
bounded provider roots:          31
accepted provider decision rows: 42
current-scope concrete members:  41
accepted target-policy rows:     82
existing digest-bound results:     14
indexed v101 replacements:         23
append-only legacy index upgrades:  4
supply coordinate/index gaps:     0
exact member sizes:              41
open member sizes:               0
exact member bytes:      29,047,112
receipt reservation:      1,048,576
final resource preflight: 59,142,800
materializer object-plan rows:    41
materializer state rows:          20
ordered operation rows:           24
runtime preflight checks:         20
verification checks:              18
publication/recovery contracts:   11
materializer design candidate: QUALIFIED_NON_EXECUTING_READ_ONLY_DESIGN_CANDIDATE
intervention: prior retained; conditionally lifted for read-only design review only
design acceptance:             OPEN
execution authorization:       NO
population state:              UNPOPULATED_SCHEMA_ONLY
materialization/publication:   blocked / blocked
activation:                    blocked
```

The candidate design uses a content-addressed object store, same-device hardlinks with no copy fallback, regular-file completion before relative SONAME aliases, four atomic-family barriers, a 1 MiB receipt cap, immutable generation rename, and `previous`-before-`current` selector publication.

A future execution must first provide a separate accepted authorization and a 41-row local read-only supply map. The design candidate itself creates no runtime path and reads no provider bytes.

## Current phase

The active task is `review-and-accept-read-only-selected-provider-materializer-runtime-preflight-design-boundary`. Only the exact design candidate may be accepted or rejected. Execution, localization, byte acquisition, root creation, population, publication, deployment and activation remain unauthorized.
