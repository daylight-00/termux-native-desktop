# Active task: review and accept the non-executing exact input-set collection candidate

> Task ID: `review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-candidate-boundary`
>
> Expected completion: accept or reject the exact collection/sealing candidate without consuming the owner transaction or creating live authority.

## Objective

Review only `SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-EXACT-INPUT-SET-COLLECTION-REVIEW-001` and its exact six artifacts.

## Why now

One non-executing collection, sealing and review transaction is accepted. The candidate now demonstrates explicit-path handling, canonical document sealing, provider/replay metadata-only capture and isolated envelope output. Candidate acceptance remains separate from live collection.

## Required reading

- `docs/evidence/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-review.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance.md`

## Pending external inputs

Owner token, canonical 41-row receipt, revocation document, trusted-time evidence, execution authorization, replay baseline and selected-provider coordinates remain absent.

## In scope

Exact artifact digests; 20 input rows; one success and twenty failures; five isolated document reads; forty-one provider `lstat` calls; one replay `lstat`; repository/remote/executor metadata; two isolated envelope writes; owner accounting `1 / 0 / 1`.

## Out of scope

Live input acceptance; path discovery; provider content open/read; provider-byte hashing; project replay open/read/write; execution; local-map production; population, materialization, publication, deployment or activation.

## Stop conditions

Stop on inferred paths, accepted-oracle imports, provider content access, project replay access, transaction consumption, live input acceptance, provider-gate arming or execution authority.

## Completion criteria

The exact candidate is accepted or reproducibly rejected while all current authority counts remain zero.

## Next valid action

Review and accept only the candidate. Do not collect live input or execute the production implementation.

Do not acquire or populate provider bytes.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate bytes.
