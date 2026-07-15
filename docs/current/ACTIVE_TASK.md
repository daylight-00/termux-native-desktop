# Active task: review the libepoxy reference-consumed provider root

> Task ID: `review-libepoxy-reference-consumed-provider-authority`
>
> Expected state on completion: `gpkg/libepoxy` has a bounded provider-authority decision or an explicit remaining gap; no composition, target membership, materialization, or activation is implied.

## Objective

Review provider authority for the exact Class A root:

```text
gpkg/libepoxy
```

Determine whether its exact Termux member is necessary and suitable as the selected GL dispatch provider for the bounded GTK 3.24.49 capability. Keep artifact identity, recipe semantics, provider authority, composition, target population, and activation as separate decisions.

## Why now

Five no-token roots now have bounded provider authority: four X.Org providers for the selected GTK X11 scope and `libtasn1` for the exact external GnuTLS 3.8.9 ASN.1/security scope. `libepoxy` is the next no-token root without concrete-filename drift, but its upstream GLX/EGL/X11 feature selection is environment-sensitive and must be bounded explicitly.

## Current accepted decisions

- All seven no-token recipes are Class A for package-specific adaptation.
- `libxfixes`, `libxcomposite`, `libxi`, and `libxinerama` have bounded provider authority for exact members and selected GTK X11 capabilities.
- `libtasn1` has bounded provider authority for its exact member and the selected external GnuTLS 3.8.9 ASN.1/security capability.
- None of those decisions implies complete composition, target membership, materialization, or activation.
- `libepoxy` artifact/member identity and recipe semantics are accepted only as inputs; provider authority remains open.
- Pango filename drift and provider authority remain open and are excluded from this tranche.
- No SUP-02 request is currently required.

## In scope

- Review exact artifact `libepoxy-glibc` 1.5.10.
- Bind exact member `libepoxy.so.0.0.0`, its digest, and SONAME `libepoxy.so.0`.
- Determine the selected GTK 3.24.49 GL dispatch consumer binding.
- Bound upstream GLX, EGL, and X11 auto-selection to the actual selected supplier contract.
- Review dynamic candidates, conflicts, and explicit exclusions.
- Define update and rollback triggers.
- Use targeted passive artifact observation only if the existing recipe/upstream/consumer evidence cannot resolve a material feature ambiguity.

## Out of scope

- Pango concrete-filename drift or provider decision.
- Complete graphics or application composition.
- Provider target paths, aliases, extraction, copying, or installation.
- Runtime launch, selector mutation, deployment, or activation.
- Blanket producing-build provenance or SUP-02 execution.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/provider-claim-classification.md`
- `docs/evidence/no-token-recipe-semantic-review.md`
- `docs/evidence/xorg-reference-consumed-provider-authority.md`
- `docs/evidence/libtasn1-reference-consumed-provider-authority.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

Do not read historical refactor or handoff records by default.

## Known facts

```text
root review:  generic-root-review:2f6c3972ae083cff8dd2
recipe tree: bb827daab0491d4ff49c822f96dd4bbb80102ef0
artifact:     libepoxy-glibc 1.5.10
artifact id:  generic-artifact:e53dc3b7f5419f13eb09
artifact SHA: e53dc3b7f5419f13eb0948d2e16994061d2d593c1db2c535022c0d504af6a0e8
member:       libepoxy.so.0.0.0
member SHA:   403f566468fb5212173407d041a660af0ff459841e9b0ca2274e9c28ac98c723
SONAME:       libepoxy.so.0
semantic:     CONFIRMED_A
```

The recipe adds no package-specific patch, hook, build option, or output transformation. Upstream Meson defaults select GLX and EGL from the host/dependency environment; this is the material provider-review boundary.

## Pending external inputs

None. Existing repository evidence is sufficient to begin the bounded review. Request passive artifact evidence only if a named feature-selection or consumer-binding ambiguity remains after the semantic comparison.

## Next valid action

Construct one canonical provider-review row binding the exact libepoxy member to the selected GTK GL dispatch capability, with explicit feature-selection, conflict/exclusion, update, rollback, and prohibited-inference fields.

## Stop conditions

Stop without accepting provider authority if:

- the selected GLX/EGL/X11 feature set cannot be bounded from existing evidence;
- the exact member or SONAME conflicts with canonical inventory;
- multiple dynamic provider candidates remain unresolved;
- the proposed decision implies composition, target population, materialization, or activation.

## Completion criteria

- one canonical libepoxy provider-review row exists;
- the claim generator reproduces the updated provider state deterministically;
- negative tests reject feature/SONAME drift and authority broadening;
- current state advances to the next bounded provider tranche;
- repository and runtime remain unmodified outside documentation and review metadata.
