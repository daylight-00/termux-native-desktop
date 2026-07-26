# Current project brief

> Semantic state version: `2026-07-26.12`

## Purpose and operational boundary

`termux-native-desktop` develops a native Termux/glibc workstation while separating provider authority, composition, target policy, supply evidence, materializer design, design acceptance, local-supply mapping, execution authorization, population and activation. User Termux remains authoritative for execution and remote mutation.

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
open member sizes:                0
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
materializer design acceptance: ACCEPTED_BOUNDED_READ_ONLY_DESIGN_AUTHORITY
intervention: prior retained; conditionally lifted for read-only design review only
local supply map contract:     QUALIFIED_NON_MUTATING_CANDIDATE_ACCEPTANCE_OPEN
local supply contract rows:       41
local supply validation rules:    24
local supply populated paths:      0
local supply map:              NOT_PRODUCED_NOT_AUTHORIZED
execution authorization:       NO
population state:              UNPOPULATED_SCHEMA_ONLY
materialization/publication:   blocked / blocked
activation:                    blocked
```

`SELECTED-PROVIDER-MATERIALIZER-DESIGN-ACCEPT-001` freezes the exact nine v112 candidate artifacts. Accepted invariants include content-addressed objects, hardlink-only reuse with no copy fallback, regular-before-alias ordering, four atomic-family barriers, a 1 MiB receipt cap, immutable generation publication, `previous`-before-`current` selector ordering, rollback, resume and orphan-reporting contracts.

Design acceptance is non-executing. It creates no local supply map, reads no provider bytes and does not authorize the generation root, object writes, population, materialization, publication, deployment or activation.

## Current phase

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-REVIEW-001` qualifies a deterministic 41-row contract, 24 validation rules and a canonical empty receipt schema. The candidate contains zero local paths and grants no path-discovery or byte-read authority.

The active task is `review-and-accept-non-mutating-selected-provider-local-supply-map-contract-boundary`. It may freeze and accept the exact contract artifacts only. It may not search, acquire, read, extract or localize provider bytes.
