# Active task: await owner activation and the exact selected-provider local-supply live-authority transaction input set

> Task ID: `await-owner-activation-and-exact-selected-provider-local-supply-live-authority-transaction-input-set`
>
> Expected state on completion: the exact owner activation decision and immutable five-document live-authority transaction input set are either absent, or separately reviewed without executing the transaction or opening a selected-provider path.

## Objective

Hold the accepted production transaction implementation at the external-input gate. Review no transaction until the owner explicitly supplies one immutable activation decision, owner authorization token, canonical 41-row coordinate receipt, revocation document and execution authorization with the exact replay-registry identity and selected-provider coordinates required by the accepted design.

## Why now

The design, synthetic implementation and production-capable isolated-fixture implementation have all been accepted. Further internal implementation work would not create the missing owner decision or live authority documents and must not be treated as authorization.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-production-implementation-review.md`

## Pending external inputs

- owner activation decision;
- owner authorization token;
- canonical 41-row coordinate receipt;
- revocation-status document;
- execution authorization;
- exact project replay-registry identity and initial integrity state;
- exact selected-provider coordinate set and repository/remote baselines bound by those documents.

None is currently supplied or authorized.

## In scope

- preserve the accepted implementation and all zero-authority counts;
- receive an explicit owner-supplied input set only when available;
- verify that the entire set is immutable, complete, cross-bound and consistent before any later execution review;
- reject partial, inferred, environment-discovered, rewritten or interactively completed input sets.

## Out of scope

Generating or signing owner documents; project replay mutation; provider-open gate activation; selected-provider discovery/open/read; provider-byte acquisition; orchestration execution; local-map production; generation-root creation; population; materialization; publication; deployment or activation.

## Stop conditions

Stop if any live document is inferred rather than explicitly supplied, the set is incomplete, any digest or baseline disagrees, trusted time is absent, replay identity is ambiguous, a selected-provider path is opened or read, project replay state is written, or any current authority count becomes nonzero.

## Completion criteria

No execution occurs. A later transaction review may begin only after the owner explicitly supplies the complete immutable input set and its exact bindings.

## Next valid action

Await the owner activation decision and exact live-authority transaction input set. Do not generate substitute documents and do not execute the accepted implementation.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
