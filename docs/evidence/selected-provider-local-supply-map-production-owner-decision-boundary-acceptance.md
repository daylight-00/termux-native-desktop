# Selected-provider local-supply map production owner decision boundary acceptance

> Acceptance ID: `SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-PRODUCTION-OWNER-DECISION-ACCEPT-001`
>
> Decision: `ACCEPTED_EXPLICIT_ONE_EXACT_COORDINATE_BINDING_MAP_GENERATION_SEALING_REVIEW_TRANSACTION_ONLY`

## Exact owner statement

The owner supplied the following exact UTF-8 statement at `2026-08-01T03:12:00+09:00` in `Asia/Seoul`:

```text
검증된 41개 selected-provider member에 대한 local-supply map production transaction을 승인한다. 범위는 exact coordinate binding과 map 생성·봉인·검토로 제한하며, target population, materialization, publication, deployment, activation 및 live provider mutation은 승인하지 않는다.
```

Its newline-terminated UTF-8 SHA-256 is `0a68ff343e98680b6409f603dc67d6b578e859fb0013abb7e2f4bc580c2d68f0`. Conversation ownership is the attribution boundary; this record is not a cryptographic signature.

## Bound repository and evidence

```text
repository HEAD: 017527d92cac73d95b771c9fbd4dcf48ad681a9c
repository tree: eb5531119eb5b00a1b455ca51be20d30803274c4
remote main:     017527d92cac73d95b771c9fbd4dcf48ad681a9c
accepted production-bootstrap result SHA-256: 55807be078f3861de6d7f596cb3dcfeefabd8acd122de77e9cae8ba32e65b77d
accepted provider members: 41
accepted provider bytes: 29,047,112
```

## Accepted transaction

Exactly one transaction is accepted. It may bind the accepted 41 member identities to canonical isolated local paths, reuse or reacquire only exact digest-bound carriers, validate size/SHA-256/ELF/SONAME, generate the canonical local-supply map and receipts, seal all outputs and review the result.

```text
accepted / consumed / remaining: 1 / 0 / 1
local-supply maps produced now:  0
live authority:                  0
```

The transaction may write only isolated transaction outputs and repository review evidence. It must fail closed before any target-population effect.

## Prohibited widening

This acceptance does not authorize selected-provider live-path discovery or mutation, arbitrary source acquisition, project replay mutation, target population, materialization, publication, deployment, activation, package installation or live glibc-prefix mutation.

It does not reuse or reopen the historical collection-only transaction, whose accounting remains `1 / 1 / 0`.

## Next action

`execute-one-owner-authorized-selected-provider-local-supply-map-production-transaction`

A separately reviewed production result and separate repository promotion remain required. No target population follows automatically from map production.
