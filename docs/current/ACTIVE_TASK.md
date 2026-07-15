# Active task: review Pango provider authority and concrete-filename drift

> Task ID: `review-pango-reference-consumed-provider-authority-and-concrete-filename-drift`
>
> Expected state on completion: `gpkg/pango` has a bounded provider decision and an explicit CF-001–CF-004 continuity policy, or a precise remaining gap; no complete composition, target population, materialization, or activation is implied.

## Objective

Review the final no-token Class A root:

```text
gpkg/pango
```

Separate provider capability from concrete-filename continuity. Decide whether the observed SONAME aliases and drifted concrete members can support the selected GTK 3.24.49 text stack without treating an alias observation as target-path authority.

## Why now

Six no-token roots now have bounded provider authority: four X.Org providers, `libtasn1`, and `libepoxy`. Pango is the remaining no-token root and the only one with unresolved concrete-filename drift.

## Current accepted decisions

- All seven no-token recipes are Class A for package-specific adaptation.
- Six exact provider decisions are bounded to named consumer capabilities.
- `libepoxy.so.0` is accepted only for GTK 3.24.49 X11 GLX dispatch; EGL is not claimed.
- Pango provider authority and CF-001–CF-004 remain open.
- Composition, target population, materialization, activation, and blanket SUP-02 execution remain blocked.

## In scope

- Review `pango-glibc` 1.54.0 and its exact artifact identity.
- Review observed SONAME aliases and drifted concrete filenames for `libpango`, `libpangoft2`, and `libpangocairo`.
- Bind required capabilities to GTK 3.24.49, Cairo, Fontconfig, FreeType, HarfBuzz, Fribidi, and Xft only as supported by existing evidence.
- Decide CF-001 alias necessity, CF-002 successor selection, CF-003 update boundary, and CF-004 rollback continuity.
- Define conflict and exclusion rules without choosing target paths or materializing files.
- Request a bounded Termux analyzer only when exact target ELF identity or consumer binding cannot be resolved from retained evidence.

## Out of scope

- Complete GTK/application runtime composition.
- Provider extraction, target paths, copying, installation, or alias creation.
- Runtime launch, selector mutation, deployment, or activation.
- Reconstructing the supplier producing build without a recorded Class C escalation.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/provider-claim-classification.md`
- `docs/evidence/no-token-recipe-semantic-review.md`
- `docs/evidence/libepoxy-reference-consumed-provider-authority.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-recipe-binding-and-drift-target-receipt-review.tsv`

Do not load historical handoff or refactor records by default.

## Known facts

```text
root review: generic-root-review:0dacddae106c6bd1006b
recipe tree: f9e9e2303e2c91322f7edcf1bc0c3b99f2d1d74a
artifact: pango-glibc 1.54.0
semantic: CONFIRMED_A
observed state: expected SONAME aliases present, concrete filenames drifted
open issues: CF-001;CF-002;CF-003;CF-004
```

## Pending external inputs

None at task start. Use the registered web-chat stop-loss and create a one-command Termux analyzer only for a named unresolved ELF or consumer-binding fact.

## Next valid action

Construct a canonical Pango review surface that separates exact artifact/member evidence, SONAME alias continuity, provider capability, successor policy, update boundary, rollback, and prohibited inference.

## Stop conditions

Stop without accepting provider authority if:

- alias targets cannot be bound to exact ELF members and SONAMEs;
- multiple non-equivalent successors remain unresolved;
- consumer binding is inferred only from package-wide presence;
- the decision would choose target paths, create aliases, materialize files, or authorize activation.

## Completion criteria

- canonical Pango provider and drift-policy rows exist;
- CF-001–CF-004 each have an explicit disposition or remaining gap;
- generated claims reproduce deterministically;
- negative tests reject alias drift and authority broadening;
- current state advances beyond the no-token provider tranche;
- repository and runtime remain unchanged outside review metadata and tests.
