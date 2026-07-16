# Active task: review exact libthai provider authority

> Task ID: `review-libthai-bounded-provider-authority`
>
> Expected state on completion: exact `libthai.so.0.3.1` is either accepted for the selected GTK/Pango Thai text capability or left open with a precise Class B `BUILD_IN_SRC`, dependency, data-binding, or consumer blocker. No target population, deployment or activation occurs.

## Objective

Review the single-member `gpkg/libthai` root under ADR 0005 using its exact artifact/member identity, pinned recipe tree, `BUILD_IN_SRC` semantics, selected Pango/GTK necessity, dependency and data binding, conflict/exclusion, update and rollback boundaries.

## Why now

The exact `libXcursor.so.1.0.2` provider is bounded and accepted for GTK 3.24.49 X11 cursor handling, reducing the selected composition gap count from 20 to 19. `libthai` is the next smallest reviewed-root, single-member GTK text gap.

## Known coordinates

```text
root review:    generic-root-review:88cec59d1ec77cd9f7bd
recipe root:    gpkg/libthai
recipe tree:    4943c66ff96eeddc0d6d05a57fb24418fb0cd7d2
artifact:       libthai-glibc 0.1.29
artifact SHA:   5aa1d090525e71302abf48532d522049c59f6aae76880b558558ea97b2c73cd8
member:         libthai.so.0.3.1
member SHA:     773a629e30546b57d650d9d991d18c64490ef5cf53062fec1e02c69ece66bf9c
SONAME:         libthai.so.0
selected row:   selected:fec77ea4c45ec1a2990d
```

## In scope

- exact member and SONAME identity;
- Class B `BUILD_IN_SRC` configuration/packaging semantics;
- selected Pango/GTK Thai shaping necessity and bounded consumer binding;
- `libdatrie` and any runtime data dependency boundary;
- conflict, exclusion, update and rollback review.

## Out of scope

- other libthai package surfaces or command-line utilities;
- complete text-stack or GTK composition acceptance;
- target generation, installation, materialization, deployment or activation;
- SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libxcursor-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact consumer, data, or dependency binding cannot be resolved from retained evidence.

## Next valid action

Perform a bounded exact-file recipe and provider review. Request device execution only if static evidence cannot resolve a material ambiguity.

## Stop conditions

Stop without accepting authority if exact identity, `BUILD_IN_SRC` semantics, dependency/data binding, selected necessity, collision/exclusion, update or rollback boundaries cannot be bounded.

## Completion criteria

- Exact artifact, member, SONAME and recipe coordinates remain pinned.
- Class B configuration/packaging semantics are explicit.
- Necessity, consumer/data/dependency binding, conflict/exclusion, update and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population and activation remain separate.
