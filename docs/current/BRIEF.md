# Current project brief

> Semantic state version: `2026-07-28.02`

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
local supply map contract:     QUALIFIED_NON_MUTATING_CANDIDATE_HISTORICAL
local supply contract acceptance: ACCEPTED_BOUNDED_NON_MUTATING_CONTRACT_AUTHORITY
local supply contract rows:       41
local supply validation rules:    24
local supply populated paths:      0
local supply map:              NOT_PRODUCED_NOT_AUTHORIZED
local supply evidence transaction design: QUALIFIED_NON_EXECUTING_READ_ONLY_CANDIDATE_HISTORICAL
local supply evidence design acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_READ_ONLY_DESIGN_AUTHORITY
evidence design inputs/states:  12 / 16
evidence design operations/failures: 32 / 18
current authorized coordinates/provider reads: 0 / 0
authorization/coordinate contract: QUALIFIED_NON_MUTATING_CANDIDATE_HISTORICAL
authorization/coordinate contract acceptance: ACCEPTED_BOUNDED_NON_MUTATING_CONTRACT_AUTHORITY
authorization claims / coordinate rows / validation rules: 18 / 41 / 30
current live tokens / coordinate rows: 0 / 0
authorization issuance/coordinate production design: QUALIFIED_NON_EXECUTING_DESIGN_CANDIDATE_HISTORICAL
authorization issuance/coordinate production design acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_DESIGN_AUTHORITY
issuance design inputs/states/operations/failures: 14 / 18 / 36 / 20
authorization issuance/coordinate production implementation: QUALIFIED_NON_EXECUTING_SYNTHETIC_CANDIDATE_HISTORICAL
implementation coverage inputs/states/operations/failures: 14 / 18 / 36 / 20
implementation total coverage / synthetic cases: 88 / 1+20
implementation synthetic coordinate rows/provider reads/writes: 41 / 0 / 0
implementation acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_IMPLEMENTATION_AUTHORITY
live-input adapter / execution-authorization contract: QUALIFIED_NON_EXECUTING_CANDIDATE_HISTORICAL
live-input adapter / execution-authorization contract acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_CONTRACT_AUTHORITY
adapter inputs / envelope fields: 10 / 20
execution authorization claims: 27
adapter validation/states/operations/failures: 37 / 18 / 32 / 20
current live inputs / adapter envelopes / execution authorizations: 0 / 0 / 0
synthetic implementation role: IMMUTABLE_ORACLE_NOT_LIVE_EXECUTOR
live-to-synthetic path rewrite: FORBIDDEN
execution authorization:       NO
population state:              UNPOPULATED_SCHEMA_ONLY
materialization/publication:   blocked / blocked
activation:                    blocked
```

`SELECTED-PROVIDER-MATERIALIZER-DESIGN-ACCEPT-001` freezes the exact nine v112 candidate artifacts. Accepted invariants include content-addressed objects, hardlink-only reuse with no copy fallback, regular-before-alias ordering, four atomic-family barriers, a 1 MiB receipt cap, immutable generation publication, `previous`-before-`current` selector ordering, rollback, resume and orphan-reporting contracts.

Design acceptance is non-executing. It creates no local supply map, reads no provider bytes and does not authorize the generation root, object writes, population, materialization, publication, deployment or activation.

## Current phase

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001` accepts the exact four-artifact contract boundary: 41 rows, 24 validation rules, a canonical empty receipt schema, the 23/4/14 index-contract split and zero populated local paths. Acceptance grants no path discovery, byte read or execution authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-REVIEW-001` qualifies a deterministic non-executing design: 12 input contracts, 16 states, 32 ordered operations, 18 failure contracts, 24 inherited validation rules and 41 future receipt rows. It contains zero authorized coordinates and zero provider reads.

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001` accepts the exact six-artifact design boundary while preserving zero authorized coordinates and zero provider reads. Acceptance grants no evidence execution or runtime authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-REVIEW-001` qualifies an 18-claim owner-authorization token schema, canonical 41-row/10-field coordinate-receipt schema and 30 fail-closed validation rules. It contains zero live tokens, zero coordinate rows and zero provider reads.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-ACCEPT-001` accepts the exact four-artifact 18/41/10/30 contract boundary while preserving zero live tokens, zero coordinate rows and zero provider reads. Acceptance grants no issuance, discovery, read or execution authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-DESIGN-REVIEW-001` qualifies a deterministic 14-input/18-state/36-operation/20-failure non-executing issuance/production transaction design. It contains zero live tokens, zero coordinate rows, zero provider reads and zero live authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-DESIGN-ACCEPT-001` accepts the exact six-artifact design boundary while preserving zero issued tokens, coordinate rows, provider reads and live authority. Acceptance grants no issuance, production, discovery, read or execution authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-REVIEW-001` qualifies a deterministic synthetic-only implementation candidate. It maps all 14 inputs, 18 states, 36 operations and 20 failures into 88 coverage rows, validates one 41-row success fixture and rejects twenty exact failure cases. The implementation accepts repository-owned synthetic fixtures only, opens no provider path, reads no provider byte, performs no write and creates no live authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001` accepts the exact six-artifact synthetic-only implementation boundary while preserving zero issued tokens, coordinates, provider reads, writes and live authority. Acceptance grants no live-input, issuance, production, read or execution authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-REVIEW-001` historically qualifies the exact eight-artifact non-executing contract candidate: ten explicit input channels, a twenty-field inactive adapter envelope, a 27-claim execution authorization, 37 validation rules, 18 states, 32 operations and 20 failure contracts.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-ACCEPT-001` accepts that exact boundary while preserving zero live inputs, zero adapter envelopes, zero execution authorizations, zero provider reads, zero writes and zero live authority. The accepted synthetic implementation remains an immutable semantic/regression oracle and is not a live executor. Live-to-synthetic rewriting and live synthetic invocation remain forbidden.

The active task is `generate-and-review-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-implementation-candidate`. It may create deterministic repository-owned synthetic implementation evidence only. It may not supply live inputs, issue authorization, search, open, read, localize or execute provider bytes.
