# Active task: review exact Fontconfig provider authority and filename continuity

> Task ID: `review-fontconfig-bounded-provider-authority`
>
> Expected state on completion: the exact Termux candidate `libfontconfig.so.1.14.0` is either accepted for a bounded selected Pango/GTK font-discovery and matching capability while preserving SONAME `libfontconfig.so.1`, or left open with a precise custom-step, configure, patch, subpackage, prefix, package-revision, concrete-filename drift, consumer-binding, conflict, update, or rollback blocker. No target population, deployment, or activation occurs.

## Objective

Review the single selected member from `gpkg/fontconfig` under ADR 0005, explicitly reconciling the selected concrete label with the retained exact Termux candidate and bounding all recipe adaptation tokens and prefix-dependent policy.

## Why now

Exact HarfBuzz authority is bounded and accepted, reducing selected composition gaps from 13 to 12. Fontconfig is the next single-member reviewed-root tranche and is directly relevant to the accepted Pango/GTK font path.

## Known coordinates

```text
root review:       generic-root-review:26c46ad7612eb40ca721
recipe root:       gpkg/fontconfig
recipe tree:       c5c62dc15d6a897251c88cb7c2306b2a12dd16ba
artifact:          fontconfig-glibc 2.15.0-1
artifact SHA:      c6bc4c9801ee7a45b506d3cc501f1c73a2fe6f1d4b5690eddede158f2b78aafb
selected identity: libfontconfig.so.1.12.1
selected row:      selected:33fe337448a19e2c6f2f
exact candidate:   libfontconfig.so.1.14.0
candidate SHA:     33769b91e5bc82e4453766c957733fecc45cf6d0c696fe52c3cdb4084daa591e
SONAME:            libfontconfig.so.1
```

## In scope

- exact candidate/member digest and SONAME identity;
- custom Termux step, configure arguments, package revision, patch, subpackage, and Termux-prefix semantics;
- concrete filename drift and SONAME-alias continuity;
- selected Pango/GTK font discovery and matching consumer binding;
- configuration/data-path boundary, conflict, exclusion, update, and rollback.

## Out of scope

Font cache/configuration population, system fonts, CLI tools, development surfaces, complete text composition, target generation, installation, materialization, deployment, activation, and SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/harfbuzz-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-recipe-binding-and-drift-target-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact adaptation impact, consumer binding, filename continuity, or configuration-path semantics cannot be resolved from retained evidence.

## Stop conditions

Stop without accepting authority if exact candidate digest, patch/configure/subpackage/prefix semantics, selected identity-to-SONAME continuity, consumer binding, data/configuration boundary, conflict/exclusion, update, or rollback cannot be bounded.

## Next valid action

Perform a bounded exact-file recipe, patch/configure/subpackage/prefix, filename-continuity, and Pango/GTK font consumer review. Request device execution only if retained static evidence cannot resolve a material ambiguity.

## Completion criteria

- Exact artifact, candidate member, SONAME, and recipe coordinates remain pinned.
- Every adaptation token, prefix/data boundary, and concrete-filename continuity rule is explicit.
- Necessity, consumer binding, conflict/exclusion, update, and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population, and activation remain separate.
