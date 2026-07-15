# Active task: resolve the `libjpeg.so.62` provider-candidate gap

> Task ID: `resolve-libjpeg-so-62-provider-candidate-gap`
>
> Expected state on completion: OJ-001 has an exact required-identity/provider-candidate disposition, or a precise bounded external input request; no provider composition, target population, materialization, or activation is implied.

## Objective

Resolve the sole T0 object-requirement mismatch:

```text
required lookup identity: libjpeg.so.62
current rejected candidate family: libjpeg.so.8
recipe root: gpkg/libjpeg-turbo
```

Determine whether an exact authoritative Termux glibc `libjpeg.so.62` candidate exists, whether the requirement itself must be corrected, or whether the selected capability must remain blocked.

## Why now

All seven no-token Class A roots now have bounded provider authority. Pango's CF-001–CF-004 continuity policy is explicit. Before beginning broader reference-adapted provider review, the unique T0 provider-candidate mismatch should be resolved so later composition work does not inherit a known identity contradiction.

## Current accepted decisions

- Seven no-token recipes are Class A for package-specific adaptation.
- Seven bounded provider claims are accepted: four X.Org roots, `libtasn1`, `libepoxy`, and the three-member Pango family.
- Pango concrete suffix `5400.0` is accepted for the exact 1.54.0 family; SONAME aliases are the continuity contract, not oracle suffix `5600.3`.
- All 28 SUP-02 requests remain historical and zero are required now.
- Composition, target population, materialization, and activation remain blocked.

## In scope

- Re-read the accepted SUP-01 OJ-001 correction and canonical requirement rows.
- Inspect exact candidate artifacts and authoritative lookup-name requirements for `libjpeg.so.62`.
- Distinguish requirement correction, provider discovery, compatibility bridge, and unsupported substitution.
- Use one bounded Termux acquisition/analyzer package only if exact repository bytes or ELF identity are unavailable in the web runtime.
- Define update and rollback boundaries without selecting target paths or materializing files.

## Out of scope

- Accepting `libjpeg.so.8` as a silent substitute for `libjpeg.so.62`.
- Installing, removing, upgrading, downgrading, copying, or linking packages.
- Complete GTK/image provider composition.
- Target paths, alias creation, generation publication, deployment, or activation.
- Reconstructing all supplier producing-build provenance without a recorded Class C escalation.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/provider-claim-classification.md`
- `docs/evidence/pango-reference-consumed-provider-authority-and-filename-continuity.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-object-review-set.tsv`

Do not load historical handoff or refactor records by default.

## Pending external inputs

None at task start. If exact package bytes are required and sandbox DNS/egress is unavailable, create one self-contained Termux acquisition/analyzer wrapper with exact repository coordinates and expected digests.

## Next valid action

Construct a canonical OJ-001 review surface that compares the authoritative `libjpeg.so.62` requirement with every exact eligible Termux candidate and records one of: exact provider found, requirement corrected, explicit compatibility bridge required, or capability remains blocked.

## Stop conditions

Stop without accepting a provider if:

- only a `libjpeg.so.8` candidate is available;
- consumer binding or required SONAME authority is ambiguous;
- multiple non-equivalent `libjpeg.so.62` candidates remain unresolved;
- the decision would create an alias, select a target path, materialize bytes, or activate a generation.

## Completion criteria

- OJ-001 has one explicit canonical disposition;
- generated claims reproduce deterministically;
- negative tests reject SONAME-8 substitution and authority broadening;
- the next reference-adapted provider tranche is named;
- repository and runtime remain unchanged outside review metadata and tests.
