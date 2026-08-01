# Active task: await an explicit target-population owner decision

> Task ID: `await-explicit-owner-decision-for-selected-provider-target-population-production-transaction`
>
> Status: exact 41-row map accepted; target population unauthorized

## Objective

Preserve the accepted map while awaiting a separate explicit owner decision for target population.

## Why now

The map-production transaction is exhausted. Map acceptance does not authorize copying or linking provider bytes.

## Required reading

- `docs/evidence/selected-provider-local-supply-map-production-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-map-production-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-production-candidate.json`

## Pending external inputs

One explicit owner statement defining a bounded target-population transaction and its exclusions.

## In scope

Maintain the accepted map, receipt, `1 / 1 / 0` accounting and zero-later-effect boundary.

## Out of scope

Selected-provider live-path discovery, open, read or mutation; population and all later effects.

## Next valid action

Receive and review the explicit owner statement.

## Stop conditions

Stop on any digest, seal, row, accounting, repository, protected-state or authority mismatch.

## Completion criteria

No execution occurs before a future owner decision is separately reviewed and accepted.

Do not populate, materialize, publish, deploy or activate.
