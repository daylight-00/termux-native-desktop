# Selected-provider materializer and runtime-preflight design review

## Decision

```text
design review id:          SELECTED-PROVIDER-MATERIALIZER-DESIGN-REVIEW-001
candidate state:           QUALIFIED_NON_EXECUTING_READ_ONLY_DESIGN_CANDIDATE
acceptance state:          OPEN_SEPARATE_ACCEPTANCE_REQUIRED
target policy rows:        82
regular objects / aliases: 41 / 41
exact member bytes:        29,047,112
receipt reservation:       1,048,576
runtime free-space gate:   59,142,800
execution authorized:      NO
population authorized:     NO
```

The accepted target policy, indexed supply evidence, complete member-size census, deterministic receipt reservation and seven generation contracts are sufficient to qualify a **design candidate**. They are not sufficient to execute it. This review creates no program that can acquire, extract, copy, link, populate or publish provider bytes.

The exact generated design is locked by:

```text
selected-target-materializer-runtime-preflight-design.json
SHA-256: 323d834e58397364561a4b89f4b344a9633e4f3c472728e75e5b620017db44be
bytes:   195,029
```

## Exact per-object plan

`selected-target-materializer-object-plan.tsv` contains 41 deterministic rows. Each row binds:

- the accepted composition row and provider object;
- package, version, exact concrete member SHA-256, size and SONAME;
- one regular generation path and one relative SONAME alias path;
- the accepted supply-evidence closure kind and immutable result/index identity;
- the future content-addressed object path;
- the accepted atomic-family boundary;
- an explicit future local-supply localization requirement.

The content-addressed path contract is:

```text
objects/sha256/<first-two-hex>/<full-member-sha256>
```

A future generation uses the accepted target-relative path directly beneath:

```text
generations/<generation-id>/
```

No object-store path, generation path, regular file or alias is created by this review.

## Input boundary

Thirteen canonical input surfaces are SHA-locked before any future execution:

1. selected composition members;
2. composition acceptance;
3. 82-row target manifest;
4. 41 object bindings;
5. 41 alias bindings;
6. target-policy acceptance;
7. 41-row indexed supply closure;
8. historical 40-plus-one size census;
9. exact Pixman size evidence;
10. final resource budget;
11. seven generation contracts;
12. ten design-only intervention prerequisites;
13. the canonical verification-receipt prototype.

The materializer design consumes only an immutable authority snapshot derived from those digests. Drift in any source is a pre-mutation abort.

## Supply localization interface

The design deliberately does not download provider or result archives. A future, separately authorized localization transaction must supply a 41-row read-only map binding each plan row to:

- a local regular file reached without following symlinks;
- exact outer result SHA-256;
- accepted result-index or append-only index identity;
- exact container decoder class;
- exact artifact and member locator;
- the already accepted member SHA-256 and size.

No whole-archive extraction is permitted. The future materializer may stream only the exact selected member into a transaction-scoped object temporary file. Absence of a complete localization receipt is a hard preflight failure, not acquisition authority.

## Identity and transaction model

```text
generation_id = SHA256(canonical authority snapshot JSON)
transaction_id = SHA256(generation_id NUL execution_authorization_id)
```

Both identifiers use the full 64 hexadecimal characters. The execution authorization ID does not exist yet. It must be created by a later explicit authority decision that binds the accepted design digest and the exact permitted effects.

The current design state stops before that gate:

```text
MAT-S00 DESIGN_CANDIDATE_QUALIFIED
MAT-S01 DESIGN_ACCEPTANCE_REQUIRED
MAT-S02 EXECUTION_AUTHORIZATION_REQUIRED
```

States after `MAT-S02` are future contracts only.

## Content-addressed object handling

For each of the 41 objects, the future design requires this order:

1. open an exact transaction-scoped temporary object with `O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`;
2. stream only the exact selected archive member;
3. enforce the accepted size limit while streaming;
4. verify SHA-256, ELF64, little-endian, AArch64, `ET_DYN`, SONAME, RPATH/RUNPATH and `DT_NEEDED` evidence;
5. change the verified object to immutable mode `0444` with no set-ID or world-write bits;
6. fsync the object;
7. rename it without replacement to its content-addressed path;
8. fsync the object-store parent.

An existing final object may be reused only after the same complete verification. A mismatching object at the expected digest path is store corruption and aborts the transaction. It is never overwritten or repaired in place.

## Generation assembly order

Generation construction is deliberately ordered:

```text
all 41 objects verified
→ staging generation directories
→ all 41 regular hardlinks
→ four atomic-family barriers
→ all 41 relative SONAME aliases
→ whole-generation verification
→ canonical receipt and result index
→ tree seal and fsync
→ immutable generation rename
→ receipt publication
→ previous selector
→ current selector
```

Regular generation files are hardlinks from the verified content-addressed store. Copy fallback is prohibited. Failure to support same-device hardlinks is a preflight blocker and requires a new design review.

The four accepted atomic families are preserved as all-or-none barriers:

```text
AT-SPI2 / ATK: 3
Cairo:         2
Pango:         3
GDK / GTK:     2
```

Aliases are created only after all regular objects and all atomic-family barriers pass. Every alias target is a relative basename within the generation `lib` directory; absolute targets and `..` components are rejected.

## Runtime preflight contract

Twenty runtime checks are defined but not run. They require, among other things:

- a separate execution-authorization token;
- the exact absolute generation base;
- no overlap with `$PREFIX`, `$HOME/gl`, the repository, package databases or the live glibc prefix;
- component-by-component `lstat` with no symlink ancestors;
- current-user ownership and exact mode policy;
- one filesystem device for object store, staging, generations, receipts, locks and selectors;
- at least `59,142,800` available bytes;
- hardlink and atomic no-replace rename capability;
- one exclusive no-follow lock;
- a complete 41-row local supply map;
- exact result, index and member locators;
- 82 target rows, zero collisions and four complete atomic families;
- a canonical receipt not exceeding the 1 MiB reservation;
- valid relative `current` and `previous` selectors;
- an orphan report and protected-state pre-snapshot.

A preflight contract is not a preflight pass. No check in this review touches the proposed runtime root.

## Verification order

Eighteen publication-blocking verification rows cover:

- authority-snapshot and design-digest identity;
- result archive and index identity;
- exact member locator;
- member size and SHA-256;
- ELF machine/type and SONAME;
- RPATH/RUNPATH and `DT_NEEDED` capture;
- canonical glibc-loader resolution with no `$HOME/gl`, Bionic or package-database mapping;
- content-addressed object identity;
- 41 regular hardlinks and 41 aliases;
- zero unexpected nodes or collisions;
- atomic-family completeness;
- immutable owner/mode policy;
- canonical receipt serialization and result index;
- generation and selector publication fields.

Any failure blocks the next publication boundary and preserves a transaction-scoped failure record.

## Receipt and space boundary

The accepted receipt prototype remains the field contract. Runtime serialization must be canonical UTF-8 JSON with sorted keys and one trailing newline.

```text
exact member bytes:       29,047,112
100% member margin:       29,047,112
receipt reservation:       1,048,576
required free bytes:      59,142,800
```

A receipt exceeding `1,048,576` bytes aborts before generation publication. The reservation may not be silently raised at runtime.

## Publication, rollback and recovery

A sealed generation is renamed without replacement into `generations/<generation-id>` only after bottom-up fsync of the tree and its parent. Its receipt is published separately before any selector change.

Selector ordering is:

1. publish `previous` as a relative symlink to the prior verified `current` target;
2. fsync the selector parent;
3. publish `current` as a relative symlink to the new verified generation;
4. fsync the selector parent again.

A crash between the two selector operations leaves `current` on a complete prior generation. Rollback requires both selector targets and both receipts to verify and is itself a separately authorized operation.

Resume is allowed only for the exact transaction ID when its journal binds the same design, authority snapshot, generation ID, execution authorization and local supply map. Unknown staging trees, temporary selectors and unselected complete generations are reported, not automatically deleted. No cleanup operation may touch another transaction, package database, live prefix or immutable generation.

## No implementation or execution authority

The following remain `NO`:

```text
execution authorization
target population
provider-byte acquisition
generation-root creation
object-store write
generation materialization
receipt publication
selector publication
deployment
activation
```

The generated recipe is a deterministic **review-artifact generator**, not a materializer. It writes only repository review files when invoked by repository maintainers.

## Candidate disposition

```text
candidate: QUALIFIED_NON_EXECUTING_READ_ONLY_DESIGN_CANDIDATE
acceptance: OPEN_SEPARATE_ACCEPTANCE_REQUIRED
```

A separate acceptance transaction must verify the exact nine generated design artifacts and decide whether this design boundary is accepted. Even acceptance must not authorize execution or population.

## Next action

```text
review-and-accept-read-only-selected-provider-materializer-runtime-preflight-design-boundary
```
