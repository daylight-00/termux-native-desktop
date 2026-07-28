# Active task: design and review a non-executing local-supply evidence implementation live-input adapter and execution-authorization contract

> Task ID: `design-and-review-non-executing-selected-provider-local-supply-evidence-implementation-live-input-adapter-and-execution-authorization-contract`
>
> Expected state on completion: a deterministic non-executing contract defines how a future explicit owner decision and canonical 41-row coordinate receipt may be presented to the accepted synthetic implementation through a separate adapter, while live inputs, provider reads, evidence execution and runtime mutation remain absent and unauthorized.

## Objective

Define the interface and authorization boundary between the accepted synthetic-only implementation and any future live owner-decision or coordinate-receipt inputs. The contract must preserve explicit-input-only semantics, digest and baseline binding, revocation and replay controls, inactive staging, no provider read before separate execution authorization, and protected-state invariance.

## Why now

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001` accepts the exact synthetic-only implementation boundary. That implementation deliberately cannot accept arbitrary or live input. Before any live transaction can be considered, a separate adapter and execution-authorization contract must define the allowed interface without enabling it.

## In scope

- define a non-executing live-input adapter contract;
- bind owner decision, authorization token, coordinate receipt, repository HEAD/tree, remote HEAD, executor and time window;
- require exact 41-row coordinate completeness and digest cross-binding;
- define revocation, replay, expiry and stale-baseline rejection;
- require zero provider reads before a separate evidence-execution authorization;
- define inactive staging, failure receipt and protected-state invariance;
- preserve synthetic implementation bytes unchanged.

## Out of scope

Supplying a real owner decision, issuing or activating a token, producing or accepting live coordinates, searching storage, opening or reading provider files, downloading or extracting evidence, executing evidence collection, producing a local map, creating runtime roots, population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.tsv`

## Pending external inputs

None for contract design. Live owner decisions, coordinates and execution authority require later separate transactions.

## Stop conditions

Stop if the contract embeds a live token or path, permits discovery or inference, allows provider reads before separate execution authorization, modifies the accepted implementation, creates runtime state or weakens revocation, replay, failure or invariance boundaries.

## Completion criteria

Machine-readable adapter and authorization contracts are deterministic and contain zero live inputs, zero provider reads, zero writes and zero live authority. Implementation execution and all runtime effects remain blocked.

## Next valid action

Design and review contracts only. Do not issue, activate, search, acquire, open, read, extract, localize, populate or execute against live inputs.

Do not acquire or populate provider bytes.
