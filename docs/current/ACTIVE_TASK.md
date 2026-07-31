# Active task: execute one owner-authorized local-supply map production transaction

> Task ID: `execute-one-owner-authorized-selected-provider-local-supply-map-production-transaction`

## Objective

Produce and seal one exact 41-row local-supply map while consuming one accepted transaction.

## Why now

The accepted boundary contains 9 sources, 33 carriers, 41 members, 29,047,112 bytes and zero live authority. The owner authorized one map-production transaction with SHA-256 `0a68ff343e98680b6409f603dc67d6b578e859fb0013abb7e2f4bc580c2d68f0`.

## Required reading

- `docs/evidence/selected-provider-local-supply-map-production-owner-decision-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-map-contract-boundary-acceptance.md`

## Pending external inputs

None. Use only accepted coordinates and fail closed on missing or changed input.

## In scope

Bind 41 verified isolated members, reuse or reacquire exact carriers, generate and seal the map and receipts, review the result and consume one transaction.

## Out of scope

Selected-provider live-path discovery, open, read or mutation; project replay mutation; population, materialization, publication, deployment, activation, package installation or live-prefix mutation.

## Next valid action

Generate and run one fail-closed production package that emits the exact local-supply map and review evidence without populating a target.

## Stop conditions

Stop on any identity, digest, repository, transaction-count or protected-state mismatch, and before population or live mutation.

## Completion criteria

One 41-row map and its receipts are generated, sealed and reviewed; transaction accounting becomes `1 accepted / 1 consumed / 0 remaining`; repository authority is promoted separately; target population and all later effects remain unauthorized.

Do not populate, materialize, publish, deploy or activate.
