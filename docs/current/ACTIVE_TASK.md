# Active task: review four X.Org reference-consumed provider roots

> Task ID: `review-xorg-reference-consumed-provider-authority`
>
> Expected state on completion: `libxfixes`, `libxcomposite`, `libxi`, and `libxinerama` each have a bounded provider-authority decision or an explicit remaining gap; no composition, target membership, or activation is implied.

## Objective

Review the provider-authority claims for the four Class A X.Org recipe roots:

```text
gpkg/libxfixes
gpkg/libxcomposite
gpkg/libxi
gpkg/libxinerama
```

Determine whether each exact package member is necessary and suitable as the runtime provider for its declared X11 capability scope. Keep artifact identity, recipe semantics, provider authority, composition, target population, and activation as separate decisions.

## Why now

The seven no-token recipe reviews are complete: all seven are confirmed Class A for package-specific recipe adaptation, with no Class B reclassification. The four X.Org roots form the smallest coherent provider chain because they share an authoritative release model, have no package-specific recipe delta, have no concrete-filename drift row, and expose explicit dependency relationships.

## Current accepted decisions

- The seven no-token roots are Class A for package-specific recipe adaptation.
- Their generic cross-build framework and upstream build semantics remain a relied-upon supplier boundary, not a project reproduction claim.
- The four X.Org roots still have open Class B provider-authority claims.
- Pango filename drift remains open and is excluded from this tranche.
- No SUP-02 request is currently required.
- Provider acceptance does not imply complete composition, target membership, or activation.

## In scope

- Review exact artifact/member identities and observed SONAMEs for the four roots.
- Review package dependency edges and capability relationships.
- Determine capability necessity for the selected Obsidian runtime boundary.
- Review candidate conflicts, exclusions, update boundaries, and rollback alternatives.
- Use bounded passive consumer-binding evidence only where the dependency or runtime selection is ambiguous.
- Record one provider-authority row per root with decision, evidence, remaining gap, and prohibited inference.

## Out of scope

- Reviewing `libepoxy`, `libtasn1`, or `pango` provider authority.
- Resolving Pango concrete-filename drift.
- Reviewing the twenty-one explicit-delta recipe roots.
- Issuing or fulfilling SUP-02.
- Materializing a provider target.
- Authoring a complete composition manifest.
- Mutating the selected generation or activation selector.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/no-token-recipe-semantic-review.md`
- `docs/evidence/provider-claim-classification.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-comparison-artifacts.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/authority-coverage-ledger.tsv`

## Known facts

- All four recipes are Class A for package-specific adaptation.
- Artifact/member identity evidence is already bounded, but does not establish provider authority.
- The roots form a dependency chain around XFixes, Composite, XI, and Xinerama capabilities.
- No concrete-filename drift is recorded for these four roots.
- Provider claims remain open for capability necessity, consumer binding, conflicts/exclusions, and update/rollback.

## Pending external inputs

None initially. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

Passive runtime evidence may be requested only if repository evidence cannot resolve an explicit consumer-binding ambiguity.

## Next valid action

Construct a four-row provider-authority review table from the canonical artifact/member, dependency, capability, and runtime evidence. Decide each row as `ACCEPTED_BOUNDED_PROVIDER`, `REJECTED_PROVIDER`, or `OPEN_EXPLICIT_GAP` without changing composition or target state.

## Stop conditions

Stop before provider acceptance if:

- the exact member or SONAME is ambiguous;
- capability necessity is inferred only from package presence;
- multiple non-equivalent provider candidates are not compared;
- consumer binding remains ambiguous and no bounded passive observation is available;
- provider acceptance would require resolving a composition-wide conflict;
- an accepted provider is silently treated as target membership or activation authority.

## Completion criteria

- All four roots have an explicit provider-authority review row.
- Every row states exact member identity, capability scope, necessity basis, conflict/exclusion result, update and rollback boundary, decision, and prohibited inference.
- Any requested runtime observation is narrow, passive, and claim-specific.
- No composition, target, or activation state changes by implication.
- The next active task selects the smallest unresolved provider or explicit-delta tranche.
