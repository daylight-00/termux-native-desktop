# Active task: review exact libxkbcommon provider authority and filename continuity

> Task ID: `review-libxkbcommon-bounded-provider-authority`
>
> Expected state on completion: the exact Termux candidate `libxkbcommon.so.0.8.0` is either accepted for the selected GTK XKB keyboard/keymap capability while preserving SONAME `libxkbcommon.so.0`, or left open with a precise custom-step, concrete-filename drift, consumer-binding, conflict, update, or rollback blocker. No target population, deployment, or activation occurs.

## Objective

Review the single-member `gpkg/libxkbcommon` root under ADR 0005, explicitly reconciling the selected/oracle concrete label with the retained exact Termux candidate filename.

## Why now

FreeType and its exact compression-feature closure are bounded and accepted, reducing selected composition gaps from 15 to 14. libxkbcommon is the smallest remaining reviewed-root, single-member Class B tranche.

## Known coordinates

```text
root review:       generic-root-review:778b62f6da21fd02f1bb
recipe root:       gpkg/libxkbcommon
recipe tree:       5fda5da07e6b38230082785d352adc4e6fb9c4da
artifact:          libxkbcommon-glibc 1.8.0
artifact SHA:      e58eca6f9c0e0d068d80dabd3b289d6b1b4cdaa25fc91053d21392ecfbf54f97
selected identity: libxkbcommon.so.0.0.0
selected row:      selected:0eab80f8c75b58f5c92a
exact candidate:   libxkbcommon.so.0.8.0
SONAME:            libxkbcommon.so.0
```

## In scope

- exact candidate/member digest and SONAME identity;
- Class B custom Termux step semantics;
- concrete filename drift and SONAME-alias continuity;
- selected GTK XKB keymap/keyboard consumer binding;
- conflict, exclusion, update, and rollback boundaries.

## Out of scope

Package tools, development surfaces, complete input/GTK composition, target generation, installation, materialization, deployment, activation, and SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/freetype-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact consumer or filename-continuity impact cannot be resolved from retained evidence.

## Stop conditions

Stop without accepting authority if exact candidate digest, custom-step semantics, selected identity-to-SONAME continuity, consumer binding, conflict/exclusion, update, or rollback cannot be bounded.

## Next valid action

Perform a bounded exact-file recipe, filename-continuity, and GTK XKB consumer review. Request device execution only if retained static evidence cannot resolve a material ambiguity.

## Completion criteria

- Exact artifact, candidate member, SONAME, and recipe coordinates remain pinned.
- Custom-step semantics and concrete-filename continuity are explicit.
- Necessity, consumer binding, conflict/exclusion, update, and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population, and activation remain separate.
