# Provider claim classification under ADR 0005

## Status

```text
classification: COMPLETE / REVIEWED BOUNDED INVENTORY
policy: ADR 0005
roots: 28
objects: 37
claims: 89
new evidence collected: 0
provider authority accepted: 0
composition accepted: 0
target rows accepted: 0
activation accepted: 0
```

This document is the current review surface for the provider-authority decision boundary accumulated in records 0118–0165. It replaces the former assumption that every root must complete the same producing-build evidence campaign before any claim can be reviewed.

The classification is generated from the current canonical review tables by:

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    generate-provider-claim-classification.py
```

Canonical outputs:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    provider-claim-classification.tsv
    provider-sup-02-request-disposition.tsv
    provider-claim-classification-metadata.tsv
```

## Claim separation

The classification does not permit one package or root row to stand for every authority state. Each of the 28 roots has three distinct claims:

```text
ARTIFACT_IDENTITY
    exact reference artifact and named-member candidate identity

ADAPTATION_SEMANTICS
    whether the pinned recipe is unchanged for the claim or contains bounded Termux/Android adaptation

PROVIDER_AUTHORITY
    whether the exact member may be selected as the runtime provider for its capability scope
```

The inventory also records separately:

```text
OJ-001 required-object identity
supplier producing-build provenance
application runtime composition
target population
selected-generation activation
```

Artifact identity can be sufficiently evidenced while adaptation and provider authority remain open. Provider authority can later be accepted without implying complete composition, target membership, or activation.

## ADR class result

```text
Class A: 36 claims
    28 exact artifact/member identity claims
     7 no-explicit-delta adaptation claims confirmed by bounded semantic review
     1 authoritative required-object identity claim

Class B: 49 claims
    21 reference-adapted recipe claims
    28 project integration/provider-selection claims

Class C: 1 global conditional claim
    producing-build equivalence or independent reproduction
    deferred because no current root claim is classified as independently reproduced

Class D: 3 global project-authored claims
    composition
    target population
    activation
```

The single Class C row does not request evidence. It records the conditions that would make producing-build evidence proportionate.

## Existing evidence retained

The classification retains the following evidence without overpromoting it:

- exact package metadata and artifact SHA-256;
- stream-inspected artifact members, member digests, and observed SONAMEs;
- pinned recipe root, recipe tree, upstream source locator and source digest;
- recipe-file inventory and bounded adaptation tokens;
- selected/reference runtime evidence and capability coverage;
- the accepted OJ-001 correction that the required ABI identity is `libjpeg.so.62`, not `libjpeg.so.8`;
- all historical SUP-02 request, acquisition, receipt, and producer records.

These remain evidence inputs. They do not create final provider authority.

## SUP-02 disposition

All 28 issued requests remain historical records, but none is currently required for execution.

```text
STILL_NECESSARY: 0
NARROWED:       14
REPLACED:        7
UNNECESSARY:     7
```

### Narrowed — 14 roots

The T1 and T2 material-delta roots remain Class B. They require semantic recipe review, platform-necessity classification, and object-impact review first.

A custodian export is retained only as an escalation path for a claim-specific field when:

```text
recipe semantics cannot bound generated output;
an observed artifact conflicts with the pinned recipe;
the claim is explicitly reclassified as Class C;
a high-consequence output remains opaque after bounded review.
```

The original three-record export for every root is not the default next action.

### Replaced — 7 roots

T4 configuration/packaging roots and the T5 no-token-with-drift root use:

```text
authoritative artifact/member identity
    + pinned recipe/upstream semantic review
    + project integration and drift-policy evidence
```

This is proportionate to a reference-consumed or reference-adapted claim. It does not require independent reproduction by default.

### Unnecessary — 7 roots

Six T6 no-token roots have completed bounded recipe/upstream semantic comparison and are confirmed Class A for package-specific adaptation. Their historical SUP-02 requests remain unnecessary.

The `libjpeg-turbo` SUP-02 request is also unnecessary at the current boundary because producing-build evidence for a package that does not provide the required `libjpeg.so.62` identity cannot close OJ-001.

## Authority states that remain open

```text
provider authority: OPEN for all 28 roots
application runtime composition: NOT REACHED
target population: BLOCKED
selected-generation activation: BLOCKED
```

The classification does not authorize extraction, installation, target population, provider promotion, selected-generation mutation, or activation.

## Seven-root semantic-review result

The seven-root no-token semantic review is complete:

```text
confirmed Class A: 7
reclassified Class B: 0
provider authority accepted: 0
```

Canonical review surface:

```text
docs/evidence/no-token-recipe-semantic-review.md
experiments/glibc/selected-obsidian-provider-authority/review/no-token-recipe-semantic-review.tsv
```

For all seven roots, the pinned recipe contains only source/version identity and dependency/package metadata. No package-specific patch, hook, build option, install transform, or output rewrite was found. The generic Termux glibc cross-build framework and upstream build defaults remain relied-upon supplier boundaries rather than project-owned producing claims.

`pango` concrete-filename drift remains a separate provider-integration and continuity question. It was not closed by the Class A recipe result.

## Smallest next phase

The next bounded phase is the four-root X.Org provider-authority review:

```text
gpkg/libxfixes
gpkg/libxcomposite
gpkg/libxi
gpkg/libxinerama
```

Each root remains Class B for provider selection and integration. The review may decide exact capability necessity, consumer binding, conflicts/exclusions, update boundary, and rollback. It must not infer complete composition, target membership, or activation.

## Stop line

Do not:

- interpret this classification as provider acceptance;
- fulfill a SUP-02 request solely because it was historically issued;
- combine artifact identity, adaptation, provider authority, composition, target population, and activation into one decision;
- use package metadata or build provenance as a substitute for runtime provider selection;
- use successful launch as proof of complete composition;
- populate or activate a target before the corresponding Class D claim is reviewed.
