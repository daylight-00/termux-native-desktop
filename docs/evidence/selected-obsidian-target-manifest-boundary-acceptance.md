# Selected Obsidian target manifest boundary acceptance

## Decision

```text
acceptance id:                 SELECTED-TARGET-MANIFEST-ACCEPT-001
decision:                      ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_TARGET_MANIFEST
candidate review:              SELECTED-TARGET-MANIFEST-REVIEW-001
accepted target rows:          82
regular / SONAME alias rows:   41 / 41
unique paths:                  82
collisions / unresolved alias: 0 / 0
population state:              UNPOPULATED_SCHEMA_ONLY
target population authorized: NO
materializer design authorized:NO
deployment / activation:       NO / NO
```

The exact five-file v105 candidate is accepted as a bounded Class D target-policy decision. The review artifacts remain immutable evidence and therefore retain their candidate-time `TARGET-MANIFEST-ACCEPTANCE-OPEN` and `PROVISIONAL_BLOCKED` fields. This separate acceptance record closes that candidate issue without rewriting the frozen review rows.

## Frozen candidate digests

```text
selected-target-manifest.tsv
1ec7f427599437bc0fc22df6ff171294a490296ef900f490b8c36f86c00ee63b

selected-target-manifest-object-bindings.tsv
719484decceadd38d0c0a76c336d838f98f672eb6e27e26ad96143e54767ce60

selected-target-manifest-alias-bindings.tsv
39bbac0376e31b0b792fc6c3af044e620472128337b2d06683e6d57846a2383b

selected-target-manifest-collisions.tsv
5bb3a842bc757e66a903db8ab7e95599a4a77bc7c2266cfb8bee4f86f5c8cad8

selected-target-manifest-metadata.tsv
1cfb289a7355945160184ba0a527f3c2d13682e9fc2157b21ce507baf2e79a09
```

The accepted overlay state is `ACCEPTED_BOUNDED_TARGET_POLICY`. All 82 rows remain `UNPOPULATED_SCHEMA_ONLY`. No directory, regular file or symlink is created.

## Remaining gates

```text
TARGET-POPULATION-INTERVENTION-LIFT-OPEN
SUPPLY-BYTE-BINDING-OPEN
```

Before materializer design, a separate review must prove that intervention lift is justified and that every concrete object can be bound to retained, immutable, independently verified supply bytes and exact archive member paths. The two gates are conjunctive; closing either one alone does not authorize implementation.

## Exclusions

This acceptance does not authorize byte acquisition, extraction, copy, installation, target-directory creation, symlink creation, supply artifact binding, loader-search policy, population order, materialization, immutable generation creation, deployment, display/service execution, module or schema registration, cache generation or activation.

## Update and rollback

Any target path, node policy, alias relation, object binding digest, atomic-family relation, composition or capability change requires a new Class D target-policy review. Before population the acceptance can be revoked directly. Any later rollback must select a prior immutable whole generation and preserve atomic families.

## Next action

```text
review-target-population-intervention-lift-and-supply-byte-binding-boundary
```

That review is non-mutating and does not itself authorize materializer implementation or population.


## Current intervention disposition

`TARGET-POPULATION-INTERVENTION-SUPPLY-REVIEW-001` reviewed the two open gates and retained the intervention. Fourteen concrete objects have qualified read-only retained-result binding inputs; twenty-seven lack retained result coordinates. Generation-root, atomic publication, resource, verification-receipt, rollback-selector and failure-observability prerequisites also remain open. No population or materializer-design authority is created.
