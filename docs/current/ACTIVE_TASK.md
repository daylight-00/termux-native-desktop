# Active task: review exact HarfBuzz provider authority and filename continuity

> Task ID: `review-harfbuzz-bounded-provider-authority`
>
> Expected state on completion: the exact Termux candidate `libharfbuzz.so.0.61010.0` is either accepted for a bounded selected Pango/GTK shaping capability while preserving SONAME `libharfbuzz.so.0`, or left open with a precise patch, configure, subpackage, concrete-filename drift, consumer-binding, conflict, update, or rollback blocker. No target population, deployment, or activation occurs.

## Objective

Review the single selected member from `gpkg/harfbuzz` under ADR 0005, explicitly reconciling the selected concrete label with the retained exact Termux candidate and bounding all recipe adaptation tokens.

## Why now

Exact libxkbcommon authority is bounded and accepted, reducing selected composition gaps from 14 to 13. HarfBuzz is the next single-member reviewed-root tranche, but it has a broader Class B adaptation surface than libxkbcommon.

## Known coordinates

```text
root review:       generic-root-review:706bd01fdd0555fcabc9
recipe root:       gpkg/harfbuzz
recipe tree:       f353d5f116250f7bcab7ecf062cdb13728b0ecc8
artifact:          harfbuzz-glibc 10.1.0
artifact SHA:      d0e4a83180560341dc02fccd3b2df1892338a84c4cecfa4c7f6bc1c2566eacfc
selected identity: libharfbuzz.so.0.61020.0
selected row:      selected:c41cd8cc82847fba1410
exact candidate:   libharfbuzz.so.0.61010.0
candidate SHA:     179133d6e95f6e378f44ad9222255620ecdd39c30c5aedce028d99f2b28470c6
SONAME:            libharfbuzz.so.0
```

## In scope

- exact candidate/member digest and SONAME identity;
- custom Termux step, extra configure arguments, patch, and subpackage semantics;
- concrete filename drift and SONAME-alias continuity;
- selected Pango/GTK shaping consumer binding;
- conflict, exclusion, update, and rollback boundaries.

## Out of scope

Sibling HarfBuzz libraries and tools, complete text composition, target generation, installation, materialization, deployment, activation, and SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libxkbcommon-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact adaptation impact, consumer binding, or filename continuity cannot be resolved from retained evidence.

## Stop conditions

Stop without accepting authority if exact candidate digest, patch/configure/subpackage semantics, selected identity-to-SONAME continuity, consumer binding, conflict/exclusion, update, or rollback cannot be bounded.

## Next valid action

Perform a bounded exact-file recipe, patch/configure/subpackage, filename-continuity, and Pango/GTK shaping consumer review. Request device execution only if retained static evidence cannot resolve a material ambiguity.

## Completion criteria

- Exact artifact, candidate member, SONAME, and recipe coordinates remain pinned.
- Every adaptation token and concrete-filename continuity rule is explicit.
- Necessity, consumer binding, conflict/exclusion, update, and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population, and activation remain separate.
