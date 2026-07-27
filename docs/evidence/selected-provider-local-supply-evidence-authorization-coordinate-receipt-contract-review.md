# Selected-provider local-supply evidence authorization and coordinate-receipt contract review

## Decision

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-REVIEW-001` qualifies a deterministic non-mutating interface candidate:

```text
QUALIFIED_NON_MUTATING_AUTHORIZATION_AND_COORDINATE_RECEIPT_CONTRACT_CANDIDATE
```

The candidate defines two future external authority inputs required by the accepted read-only local-supply-map evidence transaction:

1. an immutable owner-authorization token;
2. a canonical complete 41-row local coordinate receipt.

This review issues neither input. current token count: 0. current coordinate rows: 0. current provider reads: 0.

## Source authority

The candidate is bound to:

- `SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001`;
- `SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001`;
- the exact accepted 41-row local-supply-map contract;
- the exact accepted 24-rule local-supply validation contract.

Any source digest change requires a new contract review.

## Owner-authorization token schema

The schema requires 18 claims:

- schema and token identities;
- immutable owner identity and decision ID;
- issue, not-before and expiry timestamps;
- unique nonce and revocation epoch;
- transaction ID;
- accepted contract and evidence-design IDs;
- exact repository HEAD and tree;
- exact remote HEAD;
- exact executor UID;
- exact canonical coordinate-receipt SHA-256.

The validity interval may not exceed 86,400 seconds and permits no clock-skew tolerance. The only permitted effect is read-only provider validation plus transaction-scoped evidence outputs. Acquisition, extraction, provider mutation, runtime mutation, local-map acceptance, materializer execution, generation-root creation, population, publication, deployment and activation are explicitly denied.

## Coordinate-receipt schema

A future coordinate receipt must contain exactly 41 rows and the exact accepted contract-row ID set. Every row requires ten fields:

1. contract row ID;
2. sequence;
3. provider object ID;
4. expected member SHA-256;
5. expected member size;
6. expected SONAME;
7. absolute canonical path;
8. immutable coordinate-authority ID;
9. coordinate origin;
10. SHA-256 of the canonical path text.

Missing, duplicate, unknown or inferred coordinates reject the whole receipt. Paths may not contain dot/dot-dot components, glob syntax, variables, command expansion, basename fallback or filesystem-search expressions.

## Validation boundary

Thirty ordered validation rules cover owner authority, time and replay boundaries, revocation, accepted contract/design binding, repository/remote identity, executor identity, receipt digest binding, exact effect scope, 41-row completeness, exact object identity, canonical path constraints, coordinate authority and canonical digest production.

The candidate contains no live token, no live coordinate receipt, no local path and no evidence-execution authority.

## Acceptance gate

```text
SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-ACCEPTANCE-OPEN
```

Separate acceptance is required before any live token or coordinate receipt may even be reviewed. Acceptance would still not issue a token, populate a path, read provider bytes or authorize execution.

## Authority exclusions

This review does not authorize:

- local path discovery or inference;
- result or package acquisition;
- archive or package extraction;
- provider-file open or read;
- evidence-transaction execution;
- local-supply-map production or acceptance;
- generation-root or object-store creation;
- materialization, target population or publication;
- deployment or activation.

## Next action

`review-and-accept-non-mutating-selected-provider-local-supply-evidence-authorization-and-coordinate-receipt-contract-boundary`
