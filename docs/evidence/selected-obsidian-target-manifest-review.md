# Selected Obsidian non-mutating target manifest review

## Decision

```text
review id:                       SELECTED-TARGET-MANIFEST-REVIEW-001
decision:                        QUALIFIED_NON_MUTATING_SELECTED_TARGET_MANIFEST
accepted composition:            SELECTED-COMPOSITION-ACCEPT-001
composition decision rows:       42
included concrete members:       41
deferred members:                 1
regular target rows:             41
SONAME alias target rows:        41
total proposed target rows:      82
unique target paths:             82
target-path collisions:           0
unresolved aliases:               0
target population authorized:    NO
materialization authorized:      NO
deployment authorized:           NO
activation authorized:           NO
```

The accepted bounded composition is translated deterministically into a dry-run target manifest under the existing 20-field target-layout schema. The manifest is a reviewed candidate only. It creates no files, directories, symlinks, package state, loader state, generation, selector, service, module, schema, cache or activation state.

## Proposed layout policy

All 41 included concrete ELF members are proposed in one semantic domain:

```text
target domain:        SHARED_PROVIDER
target relative root: lib
concrete node type:   REGULAR
concrete mode policy: IMMUTABLE_READONLY
owner policy:         PROVIDER_OWNER
mutability:           IMMUTABLE
collision policy:     ERROR
update domain:        GENERIC_PROVIDER_UPDATE
rollback domain:      PROVIDER
```

Each exact concrete member is proposed as `lib/<member_basename>`. Each accepted SONAME runtime alias is proposed as `lib/<soname>` and resolves only to its matching concrete row. Alias destinations are retained in `selected-target-manifest-alias-bindings.tsv` because the base target-layout schema models node policy but does not contain a symlink-target column.

The deterministic row order is review order only. It is not extraction order, copy order, package installation order, dynamic-loader search order, activation order or rollback execution order.

## Object-reference boundary

`selected-target-manifest-object-bindings.tsv` gives each included member a stable content-addressed `object:<first-24-SHA256>` identifier and binds it to the exact accepted composition row, provider review, recipe coordinate, artifact package/version, member basename, full member SHA-256 and SONAME.

These composition-local bindings are target-review references only. They do not publish a package-wide provider, assert a clean-acquisition contract, create a supply artifact, replace historical registry evidence, or authorize extraction. Supply artifact identifiers and archive member paths remain unset in the proposed target rows; any later materializer must bind retained bytes independently before population can be accepted.

## Alias and collision review

The 41 SONAME aliases are represented as separate `SYMLINK` rows with `SONAME_RUNTIME_ALIAS`. Every alias companion row:

- resolves to one included concrete target row;
- has an alias basename equal to the accepted SONAME;
- has an alias target basename equal to the exact accepted concrete member;
- remains `PROVISIONAL_BLOCKED` and `UNPOPULATED_SCHEMA_ONLY`;
- creates no symlink in this transaction.

The collision table contains only its header. All 82 proposed relative paths are unique. Silent last-writer-wins and declared overrides are absent.

## Atomic-family review

The manifest contains complete proposed concrete and alias rows for each accepted atomic family:

```text
AT-SPI2 / ATK: 3 concrete + 3 aliases
Cairo:         2 concrete + 2 aliases
Pango:         3 concrete + 3 aliases
GDK / GTK:     2 concrete + 2 aliases
```

No family is partially represented. This does not choose population order; future population and rollback must still operate on accepted immutable whole generations with family atomicity preserved.

## Deferred and excluded scope

`libtasn1.so.6.6.4 -> libtasn1.so.6` remains absent from the current target candidate because its GnuTLS security or printing profile is deferred. The manifest also excludes development aliases, headers, pkg-config, static libraries, tools, helpers, `broadwayd`, modules, print backends, schemas, services, data, font population, pixbuf modules/cache, GIR/typelib target membership, generated caches and mutable state.

## Population boundary

Every proposed row has:

```text
authority acceptance state: PROVISIONAL_BLOCKED
authority issue id:         TARGET-MANIFEST-ACCEPTANCE-OPEN
population state:           UNPOPULATED_SCHEMA_ONLY
```

Therefore this review does not lift the target-population intervention. A separate Class D acceptance transaction must review and accept the exact manifest digests before any intervention-lift, supply-byte binding, materializer design, target population or activation work.

## Next action

```text
review-and-accept-non-mutating-selected-target-manifest-boundary
```

That transaction may accept the exact reviewed target rows and companion relations as target policy. It may not copy, install, populate, materialize, deploy or activate anything.
