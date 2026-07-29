# Active task: generate and review the non-executing selected-provider local-supply live-authority transaction implementation candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-live-authority-transaction-implementation-candidate`
>
> Expected state on completion: a repository-owned implementation candidate covers the accepted 20-input, 26-state, 52-operation and 30-failure design while all live-document, replay-write, selected-provider open/read, provider-byte, local-map and live-authority counts remain zero.

## Objective

Implement the accepted live-authority transaction semantics as a deterministic non-executing candidate and review its exact coverage, fixtures and fail-closed behavior.

## Why now

The design boundary is accepted and immutable. A separately reviewed implementation candidate is required before any later owner-authorized execution transaction can be considered. Implementation must not silently convert design authority into live authority.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-design-review.md`
- `docs/evidence/selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.md`

## Pending external inputs

None. This stage uses repository-owned synthetic or isolated fixtures only. No owner decision, live token, coordinate receipt, revocation document, execution authorization, replay tuple, selected-provider path or provider byte may be supplied.

## In scope

- exact implementation coverage for all accepted inputs, states, operations and failures;
- deterministic synthetic or isolated success and fail-closed fixtures;
- immutable live-document and replay interfaces with no persistent writes;
- proof that provider-open gates remain closed in every current execution;
- explicit separation from accepted synthetic oracles and the production orchestration implementation;
- zero-authority and protected-state regression evidence.

## Out of scope

Supplying or accepting live authority documents; opening or writing a replay registry; selected-provider discovery/open/read; provider-byte acquisition; live evidence execution; local-map production or acceptance; generation-root creation; population; materialization; publication; deployment or activation.

## Stop conditions

Stop if the implementation consumes ambient live inputs, writes replay state, opens selected-provider paths, invokes accepted synthetic oracles as live executors, executes production orchestration against live inputs or widens protected-state effects.

## Completion criteria

A separately reviewable candidate and coverage ledger prove exact accepted-design coverage and fail closed while all current authority counts remain zero. Acceptance remains a later transaction.

## Next valid action

Generate and review only the non-executing implementation candidate. Do not accept or execute it and do not provide live inputs.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
