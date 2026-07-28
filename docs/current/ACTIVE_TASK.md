# Active task: review and accept the non-executing local-supply evidence live-input adapter and execution-authorization contract candidate boundary

> Task ID: `review-and-accept-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-contract-candidate-boundary`
>
> Expected state on completion: the exact eight-artifact live-input adapter and execution-authorization contract candidate is accepted as bounded non-executing project authority while the accepted synthetic implementation remains an immutable oracle, live inputs and authorizations remain absent, and provider reads, evidence execution and runtime mutation remain unauthorized.

## Objective

Review `SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-REVIEW-001` and decide whether its exact adapter schema, execution-authorization schema, 37 validation rules, 18 states, 32 operations, 20 failures, receipt contract and metadata may be accepted without widening the synthetic implementation or creating live authority.

## Why now

The contract review found that the accepted implementation is hard-bound to synthetic fixtures, paths and origins and therefore cannot safely become a live executor through path rewriting. The candidate preserves those bytes as a semantic/regression oracle and requires a separately reviewed future live adapter implementation. Before implementation work begins, the exact contract boundary requires a Class D acceptance decision.

## In scope

- verify all eight candidate artifact digests and cardinalities;
- verify the exact accepted synthetic implementation digest and oracle-only role;
- verify live-to-synthetic path/origin rewriting and live synthetic CLI invocation are forbidden;
- verify ten explicit input channels, the twenty-field inactive envelope and exact 41-row/10-field coordinate binding;
- verify the 27-claim execution authorization, one-hour validity, revocation, replay, baseline, executor, resource and output bindings;
- verify the first provider-open gate requires all validations and atomic replay consumption;
- verify zero current live inputs, envelopes, authorizations, provider reads, writes and live authority;
- accept or reject the exact frozen candidate without modifying it.

## Out of scope

Modifying the candidate, implementing a live adapter or executor, supplying a real owner decision or coordinate receipt, issuing or activating authorization, rewriting live paths into synthetic paths, invoking the synthetic implementation with live inputs, searching storage, opening or reading provider files, executing evidence collection, producing a local map, creating runtime roots, population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-contract.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-execution-authorization-schema.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-validation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-operation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-failure-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-receipt-contract.json`

## Pending external inputs

None for contract acceptance. Live owner decisions, coordinates, adapter implementation and execution authorization require later separate transactions.

## Stop conditions

Stop if any digest or cardinality differs, the candidate permits live-to-synthetic rewriting or live invocation of the accepted synthetic implementation, embeds a live path/token/authorization, permits discovery, opens provider bytes before the separate execution gate, widens output or resource scope, or creates runtime state.

## Completion criteria

A separate append-only acceptance record freezes the exact candidate while preserving zero live inputs, zero provider reads, zero writes and zero live authority. The next task may implement the accepted adapter contract only through a separately reviewed candidate; it may not execute against live inputs.

## Next valid action

Review and accept or reject the exact contract candidate boundary only.

Do not implement, issue, activate, discover, open, read, localize, populate or execute against live inputs.

Do not acquire or populate provider bytes.
