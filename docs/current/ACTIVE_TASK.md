# Active task: review exact FriBidi provider authority

> Task ID: `review-fribidi-bounded-provider-authority`
>
> Expected state on completion: exact `libfribidi.so.0.4.0` is either accepted for selected Pango/GTK bidirectional-text processing or left open with a precise Class B custom-step, consumer-binding, conflict, update or rollback blocker. No target population, deployment or activation occurs.

## Objective

Review the single-member `gpkg/fribidi` root under ADR 0005 using its exact artifact/member identity, pinned recipe tree, custom Termux step semantics, selected Pango/GTK necessity, consumer binding, conflict/exclusion, update and rollback boundaries.

## Why now

The exact libcloudproviders member is bounded and accepted for selected GTK 3.24.49 PlacesSidebar cloud-account integration, reducing the selected composition gap count from 17 to 16. FriBidi is the smallest remaining reviewed-root, single-member T2 material-delta tranche.

## Known coordinates

```text
root review:    generic-root-review:c38f6cb7aef89fe33a48
recipe root:    gpkg/fribidi
recipe tree:    41ad596c81980f710112cd74d4f1b428cfbc6d6a
artifact:       fribidi-glibc 1.0.16
artifact SHA:   9e99711a88e10441c0eee7af77c64b9ee1a6c93484b0e16ac381ed242057219f
member:         libfribidi.so.0.4.0
member SHA:     71668fd02e89fa7546446bb7961bb618f6d22e1506f7444bbea6788befbb7895
SONAME:         libfribidi.so.0
selected row:   selected:5d210dfa49b6cf4c1077
```

## In scope

- exact member and SONAME identity;
- Class B custom Termux step semantics;
- selected Pango/GTK bidirectional-text necessity and bounded consumer binding;
- conflict, exclusion, update and rollback review.

## Out of scope

- package tools, documentation and development surfaces;
- complete text or GTK composition acceptance;
- target generation, installation, materialization, deployment or activation;
- SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libcloudproviders-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact consumer or custom-step impact cannot be resolved from retained evidence.

## Next valid action

Perform a bounded exact-file recipe and Pango consumer review. Request device execution only if static evidence cannot resolve a material ambiguity.

## Stop conditions

Stop without accepting authority if exact identity, custom-step semantics, consumer binding, conflict/exclusion, update or rollback boundaries cannot be bounded.

## Completion criteria

- Exact artifact, member, SONAME and recipe coordinates remain pinned.
- Class B custom-step semantics are explicit.
- Necessity, consumer binding, conflict/exclusion, update and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population and activation remain separate.
