# Current project brief

> Semantic state version: `2026-07-26.05`

## Purpose and operational boundary

`termux-native-desktop` develops a native Termux/glibc workstation while keeping artifact identity, provider authority, composition, target policy, population and activation separate. User Termux remains authoritative for execution and remote mutation.

## Current boundary

```text
claims: 95
bounded provider roots: 31
bounded provider roots accepted overall: 31
accepted provider decision rows: 42
current-scope concrete members: 41
deferred members: 1
selected identity gaps: 0
composition: accepted bounded complete
target manifest: qualified non-mutating candidate (82 rows)
target manifest acceptance: accepted bounded non-mutating policy (82 rows)
target manifest: accepted bounded non-mutating policy (82 rows)
regular / SONAME alias rows: 41 / 41
path collisions / unresolved aliases: 0 / 0
population state: UNPOPULATED_SCHEMA_ONLY
supply-byte binding: blocked
intervention lift: blocked
materializer design: blocked
target population: blocked
activation: blocked
```

`SELECTED-TARGET-MANIFEST-ACCEPT-001` accepts the exact v105 five-file target-policy candidate by digest. The frozen candidate still contains candidate-time open markers; the separate acceptance record closes that review issue without rewriting evidence. No supply artifact or archive member is bound and no target path exists on disk.

## Current phase

The active task is `review-target-population-intervention-lift-and-supply-byte-binding-boundary`. It is read-only. It must determine whether the target-population intervention may be lifted and whether every concrete object has an exact retained supply-byte binding before any materializer design. It may not acquire, extract, copy, install, populate, deploy or activate anything.
