# Active task: review the libtasn1 reference-consumed provider root

> Task ID: `review-libtasn1-reference-consumed-provider-authority`
>
> Expected state on completion: `gpkg/libtasn1` has a bounded provider-authority decision or an explicit remaining gap; no security composition, target membership, or activation is implied.

## Objective

Review provider authority for the exact Class A root:

```text
gpkg/libtasn1
```

Determine whether its exact package member is necessary and suitable as the selected runtime provider for the ASN.1 capability used by the Obsidian security/TLS closure. Keep artifact identity, recipe semantics, provider authority, composition, target population, and activation as separate decisions.

## Why now

The four X.Org roots have bounded provider authority accepted for their exact members and selected GTK 3.24.49 X11 capability scope. `libtasn1` is the smallest remaining no-token root with no concrete-filename drift and a narrow security dependency role.

## Current accepted decisions

- The seven no-token recipes are Class A for package-specific adaptation.
- `libxfixes`, `libxcomposite`, `libxi`, and `libxinerama` have bounded provider authority for exact members and selected GTK X11 capabilities.
- Those four decisions do not imply complete composition, target membership, or activation.
- `libtasn1` artifact/member identity and recipe semantics are accepted only as inputs; provider authority remains open.
- Pango filename drift remains open and is excluded from this tranche.
- No SUP-02 request is currently required.

## In scope

- Review the exact `libtasn1` artifact, member and SONAME.
- Establish ASN.1 capability necessity and the concrete GnuTLS/security consumer binding.
- Compare dynamic provider candidates and exclusions.
- Record update and rollback boundaries.
- Decide `ACCEPTED_BOUNDED_PROVIDER`, `REJECTED_PROVIDER`, or `OPEN_EXPLICIT_GAP`.

## Out of scope

- Reviewing `libepoxy` or `pango` provider authority.
- Resolving Pango concrete-filename drift.
- Reviewing explicit-delta recipe roots.
- Issuing or fulfilling SUP-02.
- Authoring the complete security or application composition.
- Populating or activating a provider generation.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/xorg-reference-consumed-provider-authority.md`
- `docs/evidence/no-token-recipe-semantic-review.md`
- `docs/evidence/provider-claim-classification.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Known facts

- The `libtasn1` recipe is Class A with no package-specific patch, hook, build option or output transformation.
- Exact artifact/member identity is bounded and has no concrete-filename drift.
- The provider claim is Class B because the project selects and integrates the member into a mixed-world security runtime.
- The likely consumer relationship is GnuTLS, but provider authority requires an exact bounded consumer-binding decision rather than package-presence inference.

## Pending external inputs

None initially. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

Passive runtime evidence may be requested only if repository and authoritative upstream evidence cannot resolve a concrete consumer-binding ambiguity.

## Next valid action

Construct one `libtasn1` provider-authority row from exact artifact/member, recipe, security dependency and selected-closure evidence. Preserve the four accepted X.Org rows without broadening their scope.

## Stop conditions

Stop before provider acceptance if:

- the exact member or SONAME is ambiguous;
- ASN.1 capability necessity is inferred only from package presence;
- the GnuTLS/security consumer binding cannot be bounded;
- multiple non-equivalent dynamic provider candidates are not compared;
- a security or ABI conflict remains unresolved;
- provider acceptance would be treated as complete security composition, target membership or activation.

## Completion criteria

- `libtasn1` has one explicit provider-authority review row.
- The row states exact member identity, capability scope, necessity basis, consumer binding, conflicts/exclusions, update boundary, rollback boundary, decision and prohibited inference.
- Any runtime observation is narrow, passive and claim-specific.
- No composition, target, materialization or activation state changes by implication.
- The next active task chooses `libepoxy`, Pango drift/provider review, or the smallest explicit-delta tranche.
