# Active task: prepare the exact input-set collection envelope

> Task ID: `prepare-and-review-one-non-executing-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-envelope`
>
> Expected completion: produce or reject an explicit non-executing envelope without consuming the owner transaction or accessing provider/replay content.

## Objective

Prepare the path and argument envelope. Bind acceptance, repository and remote baselines, executor identity, five document paths, forty-one provider paths, replay path and isolated output root.

## Why now

The implementation is accepted and one transaction remains, but no live input set is supplied.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-review.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.md`

## Pending external inputs

Owner token, coordinate receipt, revocation, trusted time, execution authorization, replay baseline and provider paths remain unsupplied. Treat them as required; do not invent values.

## In scope

Envelope schema, path provenance, repository and remote bindings, owner accounting `1 / 0 / 1`, isolated output and pre-access validation.

## Out of scope

Path discovery, provider-content access, project-replay access, live-input acceptance, owner-transaction consumption, execution, local-map production, population, materialization, publication, deployment and activation.

## Next valid action

Generate and review only an envelope candidate. Do not run the collector.

## Stop conditions

Stop on absent or inferred inputs, ambiguous paths, baseline mismatch, accounting change, content access, replay access or authority widening.

## Completion criteria

An exact envelope candidate is produced for separate review, or preparation fails closed with authority counts unchanged.

Do not acquire or populate provider bytes.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.
