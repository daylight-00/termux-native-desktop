# Selected-provider local-supply live-authority transaction design review

> Review ID: `SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-DESIGN-REVIEW-001`
>
> Decision: `QUALIFIED_NON_EXECUTING_SELECTED_PROVIDER_LOCAL_SUPPLY_LIVE_AUTHORITY_TRANSACTION_DESIGN_CANDIDATE`
>
> Acceptance gate: `SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-DESIGN-ACCEPTANCE-OPEN`

## Scope

This review defines the first separately owner-authorized transaction boundary that could later deliver exact live authority documents to the accepted production orchestration implementation. It orders owner activation, token and coordinate receipt verification, revocation, execution authorization, repository and remote baselines, executor identity, trusted time, append-only replay preflight, protected-state snapshots, the first selected-provider open gate, orchestration invocation and indexed terminal receipts.

The review is design-only. It creates, accepts and consumes no live owner decision, token, coordinate receipt, revocation document or execution authorization. It opens no selected-provider path, reads no provider byte, appends no replay tuple and produces no local-supply map.

## Frozen source authority

The design consumes only four accepted repository boundaries:

- the accepted synthetic authorization-issuance and 41-row coordinate-production implementation;
- the accepted synthetic live-input adapter and execution-authorization implementation;
- the accepted read-only local-supply-map evidence transaction design;
- the accepted production-capable isolated-fixture orchestration implementation.

Their inherited semantic coverage is `88 + 164 + 78 + 118 = 448` rows. These authorities remain immutable oracles and accepted implementation surfaces. None is interpreted as current live authority.

## Candidate structure

```text
future input contracts:           20
state-machine states:             26
ordered operations:               52
transaction failure contracts:    30
inherited semantic coverage:      448
future live-document roles:         5
future replay-tuple fields:        10
current live documents:             0
current execution authorizations:   0
current replay writes:              0
current selected-provider opens:    0
current selected-provider reads:    0
current provider bytes:              0
current local-supply maps:           0
current live authority:              0
```

## Future live-document authority

A future transaction may begin only with five immutable documents supplied as explicit file arguments: an owner activation decision, owner authorization token, canonical 41-row coordinate receipt, revocation-status document and execution authorization. Every document must bind the same transaction, accepted source digests, repository HEAD/tree, remote HEAD, executor identity, trusted-time window, replay-registry identity, resource limits, output root and orchestration implementation digest.

No document may be inferred from environment variables, discovered by filename, rewritten into a synthetic fixture or supplied interactively after execution begins.

## Replay and ordering boundary

The future replay registry is append-only. The transaction first verifies registry ownership, mode, schema, integrity root and monotonic sequence; then proves the canonical transaction tuple is absent. The tuple remains in memory until the orchestration receipt is complete and verified. Exactly one append, file `fsync`, parent-directory `fsync` and readback verification may then occur. Failure before that point performs zero replay writes. Failure during append is terminal and requires a new authorization transaction.

The provider-open gate remains closed until package, source authorities, all five live documents, local and remote baselines, executor, trusted time, replay preflight, protected-before snapshot, output root, resource limits and orchestration identity have all passed.

## Future execution and receipt boundary

Only the accepted production orchestration implementation may be invoked after the gate is armed. It remains responsible for exact 41-row order, component `lstat`, `O_NOFOLLOW`, stable `fstat`, streaming SHA-256, ELF64/AArch64 and exact `DT_SONAME` checks. The transaction verifies the complete canonical evidence receipt before any replay append.

Success and failure receipts bind every live-document digest, baseline, executor, time evidence, orchestration digest, provider-open/read/byte counts, replay tuple, protected-state snapshots and result index. The output scope is limited to transaction evidence and the append-only replay tuple. Provider paths, package databases, the live glibc prefix, generation roots, targets and selectors remain immutable.

## Failure and recovery

Thirty fail-closed contracts cover package/source drift, each authority document, repository and remote baselines, executor and time, replay registry and duplicates, protected-state snapshots, output and resource limits, orchestration identity, synthetic rewrite, premature provider open, provider path/content, whole-map completeness, receipt integrity, replay append, result delivery and bounded recovery.

Any failure closes exact descriptors, rejects the entire transaction and emits a canonical failure receipt when possible. Cleanup is restricted to exact transaction evidence temporaries. The replay registry, provider paths, live prefix, generation roots and unknown paths are never deleted or rewritten.

## Decision

```text
QUALIFIED_NON_EXECUTING_SELECTED_PROVIDER_LOCAL_SUPPLY_LIVE_AUTHORITY_TRANSACTION_DESIGN_CANDIDATE
```

This decision grants no owner activation, live-document acceptance, execution authorization, replay persistence, selected-provider open/read, local-map production, generation-root creation, target population, materialization, publication, deployment or activation authority.

## Next action

`review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-design-boundary`
