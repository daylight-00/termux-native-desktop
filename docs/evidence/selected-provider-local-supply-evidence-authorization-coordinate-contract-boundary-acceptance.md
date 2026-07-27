# Selected-provider local-supply evidence authorization and coordinate-receipt contract boundary acceptance

## Decision

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-ACCEPT-001` accepts the exact v118 candidate boundary:

```text
ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_PROVIDER_LOCAL_SUPPLY_EVIDENCE_AUTHORIZATION_AND_COORDINATE_RECEIPT_CONTRACT
```

The accepted interface contains an 18-claim owner-authorization token schema, a canonical 41-row coordinate-receipt schema with ten fields per row, 30 fail-closed validation rules and zero live authority.

## Frozen candidate evidence

The acceptance freezes these exact SHA-256 values:

- owner-authorization token schema: `27d11e8bb8de3238b49aef77757f0328a2269a156f55fdcbdddcf4dcb4fd411b`;
- coordinate-receipt schema: `b94c25994ecc26e402607b9e61c0cee796c74b15435bc168a18821def9096f83`;
- validation contract: `64a6c168e30c7a559387c27d6baa7d3bd49953d7ea304d1bd98e4043cbb57f56`;
- candidate metadata: `a8f3c7dda27757eebc08f71465c7536df27e9f2979800c28da11a8722dc6bb48`.

Historical candidate artifacts remain unchanged and continue to state `QUALIFIED_NON_MUTATING_AUTHORIZATION_AND_COORDINATE_RECEIPT_CONTRACT_CANDIDATE`.

## Accepted owner-authorization contract

A future token must contain all 18 exact claims, bind the accepted local-supply contract and evidence-transaction design, bind repository HEAD/tree and remote HEAD, bind executor UID and the canonical coordinate-receipt digest, enforce a zero-skew maximum 86,400-second validity interval, and provide replay and revocation protection.

The accepted contract does not create or imply an owner decision, token, authorization nonce or execution authority.

## Accepted coordinate-receipt contract

A future receipt must contain exactly 41 unique accepted contract row IDs and exactly ten fields per row. Every coordinate must be an explicit absolute canonical UTF-8 path bound to an immutable coordinate authority and exact provider-object digest, size and SONAME. Missing, duplicate, unknown, inferred, globbed, variable-expanded, basename-derived or filesystem-searched coordinates reject the entire receipt.

## Current authority state

```text
current live tokens: 0
current coordinate receipts: 0
current coordinate rows: 0
current provider reads: 0
```

Owner authorization issuance, coordinate-receipt production, path discovery, provider-file reads, evidence execution, local-map acceptance and all runtime effects remain separate and unauthorized.

## Authority exclusions

This acceptance does not authorize:

- issuing a live token or coordinate receipt;
- local path discovery or inference;
- downloading or extracting result/package bytes;
- opening or reading provider files;
- executing the evidence transaction;
- producing or accepting a local supply map;
- creating generation roots or object stores;
- materialization, target population, publication, deployment or activation.

## Next action

`design-and-review-non-executing-selected-provider-local-supply-evidence-authorization-issuance-and-coordinate-receipt-production-transaction`
