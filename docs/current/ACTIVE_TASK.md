# Active task: review exact FreeType provider authority

> Task ID: `review-freetype-bounded-provider-authority`
>
> Expected state on completion: exact `libfreetype.so.6.20.2` is either accepted for selected Pango/GTK font rasterization and metrics or left open with a precise Class B custom-step/configuration, consumer-binding, conflict, update or rollback blocker. No target population, deployment or activation occurs.

## Objective

Review the single-member `gpkg/freetype` root under ADR 0005 using its exact artifact/member identity, pinned recipe tree, custom Termux step and configure semantics, selected Pango/GTK necessity, consumer binding, conflict/exclusion, update and rollback boundaries.

## Why now

The exact FriBidi member is bounded and accepted for Pango 1.54.0 core Unicode bidirectional processing, reducing the selected composition gap count from 16 to 15. FreeType is the remaining reviewed-root, single-member T2 material-delta tranche.

## Known coordinates

```text
root review:    generic-root-review:af39bbec812180537c5a
recipe root:    gpkg/freetype
recipe tree:    3a92f7895a8a4ef5cfe33fcc8b806acccffd0313
artifact:       freetype-glibc 2.13.3
artifact SHA:   8e1d9d34f13c6c95aba5e9a5f636facc94e0ca7c073f68cf605858a499a54e7b
member:         libfreetype.so.6.20.2
member SHA:     04723b724b36bd516936461db4ee32a692f15af7abb99cd52cd287afa36118cf
SONAME:         libfreetype.so.6
selected row:   selected:654806f659f7b97ba9d1
```

## In scope

- exact member and SONAME identity;
- Class B custom Termux step and configure semantics;
- selected Pango/GTK font rasterization and metrics necessity and bounded consumer binding;
- conflict, exclusion, update and rollback review.

## Out of scope

- package tools, documentation and development surfaces;
- complete font/text or GTK composition acceptance;
- target generation, installation, materialization, deployment or activation;
- SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/fribidi-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact consumer or custom-step/configuration impact cannot be resolved from retained evidence.

## Next valid action

Perform a bounded exact-file recipe and Pango consumer review. Request device execution only if static evidence cannot resolve a material ambiguity.

## Stop conditions

Stop without accepting authority if exact identity, custom-step/configuration semantics, consumer binding, conflict/exclusion, update or rollback boundaries cannot be bounded.

## Completion criteria

- Exact artifact, member, SONAME and recipe coordinates remain pinned.
- Class B custom-step/configuration semantics are explicit.
- Necessity, consumer binding, conflict/exclusion, update and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population and activation remain separate.
