# Selected-provider local-supply evidence authorization issuance and coordinate-receipt production implementation boundary acceptance

## Decision

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001` accepts the exact v122 candidate boundary:

```text
ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_IMPLEMENTATION_AUTHORITY
```

This is bounded implementation authority for repository-owned synthetic fixtures only. It is not authority to accept live inputs, issue or activate a token, produce coordinates, read provider bytes or execute evidence collection.

## Frozen candidate evidence

The acceptance freezes these exact SHA-256 values:

- implementation source: `039593be6144845b8be817bc45144be58c0f9a03bc60278a73748213d269df61`;
- synthetic fixture: `8a8f16ed58f4964ed553da50d1dfaee8420ddc8b0691a3fac6cf462b1853929e`;
- negative cases: `65d3c7721e522455c6ebfa617c51d60f6d0c1c522c880a5e77f0ed1882a42874`;
- 88-row coverage ledger: `b1abeac98acf9bb583f594ad043a5fa9e24fb6dfd5067e401a4e385b9aa63e93`;
- synthetic success receipt: `fc0b3ef73ee8df3b7655a9d56e04cf055214bacddf12579498d389f47c2721f8`;
- candidate metadata: `297d3a82d6ade0925323face82e38160dcd5563ce3daa1b8d29c0a5ed82ab32d`.

Historical candidate artifacts remain unchanged and continue to state `QUALIFIED_NON_EXECUTING_SYNTHETIC_IMPLEMENTATION_CANDIDATE`.

## Accepted implementation boundary

```text
input coverage:             14
state coverage:             18
operation coverage:         36
failure coverage:           20
total coverage rows:        88
synthetic success cases:     1
fail-closed cases:          20
synthetic coordinate rows:  41
provider reads:              0
writes:                      0
live authority:              0
```

The implementation may parse only a repository-owned fixture marked `SYNTHETIC_REPOSITORY_FIXTURE_ONLY`. It may validate synthetic coordinate strings but may not search, glob, infer, open or read filesystem provider paths. It has no subprocess, network, package-manager or archive-extraction surface.

## Current authority state

```text
issued tokens: 0
coordinate receipts: 0
coordinate rows: 0
provider reads: 0
writes: 0
live authority: 0
```

## Authority exclusions

This acceptance does not authorize:

- arbitrary or live fixture input;
- owner-token issuance or activation;
- coordinate-receipt production or acceptance;
- local path discovery, inference or binding;
- downloading, extracting, opening or reading provider bytes;
- evidence-transaction execution;
- local-supply-map production or acceptance;
- generation-root or object-store creation;
- target population, materialization, publication, deployment or activation.

## Next action

`design-and-review-non-executing-selected-provider-local-supply-evidence-implementation-live-input-adapter-and-execution-authorization-contract`

The next step may define a non-executing adapter and authorization interface only. It may not bind live paths, consume a real owner decision, read provider bytes or create runtime authority.
