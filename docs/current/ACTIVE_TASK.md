# Active task: generate and review a non-executing exact input-set collection candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-candidate`
>
> Expected state on completion: a deterministic collector and immutable submission envelope are qualified for the single accepted non-executing transaction; no live input is accepted, no selected-provider path is opened/read, no project replay state is mutated and no execution authority is created.

## Objective

Generate and review the bounded mechanism that can receive one explicitly supplied live-authority input set, seal each component by digest and produce a review candidate without executing the accepted production implementation.

## Why now

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-OWNER-ACTIVATION-ACCEPT-001` accepts one non-executing input-set collection, sealing and review transaction. Zero transactions are consumed and one remains. The input set is absent.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.md`

## Pending external inputs

Owner authorization token; canonical 41-row coordinate receipt; revocation document; trusted-time evidence; execution authorization; exact project replay-registry baseline; exact selected-provider coordinate set and provider baselines.

## In scope

- deterministic manifest and canonical submission envelope;
- explicit paths only, with no search or inference;
- digest sealing and cross-binding validation;
- repository/remote baseline capture;
- replay-registry identity capture without opening or writing it;
- selected-provider coordinate metadata capture without opening or reading provider content;
- one-transaction accounting, unconsumed until a complete candidate is submitted;
- fail-closed receipts for missing, stale or inconsistent inputs.

## Out of scope

Generating or signing owner documents; accepting placeholders or partial inputs; provider discovery/open/read; provider-byte hashing; project replay mutation; transaction execution; local-map production; generation-root creation; population; materialization; publication; deployment or activation.

## Stop conditions

Stop if an input is inferred, generated or substituted; a selected-provider path is opened/read; project replay is opened/written; the accepted transaction is consumed before a complete envelope exists; or any current authority count becomes nonzero.

## Completion criteria

A deterministic non-executing collection candidate and failure contract are qualified or rejected. The live input set remains separately supplied and reviewed.

## Next valid action

Generate and review only the collection/sealing candidate. Do not collect live input during repository review or execute the production implementation.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
