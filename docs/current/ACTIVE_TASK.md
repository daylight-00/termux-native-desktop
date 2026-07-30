# Active task: supply explicit exact input-set envelope inputs

> Task ID: `supply-explicit-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-envelope-inputs`

## Objective

Receive one complete explicit input manifest. Do not generate an envelope while any required group is absent.

## Why now

Preparation was rejected as `REJECTED_FAIL_CLOSED_MISSING_EXPLICIT_INPUTS`: ten groups are required and zero are supplied. Owner accounting remains `1 / 0 / 1`.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-envelope-preparation-review.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.md`

## Pending external inputs

Five canonical document paths, trusted-time binding, replay path/baseline, forty-one ordered provider paths, expected UID/GID and an empty isolated output root.

## In scope

Explicit values and exact baseline validation only.

## Out of scope

Target population remains blocked. Do not acquire or populate provider bytes. Discovery, inferred defaults, provider or replay content access, transaction consumption, execution, mapping, population, materialization, publication, deployment and activation.

## Next valid action

Supply all ten groups in one immutable manifest for separate review.

## Stop conditions

Stop on absence, placeholders, ambiguous paths, duplicates, baseline mismatch, accounting change or authority widening.

## Completion criteria

A complete manifest is available for review, or the boundary remains fail-closed with no envelope and zero authority.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.
