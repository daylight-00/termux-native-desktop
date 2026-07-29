# Active task: generate and review the non-executing selected-provider local-supply live-authority transaction design candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-live-authority-transaction-design-candidate`
>
> Expected state on completion: an exact repository-owned non-executing transaction design defines future owner activation, live-document delivery, replay persistence and invocation of the accepted production orchestration implementation without creating or consuming live authority.

## Objective

Design the first separately owner-authorized transaction boundary that could later deliver exact owner-decision, token, coordinate-receipt, revocation and execution-authorization documents to the accepted production orchestration implementation.

## Why now

The production-capable orchestration implementation is accepted only for isolated fixtures. Before any selected-provider path can be opened, the repository needs an explicit design for owner activation, input provenance, append-only replay persistence, protected-state snapshots, indexed receipts and fail-closed rollback.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.md`

## Pending external inputs

None. This stage designs the future transaction only. No owner decision, token, coordinate receipt, execution authorization, provider path or provider byte may be supplied.

## In scope

- exact future input and provenance contracts;
- owner activation and execution-authorization ordering;
- append-only replay-registry persistence interface;
- repository HEAD/tree, remote HEAD, executor UID and trusted-time binding;
- protected-state pre/post snapshots and rollback boundary;
- first selected-provider open gate and indexed success/failure receipts;
- deterministic state, operation and fail-closed coverage.

## Out of scope

Creating or accepting live authority documents, opening selected-provider paths, reading provider bytes, persisting a replay tuple, executing evidence collection, producing a local-supply map, generation-root creation, target population, materialization, publication, deployment or activation.

## Stop conditions

Stop if the design embeds a live secret or path, treats accepted isolated fixtures as live authority, authorizes a provider open before every authority and replay gate, permits non-append-only replay state, or widens protected-state effects.

## Completion criteria

A non-executing transaction design candidate and deterministic review artifacts cover every future live-authority input, state, operation and failure while all current live-document, selected-provider open/read, replay-write and local-map counts remain zero.

## Next valid action

Generate and review the transaction design candidate only. Do not execute it and do not provide live inputs.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
