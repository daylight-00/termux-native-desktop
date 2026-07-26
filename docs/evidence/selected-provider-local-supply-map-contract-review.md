# Selected-provider local-supply-map contract review

## Decision

```text
review id:                      SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-REVIEW-001
decision:                       QUALIFIED_NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_CANDIDATE
contract rows:                  41
validation rules:               24
populated local paths:           0
contract acceptance:            OPEN
actual local supply map:         NOT PRODUCED
execution authorized:            NO
```

The accepted non-executing materializer design requires one future local regular-file evidence row for each of its 41 object-plan rows. This review defines that interface without searching storage, reading a provider byte, choosing a path or producing a map.

## Exact immutable identity

Every contract row freezes the accepted materializer plan identity:

- materializer plan row and provider object;
- provider review, package and version;
- exact member basename, size, SHA-256 and SONAME;
- retained-result remote or accepted digest sentinel;
- Drive file ID when one exists;
- result outer SHA-256;
- exact result-index SHA, append-only receipt SHA or existing-authority digest sentinel;
- container class and exact container/member locator;
- future content-addressed object and generation regular/alias paths.

The index split remains exact:

```text
v101 result-index SHA rows:            23
append-only legacy index receipt rows:  4
existing-authority digest rows:        14
```

No basename lookup, recursive search, glob, environment-variable expansion or path guessing may replace an exact locator.

## Future local path contract

The candidate contains an empty `local_regular_file_path` field in all 41 rows. A later separately authorized read-only localization receipt must provide one absolute canonical path per row.

A future path is acceptable only when all of the following hold:

1. every path component is checked with `lstat` and no component is a symlink;
2. the final open is read-only with close-on-exec and no-follow semantics;
3. `lstat` and `fstat` both identify a regular file;
4. the owner UID equals the localization transaction UID;
5. group-write and other-write mode bits are clear;
6. device, inode, size, mtime and ctime stay unchanged before open, after open and after hashing;
7. exact size and streamed SHA-256 match the contract;
8. the object is ELF64 little-endian AArch64 `ET_DYN` with the exact `DT_SONAME`.

A path may not be discovered by scanning local storage. It must be supplied by a later bounded localization receipt whose own authority is separately reviewed.

## Receipt schema

`selected-provider-local-supply-map-receipt-schema.json` defines canonical compact UTF-8 JSON. The candidate receipt contains zero rows and has no path or byte authority. A future receipt must contain exactly 41 unique contract rows, bind all exact result/index/container/member identities, record stable file metadata and content verification, and include complete results for all four atomic families.

Any failed row rejects the whole map. Partial-map acceptance is prohibited.

## Authority boundary

This review qualifies only a non-mutating contract candidate. It does not authorize:

- local path discovery or search;
- opening or reading provider files;
- downloading retained results;
- archive or package extraction;
- generation-root or object-store creation;
- hardlinks, symlinks, receipts or selectors;
- materializer execution;
- target population, publication, deployment or activation.

## Next action

```text
review-and-accept-non-mutating-selected-provider-local-supply-map-contract-boundary
```

The next transaction may accept the exact contract artifacts. It still may not produce a local map or authorize execution.
