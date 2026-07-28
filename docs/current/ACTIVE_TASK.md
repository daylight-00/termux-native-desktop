# Active task: generate and review the non-executing production-capable local-supply live-evidence orchestration implementation candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-live-evidence-orchestration-production-implementation-candidate`
>
> Expected state on completion: a separate repository-owned production-capable orchestration candidate composes the accepted authorization/coordinate, live-input adapter/execution-authorization and read-only evidence contracts without consuming live documents or selected provider bytes.

## Objective

Generate and review a non-executing production-capable implementation candidate for the selected-provider local-supply evidence flow. The candidate must preserve every accepted cardinality, digest binding, fail-closed rule, replay boundary and protected-state invariant while remaining separate from all accepted synthetic oracle bytes.

## Why now

The three semantic layers are now accepted as exact synthetic-only authorities: authorization/coordinate issuance, live-input adapter/execution authorization, and read-only local-supply-map evidence collection. The remaining implementation gap is a separate production-capable orchestration candidate; live-to-synthetic rewriting and invocation of the accepted synthetic CLIs remain forbidden.

## In scope

- compose exact explicit owner-decision, token, coordinate-receipt, revocation and execution-authorization inputs;
- implement canonical digest and repository/remote/executor/time binding against the accepted schemas;
- define the append-only replay-registry interface and first-open gate;
- implement no-follow, regular-file, ownership/mode, stability, streaming hash, ELF and SONAME surfaces in separate production code;
- exercise only isolated temporary fixture files created by the test harness;
- prove selected provider paths, package databases and the live glibc prefix remain untouched;
- preserve separate review and acceptance before any live execution.

## Out of scope

Supplying a live owner decision, issuing or activating a live token, producing a live coordinate receipt, issuing execution authorization, reading any selected provider path, producing or accepting a live local-supply map, persisting a production replay tuple, creating a generation root, target population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.md`

## Pending external inputs

None. Production candidate review must use repository-owned schemas and isolated temporary fixtures only. Live authorization and coordinate documents belong to a later separately authorized transaction.

## Stop conditions

Stop if the candidate imports or invokes an accepted synthetic CLI as a live executor, rewrites live paths into the synthetic namespace, searches storage, reads a selected provider path, mutates package databases or the live glibc prefix, persists production authority, or widens any accepted cardinality or output scope.

## Completion criteria

A separate production-capable candidate and deterministic isolated-fixture tests cover the accepted orchestration boundary with zero selected-provider reads, zero runtime writes and zero live authority.

## Next valid action

Generate and review the production-capable orchestration implementation candidate only. Do not execute it against live provider inputs.

Do not acquire or populate provider bytes.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.
