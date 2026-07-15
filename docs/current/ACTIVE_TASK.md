# Active task: review seven no-token roots

> Task ID: `review-no-token-reference-consumed-roots`
>
> Expected state on completion: the seven roots with no explicit bounded adaptation token have an exact pinned-recipe/upstream semantic review that either confirms Class A reference-consumed status or reclassifies the exact changed boundary as Class B; no provider authority, target membership, or activation is accepted.

## Objective

Review the seven no-token roots identified by the ADR 0005 claim classification:

```text
gpkg/libepoxy
gpkg/libtasn1
gpkg/libxcomposite
gpkg/libxfixes
gpkg/libxi
gpkg/libxinerama
gpkg/pango
```

For each root, compare the exact pinned recipe tree and file manifest with the pinned upstream source baseline. Confirm that the relevant claim is reference-consumed Class A, or record the exact recipe behavior that requires Class B treatment.

## Why now

The 89-row provider claim inventory is complete. It separates artifact identity, adaptation semantics, provider authority, composition, target population, and activation. The 28 SUP-02 requests are now classified as 14 narrowed, 7 replaced, and 7 unnecessary; none is currently required.

The smallest next phase is therefore an agent-only semantic review of the seven roots whose earlier collector found no explicit adaptation token. This review can reduce uncertainty without external evidence collection or runtime mutation.

## Current accepted decisions

- Exact artifact and named-member candidate identity is a Class A claim distinct from provider authority.
- Twenty-one roots have explicit recipe-delta evidence and are Class B for adaptation review.
- Seven roots have no explicit bounded token and remain Class A only as a hypothesis pending full semantic comparison.
- Producing-build provenance is a conditional Class C claim, not a blanket prerequisite.
- Composition, target population, and activation are separate Class D claims.
- No SUP-02 request is currently required; historical requests remain preserved.
- OJ-001 confirms the required identity `libjpeg.so.62`, but an exact provider candidate remains open.

## In scope

- Read the exact pinned recipe files for the seven roots.
- Compare recipe behavior with the pinned upstream source/build baseline.
- Identify implicit patches, generated configuration, environment-sensitive behavior, custom install layout, or packaging hooks not captured by the earlier token collector.
- Record one row per root with the reviewed files, semantic result, ADR class result, changed boundary, object impact, and residual risk.
- Keep `pango` concrete-filename drift separate from recipe adaptation classification.
- Update the provider claim inventory only where this review changes a class or gap.

## Out of scope

- Reviewing the other twenty-one explicit-delta roots.
- Issuing or fulfilling SUP-02.
- Collecting device, custodian, builder, or independent-witness evidence.
- Accepting provider authority.
- Authoring a composition manifest.
- Populating a target or activating a selected generation.
- Inferring equivalence merely from the absence of collector tokens.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/provider-claim-classification.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-recipe-binding-and-drift-target-receipt-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-source-authority-boundary.tsv`

## Known facts

- The classification contains 89 claims: 36 Class A, 49 Class B, 1 conditional Class C, and 3 Class D.
- The seven roots in this task have `NONE_DECLARED` adaptation tokens.
- Six are T6 no-token exact roots; `pango` is T5 no-token with concrete-filename drift.
- Absence of a token is not evidence of upstream equivalence.
- Exact artifact/member identity is already bounded evidence and does not need producing-build reconstruction for this review.
- Provider authority remains open even if a root is confirmed Class A.

## Pending external inputs

None. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

## Next valid action

Construct a seven-row semantic-review table from the pinned recipe trees and upstream baselines. Review each recipe file and build/install behavior, then record `CONFIRMED_A` or `RECLASSIFIED_B` with the exact changed boundary and object impact.

## Stop conditions

Stop before external evidence collection or provider decision if:

- a root is called Class A only because no token was observed;
- the exact pinned recipe tree or upstream baseline cannot be identified;
- packaging-only behavior is conflated with runtime semantic adaptation;
- `pango` filename drift is treated as proof of recipe adaptation or ignored as an integration risk;
- a semantic review result is used to accept provider authority;
- a SUP-02 request is reactivated without a recorded Class C or escalation trigger.

## Completion criteria

- All seven roots have a bounded semantic-review row.
- Every row identifies reviewed files, upstream baseline, semantic result, ADR class, changed boundary, object impact, and residual risk.
- Any Class B reclassification updates the claim inventory deterministically.
- Confirmed Class A rows state what supplier boundary is relied upon.
- No provider, composition, target, or activation state changes by implication.
- The next active task selects one smallest provider-authority or explicit-delta review tranche.
