# Active task: review and accept the non-executing selected-provider local-supply live-authority transaction design boundary

> Task ID: `review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-design-boundary`
>
> Expected state on completion: the exact 20-input, 26-state, 52-operation and 30-failure design artifacts are accepted as a bounded non-executing transaction design while every live-document, replay-write, selected-provider open/read and local-map count remains zero.

## Objective

Review the exact repository-owned live-authority transaction design candidate and accept or reject its frozen input, state, operation, failure, receipt and metadata artifacts.

## Why now

The production-capable orchestration implementation is accepted only for isolated fixtures, and the new live-authority transaction design candidate now freezes every future owner-activation, live-document, replay, first-open and rollback gate. That design must be accepted as an exact non-executing boundary before any later implementation work can begin.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-design-review.md`
- `docs/evidence/selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-boundary-acceptance.md`

## Pending external inputs

None. This stage reviews repository-owned design artifacts only. No owner decision, token, coordinate receipt, execution authorization, replay tuple, provider path or provider byte may be supplied.

## In scope

- exact six-artifact digest and cardinality review;
- ordering of owner decision, token, coordinate, revocation and execution-authorization gates;
- append-only replay precheck and single-append interface;
- first selected-provider-open gate and protected-state invariance;
- deterministic fail-closed and rollback boundaries;
- proof that all current live authority counts remain zero.

## Out of scope

Creating, supplying, accepting or consuming live authority documents; writing a replay tuple; opening selected-provider paths; reading provider bytes; running the orchestration implementation; producing a local-supply map; generation-root creation; population; materialization; publication; deployment or activation.

## Stop conditions

Stop if any accepted artifact grants current live authority, permits provider open before every authority/replay gate, invokes a synthetic oracle as a live executor, permits mutable replay state or widens protected-state effects.

## Completion criteria

An exact acceptance record freezes the six design artifacts and preserves zero current live documents, execution authorizations, replay writes, selected-provider opens/reads, provider bytes, local-supply maps and live authority.

## Next valid action

Review and accept or reject the exact transaction design boundary only. Do not implement or execute it and do not provide live inputs.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
