# Active task: generate and review a non-executing live-input adapter and execution-authorization implementation candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-implementation-candidate`
>
> Expected state on completion: a deterministic repository-owned implementation candidate validates synthetic representations of the accepted ten-input adapter envelope and 27-claim execution authorization without accepting live inputs, opening provider paths, reading provider bytes, writing runtime state or creating live authority.

## Objective

Implement the exact accepted live-input adapter and execution-authorization contract as a bounded non-executing candidate. The candidate must preserve the accepted synthetic issuance/coordinate implementation as an immutable semantic and regression oracle rather than modifying or invoking it as a live executor.

## Why now

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-ACCEPT-001` freezes the exact adapter, authorization, validation, state, operation, failure, receipt and metadata boundary. Implementation work may now begin, but only against repository-owned synthetic fixtures and only as a separate candidate requiring later acceptance.

## In scope

- map all ten explicit input channels, twenty envelope fields, 27 authorization claims, 37 validations, 18 states, 32 operations and 20 failures into deterministic implementation coverage;
- validate exact 41-row/10-field coordinate binding without opening paths;
- validate repository HEAD/tree, remote HEAD, executor, time, revocation, replay, resource and output bindings using synthetic values;
- prove live-to-synthetic rewriting and live invocation of the accepted synthetic CLI remain impossible;
- produce deterministic synthetic success and fail-closed cases;
- preserve zero current live inputs, envelopes, authorizations, provider reads, writes and live authority.

## Out of scope

Supplying a real owner decision, token or coordinate receipt; issuing execution authorization; accepting live paths; storage search or discovery; opening or reading provider files; consuming a live replay tuple; executing evidence collection; producing a local-supply map; creating generation roots; population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-contract.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-execution-authorization-schema.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-validation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-operation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-failure-contract.tsv`

## Pending external inputs

None. Live owner decisions, coordinates and execution authorization belong to later separate transactions and must not be supplied during implementation-candidate work.

## Stop conditions

Stop if the candidate accepts non-repository fixtures, opens any coordinate path, imports discovery/network/process surfaces, writes outside an explicitly supplied synthetic output file, mutates the accepted synthetic implementation, rewrites live paths into synthetic paths, permits live synthetic invocation, or claims live authority.

## Completion criteria

A separately reviewable implementation candidate and deterministic synthetic evidence cover the accepted contract exactly while reporting zero live inputs, zero provider reads, zero writes and zero live authority.

## Next valid action

Generate and review the non-executing implementation candidate only.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
