# Current project brief

> Semantic state version: `2026-07-28.18`

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

owner activation decision: QUALIFIED_EXPLICIT_OWNER_ACTIVATION_DECISION_CANDIDATE_HISTORICAL
owner activation decision acceptance: ACCEPTED_EXPLICIT_ONE_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AND_REVIEW_TRANSACTION_ONLY
owner activation statement SHA-256: aa143dbbd2b188f7c1000cda2e1a6c89bf4e526569c124d0534e5ecdded175d3
owner activation acceptance statement SHA-256: b0e9fb7171f3dec721b505ad47acc09fa74e986ed4a06ff9ba09e682461d1af7
owner activation authorized scope: ONE_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AND_REVIEW_TRANSACTION_ONLY
owner activation transactions accepted / consumed / remaining: 1 / 0 / 1
exact input-set collection candidate: QUALIFIED_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_CANDIDATE_HISTORICAL
exact input-set collection acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AUTHORITY
exact input-set collection coverage / cases: 20 inputs / 1 success + 20 fail-closed
exact input-set isolated document opens / reads: 5 / 5
exact input-set isolated provider lstats / replay lstats: 41 / 1
exact input-set isolated repository / remote / executor captures: 2 / 1 / 1
exact input-set isolated envelope writes: 2
exact input-set selected-provider opens / reads / bytes: 0 / 0 / 0
exact input-set project replay opens / reads / writes / live authority: 0 / 0 / 0 / 0
live-authority input set: NOT_SUPPLIED_NOT_AUTHORIZED
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
local supply evidence transaction implementation: QUALIFIED_NON_EXECUTING_SYNTHETIC_CANDIDATE_HISTORICAL
local supply evidence transaction implementation acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_READ_ONLY_IMPLEMENTATION_AUTHORITY
local supply evidence transaction implementation coverage: 12 + 16 + 32 + 18 = 78
local supply evidence transaction synthetic cases: 1 success + 18 fail-closed
local supply evidence transaction synthetic rows: 41
local supply evidence transaction provider opens / reads / writes / live authority: 0 / 0 / 0 / 0
live evidence orchestration production implementation: QUALIFIED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_CANDIDATE_HISTORICAL
production orchestration coverage: 18 + 24 + 48 + 28 = 118
inherited semantic implementation coverage: 88 + 164 + 78 = 330
production orchestration isolated cases: 1 success + 28 fail-closed
production orchestration isolated rows / opens / reads: 41 / 41 / 41
production orchestration selected-provider opens / reads / writes / live authority: 0 / 0 / 0 / 0
production orchestration acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_IMPLEMENTATION_AUTHORITY
live authority transaction design: QUALIFIED_NON_EXECUTING_CANDIDATE_HISTORICAL
live authority transaction design coverage: 20 + 26 + 52 + 30 = 128
live authority inherited semantic coverage: 88 + 164 + 78 + 118 = 448
live authority transaction design acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_DESIGN_AUTHORITY
future live-document roles / replay-tuple fields: 5 / 10
current live documents / execution authorizations / replay writes: 0 / 0 / 0
current selected-provider opens / reads / provider bytes / local maps / live authority: 0 / 0 / 0 / 0 / 0
live authority transaction implementation: QUALIFIED_NON_EXECUTING_SYNTHETIC_CANDIDATE_HISTORICAL
live authority transaction implementation acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_IMPLEMENTATION_AUTHORITY
live authority transaction production implementation: QUALIFIED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_CANDIDATE_HISTORICAL
live authority implementation coverage: 20 + 26 + 52 + 30 = 128
live authority implementation inherited coverage: 448
live authority implementation cases: 1 success + 30 fail-closed
live authority implementation synthetic document roles / coordinate rows / replay fields: 5 / 41 / 10
production transaction isolated cases: 1 success + 30 fail-closed
production transaction isolated documents / opens / reads: 5 / 5 / 5
production transaction isolated replay appends / result writes: 2 / 2
production transaction selected-provider opens / reads / provider bytes / project replay writes / live authority: 0 / 0 / 0 / 0 / 0
live authority transaction production implementation acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_IMPLEMENTATION_AUTHORITY
production transaction acceptance gate: ACCEPTED_CLOSED_EXACT_BOUNDARY
owner activation / exact live-authority input set: ACCEPTED_ONE_NON_EXECUTING_COLLECTION_REVIEW_ONLY / NOT_SUPPLIED_NOT_AUTHORIZED
live authority implementation current live documents / replay writes / selected-provider opens / reads / provider bytes / local maps / live authority: 0 / 0 / 0 / 0 / 0 / 0 / 0
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
live-input adapter / execution-authorization implementation: QUALIFIED_NON_EXECUTING_SYNTHETIC_CANDIDATE_HISTORICAL
adapter implementation acceptance: ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_IMPLEMENTATION_AUTHORITY
adapter implementation coverage: 10 + 20 + 27 + 37 + 18 + 32 + 20 = 164
adapter implementation synthetic cases: 1 success + 20 fail-closed
adapter implementation provider reads / writes / live authority: 0 / 0 / 0
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

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-IMPLEMENTATION-REVIEW-001` qualifies a deterministic repository-owned synthetic-only implementation candidate. It maps ten inputs, twenty envelope fields, 27 authorization claims, 37 validations, 18 states, 32 operations and 20 failures into 164 coverage rows. One success and twenty fail-closed cases preserve zero live inputs, provider reads, writes and live authority. Replay consumption is validated in memory only; the accepted synthetic CLI is not invoked and evidence delegation is not executed.

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-IMPLEMENTATION-ACCEPT-001` accepts the exact six-artifact, 164-row synthetic-only implementation boundary with zero live inputs, provider reads, writes, replay persistence and live authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-REVIEW-001` qualifies a deterministic repository-owned synthetic-only implementation candidate. It maps twelve inputs, sixteen states, thirty-two operations and eighteen failures into 78 coverage rows. One success and eighteen fail-closed cases preserve zero provider opens, reads, writes and live authority. The no-follow, hash, stability, ELF and SONAME operations are modeled only and are not executed.

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-ACCEPT-001` accepts the exact six-artifact, 78-row synthetic-only read-only evidence implementation boundary with zero provider opens, reads, writes, replay persistence and live authority.

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-EVIDENCE-ORCHESTRATION-PRODUCTION-IMPLEMENTATION-ACCEPT-001` accepts the exact six-artifact, 118-row production-capable isolated-fixture orchestration implementation boundary. Forty-one isolated fixture opens/reads remain accepted test evidence; selected-provider opens/reads, filesystem writes, replay persistence and live authority remain zero.

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-DESIGN-REVIEW-001` qualifies the exact non-executing 20-input, 26-state, 52-operation and 30-failure transaction design. It orders five future authority documents, append-only replay preflight and a first selected-provider-open gate while all current live authority counts remain zero.

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-DESIGN-ACCEPT-001` accepts the exact six-artifact 20/26/52/30 design boundary and 448 inherited semantic rows while preserving zero live documents, execution authorizations, replay writes, selected-provider opens/reads, provider bytes, local maps and live authority.

The active task is `generate-and-review-non-executing-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-candidate`. The collector must remain explicit-path-only and fail closed before provider open/read or project replay mutation; no live input is supplied during repository review.


## Explicit owner activation decision candidate

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-OWNER-ACTIVATION-REVIEW-001` records the exact owner statement `바로 진행하자` with SHA-256 `aa143dbbd2b188f7c1000cda2e1a6c89bf4e526569c124d0534e5ecdded175d3` and qualifies it only for one non-executing exact input-set review transaction. It is not a cryptographic signature or execution authorization. All required live documents, replay baseline and selected-provider coordinates remain unsupplied; all current authority counts remain zero. Separate acceptance is required.

## Explicit owner activation decision boundary acceptance

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-OWNER-ACTIVATION-ACCEPT-001` accepts the exact v143 candidate and the explicit approval statement with SHA-256 `b0e9fb7171f3dec721b505ad47acc09fa74e986ed4a06ff9ba09e682461d1af7`. The accepted scope is one non-executing exact input-set collection, sealing and review transaction only. Zero transactions are consumed and one remains. No input document, provider coordinate, replay baseline or execution authorization is supplied; selected-provider and live-authority effects remain zero.



## Exact input-set collection boundary acceptance

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-EXACT-INPUT-SET-COLLECTION-ACCEPT-001` accepts the exact six-artifact non-executing collection/sealing implementation. One owner-authorized transaction remains unconsumed. Live authority documents, exact provider coordinates, replay baseline, trusted time and execution authorization remain unsupplied; selected-provider content access and project replay access remain forbidden.
