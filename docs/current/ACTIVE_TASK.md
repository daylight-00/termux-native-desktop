# Active task: review the atomic AT-SPI2/ATK 2.56.2 candidate for bounded provider authority

> Task ID: `review-at-spi2-core-2-56-2-atomic-candidate-bounded-provider-authority`
>
> Expected state on completion: one explicit bounded decision either accepts all three exact local Class C members as one atomic provider family for a narrowly stated selected GTK accessibility capability, or rejects/defers authority with a precise capability, consumer-binding, dependency, collision, service-lifecycle, update, or rollback blocker. No supplier publication, installation, target population, D-Bus activation, accessibility enablement, deployment, or selected-generation activation occurs.

## Objective

Review the frozen Class B recipe and Class C `at-spi2-core-glibc 2.56.2` package/member family without rebuilding or widening it. Decide whether the exact three-member family has bounded provider authority for the selected GTK accessibility linkage while preserving all service and activation boundaries.

## Why now

The candidate-preparation lane completed with exact package, member, GIR, disabled-service, and protected-state evidence. ADR 0005 requires a separate provider-authority decision before any selected composition effect, so review must occur now without rebuilding or treating successful production as authority.

## Frozen candidate coordinates

```text
result archive: 461b24dac879ca71252c209f0013ff17cb8f8ed1a889a32f0376b87372f3d3a4
evidence freeze: b516ed70c10b6bf91fac08e2a461dc55e9f2b5337a4dade5b995e96fa5b4b40d
recipe:         6f727204730b6b0a3496c169f635c5016903cb64b816b7c84ca91fcbc9d4e30d
package:        9a1395e893448508cfb8fbdee8ef0dd8268b8d21e9ac7bbe792f163dce6c365a
member family:  libatk-1.0.so.0.25611.1
                libatk-bridge-2.0.so.0.0.0
                libatspi.so.0.0.1
```

## In scope

- verify exact capability necessity and GTK consumer bindings for all three members;
- preserve atomic update and rollback of package, aliases, GIR/typelib files, and disabled activation metadata;
- review exact direct dependencies including the bounded `gcc-libs-glibc` exception-runtime relation;
- verify collision and exclusion boundaries against accepted providers and wrong-world bytes;
- decide whether helper executables and disabled metadata remain package content only, with no service authority;
- record one machine-readable bounded provider decision or precise blocker.

## Out of scope

Recipe redesign, rebuilding, accepting only one or two members, supplier publication, package installation, active D-Bus service files, bus ownership, registry-daemon acceptance, accessibility enablement, target layout, materialization, deployment, or activation.

## Required reading

- `docs/evidence/at-spi2-core-production-recipe-candidate-result-review.md`
- `docs/evidence/at-spi2-core-provider-evidence-blocker.md`
- `docs/evidence/missing-glibc-provider-production-boundary.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None. The exact result archive and compact evidence freeze are already retained; this task is a bounded repository review of those frozen coordinates.

## Completion criteria

The decision binds the exact package, all three member and SONAME identities, capability/consumer scope, dependency closure, GIR relation, seven-file disabled activation namespace, helper non-execution boundary, collision/exclusion state, coordinated update and rollback, and explicit prohibited inference. Candidate qualification alone is not sufficient.

## Stop conditions

Stop without authority if one member can be updated independently, a selected consumer edge is absent or ambiguous, required runtime providers are not accepted or exactly bounded, any active service lifecycle is necessary for library validation, collision/exclusion cannot be bounded, or rollback cannot revoke the whole family coherently.

## Next valid action

Prepare the narrative and machine-readable bounded provider-authority review from the frozen evidence. Do not rebuild, install, restore activation metadata, start services, or widen into GTK 3 core.
