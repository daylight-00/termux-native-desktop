# Read-only selected-provider local-supply-map evidence transaction design review

> Review ID: `SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-REVIEW-001`
>
> Decision: `QUALIFIED_NON_EXECUTING_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_DESIGN_CANDIDATE`
>
> Acceptance gate: `SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPTANCE-OPEN`

## Scope

This review translates the accepted 41-row local-supply-map contract into a non-executing transaction design. It defines how a future separately authorized transaction would receive exact coordinates, validate each file without discovery or symlink following, produce a canonical candidate or failure receipt, verify protected-state invariance and deliver an indexed result archive.

No actual authorization token, coordinate receipt or provider path is present. The review opens no provider file, performs no local search, reads no provider byte and creates no runtime path.

## Frozen source boundary

The design consumes only the accepted contract boundary:

- one accepted Class D contract record;
- 41 unbound object rows;
- 24 ordered fail-closed validation rules;
- one canonical empty local-map receipt schema;
- zero populated local paths.

Any source digest or count change requires a new contract review before this transaction design can be reconsidered.

## Candidate structure

```text
input contracts:                12
state-machine states:           16
ordered operations:             32
transaction failure contracts:  18
inherited validation rules:      24
future receipt rows:             41
current authorized coordinates:  0
current provider reads:           0
```

## Future input authority

A future execution may begin only with an immutable owner-approved authorization token and a canonical 41-row coordinate receipt supplied as explicit file arguments. The token binds the contract acceptance, repository HEAD/tree, remote HEAD, transaction ID, executor UID, expiry and coordinate-receipt SHA-256.

Search, globbing, environment inference, basename matching and recursive discovery are prohibited. Absence of an exact coordinate is a failure, not permission to look for one.

## Bounded read algorithm

After all authorization, baseline, contract, toolchain and protected-state preflight gates pass, rows are processed in accepted contract order. For each supplied path the future transaction must:

1. require an absolute canonical path;
2. `lstat` every component and reject symlinks;
3. open the final path with `O_RDONLY | O_CLOEXEC | O_NOFOLLOW`;
4. require matching regular-file `lstat` and `fstat` identities;
5. require the authorized UID and reject group/other writable modes;
6. record device, inode, size, mtime and ctime before streaming;
7. stream SHA-256 through the already opened descriptor;
8. re-check the stable identity after streaming;
9. require exact size, digest, ELF64 little-endian AArch64 `ET_DYN` and `DT_SONAME`;
10. require exact result/index/container/member identities;
11. seal a canonical row receipt.

The four accepted atomic families must pass as complete units. One failed or missing row rejects the whole map.

## Output and mutation boundary

The future evidence transaction may write only transaction-scoped logs, temporary row receipts, canonical candidate/failure receipts, protected-state snapshots, the result index and the result archive. These outputs remain outside the generation root and live glibc prefix.

It may not modify provider files, package databases, the live prefix, object storage, generation roots, target paths or selectors. A successful receipt is only a `QUALIFIED_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_CANDIDATE`; separate acceptance and execution decisions remain required.

## Failure and recovery

Eighteen transaction-level failure classes cover authorization, baseline, contract, coordinates, discovery, path safety, file identity, content, ELF/SONAME, supply identity, atomic-family completeness, receipt limits, protected-state invariance and result delivery.

Every failure closes open descriptors, rejects the entire map and writes a canonical failure receipt when possible. Cleanup is restricted to exact transaction temporary evidence files. Provider paths, unknown paths, generation roots and other transaction state are never automatically deleted.

## Decision

```text
QUALIFIED_NON_EXECUTING_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_DESIGN_CANDIDATE
```

This decision grants no path-discovery, provider-byte-read, local-map-production, execution, generation-root, population, materialization, publication, deployment or activation authority.

## Next action

`review-and-accept-read-only-selected-provider-local-supply-map-evidence-transaction-design-boundary`
