# Selected target indexed-replacement and member-size review

## Decision

```text
review:                         INDEXED-REPLACEMENT-MEMBER-SIZE-REVIEW-001
decision:                       INTERVENTION_RETAINED_ALL_COORDINATE_AND_INDEX_GAPS_CLOSED_ONE_MEMBER_SIZE_OPEN
concrete objects:               41
existing digest-bound inputs:   14
v101 indexed replacements:      23
append-only legacy upgrades:     4
coordinate gaps:                 0
result-index gaps:               0
exact member sizes:             40
open member sizes:               1
population authorized:          NO
materializer design authorized: NO
```

## Indexed replacement boundary

Twenty-three formerly blocked bindings are replaced for review purposes by the exact indexed v101 result:

```text
Drive file ID: 1ST696OLuGiBt_lLvJbXOt6EIT0X17Fy9
outer SHA-256: ba0fa0e31cfea2a31f8065ecaccf998a49901c12aa5f62af978728ddd8f10b3a
result-index SHA-256: 9b360f096afd8c464400a211feedc9ab20146b504415658c7a44c04cf6f026a0
```

The indexed result contains exact frozen package archives and member bytes for Fontconfig, FreeType, FriBidi, GLib, libpng, HarfBuzz, libcloudproviders, libdatrie, libepoxy, libiconv, libthai, libXcursor, libxkbcommon, Pango and Xorg family rows. Its successful core transaction, success action, `FAILURE_REASON=none`, package state and loader state are retained. Its outer `TRANSACTION_RC=1` is recorded as a final status-surface defect and is not hidden or reinterpreted as a fully clean envelope.

Four FreeType transitive rows are closed by an append-only file-index receipt over the unchanged historical authority archive. The historical archive is not rewritten. The receipt covers 30 regular files and has SHA-256 `eed95221332a7dd309788b72e651ccb7c40ca91ffe6f7f3ea231433804b787f7`.

These closures are supply-evidence metadata only. They do not authorize downloading, extracting, installing or copying provider bytes.

## Member-size census

Forty exact member sizes are bound to exact member digests. Their sum is:

```text
28,586,192 bytes
```

The 100% margin lower bound before receipt overhead is:

```text
57,172,384 bytes
```

The exact size of `libpixman-1.so.0.46.4` remains open. Package size, archive size or a different Pixman generation cannot substitute for the exact selected member size. Receipt overhead is also not yet censused. Therefore the final resource budget is blocked.

## Intervention decision

Coordinate and result-index gaps are closed, but the population intervention remains in force because one exact member size and receipt-overhead budget remain open. No generation root, staging tree, receipt, selector or target path is created.

## Next action

```text
close-exact-pixman-member-size-and-review-population-intervention-lift-gate
```

That action remains read-only until the exact selected Pixman member size and full budget are verified.
