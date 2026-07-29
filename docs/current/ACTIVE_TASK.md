# Active task: review and accept the non-executing selected-provider local-supply live-authority transaction implementation candidate

> Task ID: `review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-implementation-candidate-boundary`
>
> Expected state on completion: the exact six-artifact 128-row synthetic-only implementation candidate is accepted without creating live documents, replay writes, selected-provider opens or reads, provider bytes, local maps or live authority.

## Objective

Review and accept only the exact repository-owned live-authority transaction implementation candidate and its deterministic synthetic fixtures, coverage and fail-closed behavior.

## Why now

The accepted design has been implemented as a separately reviewable synthetic-only candidate. Acceptance must freeze that exact implementation boundary before any later live-authority execution work can be considered.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-implementation-review.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.md`

## Pending external inputs

None. No owner activation decision, live token, live coordinate receipt, revocation document, trusted-time evidence, execution authorization, replay registry, selected-provider path or provider byte may be supplied.

## In scope

- exact digest acceptance of the six implementation artifacts;
- exact 20/26/52/30 and 128-row coverage acceptance;
- one deterministic success and thirty fail-closed cases;
- five synthetic non-live document roles, forty-one synthetic coordinates and ten replay fields;
- proof that every current authority and side-effect count remains zero.

## Out of scope

Live document acceptance or consumption; replay-registry open or append; provider-open gate arming; selected-provider discovery/open/read; provider-byte acquisition; orchestration execution; local-map production; generation-root creation; population; materialization; publication; deployment or activation.

## Stop conditions

Stop if any artifact digest drifts, a design row is missing, a live input is consumed, replay persistence occurs, the provider-open gate is armed, selected-provider data is opened or read, or any current authority count becomes nonzero.

## Completion criteria

A separate acceptance record freezes the exact candidate and preserves zero current authority. Implementation acceptance must remain distinct from execution authorization.

## Next valid action

Review and accept only the exact non-executing implementation candidate. Do not execute it or provide live inputs.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
