# Active task: generate and review the non-executing selected-provider local-supply live-authority transaction production implementation candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-live-authority-transaction-production-implementation-candidate`
>
> Expected state on completion: a separate production-capable transaction implementation candidate is generated and reviewed only against isolated temporary authority documents, replay storage and provider fixtures; no live authority or selected-provider effect is created.

## Objective

Implement the accepted live-authority transaction design as a separately reviewable production-capable candidate without importing or invoking the accepted synthetic implementation as the executor.

## Why now

The exact synthetic implementation has been accepted as an immutable semantic and regression oracle. A separate production implementation is required before any later execution-readiness or live-authority decision can be reviewed.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.md`

## Pending external inputs

None. No owner activation decision, live authority document, trusted-time evidence, execution authorization, replay registry, selected-provider path or provider byte may be supplied.

## In scope

- a separate production-capable implementation of exact document binding, revocation/trusted-time checks, append-only replay preflight and terminal receipt handling;
- isolated temporary fixtures only;
- independent conformance to the accepted 20/26/52/30 design and 448 inherited semantic rows;
- proof that selected-provider opens/reads, provider bytes, persistent project replay writes, local maps and live authority remain zero.

## Out of scope

Live authority-document delivery or consumption; project replay-registry mutation; provider-open gate activation; selected-provider discovery/open/read; production orchestration against project provider paths; local-map production; generation-root creation; population; materialization; publication; deployment or activation.

## Stop conditions

Stop if the accepted synthetic implementation is imported or invoked as the production executor, a live input is consumed, project replay state is written, a selected-provider path is opened or read, provider bytes are acquired, or any current authority count becomes nonzero.

## Completion criteria

A separate production-capable candidate and isolated-fixture evidence are generated and reviewed with exact fail-closed behavior and zero current authority. Acceptance remains a later independent step.

## Next valid action

Generate and review only the non-executing production implementation candidate. Do not execute against live provider inputs or supply live authority documents.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
