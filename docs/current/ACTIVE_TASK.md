# Active task: review target-population intervention lift and supply-byte binding

> Task ID: `review-target-population-intervention-lift-and-supply-byte-binding-boundary`
>
> Expected state on completion: either retain the intervention because one or more exact supply-byte bindings or safety prerequisites are missing, or accept a bounded implementation-design gate without copying or populating any target.

## Objective

Review the two conjunctive gates opened by `SELECTED-TARGET-MANIFEST-ACCEPT-001`:

```text
TARGET-POPULATION-INTERVENTION-LIFT-OPEN
SUPPLY-BYTE-BINDING-OPEN
```

For each of the 41 concrete objects, identify an immutable retained supply artifact, exact artifact digest, exact archive member path, member digest and acquisition/verification authority. Separately review filesystem, atomic-family, rollback, collision, ownership, mutation and observability preconditions for lifting the intervention.

## Why now

The exact 82-row target-policy candidate is now accepted, but it contains no supply artifact or archive-member bindings and the project has not audited whether filesystem intervention may be lifted. Both questions must be answered before materializer design.

## In scope

- exact 41-object supply-byte binding census;
- retained archive and clean-acquisition authority;
- archive-member-to-object digest equality;
- atomic-family and whole-generation materialization requirements;
- rollback, interruption, collision and protected-state failure model;
- decision whether materializer design may begin.

## Out of scope

Downloading missing bytes, extracting archives, creating target directories or symlinks, writing a materializer, package installation, population, immutable generation creation, deployment, selector publication, loader mutation, service/module/schema/cache generation, display execution or activation.

## Required reading

- `docs/evidence/selected-obsidian-target-manifest-boundary-acceptance.md`
- `docs/evidence/selected-obsidian-target-manifest-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest-object-bindings.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/unresolved-authority-ledger.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/profiles/target-layout-invariants.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None required for the initial read-only census. Missing retained artifacts discovered by the census become explicit blockers rather than implicit acquisition authority.

## Stop conditions

Stop if any object lacks exact retained supply bytes or archive-member identity, if acquisition trust is ambiguous, if atomic rollback cannot be bounded, if validation would mutate filesystem/package/loader state, or if either gate is inferred from target-policy acceptance alone.

## Completion criteria

A separate review records all 41 supply bindings and intervention-lift prerequisites, then decides `INTERVENTION_RETAINED` or `BOUNDED_MATERIALIZER_DESIGN_REVIEW_AUTHORIZED`. Neither decision populates a target.

## Next valid action

Run a read-only supply-binding and intervention-lift census. Do not acquire or materialize bytes.
